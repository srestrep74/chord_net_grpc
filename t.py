import hashlib
import socket
import threading
import json
import time

class ChordNode:
    def __init__(self, port, m=8):
        self.port = port
        self.m = m  # Número de bits en el espacio de claves
        self.node_id = self.hash_function(port)
        self.successor = (self.node_id, self.port)  # (ID del sucesor, puerto del sucesor)
        self.predecessor = None
        self.finger_table = [(self.node_id, self.port)] * m  # Inicialmente, el nodo es su propio sucesor

    def hash_function(self, key):
        """ Hash simple basado en SHA-1 para generar IDs de nodo. """
        return int(hashlib.sha1(str(key).encode('utf-8')).hexdigest(), 16) % (2 ** self.m)

    def join(self, known_node=None):
        if known_node:
            # Si hay un nodo conocido, unirse al anillo a través de ese nodo
            self.predecessor = None
            self.successor = self.request_successor(known_node, self.node_id)
            if self.successor[0] != self.node_id:
                self.update_finger_table()
            else:
                print("Error al unirse al anillo, usando el nodo como único nodo.")
        else:
            # Si no hay un nodo conocido, el nodo se convierte en un anillo de un solo nodo
            self.predecessor = self.node_id
            self.successor = (self.node_id, self.port)
            self.finger_table = [(self.node_id, self.port)] * self.m  # El nodo es su propio sucesor para todas las entradas de la tabla

    def request_successor(self, node, id):
        """ Solicitar el sucesor de un nodo a otro nodo. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', node))
                s.sendall(json.dumps({"action": "find_successor", "id": id, "port": self.port}).encode('utf-8'))
                data = s.recv(1024)
            successor_id = int(data.decode('utf-8'))
            print(f"Conexión exitosa al nodo {node}, sucesor recibido: {successor_id}")
            return (successor_id, node)
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar al nodo {node}. Verifica que el nodo esté en ejecución.")
            return (self.node_id, self.port)
        except Exception as e:
            print(f"Error inesperado al conectar con el nodo {node}: {e}")
            return (self.node_id, self.port)

    def handle_request(self, conn, addr):
        """ Manejar las solicitudes entrantes. """
        try:
            data = conn.recv(1024)
            request = json.loads(data.decode('utf-8'))
            action = request.get('action')

            if action == "find_successor":
                id = request['id']
                port = request['port']
                conn.sendall(str(self.find_successor(id)[0]).encode('utf-8'))
                # Notificar que un nodo se ha conectado, usando la solicitud find_successor
                print(f"Nodo {port} con ID {id} se ha conectado al nodo {self.port} con ID {self.node_id}.")
            elif action == "get_predecessor":
                conn.sendall(str(self.predecessor).encode('utf-8'))
            elif action == "update_finger_table":
                node_id = request['node_id']
                index = request['index']
                self.update_finger_entry(index, (node_id, addr[1]))
            elif action == "send_message":
                message = request['message']
                print(f"Mensaje recibido de nodo {request['from_port']} (ID {request['from_id']}): {message}")
        except Exception as e:
            print(f"Error al manejar la solicitud de {addr}: {e}")
        finally:
            conn.close()

    def find_successor(self, id):
        """ Encuentra el sucesor de un ID dado usando la tabla de fingers. """
        if self.node_id < id <= self.successor[0]:
            return self.successor
        else:
            for i in range(self.m - 1, -1, -1):
                if self.finger_table[i] is not None and self.node_id < self.finger_table[i][0] < id:
                    return self.request_successor(self.finger_table[i][1], id)
            return self.successor

    def update_finger_table(self):
        """ Actualiza la tabla de fingers del nodo. """
        for i in range(1, self.m):
            start = (self.node_id + 2*i) % (2*self.m)
            self.finger_table[i] = self.find_successor(start)

    def update_finger_entry(self, index, node):
        """ Actualiza una entrada específica en la tabla de fingers. """
        if self.finger_table[index] is None or (self.node_id < node[0] < self.finger_table[index][0]):
            self.finger_table[index] = node

    def stabilize(self):
        """ Procedimiento para estabilizar la red Chord. """
        if self.successor[0] != self.node_id:  # Solo estabilizar si hay más de un nodo en el anillo
            successor_predecessor = self.request_predecessor(self.successor[1])
            if successor_predecessor is not None and self.node_id < successor_predecessor < self.successor[0]:
                self.successor = (successor_predecessor, self.successor[1])
            self.notify(self.successor[1])

    def notify(self, node):
        """ Notifica a un nodo que podría ser su predecesor. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', node))
                s.sendall(json.dumps({"action": "get_predecessor"}).encode('utf-8'))
                data = s.recv(1024)
            pred = int(data.decode('utf-8'))
            if pred is None or self.node_id > pred:
                self.predecessor = self.node_id
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar al nodo {node}. Verifica que el nodo esté en ejecución.")
        except Exception as e:
            print(f"Error inesperado al notificar el nodo {node}: {e}")

    def request_predecessor(self, node):
        """ Solicitar el predecesor de un nodo. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', node))
                s.sendall(json.dumps({"action": "get_predecessor"}).encode('utf-8'))
                data = s.recv(1024)
            return int(data.decode('utf-8'))
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar al nodo {node}. Verifica que el nodo esté en ejecución.")
            return None
        except Exception as e:
            print(f"Error inesperado al solicitar el predecesor del nodo {node}: {e}")
            return None

    def send_message(self, target_port, message):
        """ Enviar un mensaje a otro nodo. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', target_port))
                s.sendall(json.dumps({
                    "action": "send_message",
                    "message": message,
                    "from_id": self.node_id,
                    "from_port": self.port
                }).encode('utf-8'))
            print(f"Mensaje enviado a nodo en puerto {target_port}.")
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar al nodo en puerto {target_port}.")
        except Exception as e:
            print(f"Error inesperado al enviar mensaje al nodo en puerto {target_port}: {e}")

    def run(self):
        """ Inicia el nodo Chord. """
        time.sleep(1)  # Agrega un pequeño delay para permitir que el nodo se configure
        threading.Thread(target=self.periodic_stabilize).start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.port))
            s.listen()
            print(f"Node {self.node_id} listening on port {self.port}...")

            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_request, args=(conn, addr)).start()

    def periodic_stabilize(self):
        """ Ejecuta la estabilización periódicamente. """
        while True:
            self.stabilize()
            time.sleep(5)

if __name__ == "__main__":
    port = int(input("Enter the port for this node: "))
    known_port = input("Enter the port of a known node (or leave blank if none): ")
    
    node = ChordNode(port)
    
    if known_port:
        node.join(int(known_port))
        node.send_message(50001, "Hola desde nodo 2")
    else:
        node.join()
    
    node.run()