import sys
from datetime import date
from OldBacktester import OldBacktester
from IbRepo import IbRepo
from OrderGenerator import OrderGenerator
from SectorRotationStrategy import SectorRotationStrategy

if __name__ == '__main__':

    opt = sys.argv[1]

    if(opt == '1'):
        OldBacktester(1000000, date(2003, 1, 2), date(2017, 12, 29)).Run()
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
            if order._asset._numShares > 0:
                app.orderStock(order._type, order._asset._numShares, order._asset._symbol)
        app.disconnect()