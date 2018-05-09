from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from datetime import datetime
from FirstBacktraderStrategy import FirstBacktraderStrategy
from PandasRepo import PandasRepo

# todo:
# 1. Make the repo return a dataframe within the start/end date
# 2. make PandasRepo return df that backtrader can handle as data
    # From example, re-index so that only date is the index

class BacktraderWrapper:
    def __init__(self):
        pass

    def RunBackTest(self):
        # Variable for our starting cash
        startcash = 10000

        # Create an instance of cerebro
        cerebro = bt.Cerebro()

        # Add our strategy
        cerebro.addstrategy(FirstBacktraderStrategy)

        # Add data feed
        df = PandasRepo().GetData('IYF', datetime(2016, 1, 1), datetime(2017, 1, 1))
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(startcash)

        # Set up pyfolio
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

        # Run over everything
        results = cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
