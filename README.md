# Cotizador de Motos - Ibiza Motos

Aplicación web para generar cotizaciones de motos con gestión de catálogo.

## Requisitos

- Python 3.8+
- Flask

## Instalación

```bash
# Instalar dependencias
pip install flask

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

---

## Uso del Cotizador

### Generar una Cotización

1. **Seleccionar marca**: Elige la marca de la moto del dropdown.
2. **Seleccionar modelo**: Elige el modelo específico.
3. **Ingresar datos del asesor**:
   - **Asesor**: Nombre del vendedor (obligatorio)
   - **Celular**: Teléfono de contacto (obligatorio)
   - **Info extra**: Información adicional opcional (soporta Markdown)
4. **Seleccionar tipo de precio**: Marca las casillas de "Contado" y/o "Crédito" según lo que quieras mostrar.
5. **Generar cotización**: Haz clic en "Generar Cotización".

### Modal de Cotización

El modal de cotización muestra:
- Logo de la empresa
- Fecha de generación
- Modelo de la moto
- Imagen (si existe)
- Precios seleccionados
- Información adicional (si se llenó)
- Datos del asesor

**Impresión**: El modal está optimizado para impresión. Puedes usar `Ctrl+P` o el botón "Imprimir" para guardar como PDF en tamaño carta.

---

## Administración del Catálogo

Accede al panel de administración en `/admin`

### Agregar una Moto

1. En el panel de admin, baja hasta el formulario "Agregar nueva moto".
2. Completa los campos:
   - **Marca**: Nombre de la marca
   - **Modelo**: Nombre del modelo
   - **Precio contado**: Precio de contado
   - **Precio crédito**: Precio a crédito
3. Haz clic en "Agregar moto".

**Nota**: El nombre de la imagen se genera automáticamente como `marca_modelo.jpg` (ejemplo: `honda_cb125f.jpg`)

### Editar Precios

1. En la tabla de motos, modifica los valores en los campos de "Contado" o "Crédito".
2. Haz clic en "Guardar" en la fila correspondiente.

### Cargar/Actualizar Imagen

1. Cada moto tiene un formulario para subir imagen.
2. Selecciona un archivo JPG.
3. Haz clic en "Subir/Actualizar".

**Importante**: 
- La imagen debe ser JPG
- El nombre se genera automáticamente según el patrón: `marca_modelo.jpg`
- Si la imagen existe, se muestra una previsualización pequeña
- Si no existe, se muestra el mensaje "Sin imagen" con la ruta

### Eliminar una Moto

1. Haz clic en el botón "Eliminar" en la fila de la moto.
2. Confirma la eliminación.
3. La moto y su imagen (si existe) serán eliminadas.

### Ordenar el Catálogo

Usa el dropdown "Ordenar por fecha modificación" para ver las motos más recientes o más antiguas primero.

---

## Imágenes

### Ruta de Imágenes

Las imágenes deben estar en la carpeta `static/motos/`

### Nombre de Archivo

El sistema genera automáticamente el nombre de la imagen:
```
{marca}_{modelo}.jpg
```

Ejemplos:
- Honda CB125F → `honda_cb125f.jpg`
- Yamaha FZ-S → `yamaha_fz-s.jpg`
- Suzuki Gixxer 250 → `suzuki_gixxer_250.jpg`

### Error de Imagen

Si una imagen no existe:
- En el cotizador: Se muestra un mensaje de error con la ruta de la imagen que debería existir
- En el admin: Se muestra "Sin imagen" y la ruta

---

## Información Adicional (Markdown)

El campo "Info extra" en el cotizador soporta **Markdown** para dar formato al texto.

### Características Soportadas

- **Párrafos**: Texto normal
- **Negrita**: `**texto**` o `__texto__`
- *Cursiva*: `*texto*` o `_texto_`
- **Encabezados**: `# H1`, `## H2`, `### H3`
- **Listas**: `- elemento` o `1. elemento`
- **Links**: `[texto](url)`

### Ejemplo de Info Extra

```markdown
## Equipaje incluido
- Casco importado
- Guantes
- Chaleco reflectivo

**Precio especial**: $150.000 adicionales

*Válido solo esta semana*
```

---

## Estructura del Proyecto

```
/Cotizaciones
├── app.py                 # Aplicación Flask
├── motos.json             # Base de datos de motos
├── README.md              # Este archivo
├── templates/
│   ├── index.html         # Cotizador
│   └── admin.html         # Panel de administración
└── static/
    ├── empresa/
    │   └── ibiza.jpg      # Logo de la empresa
    └── motos/             # Imágenes de las motos
```

---

## Datos del Proyecto

- **Empresa**: Ibiza Motos
- **Desarrollado**: 2026
