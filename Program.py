import sys
from datetime import date
from Backtester import Backtester
from IbRepo import IbRepo
from OrderGenerator import OrderGenerator
from SectorRotationStrategy import SectorRotationStrategy

if __name__ == '__main__':

    opt = sys.argv[1]

    if(opt == '1'):
        Backtester(100000, date(2005, 1, 3), date(2018, 1, 20)).Run()
    elif(opt == '2'):
        # todo: request contracts rather than build them
        app = IbRepo("127.0.0.1", 4002, 168)
        currentPortfolio = app.get_current_portfolio()
        cashValue = app.get_cash_value()
        value = float(sum(a.Value for a in currentPortfolio))
        value += cashValue
        targetPortfolio = SectorRotationStrategy(value, date.today()).GetTargetPortfolio()
        orders = OrderGenerator().MakeOrders(currentPortfolio, targetPortfolio)
        for order in orders:
            app.orderStock(order._type, order._asset._numShares, order._asset._symbol)
        app.disconnect()