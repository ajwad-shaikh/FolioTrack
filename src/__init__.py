from .utils.constants import *
from flask import Flask, request
from .agents.trade_agent import fetchTradesAgency, addTradesAgency
from .agents.portfolio_agent import fetchPortfolioAgency

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/trade", methods=["GET"])
def fetchTrades():
    # Fetch Trades
    include_inactive = request.args.get(INCLUDE_INACTIVE_TRADES)
    if (include_inactive == 1):
        include_inactive = True
    else:
        include_inactive = False
    return fetchTradesAgency(include_inactive)

@app.route("/api/trade", methods=["POST"])
def addTrade():
    return addTradesAgency(trade_request=request.get_json(silent=True))

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
    return fetchPortfolioAgency()

@app.route("/api/returns", methods=["GET"])
def fetchReturns():
    # Fetch Returns
    return "Returns"
