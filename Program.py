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

    # todo: add cash via reqAccountSummary (http://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#a3e0d55d36cd416639b97ee6e47a86fe9)
    # todo: request contracts rather than build them


    app = IbRepo("127.0.0.1", 4002, 168)
    currentPortfolio = app.get_current_portfolio()
    cashValue = app.get_cash_value()
    value = sum(a.Value for a in currentPortfolio) + cashValue
    targetPortfolio = SectorRotationStrategy(value, date.today()).GetTargetPortfolio()
    orders = OrderGenerator().MakeOrders(currentPortfolio, targetPortfolio)
    for order in orders:
        app.placeOrder(order._type, order._asset._numShares, order._asset._symbol)

    app.disconnect()