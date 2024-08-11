import hashlib
import socket
import threading
import json

class ChordNode:
    def __init__(self, port, m=8):
        self.port = port
        self.m = m  # Número de bits en el espacio de claves
        self.node_id = self.hash_function(port)
        self.successor = self.node_id
        self.predecessor = None
        self.finger_table = [self.node_id] * m

    def hash_function(self, key):
        """ Hash simple basado en SHA-1 para generar IDs de nodo. """
        return int(hashlib.sha1(str(key).encode('utf-8')).hexdigest(), 16) % (2 ** self.m)

    def join(self, known_node=None):
        if known_node:
            self.predecessor = None
            self.successor = self.request_successor(known_node, self.node_id)
        else:
            self.predecessor = self.node_id
            self.successor = self.node_id

    def request_successor(self, node, id):
        """ Solicitar el sucesor de un nodo a otro nodo. """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', node))
            s.sendall(json.dumps({"action": "find_successor", "id": id}).encode('utf-8'))
            data = s.recv(1024)
        return int(data.decode('utf-8'))

    def handle_request(self, conn, addr):
        """ Manejar las solicitudes entrantes. """
        data = conn.recv(1024)
        request = json.loads(data.decode('utf-8'))
        action = request['action']

        if action == "find_successor":
            id = request['id']
            conn.sendall(str(self.find_successor(id)).encode('utf-8'))

    def find_successor(self, id):
        """ Encuentra el sucesor de un ID dado. """
        if self.node_id < id <= self.successor:
            return self.successor
        else:
            # Aquí agregarías la lógica para buscar en la tabla de fingers.
            return self.successor

    def run(self):
        """ Inicia el nodo Chord. """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.port))
            s.listen()
            print(f"Node {self.node_id} listening on port {self.port}...")

            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_request, args=(conn, addr)).start()

if __name__ == "__main__":
    port = int(input("Enter the port for this node: "))
    known_port = input("Enter the port of a known node (or leave blank if none): ")
    
    node = ChordNode(port)
    
    if known_port:
        node.join(int(known_port))
    else:
        node.join()
    
    node.run()