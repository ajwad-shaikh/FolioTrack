from .utils.constants import *
from flask import Flask, request
from .agents.trade_agent import fetchTradesAgency, addTradesAgency, removeTradesAgency, updateTradesAgency
from .agents.portfolio_agent import fetchPortfolioAgency, fetchReturnsAgency

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/trade", methods=["GET"])
def fetchTrades():
    # Fetch Trades
    include_inactive = request.args.get(INCLUDE_INACTIVE_TRADES)
    print(request.args)
    if (include_inactive == '1'):
        include_inactive = True
    else:
        include_inactive = False
    print(include_inactive)
    return fetchTradesAgency(include_inactive)

@app.route("/api/trade", methods=["POST"])
def addTrade():
    # Add Trade
    return addTradesAgency(trade_request=request.get_json(silent=True))

@app.route("/api/trade", methods=["PATCH"])
def updateTrade():
    # Update Trade
    return updateTradesAgency(update_request=request.get_json(silent=True))

@app.route("/api/trade", methods=["DELETE"])
def removeTrade():
    # Remove Trade
    return removeTradesAgency(remove_request=request.get_json(silent=True))

@app.route("/api/portfolio", methods=["GET"])
def fetchPortfolio():
    # Fetch Portfolio
    return fetchPortfolioAgency()

@app.route("/api/returns", methods=["GET"])
def fetchReturns():
    # Fetch Returns
    return fetchReturnsAgency()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)