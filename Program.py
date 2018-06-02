import sys
from ibtrader.BacktraderWrapper import BacktraderWrapper

if __name__ == '__main__':

    opt = sys.argv[1]

    if opt == '1':
        BacktraderWrapper(startCash=100000).run_backtest()
    elif opt == '2':
        BacktraderWrapper().live_trade()
