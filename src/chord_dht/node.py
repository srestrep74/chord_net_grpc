from src.rpc import chord_pb2, chord_pb2_grpc
import grpc , time
from src.utils import sha1_hash

class Node:
    def __init__(self, id, address, m_bits=6):
        self.id = id
        self.address = address
        self.m = m_bits
        self.finger_table = [None] * m_bits
        self.predecessor = None
        self.successor = None
        self.storage = {}
 
    def find_successor(self, id):
        if self.in_range(id, self.id, self.successor.id, inclusive=True):
            return self.successor
        node = self.closest_preceding_node(id)
        if node == self:
            return self.successor
        with grpc.insecure_channel(node.address) as channel:
            stub = chord_pb2_grpc.ChordServiceStub(channel)
            response = stub.FindSuccessor(chord_pb2.FindSuccessorRequest(id=id))
            return Node(response.id, response.address)
 
    def closest_preceding_node(self, id):
        for i in range(self.m - 1, -1, -1):
            if self.finger_table[i] and self.in_range(self.finger_table[i].id, self.id, id, inclusive=False):
                return self.finger_table[i]
        return self
 
    def in_range(self, id, start, end, inclusive=False):
        if inclusive:
            if start <= end:
                return start <= id <= end
            else:
                return id >= start or id <= end
        else:
            if start < end:
                return start < id < end
            else:
                return id > start or id < end
 
    def notify(self, node):
        if self.predecessor is None or self.in_range(node.id, self.predecessor.id, self.id, inclusive=False):
            self.predecessor = node
 
    def store_local(self, key, value):
        self.storage[key] = value
 
    def lookup(self, key):
        hash_key = sha1_hash(key)
        responsible_node = self.find_successor(hash_key)
        if responsible_node.id == self.id:
            return self.storage.get(key)
        with grpc.insecure_channel(responsible_node.address) as channel:
            stub = chord_pb2_grpc.ChordServiceStub(channel)
            response = stub.LookupResource(chord_pb2.LookupRequest(key=key))
            return response.value
 
    def join(self, known_node_address):
        if known_node_address:
            with grpc.insecure_channel(known_node_address) as channel:
                stub = chord_pb2_grpc.ChordServiceStub(channel)
                response = stub.FindSuccessor(chord_pb2.FindSuccessorRequest(id=self.id))
                self.successor = Node(response.id, response.address)
                self.fix_fingers()
        else:
            self.successor = self
        self.predecessor = None
 
    def stabilize(self):
        if self.successor:
            with grpc.insecure_channel(self.successor.address) as channel:
                stub = chord_pb2_grpc.ChordServiceStub(channel)
                response = stub.GetPredecessor(chord_pb2.Empty())
                x = Node(response.id, response.address) if response.id != -1 else None
                if x and self.in_range(x.id, self.id, self.successor.id, inclusive=False):
                    self.successor = x
            with grpc.insecure_channel(self.successor.address) as channel:
                stub = chord_pb2_grpc.ChordServiceStub(channel)
                stub.Notify(chord_pb2.NodeInfo(id=self.id, address=self.address))

 
    def fix_fingers(self):
        for i in range(self.m):
            next_id = (self.id + 2**i) % (2**self.m)
            self.finger_table[i] = self.find_successor(next_id)
 
    def run_background_tasks(self):
        while True:
            self.stabilize()
            self.fix_fingers()
            time.sleep(1)  
    
    def print_finger_table(self):
        print(f"Finger Table for Node ID {self.id}:")
        for i, node in enumerate(self.finger_table):
            if node is not None:
                print(f"  Finger {i}: Node ID {node.id}, Address {node.address}")
            else:
                print(f"  Finger {i}: None")
 