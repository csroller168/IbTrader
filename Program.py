import sys
from ibtrader.BacktraderWrapper import BacktraderWrapper

if __name__ == '__main__':

    opt = sys.argv[1]

    if(opt == '1'):
        BacktraderWrapper(startCash=100000).RunBackTest()
    elif(opt == '2'):
        pass
        # todo: request contracts rather than build them
        # app = IbRepo("127.0.0.1", 4002, 168)
        # currentPortfolio = app.get_current_portfolio()
        # cashValue = app.get_cash_value()
        # value = float(sum(a.Value for a in currentPortfolio))
        # value += cashValue
        # targetPortfolio = OldSectorRotationStrategy(value, date.today()).GetTargetPortfolio()
        # orders = OrderGenerator().MakeOrders(currentPortfolio, targetPortfolio)
        # for order in orders:
        #     if order._asset._numShares > 0:
        #         app.orderStock(order._type, order._asset._numShares, order._asset._symbol)
        # app.disconnect()