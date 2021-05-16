# FolioTrack 📈

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/ajwad-shaikh/FolioTrack/blob/main/LICENSE) 
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/ajwad-shaikh/FolioTrack/pulls)
[![Issues](https://img.shields.io/github/issues-raw/ajwad-shaikh/FolioTrack)](https://github.com/ajwad-shaikh/FolioTrack/issues) 
[![FolioTrack Ping Endpoint](https://img.shields.io/website?url=https%3A%2F%2Ffoliotrack.herokuapp.com%2Fping)](https://foliotrack.herokuapp.com/ping)

> API to manage and track trades, portfolio and returns. 

## How is this tool helpful?
- FolioTrack can be used to record trades and maintain personal portfolio. 
- It is intended to be an exploratory learning project to understand the nuances and edge cases of a financial-securities related product.

## Key Features
- Create trades by providing a price, action (BUY or SELL), quantity, and ticker symbol of the security.
- Fetch all trades for corresponding securities.
- Modify trade parameters like price, action or quantity.
- Cancel trades, which will not delete them but mark them an not active.
- Fetch a portfolio summary that returns net quantity and average price for all securities held.
- Fetch returns for the portfolio against current ticker price.
- Strict validation for final securities quantity to always be non-negative.

## Tech Stack
![Languages](https://img.shields.io/github/languages/count/ajwad-shaikh/FolioTrack)
- Flask | Python 3.9
- Firestore | NoSQL DB
- [![Heroku](http://heroku-badge.herokuapp.com/?app=foliotrack&style=flat&svg=1&root=ping)](https://foliotrack.herokuapp.com/ping)

## API Documentation

- Fetch Trades
  - Endpoint - `/api/trade` 
  - Method - `GET`
  - Required parameters - None
  - [Fetch all Trades](https://reqbin.com/xij8qumw)
  - Optional parameters
    - `?includeInactive=1` passing 1 as the request argument will include inactive trades in the response - i.e. trades that have been cancelled. 
      - [Fetch all trades and `includeInactive`](https://reqbin.com/zydrgw62)
- Create / Add Trade
  - Endpoint - `/api/trade` 
  - Method - `POST`
  - Required Parameters (`application/json`)
    - `price` - Price at which the trade is to be considered executed. Type - `float`
    - `action` - Either `BUY` or `SELL`. Type - `string`
    - `quantity` - Quantity of securities. Type - `float` (consider crypto)
    - `ticker` - Ticker Symbol of the security. Type - `string`
    - [BUY 1000 $DOGEUSD @ 0.4](https://reqbin.com/xg7eukeq) | [SELL 10 $DOGEUSD @ 1.0](https://reqbin.com/cxjmseox)
- Update / Modify Trade
  - Endpoint - `/api/trade` 
  - Method - `PATCH`
  - Required Parameters (`application/json`)
    - `fieldToUpdate`
    - `updateValue`
- Delete / Remove Trade
  - Endpoint - `/api/trade` 
  - Method - `DELETE`
  - Required Parameters (`application/json`)
    - `tradeId` - Trade ID to be deleted. Type - `string`
- Fetch Portfolio Summary
  - Endpoint - `/api/portfolio` 
  - Method - `GET`
  - Required Parameters - None
- Fetch Portfolio Returns
  - Endpoint - `/api/returns` 
  - Method - `GET`
  - Required Parameters - None
- Ping Endpoint
  - Endpoint - `/ping` 
  - Method - `ANY`
  - Required Parameters - None
  - [Send ping](https://reqbin.com/spiv7x8y)
