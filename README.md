# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Para el presente reto se implemento una red P2P mediante el protocolo Chord DHT. Chord es un protocolo P2P estructurado que organiza los nodos en un anillo lógico. Cada nodo tiene un identificador único generado mediante hashing (por ejemplo, SHA-1). Los archivos (o recursos) se almacenan en los nodos, y la búsqueda de archivos se realiza mediante un proceso de búsqueda en el anillo utilizando las "finger tables" de los nodos para acelerar el proceso.

## Caracteristicas principales
- Nodos P2P: Cada nodo en la red es responsable de almacenar un rango de claves (hashes) y de proporcionar servicios para la inserción, búsqueda y recuperación de archivos.
- Finger Table: Cada nodo mantiene una finger table que optimiza la búsqueda de nodos responsables de claves específicas, reduciendo la complejidad de las búsquedas a $𝑂(log_{2}𝑁)$, donde $𝑁$ es el número de nodos.
- Responsabilidad de los Nodos: Cada nodo es responsable de un intervalo de claves en el espacio de hash, y cualquier archivo que se hash en ese intervalo es responsabilidad de ese nodo.
- gRPC para Comunicación: Se utiliza gRPC para manejar la comunicación entre nodos, permitiendo que los nodos envíen y reciban solicitudes de búsqueda y transferencia de archivos.

## Servicios definidos
Este servidor Chord implementa una red distribuida utilizando el protocolo gRPC para la comunicación entre nodos. A continuación, se detalla la especificación completa de los servicios ofrecidos por esta implementación.

### 1. `FindSuccessor`

- **Método**: `FindSuccessor`
- **Tipo**: RPC
- **Descripción**: Encuentra el sucesor de un nodo dado un identificador.
- **Solicitudes**:
  - `FindSuccessorRequest`:
    - `id` (int32): El identificador del nodo cuyo sucesor se desea encontrar.
- **Respuestas**:
  - `NodeInfo`:
    - `id` (int32): Identificador del nodo sucesor.
    - `address` (string): Dirección del nodo sucesor.

### 2. `GetPredeccessor`

- **Método**: `GetPredecessor`
- **Tipo**: RPC
- **Descripción**: Obtiene la información del predecesor del nodo.
- **Solicitudes**:
  - `Empty`: No se requieren datos adicionales.
- **Respuestas**:
  - `NodeInfo`:
    - `id` (int32): Identificador del nodo predecesor.
    - `address` (string): Dirección del nodo predecesor.

### 3. `Notify`

- **Método**: `Notify`
- **Tipo**: RPC
- **Descripción**: Notifica al nodo sobre su nuevo predecesor.
- **Solicitudes**:
    - `NodeInfo`:
       - `id` (int32): Identificador del nodo que está notificando.
       - `address` (string): Dirección del nodo que está notificando.
- **Respuestas**:
 - `Empty`: No se requieren datos adicionales.

### 4. `StoreResource`

- **Método**: `StoreResource`
- **Tipo**: RPC
- **Descripción**: Almacena un recurso en el DHT.
- **Solicitudes**:
    - `StoreRequest`:
       - `key` (string): Clave del recurso.
       - `value` (string):  Valor del recurso.
- **Respuestas**:
 - `Empty`: Confirmación de que el recurso ha sido almacenado.

### 5. `LookupResource`

- **Método**: `LookupResource`
- **Tipo**: RPC
- **Descripción**: Busca un recurso en el DHT utilizando una clave
- **Solicitudes**:
    - `LookupRequest`:
       - `key` (string): Clave del recurso a buscar.
- **Respuestas**:
    - `LookupRequest`:
       - `value` (string) : Valor asociado con la clave, o un mensaje de error si no se encuentra.

### 6. `UpdateSuccessor`

- **Método**: `UpdateSuccessor`
- **Tipo**: RPC
- **Descripción**: Actualiza la información sobre el sucesor del nodo.
- **Solicitudes**:
    - `NodeInfo`:
       - `id` (int32): Identificador del nuevo sucesor.
       - `address` (string): Dirección del nuevo sucesor.
- **Respuestas**:
    - `Empty` : Confirmación de que la información ha sido actualizada.

### 7. `UpdatePredecessor`

- **Método**: `UpdatePredecessor`
- **Tipo**: RPC
- **Descripción**: Actualiza la información sobre el predecesor del nodo.
- **Solicitudes**:
    - `NodeInfo`:
       - `id` (int32): Identificador del nuevo predecesor.
       - `address` (string): Dirección del nuevo predecesor.
- **Respuestas**:
    - `Empty` : Confirmación de que la información ha sido actualizada.
      
## Diagrama de Secuencias
![Diagrama de Secuencias Chord DHT](https://www.planttext.com/api/plantuml/png/fLPDRzim3BtxLn0znK3MxLmWGu6Y6J84sT2ikmn3eCPq8yILF4bEb_twKVANP2UEr_MGHZJvI3u-qRdLXYbJl6GHsngfu56ZYd8oyItFcJ1mjP89NW7JOB-4Z-vsKYMmHdNWszB7MIf3wBikjblKcb8qW8sfZ_nLOO9TVy_e8gBPp3s4EuNCS2c0YGG-IowuU0QpGrYXUPLg3xDP5DdEuDt7Ck86rhRlyZ0HzBdXoHHOaYZ2tvWTrnjhRKsIy9IpnP6BQg4MWXlEClw7e3oKAQHK1mKPzfGHKjwMFmLTznv7B3EmIA4gWcg53n7GNoUBxQjfQBAIWWh1J6FW6r3Q2vfpaJGU3_YhG6seubcLEeuTLeX1eFvG2JD06GiQO9merFvRY5Jw19ufPp02HJ8mdhaR27op0nbmyuJsladlv4QgUUBaKyhDokeSyxKdQU8J6WynZYuH7Fh3vFubDySu6asX9pIdQl_S47MHrb4evxfVISFJevLfXTPSCVUbZh_CnMYWI-mu4jqC7r3BGf7NbnoL6wG-lI2amjPviiVZ50uiA_eBeEEwb5kMPLIq9ZjxnXyK-XDcTR1ttu5heFfpAe6J926bSTkzHG6dLa2P9olXBr_-kLIlp2ve6rRTJ9Zu9x-fSPU_Ygv96GORDnDxPRlaBwNS5td8Ve_soibje1ORP0hE-mqykofkAAqfb83ljfLcYjVFw5gCHwpTclcomeRwu5XXZI6zZgl9E8TpYUy6nnA1aqgFGqlsVCG0PUL4wQOjaHr6l8hlVtDJFm-cjgENlhTsWhoT7mC4yvWdpA0dX7PfD6zRjpdQKxi-B7GNiZ-8CiNRCtG7r6-YlH9T8XhCGULL90JlZtzQwUCKMQRvtopZzqD7RQkQb0nJu-GbAlb4j-HkVyx-1G00)


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

