import grpc
from concurrent import futures
import chord_pb2
import chord_pb2_grpc
from utils import sha1_hash
import threading
import time
import sys
from node import Node

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
        print(f"Resource stored in node {self.node.id}: {self.node.storage}")
        self.node.print_finger_table()
        return chord_pb2.Empty()

    def LookupResource(self, request, context):
        print(f"LookupResource called with key: {request.key}")        
        value = self.node.lookup(request.key)     
        print(f"Resource found: {value}")
        return chord_pb2.LookupResponse(value=value if value else "")

    def GetFingerTable(self, request, context):
        finger_table = self.node.finger_table
        self.node.print_finger_table()
        return chord_pb2.FingerTableResponse(entries=[chord_pb2.NodeInfo(id=node.id, address=node.address) for node in finger_table if node])

def serve(node):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chord_pb2_grpc.add_ChordServiceServicer_to_server(ChordServicer(node), server)
    server.add_insecure_port(node.address)
    server.start()
    print(f"Server started on {node.address}")
    print()
   
    bg_thread = threading.Thread(target=node.run_background_tasks, daemon=True)
    bg_thread.start()
   
    server.wait_for_termination()

def interactive_menu(node):
    while True:
        print("\nMenu:")
        print("1. Store resource")
        print("2. Lookup resource")
        print("3. Print finger table")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            key = input("Enter key: ")
            value = input("Enter value: ")
            node.store_local(key, value)
            print(f"Resource '{key}' stored successfully.")
        elif choice == '2':
            key = input("Enter key: ")
            value = node.lookup(key)
            if value:
                print(f"Resource '{key}' found: {value}")
            else:
                print(f"Resource '{key}' not found")
        elif choice == '3':
            node.print_finger_table()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
        
        print()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python chord_server.py <node_id> <server_address> <join_address>")
        sys.exit(1)
   
    node_id = int(sys.argv[1])
    server_address = sys.argv[2]
    join_address = sys.argv[3]

    node = Node(node_id, server_address)
   
    if join_address.lower() != 'none':
        node.join(join_address)
    else:
        node.join(None)

    # Start the gRPC server in a separate thread
    server_thread = threading.Thread(target=serve, args=(node,), daemon=True)
    server_thread.start()
   
    # Start the interactive menu
    interactive_menu(node)
