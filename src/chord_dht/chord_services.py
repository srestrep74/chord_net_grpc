import grpc, sys
from src.rpc import chord_pb2 , chord_pb2_grpc
from src.chord_dht.node import Node

class ChordServicer(chord_pb2_grpc.ChordServiceServicer):
    def __init__(self, node):
        self.node = node

    def FindSuccessor(self, request, context):
        successor = self.node.find_successor(request.id)
        return chord_pb2.NodeInfo(id=successor.id, address=successor.address)

    def GetPredecessor(self, request, context):
        predecessor = self.node.predecessor
        if predecessor:
            return chord_pb2.NodeInfo(id=predecessor.id, address=predecessor.address)
        return chord_pb2.NodeInfo(id=-1, address="")

    def Notify(self, request, context):
        self.node.notify(Node(request.id, request.address))
        return chord_pb2.Empty()

    def StoreResource(self, request, context):
        print(f"StoreResource called with key: {request.key}, value: {request.value}")        
        self.node.store_local(request.key, request.value)
        print(f"Resource stored in node {self.node.id}: {self.node.storage}")  # Verificar almacenamiento
        self.node.print_finger_table()
        return chord_pb2.Empty()

    def LookupResource(self, request, context):
        print(f"LookupResource called with key: {request.key}")        
        value = self.node.lookup(request.key)     
        print(f"Resource found: {value}")  # Verificar valor encontrado
        return chord_pb2.LookupResponse(value=value if value else "")

    def GetFingerTable(self, request, context):
        finger_table = self.node.finger_table
        self.node.print_finger_table()
        return chord_pb2.FingerTableResponse(entries=[chord_pb2.NodeInfo(id=node.id, address=node.address) for node in finger_table if node])
    
    def UpdateSuccessor(self, request, context):
        self.node.successor = Node(request.id, request.address)
        return chord_pb2.Empty()

    def UpdatePredecessor(self, request, context):
        self.node.predecessor = Node(request.id, request.address)
        return chord_pb2.Empty()

def leave_network(node):
    if node.predecessor:
        try:
            with grpc.insecure_channel(node.predecessor.address) as channel:
                stub = chord_pb2_grpc.ChordServiceStub(channel)
                stub.UpdateSuccessor(chord_pb2.NodeInfo(id=node.successor.id, address=node.successor.address))
        except grpc.RpcError:
            print("Failed to update predecessor. It might be offline.")

    if node.successor:
        try:
            with grpc.insecure_channel(node.successor.address) as channel:
                stub = chord_pb2_grpc.ChordServiceStub(channel)
                stub.UpdatePredecessor(chord_pb2.NodeInfo(id=node.predecessor.id, address=node.predecessor.address))
        except grpc.RpcError:
            print("Failed to update successor. It might be offline.")

    print("Node has left the network.")
    sys.exit(0)