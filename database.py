import sqlite3

conexion = sqlite3.connect("abarrotes.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT
)
""")    

cursor.execute("""
CREATE TABLE IF NOT EXISTS compras(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    total REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_compra(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER,
    producto TEXT,
    cantidad INTEGER,
    subtotal REAL
)
""")

cursor.execute("SELECT COUNT(*) FROM productos")

cantidad = cursor.fetchone()[0]

if cantidad == 0:

    cursor.execute("""
    INSERT INTO productos(nombre, precio, categoria)
    VALUES ('Arroz Costeño', 4.50, 'Abarrotes')
    """)

    cursor.execute("""
    INSERT INTO productos(nombre, precio, categoria)
    VALUES ('Azúcar Rubia', 3.20, 'Abarrotes')
    """)

    cursor.execute("""
    INSERT INTO productos(nombre, precio, categoria)
    VALUES ('Leche Gloria', 5.90, 'Lácteos')
    """)

    cursor.execute("""
    INSERT INTO productos(nombre, precio, categoria)
    VALUES ('Aceite Primor', 11.50, 'Abarrotes')
    """)

    cursor.execute("""
    INSERT INTO productos(nombre, precio, categoria)
    VALUES ('Coca Cola 3L', 12.50, 'Bebidas')
    """)

    cursor.execute("""
    INSERT INTO productos(nombre, precio, categoria)
    VALUES ('Detergente Bolívar', 8.90, 'Limpieza')
    """)

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")