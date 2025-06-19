import grpc
import branch_pb2
import branch_pb2_grpc
import time

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

    def createStub(self):
        port = str(50000 + self.id)
        channel = grpc.insecure_channel("localhost:" + port)
        self.stub = branch_pb2_grpc.BranchStub(channel)
    def executeEvents(self):
        for event in self.events:
            if event["interface"] == "query":
                sleep(3)
# Send request to Branch server
            response = self.stub.sendRequest(request(id=self.id, action=event["interface"],money=event["money"]))
            msg = {"interface": response.action, "result": response.result}
            if response.action == "query":
                msg["money"] = response.money
            self.recvMsg.append(msg)