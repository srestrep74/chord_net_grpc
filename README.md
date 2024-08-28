# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Para el presente reto se implemento una red P2P mediante el protocolo Chord DHT. Chord es un protocolo P2P estructurado que organiza los nodos en un anillo lógico. Cada nodo tiene un identificador único generado mediante hashing (por ejemplo, SHA-1). Los archivos (o recursos) se almacenan en los nodos, y la búsqueda de archivos se realiza mediante un proceso de búsqueda en el anillo utilizando las "finger tables" de los nodos para acelerar el proceso.

## Caracteristicas principales
- Nodos P2P: Cada nodo en la red es responsable de almacenar un rango de claves (hashes) y de proporcionar servicios para la inserción, búsqueda y recuperación de archivos.
- Finger Table: Cada nodo mantiene una finger table que optimiza la búsqueda de nodos responsables de claves específicas, reduciendo la complejidad de las búsquedas a $𝑂(log_{2}𝑁)$, donde $𝑁$ es el número de nodos.
- Responsabilidad de los Nodos: Cada nodo es responsable de un intervalo de claves en el espacio de hash, y cualquier archivo que se hash en ese intervalo es responsabilidad de ese nodo.
- gRPC para Comunicación: Se utiliza gRPC para manejar la comunicación entre nodos, permitiendo que los nodos envíen y reciban solicitudes de búsqueda y transferencia de archivos.

## Organizacion del Proyecto
