from IbRepo import IbRepo
from time import sleep
from SectorRotationStrategy import SectorRotationStrategy
from OrderGenerator import OrderGenerator
from datetime import date
from Backtester import Backtester
from datetime import date


if __name__ == '__main__':
    #Backtester(100000, date(2005, 1, 3), date(2018, 1, 20)).Run()

    # todo: maybe make this take an argument that signals what action to perform

    # todo: Get Current portfolio before building orders, or use special order type to set target amt.
        # put a loop somewhere to wait a few seconds for all portfolio positions to come in
        # see the following to get buying power or cash remaining
            # http://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#a3e0d55d36cd416639b97ee6e47a86fe9
    # todo: get recent prices from repo
    # todo: if trading today, get last closing price, not today's closing (which won't exist)
    # todo: pass target and current portfolio to order builder to get orders
    # todo: call app.placeOrder for each order

    # Get current portfolio from IB


    # Connect
    app = IbRepo("127.0.0.1", 4001, 168)
    portfolio = app.get_current_portfolio()


    #portfolio = SectorRotationStrategy(900000, date.today()).GetTargetPortfolio()
    #app.placeSampleOrder()

    #sleep(5)
    # request a contract rather than build one (test with msft)
    app.disconnect()