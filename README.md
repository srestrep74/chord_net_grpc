# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Para el presente reto se implemento una red P2P mediante el protocolo Chord DHT. Chord es un protocolo P2P estructurado que organiza los nodos en un anillo lógico. Cada nodo tiene un identificador único generado mediante hashing (por ejemplo, SHA-1). Los archivos (o recursos) se almacenan en los nodos, y la búsqueda de archivos se realiza mediante un proceso de búsqueda en el anillo utilizando las "finger tables" de los nodos para acelerar el proceso.

## Caracteristicas principales
- Nodos P2P: Cada nodo en la red es responsable de almacenar un rango de claves (hashes) y de proporcionar servicios para la inserción, búsqueda y recuperación de archivos.
- Finger Table: Cada nodo mantiene una finger table que optimiza la búsqueda de nodos responsables de claves específicas, reduciendo la complejidad de las búsquedas a $𝑂(log_{2}𝑁)$, donde $𝑁$ es el número de nodos.
- Responsabilidad de los Nodos: Cada nodo es responsable de un intervalo de claves en el espacio de hash, y cualquier archivo que se hash en ese intervalo es responsabilidad de ese nodo.
- gRPC para Comunicación: Se utiliza gRPC para manejar la comunicación entre nodos, permitiendo que los nodos envíen y reciban solicitudes de búsqueda y transferencia de archivos.

## Servicios definidos
## Diagrama de Secuencias

## Organizacion del Proyecto
La estructura del proyecto está organizada de manera que cada componente tiene un propósito específico en la implementación del DHT de Chord. A continuación se detalla la organización de directorios y la función de cada archivo.

```
src/
   utils.py
   chord_dht/
       chord_client.py
       chord_services.py
       node.py
   rpc/
      chord.proto
      chord_pb2.py
      chord_pb2_grpc.py
peer.py
```

1. **utils.py** :
  - Propósito: Contiene funciones utilitarias utilizadas en toda la aplicación.
  - Función sha1_hash(key): Calcula un hash SHA-1 de la clave dada, lo convierte en un entero y devuelve el resultado módulo $2^m$. Esto se usa para hashear claves y determinar las responsabilidades de los nodos en el Chord DHT.

2. **chord_client.py** :
   - Propósito: Proporciona la funcionalidad del lado del cliente para interactuar con el DHT de Chord.
   - Función:
      - ChordClient: Clase que se conecta a un nodo del DHT a través de gRPC y ofrece métodos para encontrar sucesores, almacenar y buscar recursos.

3. **chord_services.py** :
   - Propósito: Define y gestiona los servicios gRPC que el nodo Chord ofrece.
   - Función:
      - ChordServicer: Clase que implementa los métodos del servicio Chord usando gRPC. Maneja solicitudes para encontrar sucesores, obtener predecesores, almacenar y buscar recursos, entre otros.
      - leave_network(node): Función para manejar la salida de un nodo de la red Chord, actualizando a los nodos vecinos sobre la salida.

4. **node.py** :
   - Propósito: Implementa la lógica de un nodo dentro del DHT de Chord.
   - Función:
      - Node: Clase que representa un nodo en la red Chord. Incluye métodos para encontrar sucesores, almacenar y buscar recursos, manejar la tabla de dedos, y mantener la estabilidad del nodo en la red.
      - run_background_tasks(): Método que ejecuta tareas de mantenimiento, como estabilizar y corregir la tabla de dedos del nodo en un bucle continuo.

5. **chord.proto** :
   - Propósito: Define el protocolo gRPC para la comunicación entre nodos Chord.
   - Función : Contiene las definiciones de servicios y mensajes gRPC que se utilizarán en la red Chord. Incluye definiciones para operaciones como FindSuccessor, StoreResource, LookupResource, y más.

6. **chord_pb2.proto** :
   - Función : Generado automáticamente a partir de chord.proto, contiene las clases y métodos necesarios para manipular los mensajes definidos en el archivo proto.

7. **chord_pb2_grpc.proto** :
   - Función : Generado automáticamente a partir de chord.proto, contiene las definiciones de los stubs y servicios gRPC para la comunicación entre nodos.

8. **peer.py** :
   - Propósito: Este archivo se encarga de iniciar y ejecutar un nodo en la red Chord. Implementa tanto el servidor gRPC para el nodo como un menú interactivo para que el usuario pueda almacenar y buscar recursos. 

