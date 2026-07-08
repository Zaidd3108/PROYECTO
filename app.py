# IMPORTACIÓN DE LIBRERÍAS
from flask import Flask, render_template, request, redirect, url_for, session

# CONEXIÓN A LA BASE DE DATOS
import sqlite3
from werkzeug.utils import secure_filename
import os

# CONFIGURACIÓN DE FLASK
app = Flask(__name__)
app.secret_key = "abarrotes_joel_2026"

from flask_mail import Mail, Message
import random

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "supermercado.abarrotes.joel@gmail.com"
app.config["MAIL_PASSWORD"] = "gfmh hibc hobp rpee"

mail = Mail(app)

UPLOAD_FOLDER = "static/img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# LOGIN
USUARIO_CORRECTO = "Zaidd"
PASSWORD_CORRECTO = "3101"

# PRODUCTOS DESDE SQLITE

def obtener_productos():

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conexion.close()

    return [dict(producto) for producto in productos]

# PÁGINA PRINCIPAL
@app.route("/")
def inicio():

    busqueda = request.args.get("buscar", "").strip()
    categoria = request.args.get("categoria", "")

    productos_filtrados = obtener_productos()

    if categoria:
        productos_filtrados = [
            p for p in productos_filtrados
            if p["categoria"] == categoria
        ]

    if busqueda:
        productos_filtrados = [
            p for p in productos_filtrados
            if busqueda.lower() in p["nombre"].lower()
        ]

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT COALESCE(SUM(cantidad),0)
    FROM carrito
    WHERE usuario = ?
    """, (usuario,))

    cantidad_carrito = cursor.fetchone()[0]

    conexion.close()

    return render_template(
        "index.html",
        productos=productos_filtrados,
        cantidad_carrito=cantidad_carrito,
        busqueda=busqueda,
        categoria=categoria,
        usuario=session.get("usuario")
    )

# AGREGAR AL CARRITO
@app.route("/agregar/<int:id>")
def agregar(id):

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    usuario = session.get("usuario", "Invitado")

    cursor.execute(
        """
        SELECT * FROM carrito
        WHERE usuario=? AND producto_id=?
        """,
        (usuario, id)
    )

    existe = cursor.fetchone()

    if existe:

        cursor.execute(
            """
            UPDATE carrito
            SET cantidad = cantidad + 1
            WHERE usuario=? AND producto_id=?
            """,
            (usuario, id)
        )

    else:

        cursor.execute(
            """
            INSERT INTO carrito(usuario, producto_id, cantidad)
            VALUES(?,?,?)
            """,
            (usuario, id, 1)
        )

    conexion.commit()
    conexion.close()

    volver = request.args.get("volver", "")
    return redirect(url_for("inicio") + "#" + volver)

# VER CARRITO
@app.route("/carrito")
def ver_carrito():

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            carrito.producto_id,
            carrito.cantidad,
            productos.nombre,
            productos.precio,
            productos.imagen
        FROM carrito
        INNER JOIN productos
        ON carrito.producto_id = productos.id
        WHERE carrito.usuario = ?
    """, (usuario,))

    carrito_bd = cursor.fetchall()

    conexion.close()

    carrito_lista = []

    total = 0

    for item in carrito_bd:

        subtotal = item["precio"] * item["cantidad"]

        total += subtotal

        carrito_lista.append({
            "id": item["producto_id"],
            "nombre": item["nombre"],
            "precio": item["precio"],
            "cantidad": item["cantidad"],
            "imagen": item["imagen"],
            "subtotal": subtotal
        })

    return render_template(
        "carrito.html",
        carrito=carrito_lista,
        total=total,
        usuario=session.get("usuario")
    )

# ELIMINAR PRODUCTO
@app.route("/eliminar/<int:id>")
def eliminar(id):

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    DELETE FROM carrito
    WHERE usuario=? AND producto_id=?
    """, (usuario, id))

    conexion.commit()
    conexion.close()

    return redirect(url_for("ver_carrito"))

#SUMAR
@app.route("/sumar/<int:id>")
def sumar(id):

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    UPDATE carrito
    SET cantidad = cantidad + 1
    WHERE usuario=? AND producto_id=?
    """, (usuario, id))

    conexion.commit()
    conexion.close()

    return redirect(url_for("ver_carrito"))

#RESTAR
@app.route("/restar/<int:id>")
def restar(id):

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT cantidad
    FROM carrito
    WHERE usuario=? AND producto_id=?
    """, (usuario, id))

    resultado = cursor.fetchone()

    if resultado:

        if resultado[0] > 1:

            cursor.execute("""
            UPDATE carrito
            SET cantidad = cantidad - 1
            WHERE usuario=? AND producto_id=?
            """, (usuario, id))

        else:

            cursor.execute("""
            DELETE FROM carrito
            WHERE usuario=? AND producto_id=?
            """, (usuario, id))

    conexion.commit()
    conexion.close()

    return redirect(url_for("ver_carrito"))

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    mensaje = ""
    clase = ""

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario == USUARIO_CORRECTO and password == PASSWORD_CORRECTO:

            session["usuario"] = usuario
            return redirect(url_for("inicio"))
        
        conexion = sqlite3.connect("abarrotes.db")

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT * FROM usuarios
            WHERE usuario=? AND password=?
            """,
            (usuario, password)
            )
        
        cliente = cursor.fetchone()

        conexion.close()

        if cliente:
            session["usuario"] = usuario
            return redirect(url_for("inicio"))

        else:

            mensaje = "❌ Usuario o contraseña incorrectos"
            clase = "incorrecto"

    return render_template(
        "login.html",
        mensaje=mensaje,
        clase=clase
    )

# CERRAR SESIÓN
@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(url_for("inicio"))

# PAGAR
@app.route("/pagar")
def pagar():

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            carrito.producto_id,
            carrito.cantidad,
            productos.nombre,
            productos.precio,
            productos.imagen
        FROM carrito
        INNER JOIN productos
        ON carrito.producto_id = productos.id
        WHERE carrito.usuario = ?
    """, (usuario,))

    carrito_bd = cursor.fetchall()

    conexion.close()

    carrito_lista = []
    total = 0

    for item in carrito_bd:

        subtotal = item["precio"] * item["cantidad"]

        total += subtotal

        carrito_lista.append({
            "id": item["producto_id"],
            "nombre": item["nombre"],
            "precio": item["precio"],
            "cantidad": item["cantidad"],
            "imagen": item["imagen"],
            "subtotal": subtotal
        })

    return render_template(
        "pagar.html",
        carrito=carrito_lista,
        total=total,
        usuario=session.get("usuario")
    )

# CONFIRMAR
@app.route("/confirmar")
def confirmar():

    usuario = session.get("usuario", "Invitado")

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT
        carrito.producto_id,
        carrito.cantidad,
        productos.nombre,
        productos.precio
    FROM carrito
    INNER JOIN productos
    ON carrito.producto_id = productos.id
    WHERE carrito.usuario = ?
    """, (usuario,))

    productos = cursor.fetchall()

    total = 0

    for producto in productos:
        total += producto["precio"] * producto["cantidad"]

    cursor.execute("""
    INSERT INTO compras(usuario,total)
    VALUES(?,?)
    """, (usuario, total))

    compra_id = cursor.lastrowid

    for producto in productos:

        subtotal = producto["precio"] * producto["cantidad"]

        cursor.execute("""
        INSERT INTO detalle_compra(
            compra_id,
            producto,
            cantidad,
            subtotal
        )
        VALUES(?,?,?,?)
        """,
        (
            compra_id,
            producto["nombre"],
            producto["cantidad"],
            subtotal
        ))

    cursor.execute("""
    DELETE FROM carrito
    WHERE usuario = ?
    """, (usuario,))

    conexion.commit()
    conexion.close()

    return render_template(
        "boleta.html",
        productos=productos,
        total=total,
        usuario=usuario
    )

# COMPRAS
@app.route("/compras")
def compras():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM compras
        WHERE usuario = ?
        ORDER BY id DESC
    """, (session["usuario"],))

    compras_usuario = cursor.fetchall()

    conexion.close()

    return render_template(
        "compras.html",
        compras=compras_usuario,
        usuario=session["usuario"]
    )

#ADMIN
@app.route("/admin")
def admin():

    if session.get("usuario") != "Zaidd":
        return redirect(url_for("inicio"))

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conexion.close()

    return render_template(
        "admin.html",
        productos=productos
    )

@app.route("/dashboard")
def dashboard():

    if session.get("usuario") != "Zaidd":
        return redirect(url_for("inicio"))

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    # KPIs
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM compras")
    total_compras = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total),0) FROM compras")
    ventas_totales = cursor.fetchone()[0]

    # Últimas compras
    cursor.execute("""
    SELECT usuario,total,id
    FROM compras
    ORDER BY id DESC
    LIMIT 5
    """)
    ultimas_compras = cursor.fetchall()

    # Top clientes
    cursor.execute("""
    SELECT usuario,
           COUNT(*) as cantidad
    FROM compras
    GROUP BY usuario
    ORDER BY cantidad DESC
    LIMIT 5
    """)
    top_clientes = cursor.fetchall()

    # Productos más vendidos
    cursor.execute("""
    SELECT producto,
           SUM(cantidad) as vendidos
    FROM detalle_compra
    GROUP BY producto
    ORDER BY vendidos DESC
    LIMIT 5
    """)
    productos_vendidos = cursor.fetchall()

    conexion.close()

    return render_template(
        "dashboard.html",
        total_productos=total_productos,
        total_usuarios=total_usuarios,
        total_compras=total_compras,
        ventas_totales=ventas_totales,
        ultimas_compras=ultimas_compras,
        top_clientes=top_clientes,
        productos_vendidos=productos_vendidos
    )

@app.route("/registro", methods=["GET", "POST"])
def registro():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        try:

            conexion = sqlite3.connect("abarrotes.db")

            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO usuarios(usuario,password)
                VALUES(?,?)
                """,
                (usuario, password)
            )

            conexion.commit()
            conexion.close()

            mensaje = "✅ Cuenta creada correctamente"

        except:

            mensaje = "❌ Ese usuario ya existe"

    return render_template(
        "registro.html",
        mensaje=mensaje
    )

#EDITAR PRODUCTOS
@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    if session.get("usuario") != "Zaidd":
        return redirect(url_for("inicio"))

    conexion = sqlite3.connect("abarrotes.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    if request.method == "POST":

        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        categoria = request.form["categoria"]

        imagen_actual = request.form["imagen_actual"]

        archivo = request.files.get("imagen")

        if archivo and archivo.filename != "":

            nombre_archivo = secure_filename(archivo.filename)

            archivo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    nombre_archivo
                )
            )

            imagen = nombre_archivo

        else:

            imagen = imagen_actual

        cursor.execute("""
            UPDATE productos
            SET nombre=?,
                precio=?,
                categoria=?,
                imagen=?
            WHERE id=?
        """,
        (
            nombre,
            precio,
            categoria,
            imagen,
            id
        ))

        conexion.commit()
        conexion.close()

        return redirect(url_for("admin"))

    cursor.execute(
        "SELECT * FROM productos WHERE id=?",
        (id,)
    )

    producto = cursor.fetchone()

    conexion.close()

    if producto is None:
        return f"Producto con ID {id} no encontrado"

    return render_template(
        "editar_producto.html",
        producto=producto
    )

#AGREGAR PRODUCTOS
@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():

    if session.get("usuario") != "Zaidd":
        return redirect(url_for("inicio"))

    if request.method == "POST":

        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        categoria = request.form["categoria"]
        imagen = request.form["imagen"]

        conexion = sqlite3.connect("abarrotes.db")
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO productos(nombre, precio, categoria, imagen)
        VALUES (?, ?, ?, ?)
        """, (nombre, precio, categoria, imagen))

        conexion.commit()
        conexion.close()

        return redirect(url_for("admin"))

    return render_template("agregar_producto.html")

#ELIMINAR PRODUCTO
@app.route("/eliminar_producto/<int:id>")
def eliminar_producto(id):

    if session.get("usuario") != "Zaidd":
        return redirect(url_for("inicio"))

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id=?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect(url_for("admin"))

#ELIMINAR COMPRAS
@app.route("/eliminar_compra/<int:id>")
def eliminar_compra(id):

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = sqlite3.connect("abarrotes.db")
    cursor = conexion.cursor()

    # Verificar que la compra pertenece al usuario
    cursor.execute("""
    SELECT usuario
    FROM compras
    WHERE id=?
    """, (id,))

    compra = cursor.fetchone()

    if compra and compra[0] == session["usuario"]:

        cursor.execute("""
        DELETE FROM detalle_compra
        WHERE compra_id=?
        """, (id,))

        cursor.execute("""
        DELETE FROM compras
        WHERE id=?
        """, (id,))

        conexion.commit()

    conexion.close()

    return redirect(url_for("compras"))

if __name__ == "__main__":
    app.run(debug=True)
    