import sys
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash

# --- CROSS-PLATFORM PATH CONFIGURATION ---
# sys.frozen is True when running as a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # Directory where the .exe or binary is located
    BASE_DIR = os.path.dirname(sys.executable)
    # Temporary folder where PyInstaller extracts internal assets (templates/static)
    INTERNAL_DATA = sys._MEIPASS
else:
    # Standard development path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INTERNAL_DATA = BASE_DIR

# PERSISTENT FILES: Located in the same folder as the executable/script
DATA_FILE = os.path.join(BASE_DIR, "motos.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "motos")

# FLASK INIT: Points to internal data for templates/static UI assets
app = Flask(__name__, 
            template_folder=os.path.join(INTERNAL_DATA, "templates"),
            static_folder=os.path.join(INTERNAL_DATA, "static"))

app.secret_key = "ibiza_motos_secret"

# Ensure the upload folder exists physically on the disk
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- HELPER FUNCTIONS ---

def cargar_motos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

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
    Elimina espacios, $, puntos y comas.
    """
    limpio = valor.strip().replace(" ", "").replace("$", "").replace(".", "").replace(",", "")
    try:
        n = float(limpio)
        return n > 0
    except ValueError:
        return False

# --- ROUTES ---

@app.route("/")
def cotizador():
    motos = cargar_motos()
    marcas = sorted(list(set(m["marca"] for m in motos)))
    return render_template("index.html", motos=motos, marcas=marcas)

@app.route("/admin")
def admin():
    orden = request.args.get("orden", "desc")
    motos = cargar_motos()

    # Guardar índice original antes de ordenar para que los IDs de edición no se rompan
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

    if not validar_precio(precio_contado) or not validar_precio(precio_credito):
        flash("Los precios deben ser números positivos.", "error")
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

    if not validar_precio(precio_contado) or not validar_precio(precio_credito):
        flash("Los precios deben ser números positivos.", "error")
        return redirect("/admin")

    motos = cargar_motos()
    if 0 <= i < len(motos):
        motos[i]["precio_contado"] = precio_contado
        motos[i]["precio_credito"] = precio_credito
        motos[i]["fecha_modificacion"] = ahora()
        guardar_motos(motos)
        flash("Cambios guardados correctamente.", "ok")
    
    return redirect("/admin")

@app.route("/admin/eliminar/<int:i>")
def eliminar(i):
    motos = cargar_motos()
    if 0 <= i < len(motos):
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
    if "imagen" not in request.files:
        flash("No se seleccionó ninguna imagen.", "error")
        return redirect("/admin")

    archivo = request.files["imagen"]
    if archivo.filename == '':
        flash("Archivo no válido.", "error")
        return redirect("/admin")

    if 0 <= i < len(motos):
        moto = motos[i]
        nombre = nombre_imagen(moto["marca"], moto["modelo"])
        ruta = os.path.join(UPLOAD_FOLDER, nombre)
        
        # Ensure the directory exists right before saving
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        archivo.save(ruta)
        flash("Imagen subida correctamente.", "ok")
        
    return redirect("/admin")

if __name__ == "__main__":
    # debug=False prevents the "reloader" from opening the app twice in a bundle
    app.run(host="127.0.0.1", port=5000, debug=False)