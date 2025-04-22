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
    start_date = request.args.get("start", default=None, type=str)  # e.g., "2023-01-01"
    end_date = request.args.get("end", default=None, type=str)      # e.g., "2024-01-01"

    try:
        # Fetch data with date range using OpenBB
        stock_df = obb.equity.price.historical(
            ticker.upper(), interval="1d", start_date=start_date, end_date=end_date
        )
        print(f"Fetched data for {ticker.upper()} from {start_date} to {end_date}")
        print(stock_df.head())

        if stock_df.empty:
            return Response("No data found for ticker.", status=404)        

        # Create figure and subplots
        fig, (ax1, ax2) = plt.subplots(
            nrows=2,
            ncols=1,
            sharex=True,
            figsize=(10, 6),
            gridspec_kw={"height_ratios": [3, 1]}
        )

        # Plot closing prices
        ax1.plot(stock_df.index, stock_df["close"], label="Close Price", color="blue")
        ax1.set_title(f"{ticker.upper()} Closing Prices and Volume")
        ax1.set_ylabel("Price")
        ax1.grid(True)
        ax1.legend()

        # Plot volume
        ax2.bar(stock_df.index, stock_df["volume"], color="gray", label="Volume")
        ax2.set_ylabel("Volume")
        ax2.set_xlabel("Date")
        ax2.grid(True)
        ax2.legend()
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

        # Save chart to BytesIO
        img = BytesIO()
        plt.tight_layout()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()

        return send_file(img, mimetype="image/png")

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)


if __name__ == "__main__":
    app.run(debug=True)
