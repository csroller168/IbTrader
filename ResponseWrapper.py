from ibapi.wrapper import EWrapper, OrderId, ListOfContractDescription
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from Asset import Asset
import queue

class ResponseWrapper(EWrapper):

    ## error handling code
    def init_error(self):
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None

        return None

    def is_error(self):
        an_error_if=not self._my_errors.empty()
        return an_error_if

    def error(self, id, errorCode, errorString):
        ## Overriden method
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)

    def init_valid_id(self):
        id_queue = queue.Queue()
        self._id_queue = id_queue
        return id_queue

    def nextValidId(self, id_from_server):
        self._id_queue.put(id_from_server)

    def init_match_symbols(self):
        match_symbols_queue = queue.Queue()
        self._match_symbols_queue = match_symbols_queue
        return match_symbols_queue

    def init_order_status(self):
        order_status_queue = queue.Queue()
        self._order_status_queue = order_status_queue
        return order_status_queue

    def symbolSamples(self, reqId:int,
                      contractDescriptions:ListOfContractDescription):
        self._match_symbols_queue.put(contractDescriptions)

    def init_positions(self):
        positions_queue = queue.Queue()
        self._positionsQueue = positions_queue
        return positions_queue

    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        self._positionsQueue.put(Asset(contract.symbol, avgCost, position))
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    def init_positionEnd(self):
        positionEnd_queue = queue.Queue()
        self._positionEnd_queue = positionEnd_queue
        return self._positionEnd_queue

    def positionEnd(self):
        super().positionEnd()
        self._positionEnd_queue.put(True)

    def Close(self):
        pass

    def openOrder(self, orderId: int, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)
        pass

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str):
        super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld)
        self._order_status_queue.put(1)
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled,
        ", Remaining: ", remaining, ", AvgFillPrice: ", avgFillPrice,
        ", PermId: ", permId, ", ParentId: ", parentId, ", LastFillPrice: ",
        lastFillPrice, ", ClientId: ", clientId, ", WhyHeld: ",
        whyHeld)

