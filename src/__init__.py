from flask import Flask, jsonify, request
from .agents.trade_agent import fetchTradesAgency, addTradesAgency
from .agents.portfolio_agent import fetchPortfolioAgency

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
    return addTradesAgency(request_json=request.get_json(silent=True))

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
