import grpc
import branch_pb2
import branch_pb2_grpc

class Branch(branch_pb2_grpc.RPCServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

    def createStubs(self):
        for branchId in self.branches:
            if branchId != self.id:
                port = str(50000 + branchId)
                channel = grpc.insecure_channel("localhost:" + port)
                self.stubList.append(branch_pb2_grpc.BranchStub(channel))
    
    def Propagate_Withdraw(self, request):
        for stub in self.stubList:
            stub.propagate(request(id=request.id, action="withdraw",money=request.money))
    def Propagate_Deposit(self, request):
        for stub in self.stubList:
            stub.propagate(request(id=request.id, action="deposit",money=request.money))
    def process(self, request, propagate):
        result = "success"
        if request.money < 0:
            result = "fail"
        elif request.action == "query":
            pass
        elif request.action == "deposit":
            self.balance += request.money
            if propagate == True:
                self.Propagate_Deposit(request)
        elif request.interface == "withdraw":
            if self.balance >= request.money:
                self.balance -= request.money
                if propagate == True:
                    self.Propagate_Withdraw(request)
            else:
                result = "fail"
        else:
            result = "fail"