import hashlib
 
def sha1_hash(key):
    return int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16) % (2**6)  # Aseguramos que esté en el rango de 6 bits
 
class Node:
    def __init__(self, identifier, m_bits):
        self.id = identifier
        self.m = m_bits
        self.finger_table = [None] * m_bits
        self.successor = self
        self.predecessor = None
        self.storage = {}  # Almacenamiento para recursos
 
    def find_successor(self, id, depth=0):
        if depth > self.m:  # Evitar recursión infinita
            return self
        if self.id == id:
            return self
        elif self.in_range(id, self.id, self.successor.id, inclusive=True):
            return self.successor
        else:
            node = self.closest_preceding_node(id)
            if node == self:
                return self.successor
            return node.find_successor(id, depth + 1)
   
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
    def join(self, known_node):
        if known_node:
            self.predecessor = None
            self.successor = known_node.find_successor(self.id)
        else:
            self.predecessor = self
            self.successor = self
        self.fix_fingers()
   
    def stabilize(self):
        x = self.successor.predecessor
        if x and self.in_range(x.id, self.id, self.successor.id, inclusive=False):
            self.successor = x
        self.successor.notify(self)
   
    def notify(self, node):
        if self.predecessor is None or self.in_range(node.id, self.predecessor.id, self.id, inclusive=False):
            self.predecessor = node
 
    def fix_fingers(self):
        for i in range(self.m):
            target = (self.id + 2**i) % (2**self.m)
            self.finger_table[i] = self.find_successor(target)
   
    def check_predecessor(self):
        if self.predecessor and not self.predecessor.is_alive():
            self.predecessor = None
 
    def store(self, key, value):
        """ Store a value with the given key """
        responsible_node = self.find_successor(sha1_hash(key) % (2**self.m))
        responsible_node.storage[key] = value
 
    def retrieve(self, key):
        """ Retrieve a value by its key """
        responsible_node = self.find_successor(sha1_hash(key) % (2**self.m))
        return responsible_node.storage.get(key, None)
   
    def store_local(self, key, value):
        """ Almacena un recurso localmente en este nodo """
        self.storage[key] = value
 
    def lookup(self, key):
        hash_key = sha1_hash(key)
        responsible_node = self.find_successor(hash_key)
        return responsible_node.storage.get(key, None)
 
class ChordNetwork:
    def __init__(self, m_bits):
        self.nodes = []
        self.m = m_bits
   
    def add_node(self, id=None):
        if id is None:
            id = sha1_hash(f'node-{len(self.nodes)}') % (2**self.m)
        new_node = Node(id, self.m)
        if self.nodes:
            new_node.join(self.nodes[0])
        else:
            new_node.join(None)  # Primer nodo en la red
        self.nodes.append(new_node)
        self._stabilize_network()
   
    def _stabilize_network(self):
        for _ in range(self.m):  # Ejecutar stabilize y fix_fingers varias veces para asegurar la convergencia
            for node in self.nodes:
                node.stabilize()
                node.fix_fingers()
   
    def remove_node(self, node):
        self.nodes.remove(node)
        if node.successor != node:  # Si no es el único nodo en la red
            node.successor.predecessor = node.predecessor
            if node.predecessor:
                node.predecessor.successor = node.successor
        self._stabilize_network()
 
    def find_node(self, key):
        if not self.nodes:
            return None
        start_node = self.nodes[0]
        return start_node.find_successor(sha1_hash(key) % (2**self.m))
   
    def print_node_ranges(self):
        for node in sorted(self.nodes, key=lambda n: n.id):
            print(f"Node ID: {node.id}, Successor: {node.successor.id}, Predecessor: {node.predecessor.id if node.predecessor else 'None'}")
 
    def store_resource(self, node, key, value):
        hash_key = sha1_hash(key)
        responsible_node = node.find_successor(hash_key)
        responsible_node.store_local(key, value)
        print(f"Recurso '{key}' almacenado en el nodo con ID: {responsible_node.id}")
    def lookup_resource(self, start_node, key):
        """ Busca un recurso en la red, comenzando desde start_node """
        result = start_node.lookup(key)
        if result:
            print(f"Recurso '{key}' encontrado: {result}")
        else:
            print(f"Recurso '{key}' no encontrado")
        return result
   
# Ejemplo de uso
network = ChordNetwork(m_bits=6)
for _ in range(5):
    network.add_node()
 
network.print_node_ranges()
 
# Almacenar un recurso en un nodo específico
key = 'my_key'
value = 'my_value'
specific_node = network.nodes[1]  # Elegimos el tercer nodo para almacenar el recurso
network.store_resource(specific_node, key, value)
 
# Imprimir el contenido de almacenamiento de todos los nodos
print("\nContenido de almacenamiento de los nodos:")
for node in network.nodes:
    print(f"Node ID: {node.id}, Storage: {node.storage}")
 
# Buscar el recurso desde otro nodo
search_node = network.nodes[3]  # Comenzamos la búsqueda desde el primer nodo
print("\nBuscando recurso:")
result = network.lookup_resource(search_node, key)