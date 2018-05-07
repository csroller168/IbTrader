from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt

class BacktraderWrapper:
    def __init__(self):
        pass

    def RunBackTest(self):
        cerebro = bt.Cerebro()
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
