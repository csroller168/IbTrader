from ResponseWrapper import ResponseWrapper
from RequestClient import RequestClient
from threading import Thread

class IbRepo(ResponseWrapper, RequestClient):
    def __init__(self, ipaddress, portid, clientid):
        ResponseWrapper.__init__(self)
        RequestClient.__init__(self, wrapper=self)

        self.init_error()
        self.init_order_status()
        self.init_valid_id()
        self.connect(ipaddress, portid, clientid)

        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)