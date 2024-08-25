import grpc
import chord_pb2
import chord_pb2_grpc
from utils import  sha1_hash
import sys

 
class ChordClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = chord_pb2_grpc.ChordServiceStub(self.channel)
 
    def find_successor(self, id):
        response = self.stub.FindSuccessor(chord_pb2.FindSuccessorRequest(id=id))
        return response
 
    def get_predecessor(self):
        response = self.stub.GetPredecessor(chord_pb2.Empty())
        return response
 
    def notify(self, node_id, node_address):
        self.stub.Notify(chord_pb2.NodeInfo(id=node_id, address=node_address))
 
    def store_resource(self, key, value):
        hash_key = sha1_hash(key)
        responsible_node = self.find_successor(hash_key)
        with grpc.insecure_channel(responsible_node.address) as channel:
            stub = chord_pb2_grpc.ChordServiceStub(channel)
            stub.StoreResource(chord_pb2.StoreRequest(key=key, value=value))
 
    def store_resource(self, key, value):
        hash_key = sha1_hash(key)
        responsible_node = self.find_successor(hash_key)
        with grpc.insecure_channel(responsible_node.address) as channel:
            stub = chord_pb2_grpc.ChordServiceStub(channel)
            stub.StoreResource(chord_pb2.StoreRequest(key=key, value=value))
        print(f"Resource '{key}' stored successfully on node {responsible_node.id}")
 
    def lookup_resource(self, key):
        response = self.stub.LookupResource(chord_pb2.LookupRequest(key=key))
        if response.value:
            print(f"Resource '{key}' found: {response.value}")
        else:
            print(f"Resource '{key}' not found")
 
def main():
    if len(sys.argv) < 3:
        print("Usage: python chord_client.py <node_address> <operation> [key] [value]")
        sys.exit(1)
 
    node_address = sys.argv[1]
    operation = sys.argv[2]
 
    client = ChordClient(node_address)
 
    if operation == 'store':
        if len(sys.argv) != 5:
            print("Usage for store: python chord_client.py <node_address> store <key> <value>")
            sys.exit(1)
        key, value = sys.argv[3], sys.argv[4]
        client.store_resource(key, value)
    elif operation == 'lookup':
        if len(sys.argv) != 4:
            print("Usage for lookup: python chord_client.py <node_address> lookup <key>")
            sys.exit(1)
        key = sys.argv[3]
        client.lookup_resource(key)
    else:
        print(f"Unknown operation: {operation}")
        sys.exit(1)
 
if __name__ == '__main__':
    main()