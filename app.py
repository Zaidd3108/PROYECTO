from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "abarrotes_joel_2026"

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

@app.route("/pagar")
def pagar():

    total = sum(
        item["precio"] * item["cantidad"]
        for item in carrito
    )

    return render_template(
        "pagar.html",
        carrito=carrito,
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

#COMPRAS
@app.route("/compras")
def compras():

    if "usuario" not in session:
        return redirect(url_for("login"))

    compras_usuario = [
        compra
        for compra in historial_compras
        if compra["usuario"] == session["usuario"]
    ]

    return render_template(
        "compras.html",
        compras=compras_usuario,
        usuario=session["usuario"]
    )

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

if __name__ == "__main__":
    app.run(debug=True)