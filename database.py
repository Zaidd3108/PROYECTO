import sqlite3

conexion = sqlite3.connect("abarrotes.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT NOT NULL,
    imagen TEXT NOT NULL
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

cursor.execute("""
UPDATE productos
SET nombre=?,
    precio=?,
    categoria=?,
    imagen=?
WHERE id=?
""",
(nombre, precio, categoria, imagen, id))

cursor.execute("DELETE FROM productos")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Arroz Costeño 5kg', 24.90, 'Abarrotes', 'arroz.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Azúcar Rubia 5kg', 23.90, 'Abarrotes', 'azucar.png')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Leche Gloria 390g', 5.90, 'Lácteos', 'leche.jpg')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Aceite Primor 900ml', 11.50, 'Abarrotes', 'aceite.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Coca Cola 3L', 12.50, 'Bebidas', 'cocacola.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Detergente Bolívar 4kg', 8.90, 'Limpieza', 'detergente.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Fideos Don Vittorio', 6.10, 'Abarrotes', 'spaguetti.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Atún Florida', 6.50, 'Abarrotes', 'atun.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Galletas Oreo', 3.50, 'Abarrotes', 'oreo.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Yogurt Gloria', 4.20, 'Lácteos', 'yogurt.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Queso Edam Laive', 22.90, 'Lácteos', 'queso.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Mantequilla Laive', 10.20, 'Lácteos', 'mantequilla.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Inca Kola 3L', 12.50, 'Bebidas', 'incakola.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Sprite 3L', 6.90, 'Bebidas', 'sprite.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Frugos Fresh 3L', 7.20, 'Bebidas', 'frugos.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Lejía Sapolio 4.8kg', 10.30, 'Limpieza', 'lejia.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Lavavajilla Lavax 700g', 5.80, 'Limpieza', 'lavavajilla.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Papel Higiénico Doble Hoja Elite 40un', 19.50, 'Limpieza', 'papelhigienico.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Shampoo Head & Shoulders Anti Comezón 375ml', 18.40, 'Limpieza', 'shampoo.webp')
""")

cursor.execute("""
INSERT INTO productos(nombre, precio, categoria, imagen)
VALUES ('Sixpack Jabón Protex 110g', 19.80, 'Limpieza', 'jabon.webp')
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")