from clases.usuario import Usuario
from clases.prestamo import Prestamo
from clases.libro import Libro
from typing import List, Tuple

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import os

matplotlib.use("Agg")

def validar_estructura(carpetas):
    if not os.path.exists(carpetas):
            os.makedirs(carpetas)

def crear_nombre_archivo(tipo):
    if tipo == 0:
        tp_rep = "tabla"
    else:
        tp_rep = "grafico"
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{fecha_hora_actual}_{tp_rep}.pdf"


import matplotlib.pyplot as plt
from typing import List
from io import BytesIO

def crear_grafico(data: List[int], labels: List[str]):
    buffer = BytesIO()

    plt.figure(figsize=(6, 6))  # Aumenté ligeramente el tamaño para mejor visualización
    wedges, texts, autotexts = plt.pie(
        data, 
        labels=labels, 
        autopct='%1.1f%%', 
        textprops={'fontsize': 8}  # Tamaño de letra más pequeño para los labels
    )

    # Ajusta los porcentajes dentro del gráfico
    for autotext in autotexts:
        autotext.set_fontsize(10)  # Tamaño de letra más grande
        autotext.set_fontweight('bold')  # Texto en negrita

    plt.axis('equal')  # Asegura que el gráfico sea circular
    plt.tight_layout()  # Ajusta automáticamente los márgenes

    plt.savefig(buffer, format='png', bbox_inches='tight')  # Guarda la imagen con márgenes ajustados
    plt.close()

    buffer.seek(0)
    return buffer



def calcular_ancho_columnas(columnas: List[str], data: List[List], font_name="Helvetica", font_size=10):
    # Determina el ancho de cada columna en función del mayor elemento de cada una
    ancho_columnas = []
    for i, columna in enumerate(columnas):
        max_ancho = stringWidth(columna, font_name, font_size)
        for fila in data:
            texto = str(fila[i])
            ancho_texto = stringWidth(texto, font_name, font_size)
            if ancho_texto > max_ancho:
                max_ancho = ancho_texto
        ancho_columnas.append(max_ancho + 10)  # Añadir margen de 10 unidades
    return ancho_columnas

def crear_tabla(columnas : List[str], data : List[List], ancho_columnas: List[float]):
    tabla_data = data
    tabla_data.insert(0, columnas)

    table = Table(tabla_data, colWidths=ancho_columnas)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
    return table

# def crear_tabla(columnas : List[str], data : List[List], ancho_columnas: List[float]):
#     tabla_data = data
#     tabla_data.insert(0, columnas)

#     table = Table(tabla_data, colWidths=[1 * inch, 1 * inch, 1 * inch])
#     table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#     ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
#     return table

def generar_reporte_grafico(fileloc : str, titulo_informe : str, subtitulo : str, data : List[int], labels : List[str]):
    # Crear un documento PDF
    doc = SimpleDocTemplate(fileloc, pagesize=letter)
    # Crear una lista de elementos para agregar al informe
    elements = []
    # Agregar un título al informe
    elements.append(Paragraph(titulo_informe))
    elements.append(Spacer(1, 12))
    # Agregar un subtítulo
    elements.append(Paragraph(subtitulo))
    elements.append(Spacer(1, 12))

    grafico = crear_grafico(data, labels)

    # Agregar el gráfico al informe como una imagen
    elements.append(Image(grafico, width=300, height=300))
    elements.append(Spacer(1, 12))
    # Cerrar el documento PDF
    doc.build(elements)

def generar_reporte_tabla(fileloc : str, titulo_informe : str, subtitulo : str, columnas : List[str], data : List[List]):
    ancho_columnas = calcular_ancho_columnas(columnas, data)

    page_width = sum(ancho_columnas) + inch
    page_height = 6 * inch
    
    # Crear un documento PDF
    doc = SimpleDocTemplate(fileloc, pagesize=(page_width, page_height))
    # Crear una lista de elementos para agregar al informe
    elements = []
    # Agregar un título al informe
    elements.append(Paragraph(titulo_informe))
    elements.append(Spacer(1, 12))
    # Agregar un subtítulo
    elements.append(Paragraph(subtitulo))
    elements.append(Spacer(1, 12))

    tabla = crear_tabla(columnas, data, ancho_columnas)

    # Agregar el gráfico al informe como una imagen
    elements.append(tabla)
    # Cerrar el documento PDF
    doc.build(elements)

# def generar_reporte_tabla(fileloc : str, titulo_informe : str, subtitulo : str, columnas : List[str], data : List[List]):
#     # Crear un documento PDF
#     doc = SimpleDocTemplate(fileloc, pagesize=letter)
#     # Crear una lista de elementos para agregar al informe
#     elements = []
#     # Agregar un título al informe
#     elements.append(Paragraph(titulo_informe))
#     elements.append(Spacer(1, 12))
#     # Agregar un subtítulo
#     elements.append(Paragraph(subtitulo))
#     elements.append(Spacer(1, 12))

#     tabla = crear_tabla(columnas, data)

#     # Agregar el gráfico al informe como una imagen
#     elements.append(tabla)
#     # Cerrar el documento PDF
#     doc.build(elements)


def generar_reporte_librosmasprestados(vec : List[Tuple[Libro, int]], tipo_reporte : int):
    # Tipo reporte puede ser 0:Tabular o 1:Gráfico
    nombre_archivo = crear_nombre_archivo(tipo_reporte)

    carpeta = os.path.join('reportes', 'libros_mas_prestados')
    file = os.path.join(carpeta, nombre_archivo)
    validar_estructura(carpeta)
    
    titulo = "Libros más Prestados en el mes"
    subtitulo = ""

    if tipo_reporte == 0:
        columnas = ["ISBN", "Título del Libro", "Autor", "Género", "Año de Publicación", "Cantidad de Préstamos"]
        data = []
        for tupla in vec:
            libro = tupla[0]
            cantidad = tupla[1]
            data.append([libro._ISBN, libro._Titulo, f'{libro._Autor._Nombre} {libro._Autor._Apellido}', libro._Genero, libro._Anio , cantidad])
        subtitulo = "Tabla de Libros más prestados en el mes"
        generar_reporte_tabla(file, titulo, subtitulo, columnas, data)
    
    elif tipo_reporte == 1:
        labels = []
        data = []
        for tupla in vec:
            libro = tupla[0]
            cantidad = tupla[1]
            label = f"{libro._ISBN} - {libro._Titulo}"

            data.append(cantidad)
            labels.append(label)
        subtitulo = "Gráfico de Libros más prestados en el mes, con su ISBN y Título"
        generar_reporte_grafico(file, titulo, subtitulo, data, labels)

def generar_reporte_usuarios_con_mas_prestamos(vec : List[Tuple[Usuario, int]], tipo_reporte : int):
    # Tipo reporte puede ser 0:Tabular o 1:Gráfico
    nombre_archivo = crear_nombre_archivo(tipo_reporte)

    carpeta = os.path.join('reportes', 'usuarios_con_mas_prestamos')
    file = os.path.join(carpeta, nombre_archivo)
    validar_estructura(carpeta)
    
    titulo = "Usuarios con más libros prestados"
    subtitulo = ""

    if tipo_reporte == 0:
        columnas = ["ID del Usuario", "Nombre del Usuario", "Tipo", "Cantidad de Préstamos"]
        data = []
        for tupla in vec:
            usuario = tupla[0]
            cantidad = tupla[1]
            data.append([usuario._ID, f"{usuario._Nombre} {usuario._Apellido}", usuario.get_string_tipo(), cantidad])
        subtitulo = "Tabla de Usuarios con más libros prestados"
        generar_reporte_tabla(file, titulo, subtitulo, columnas, data)
    
    elif tipo_reporte == 1:
        labels = []
        data = []
        for tupla in vec:
            usuario = tupla[0]
            cantidad = tupla[1]
            label = f"{usuario._ID} - {usuario._Nombre} {usuario._Apellido}"

            data.append(cantidad)
            labels.append(label)
        subtitulo = "Gráfico de Usuarios con más libros prestados"
        generar_reporte_grafico(file, titulo, subtitulo, data, labels)

def generar_reporte_prestamos_vencidos(vec : List[Prestamo]):

    nombre_archivo = crear_nombre_archivo(0)

    carpeta = os.path.join('reportes', 'prestamos_vencidos')
    file = os.path.join(carpeta, nombre_archivo)
    validar_estructura(carpeta)
    
    titulo = "Préstamos vencidos"
    subtitulo = ""

    columnas = ["ID", "ID Usuario", "Nombre Usuario", "ISBN Libro", "Título del Libro", "Fecha Préstamo", "Fecha Estimada Devolución"]
    data = []
    for prestamo in vec:
        data.append([prestamo._ID, prestamo._Usuario._ID ,f"{prestamo._Usuario._Nombre} {prestamo._Usuario._Apellido}", prestamo._Libro._ISBN, prestamo._Libro._Titulo, prestamo._FechaPrestamo, prestamo.calcular_devolucion()])
    
    subtitulo = "Tabla de Préstamos Vencidos"
    generar_reporte_tabla(file, titulo, subtitulo, columnas, data)