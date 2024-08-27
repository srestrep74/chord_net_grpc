import grpc
from concurrent import futures
import chord_pb2
import chord_pb2_grpc
from utils import sha1_hash
import threading
import time
import sys
from node import Node
from chord_client import ChordClient

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


def run_menu(node):
    client = ChordClient(node.address)
    
    while True:
        print("\nMenu:")
        print("1. Store resource")
        print("2. Lookup resource")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            key = input("Enter the resource key: ")
            value = input("Enter the resource value: ")
            client.store_resource(key, value)
        elif choice == '2':
            key = input("Enter the resource key to lookup: ")
            client.lookup_resource(key)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

def serve(node):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chord_pb2_grpc.add_ChordServiceServicer_to_server(ChordServicer(node), server)
    server.add_insecure_port(node.address)
    server.start()
    print(f"Server started on {node.address}")
    
    bg_thread = threading.Thread(target=node.run_background_tasks, daemon=True)
    bg_thread.start()

    menu_thread = threading.Thread(target=run_menu, args=(node,))
    menu_thread.start()
    
    server.wait_for_termination()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python chord_server.py <node_id> <port>")
        sys.exit(1)

    node_id = int(sys.argv[1])
    port = int(sys.argv[2])
    address = f'localhost:{port}'

    node = Node(node_id, address)

    if node_id == 0:  
        node.join(None)
    else:
        node.join('localhost:50051')

    serve(node)
