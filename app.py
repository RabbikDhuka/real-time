import random
from flask import Flask, request, jsonify
import colorama

app = Flask(__name__)

colorama.init(autoreset=True)
colorama.Fore.BLACK

# Set the text color to green
colorama.Fore.GREEN

# Mock data for the stock market
stocks = [
    {
        "name": "Apple Inc.",
        "ticker": "AAPL",
        "price": 150.5,
        "highestPrice": 160.5,
        "lowestPrice": 140.5,
    },
    {
        "name": "Tesla, Inc.",
        "ticker": "TSLA",
        "price": 650.2,
        "highestPrice": 700.2,
        "lowestPrice": 600.2,
    },
    {
        "name": "Google LLC",
        "ticker": "GOOGL",
        "price": 2700.8,
        "highestPrice": 2800.8,
        "lowestPrice": 2600.8,
    },
    {
        "name": "HTC Corporation",
        "ticker": "HTC",
        "price": 65.3,
        "highestPrice": 70.3,
        "lowestPrice": 60.3,
    },
    {
        "name": "Tata Consultancy Services",
        "ticker": "TCS",
        "price": 325.9,
        "highestPrice": 330.9,
        "lowestPrice": 320.9,
    },
]


# Function to generate a random ticker symbol for new stocks
def generate_ticker_symbol():
    return "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(4))


# Function to fetch the current stock price for a specific stock
def get_current_stock_price(ticker):
    # In a real implementation, this function would fetch data from a stock market API.
    # For simplicity, we'll return a fixed price here.
    for stock in stocks:
        if stock["ticker"] == ticker:
            return stock["price"]
    return None


# Function to fetch the highest stock price for a specific stock
def get_highest_stock_price(ticker):
    for stock in stocks:
        if stock["ticker"] == ticker:
            return stock["highestPrice"]
    return None


# Function to fetch the lowest stock price for a specific stock
def get_lowest_stock_price(ticker):
    for stock in stocks:
        if stock["ticker"] == ticker:
            return stock["lowestPrice"]
    return None


# Endpoint to get details of a specific stock by ticker symbol
@app.route("/stocks/<string:ticker>", methods=["GET"])
def get_stock(ticker):
    stock = next((s for s in stocks if s["ticker"] == ticker), None)
    if stock:
        stock["price"] = get_current_stock_price(ticker)
        stock["highestPrice"] = get_highest_stock_price(ticker)
        stock["lowestPrice"] = get_lowest_stock_price(ticker)
        return jsonify(stock)
    return jsonify({"error": "Stock not found"}), 404


# Endpoint to add a new stock
@app.route("/stocks", methods=["POST"])
def add_stock():
    data = request.get_json()
    if "name" not in data or "price" not in data:
        return jsonify({"error": "Name and price are required fields"}), 400

    new_stock = {
        "name": data["name"],
        "ticker": generate_ticker_symbol(),
        "price": data["price"],
        "highestPrice": data["price"],
        "lowestPrice": data["price"],
    }
    stocks.append(new_stock)

    return jsonify({"message": "Stock added successfully"}), 201


# Endpoint to update the price of a stock
@app.route("/stocks/<string:ticker>", methods=["PUT"])
def update_stock_price(ticker):
    stock = next((s for s in stocks if s["ticker"] == ticker), None)
    if stock:
        data = request.get_json()
        if "price" not in data:
            return jsonify({"error": "Price is required for update"}), 400

        stock["price"] = data["price"]
        stock["highestPrice"] = max(stock["price"], stock["highestPrice"])
        stock["lowestPrice"] = min(stock["price"], stock["lowestPrice"])

        return jsonify({"message": "Stock price updated successfully"}), 200
    return jsonify({"error": "Stock not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
