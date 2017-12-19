from ibapi.wrapper import EWrapper
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

    def Close(self):
        pass