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
CREATE TABLE IF NOT EXISTS carrito(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL
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

cursor.execute("DELETE FROM productos")

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

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Fideos Don Vittorio', 2.80, 'Abarrotes')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Atún Florida', 6.50, 'Abarrotes')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Galletas Oreo', 3.50, 'Abarrotes')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Yogurt Gloria', 4.20, 'Lácteos')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Queso Fresco', 8.50, 'Lácteos')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Mantequilla Gloria', 6.90, 'Lácteos')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Inca Kola 3L', 12.50, 'Bebidas')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Agua San Luis 2.5L', 3.50, 'Bebidas')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Jugo Frugos', 2.50, 'Bebidas')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Lejía Sapolio', 4.90, 'Limpieza')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Lavavajilla Ayudín', 5.20, 'Limpieza')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Papel Higiénico Elite', 14.90, 'Limpieza')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Shampoo Head & Shoulders', 18.50, 'Limpieza')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria)
VALUES ('Jabón Bolívar', 2.20, 'Limpieza')
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")