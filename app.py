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
        categoria=categoria
    )

# AGREGAR AL CARRITO
@app.route("/agregar/<int:id>")
def agregar(id):

    for producto in productos:

        if producto["id"] == id:
            carrito.append(producto)

    return redirect(url_for("inicio"))

# VER CARRITO
@app.route("/carrito")
def ver_carrito():

    total = sum(item["precio"] for item in carrito)

    return render_template(
        "carrito.html",
        carrito=carrito,
        total=total
    )

# ELIMINAR PRODUCTO
@app.route("/eliminar/<int:index>")
def eliminar(index):

    if index < len(carrito):
        carrito.pop(index)

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

            mensaje = "✅ Bienvenido Zaidd"
            clase = "correcto"

        else:

            mensaje = "❌ Usuario o contraseña incorrectos"
            clase = "incorrecto"

    return render_template(
        "login.html",
        mensaje=mensaje,
        clase=clase
    )

if __name__ == "__main__":
    app.run(debug=True)