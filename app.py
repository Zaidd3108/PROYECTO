from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "abarrotes_joel_2026"

# LOGIN
USUARIO_CORRECTO = "Zaidd"
PASSWORD_CORRECTO = "3101"

# PRODUCTOS
productos = [
    {
        "id": 1,
        "nombre": "Arroz Costeño",
        "precio": 4.50,
        "categoria": "Abarrotes"
    },
    {
        "id": 2,
        "nombre": "Azúcar Rubia",
        "precio": 3.20,
        "categoria": "Abarrotes"
    },
    {
        "id": 3,
        "nombre": "Leche Gloria",
        "precio": 5.90,
        "categoria": "Lácteos"
    },
    {
        "id": 4,
        "nombre": "Aceite Primor",
        "precio": 11.50,
        "categoria": "Abarrotes"
    },
    {
        "id": 5,
        "nombre": "Coca Cola 3L",
        "precio": 12.50,
        "categoria": "Bebidas"
    },
    {
        "id": 6,
        "nombre": "Detergente Bolívar",
        "precio": 8.90,
        "categoria": "Limpieza"
    }
]

# CARRITO
carrito = []
historial_compras = []

# PÁGINA PRINCIPAL
@app.route("/")
def inicio():

    busqueda = request.args.get("buscar", "").strip()
    categoria = request.args.get("categoria", "")

    productos_filtrados = productos

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

    return render_template(
        "index.html",
        productos=productos_filtrados,
        carrito=carrito,
        busqueda=busqueda,
        categoria=categoria,
        usuario=session.get("usuario")
    )

# AGREGAR AL CARRITO
@app.route("/agregar/<int:id>")
def agregar(id):

    for item in carrito:

        if item["id"] == id:
            item["cantidad"] += 1
            return redirect(url_for("inicio"))

    for producto in productos:

        if producto["id"] == id:

            nuevo_producto = producto.copy()
            nuevo_producto["cantidad"] = 1
            carrito.append(nuevo_producto)
            break

    return redirect(url_for("inicio"))

# VER CARRITO
@app.route("/carrito")
def ver_carrito():

    total = sum(
        item["precio"] * item["cantidad"]
        for item in carrito
    )

    return render_template(
        "carrito.html",
        carrito=carrito,
        total=total,
        usuario=session.get("usuario")
    )

# ELIMINAR PRODUCTO
@app.route("/eliminar/<int:index>")
def eliminar(index):

    if index < len(carrito):
        carrito.pop(index)

    return redirect(url_for("ver_carrito"))

@app.route("/sumar/<int:id>")
def sumar(id):

    for item in carrito:

        if item["id"] == id:
            item["cantidad"] += 1

    return redirect(url_for("ver_carrito"))


@app.route("/restar/<int:id>")
def restar(id):

    for item in carrito:

        if item["id"] == id:
            item["cantidad"] -= 1
            if item["cantidad"] <= 0:
                carrito.remove(item)

            break

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

@app.route("/confirmar")
def confirmar():

    global carrito

    total = sum(
        item["precio"] * item["cantidad"]
        for item in carrito
    )

    compra = {
        "usuario": session.get("usuario", "Invitado"),
        "productos": carrito.copy(),
        "total": total
    }

    historial_compras.append(compra)

    carrito = []

    return render_template(
        "boleta.html",
        compra=compra
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

if __name__ == "__main__":
    app.run(debug=True)