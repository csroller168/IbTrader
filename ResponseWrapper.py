from ibapi.wrapper import EWrapper, OrderId
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
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

    def init_order_status(self):
        order_status_queue = queue.Queue()
        self._order_status_queue = order_status_queue
        return order_status_queue

    def Close(self):
        pass

    def openOrder(self, orderId: int, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)
        pass

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
        avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled,
        ", Remaining: ", remaining, ", AvgFillPrice: ", avgFillPrice,
        ", PermId: ", permId, ", ParentId: ", parentId, ", LastFillPrice: ",
        lastFillPrice, ", ClientId: ", clientId, ", WhyHeld: ",
        whyHeld, ", MktCapPrice: ", mktCapPrice)

