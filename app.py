import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, request, send_file, Response
from io import BytesIO
from openbb import obb

app = Flask(__name__)
obb.user.preferences.output_type = "dataframe"

@app.route("/api/stock-chart")
def stock_chart():
    ticker = request.args.get("ticker", default="AAPL", type=str)

    try:
        # Fetch data using OpenBB
        stock_df = obb.equity.price.historical(ticker.upper(), interval="1d")
        print(f"Fetched data for {ticker.upper()}")
        print(stock_df.head())

        if stock_df.empty:
            return Response("No data found for ticker.", status=404)

        # Plot closing prices
        plt.figure(figsize=(10, 5))
        plt.plot(stock_df.index, stock_df["close"], label="Close Price")
        plt.title(f"{ticker.upper()} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend()

        # Save chart to a BytesIO stream
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()

        return send_file(img, mimetype="image/png")

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

if __name__ == "__main__":
    app.run(debug=True)
