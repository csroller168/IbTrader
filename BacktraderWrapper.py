from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from datetime import datetime
from SectorRotationStrategy import SectorRotationStrategy
from PandasRepo import PandasRepo

# TODO:
# Integrate into IB
# Delete dead classes
# Organize into namespaces
# update strategy
    # add market pullout indicator

class BacktraderWrapper:
    def __init__(self,
                 startCash = 10000,
                 universe = ["IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU"],
                 startDate = datetime(2016, 1, 1),
                 endDate = datetime(2017, 12, 31)):
        self._startCash = startCash
        self._universe = universe
        self._startDate = startDate
        self._endDate = endDate

    def RunBackTest(self):
        # Create an instance of cerebro
        cerebro = bt.Cerebro()

        # Add our strategy
        cerebro.addstrategy(SectorRotationStrategy)

        # Add data feed
        for symbol in self._universe:
            df = PandasRepo().GetData(symbol, self._startDate, self._endDate)
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data, name=symbol)

        # Set our desired cash start
        cerebro.broker.setcash(self._startCash)

        # Set up pyfolio
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

        # Run over everything
        results = cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
