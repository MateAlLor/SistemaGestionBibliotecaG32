# Estructura de Base de datos:

# libro:
# - isbn -> INT (PK)
# - titulo -> VARCHAR
# - genero -> VARCHAR
# - anio -> INT
# - autorID -> INT (Referencia ID de Autor)
# - cantidad -> INT

# autor:
# - id -> INT (PK AI)
# - nombre -> VARCHAR
# - apellido -> VARCHAR
# - nacionalidad -> VARCHAR

# usuario
# - id -> INT (PK AI)
# - nombre -> VARCHAR 
# - apellido -> VARCHAR
# - tipo -> INT
# - direccion -> VARCHAR
# - telefono -> INT

# prestamo
# - id -> INT (PK AI)
# - usuario -> INT (Referencia a ID de usuario)
# - libro -> INT (Referencia a ID de libro)
# - fechaPrestamo -> DATE
# - fechaDevolucion -> DATE

import sqlite3

class Database:
    def __init__(self):
        # Hacer conexión a la DB
        pass
 