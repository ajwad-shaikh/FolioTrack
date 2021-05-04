from flask import Flask, jsonify
from .agents.fetch_trade_agent import fetchTradesAgency
from .agents.fetch_portfolio_agency import fetchPortfolioAgency

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/trade", methods=["GET"])
def fetchTrades():
    # Fetch Trades
    return jsonify(fetchTradesAgency())

@app.route("/api/trade", methods=["POST"])
def addTrade():
    # Add Trade
    return "Add Trade"

@app.route("/api/trade", methods=["PATCH"])
def updateTrade():
    # Update Trade
    return "Update Trade"

@app.route("/api/trade", methods=["DELETE"])
def removeTrade():
    # Remove Trade
    return "Remove Trade"

@app.route("/api/portfolio", methods=["GET"])
def fetchPortfolio():
    # Fetch Portfolio
    return jsonify(fetchPortfolioAgency())

@app.route("/api/returns", methods=["GET"])
def fetchReturns():
    # Fetch Returns
    return "Returns"
