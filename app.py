from flask import Flask, render_template, request, redirect, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ibiza_motos_secret"

DATA_FILE = "motos.json"
UPLOAD_FOLDER = "static/motos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def cargar_motos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_motos(motos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(motos, f, indent=4, ensure_ascii=False)


def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def nombre_imagen(marca, modelo):
    marca_file = marca.lower().replace(" ", "_")
    modelo_file = modelo.lower().replace(" ", "_")
    return f"{marca_file}_{modelo_file}.jpg"


def validar_precio(valor):
    """
    Acepta enteros o decimales positivos.
    Elimina espacios, $, puntos y comas para soportar
    formatos como $8.500.000 o 8,500,000
    """
    limpio = valor.strip().replace(" ", "").replace("$", "").replace(".", "").replace(",", "")
    try:
        n = float(limpio)
        return n > 0
    except ValueError:
        return False


@app.route("/")
def cotizador():
    motos = cargar_motos()
    marcas = sorted(list(set(m["marca"] for m in motos)))
    return render_template("index.html", motos=motos, marcas=marcas)


@app.route("/admin")
def admin():
    orden = request.args.get("orden", "desc")
    motos = cargar_motos()

    # Guardar índice original antes de ordenar
    for i, m in enumerate(motos):
        m["_idx"] = i

    motos = sorted(
        motos,
        key=lambda x: x.get("fecha_modificacion", ""),
        reverse=(orden == "desc")
    )
    return render_template("admin.html", motos=motos, orden=orden)


@app.route("/admin/agregar", methods=["POST"])
def agregar():
    marca          = request.form["marca"].strip()
    modelo         = request.form["modelo"].strip()
    precio_contado = request.form["precio_contado"].strip()
    precio_credito = request.form["precio_credito"].strip()

    if not validar_precio(precio_contado):
        flash("El precio contado debe ser un número positivo.", "error")
        return redirect("/admin")

    if not validar_precio(precio_credito):
        flash("El precio crédito debe ser un número positivo.", "error")
        return redirect("/admin")

    motos = cargar_motos()
    now = ahora()

    motos.append({
        "marca": marca,
        "modelo": modelo,
        "precio_contado": precio_contado,
        "precio_credito": precio_credito,
        "fecha_creacion": now,
        "fecha_modificacion": now
    })

    guardar_motos(motos)
    flash(f"{marca} {modelo} agregada correctamente.", "ok")
    return redirect("/admin")


@app.route("/admin/editar/<int:i>", methods=["POST"])
def editar(i):
    precio_contado = request.form["precio_contado"].strip()
    precio_credito = request.form["precio_credito"].strip()

    if not validar_precio(precio_contado):
        flash("El precio contado debe ser un número positivo.", "error")
        return redirect("/admin")

    if not validar_precio(precio_credito):
        flash("El precio crédito debe ser un número positivo.", "error")
        return redirect("/admin")

    motos = cargar_motos()
    motos[i]["precio_contado"] = precio_contado
    motos[i]["precio_credito"] = precio_credito
    motos[i]["fecha_modificacion"] = ahora()

    guardar_motos(motos)
    flash("Cambios guardados correctamente.", "ok")
    return redirect("/admin")


@app.route("/admin/eliminar/<int:i>")
def eliminar(i):
    motos = cargar_motos()
    moto = motos[i]

    nombre = nombre_imagen(moto["marca"], moto["modelo"])
    ruta = os.path.join(UPLOAD_FOLDER, nombre)

    if os.path.exists(ruta):
        os.remove(ruta)

    motos.pop(i)
    guardar_motos(motos)
    flash("Moto eliminada.", "ok")
    return redirect("/admin")


@app.route("/admin/subir_imagen/<int:i>", methods=["POST"])
def subir_imagen(i):
    motos = cargar_motos()
    archivo = request.files["imagen"]
    moto = motos[i]

    nombre = nombre_imagen(moto["marca"], moto["modelo"])
    ruta = os.path.join(UPLOAD_FOLDER, nombre)

    archivo.save(ruta)
    flash("Imagen subida correctamente.", "ok")
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)