import grpc
from concurrent import futures
from src.rpc import chord_pb2_grpc
import threading
import sys
from src.chord_dht.node import Node
from src.chord_dht.chord_client import ChordClient
from src.chord_dht.chord_services import ChordServicer, leave_network

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
            leave_network(node)
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

import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python chord_server.py <node_id> <ip:port_this_node> <ip:port_other_node>")
        sys.exit(1)

    node_id = int(sys.argv[1])
    address_this_node = sys.argv[2]  
    address_other_node = sys.argv[3]  

    node = Node(node_id, address_this_node)

    if node_id == 0:
        node.join(None)
    else:
        node.join(address_other_node)

    serve(node)

