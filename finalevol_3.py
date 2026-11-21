# -*- coding: utf-8 -*-
# RECOMENDADOR EVOLUTIVO DE VIDEOJUEGOS
# Proyecto de Programación 2 de Inteligencia Artificial.
# Adaptado del proyecto original de nattfernandez.

# ======================================================================
# MANUAL DE USUARIO
# ======================================================================

# 1. Propósito
#    El programa recomienda listas cortas de videojuegos, como lo hace una
#    plataforma de series. La primera vez pregunta tus gustos con un
#    cuestionario breve. Después aprende de las valoraciones que escribes
#    en la consola («me interesa» o «no me interesa»). Todo lo que el
#    programa sabe de ti proviene de lo que escribes en la consola: no lee
#    cuentas de Steam ni archivos de tu computadora. Las respuestas se
#    guardan en un perfil, así que no vuelve a preguntarte tus preferencias
#    en cada ejecución: este perfil aprendido sustituye a la memoria de
#    casos del diseño original.

#    Por dentro hay dos algoritmos evolutivos que solo usan mutación:
#    a) El evolutivo base arma la lista. Cada individuo es una lista
#       ordenada de N juegos. Su aptitud combina la afinidad con tus gustos,
#       la variedad de la lista y la continuidad entre juegos vecinos.
#    b) El meta-evolutivo diseña al evolutivo base. Busca su tamaño de
#       población, su cantidad de descendientes por generación, su tamaño
#       de torneo y su probabilidad de mutación dirigida. Mide cada
#       configuración con 50 ejecuciones del evolutivo base: calidad media
#       de las listas, generación media de convergencia y diversidad
#       genética media.
#    Los géneros seleccionados tienen el mismo peso inicial. La lista combina la afinidad
#    aprendida de esa persona con la variedad y la relación entre títulos consecutivos.
#    Si indicas varios favoritos, la lista también busca juegos afines a cada uno.
#    Steam aporta etiquetas que faltan en Kaggle. Las etiquetas guardadas duran 30 días.
#    Ambos niveles usan la misma clase AlgoritmoEvolutivo, porque el
#    algoritmo no depende del tipo de individuo que evoluciona.

# 2. Requisitos
#    Python 3.10 o posterior, por ejemplo el que incluye Anaconda con
#    Spyder. Solo usa la biblioteca estándar, así que no hay que instalar
#    paquetes.

# 3. Ejecución en Spyder
#    Abre este archivo y pulsa F5. Las preguntas aparecen en la consola de
#    IPython: escribe la respuesta y pulsa Enter.

# 4. Primera ejecución
#    a) Datos. No tienes que descargar nada a mano ni tener cuenta de Kaggle.
#       Cada vez que pulsas F5, el programa consulta la API de Kaggle (sección
#       10) y compara la versión de cada catálogo con la última que descargó:
#       - La primera vez, o si el autor publicó una versión nueva, descarga
#         el archivo y prepara una copia reducida en la carpeta datos_juegos.
#         El catálogo de Steam pesa cientos de megabytes, así que esa
#         descarga puede tardar varios minutos; la consola muestra el avance.
#       - Si la versión no cambió, no descarga nada y arranca en segundos.
#       - Si no hay internet, usa la última copia guardada y lo avisa.
#       Necesitas internet al menos la primera vez.
#       Las recomendaciones empiezan en 2026. También consulta hasta 16 fichas
#       de la tienda pública de Steam para incorporar anuncios. Guarda esa lista
#       durante siete días. Los favoritos pueden ser de cualquier año. Wikidata aporta
#       las consolas por AppID. Si faltan estrenos verificables para tu consola, el programa
#       lo avisa y consulta también su catálogo histórico. «Nintendo» y «Xbox» abarcan
#       su familia entera. Escribe el modelo exacto cuando solo tengas una consola.
#       El programa descarta indicios de contenido sexual o desnudez. Antes
#       de recomendar un juego de Steam comprueba los avisos de su ficha
#       pública. Si no puede comprobarlo, puede mostrar una lista más corta.
#    b) Perfil y cuestionario. Escribe tu apodo para guardar tus respuestas y valoraciones.
#       Cada persona debe usar un apodo distinto. Si ya tenías un perfil antes de esta
#       versión, pulsa Enter para abrirlo. Después responde:
#       - los géneros que te gustan, con sus números separados por comas
#         (por ejemplo 1, 3, 12) o con sus nombres (por ejemplo terror, rol);
#       - los géneros que prefieres evitar (Enter para omitir); esos juegos
#         nunca se recomiendan;
#       - hasta cinco juegos que te hayan gustado: escribe parte del título,
#         por ejemplo zelda, y elige uno de los resultados por su número; no
#         importan las mayúsculas, los acentos ni los espacios;
#       - tu plataforma, por ejemplo PC, PS4 o Wii (Enter si te da igual).
#       Debes indicar al menos un género o un juego, porque el programa no
#       arma listas solo por popularidad.
#    c) Ajuste. El meta-evolutivo busca los parámetros del evolutivo base.
#       Tarda alrededor de un minuto y se guarda para las siguientes
#       ejecuciones con la misma longitud de lista.

# 5. Ejecuciones siguientes
#    El programa muestra los gustos guardados. Pulsa Enter para continuar o
#    escribe C para contestar otra vez el cuestionario.

# 6. Valoraciones
#    Debajo de cada lista escribe los números que te interesan y, con un
#    signo menos, los que no. Por ejemplo, «1 3 -2» marca el 1 y el 3 como
#    interesantes y el 2 como no interesante. Enter omite la valoración.
#    Los juegos valorados no se vuelven a recomendar y el perfil se
#    recalcula con ellos. Después puedes pedir otra lista en la misma sesión.
#    Una lista de dos o más juegos incluye un próximo lanzamiento y un juego
#    con fecha de estreno pasada si ambos cumplen tus filtros. Steam puede
#    cambiar una fecha anunciada o dejarla por confirmar.

# 7. Opciones
#    Puedes cambiar las constantes de la sección «Opciones de ejecución»
#    antes de pulsar F5, o usar estos argumentos en una terminal:
#        python ia2.py Silent Hill 2        juego de referencia para esta ejecución
#        --plataforma PS4                   filtra solo esta ejecución
#        --longitud 8                       juegos por lista (de 1 a 10)
#        --cambiar-gustos                   repite el cuestionario
#        --sin-preguntas                    usa lo guardado y no pregunta nada
#        --perfil otro.sqlite3              usa el perfil de otra persona
#        --carpeta RUTA                     carpeta donde están los catálogos
#        --semilla 7                        otra semilla para los números aleatorios
#        --experimentos                     ejecuta los experimentos del reporte

# 8. Modo de experimentos
#    Con --experimentos, o con MODO_EXPERIMENTOS = True, el programa no
#    recomienda. Mide con 50 ejecuciones cada configuración válida del
#    evolutivo base, ejecuta 50 veces el meta-evolutivo y compara qué
#    parámetros son los mejores para cada nivel. Tarda varios minutos y
#    escribe tablas listas para el reporte.

# 9. Archivos que crea
#    datos_juegos/                  copias reducidas de los catálogos y
#                                   versiones_kaggle.json (versión de cada descarga).
#    perfil_recomendador.sqlite3    perfil local predeterminado.
#    perfiles/                      un archivo SQLite por apodo.
#    Borrar el archivo del perfil reinicia los gustos y los ajustes. Borrar
#    datos_juegos obliga a descargar otra vez los catálogos. Para usar el
#    programa en una computadora sin internet, copia la carpeta datos_juegos
#    junto a este archivo.

# 10. Fuentes de datos (API pública de Kaggle)
#    - Video Game Sales with Ratings, de rush4ratio (se descarga
#      Video_Games_Sales_as_at_22_Dec_2016.csv):
#      https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings
#    - Steam Games Dataset, de FronkonGames (se descarga solo games.csv):
#      https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
#    Orden en que se obtiene cada catálogo:
#      1. La API de Kaggle, en cada ejecución (descarga solo si hay versión nueva).
#      2. Si Kaggle no responde, la última copia guardada en datos_juegos.
#      3. Si nunca se descargó, un archivo de Kaggle colocado junto a este programa.
#    Kaggle permite descargar sin cuenta los conjuntos públicos. Si alguna vez
#    lo exigiera, el programa usa las credenciales de ~/.kaggle/kaggle.json o de
#    las variables KAGGLE_USERNAME y KAGGLE_KEY; no hay claves en este archivo.
#    Al iniciar, el programa indica de dónde salió cada catálogo y cuántos
#    juegos leyó. Las listas usan el catálogo de Steam.

# 11. Problemas frecuentes
#    - «No se pudo consultar Kaggle»: revisa tu conexión y vuelve a pulsar F5.
#      Sin internet, descarga games.csv desde la página de la sección 10 y
#      déjalo junto al programa.
#    - «Plataforma desconocida»: usa uno de los nombres que sugiere el mensaje.
#    - Para empezar de cero, borra perfil_recomendador.sqlite3.

import argparse
import base64
import csv
import difflib
import hashlib
import io
import json
import math
import os
from itertools import islice, zip_longest
import random
import re
import sqlite3
import statistics
import tempfile
import time
import unicodedata
import zipfile
import zlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from http.client import HTTPException
from pathlib import Path
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen


# ----------------------------------------------------------------------
# Opciones de ejecución. Se pueden cambiar antes de pulsar F5.
# ----------------------------------------------------------------------

JUEGO_DE_REFERENCIA = ""         # Título que orienta solo esta ejecución, por ejemplo "Silent Hill 2".
PLATAFORMA_PREFERIDA = ""        # Plataforma solo para esta ejecución; vacía usa la del cuestionario.
LONGITUD_DE_RUTA = 5             # Cantidad de juegos de cada lista recomendada (de 1 a 10).
SEMILLA_PREDETERMINADA = 2026    # Semilla de los números aleatorios; con los mismos datos repite el resultado.
HACER_PREGUNTAS = True           # False usa solo lo guardado, sin cuestionario ni valoraciones.
MODO_EXPERIMENTOS = False        # True ejecuta los experimentos del reporte en lugar de recomendar.
CARPETA_DEL_PROGRAMA = Path(__file__).resolve().parent


# ----------------------------------------------------------------------
# Parámetros del modelo y de los algoritmos evolutivos.
# ----------------------------------------------------------------------

PRESUPUESTO_DE_BUSQUEDA = 480       # Listas que evalúa el evolutivo base en una ejecución.
PRESUPUESTO_DEL_META = 40           # Configuraciones que evalúa el meta-evolutivo en un ajuste.
EJECUCIONES_POR_CONFIGURACION = 50  # Ejecuciones del evolutivo base con las que se mide una configuración.
ESCENARIOS_DE_AJUSTE = 5            # Jugadores simulados del ajuste; cada uno recibe 50 / 5 = 10 ejecuciones.
OBJETIVO_DE_CONVERGENCIA = 0.95     # Fracción de la mejora posible a partir de la cual una ejecución convergió.
TAMANO_DE_RESERVA = 200             # Candidatos de mayor afinidad entre los que muta el evolutivo base.
TAMANO_DE_PREFERIDOS = 24           # Candidatos de mayor afinidad que usa la mutación dirigida.
PROBABILIDAD_DE_INTERCAMBIO = 0.28  # Probabilidad de que una mutación intercambie dos posiciones de la lista.
ANIO_DESDE = 2026                   # Primer año de las recomendaciones. Los favoritos pueden ser anteriores.
PESO_DE_LA_RESENA = 0.20            # Parte de la afinidad que proviene de las reseñas públicas.
PESO_DEL_HISTORIAL = 0.70           # Cuando también se declararon géneros.
MINIMO_DE_RESENAS = 101             # Más de cien reseñas reales.
PESO_PREVIO_GUSTA = 1.2             # Peso inicial de un género elegido como favorito en el cuestionario.
ITERACIONES_DE_APRENDIZAJE = 70     # Vueltas del descenso de gradiente de la regresión logística.
TASA_DE_APRENDIZAJE = 0.7           # Tamaño de cada paso del descenso de gradiente.
REGULARIZACION = 0.06               # Fuerza que acerca cada peso a su valor inicial (evita pesos extremos).
MAXIMO_DE_FAVORITOS = 5             # Juegos que se pueden declarar en el cuestionario.
LONGITUD_MAXIMA = 10                # Mayor longitud de lista; más juegos hacen lento el primer ajuste.
VERSION_DEL_AJUSTE = 11             # Distingue los ajustes guardados por versiones anteriores del programa.
NOMBRE_DEL_PERFIL = "perfil_recomendador.sqlite3"
NOMBRE_DE_LAS_COPIAS = "datos_juegos"

# Kaggle es la fuente principal de los dos catálogos. En cada ejecución se consulta su
# API y solo se descarga el archivo cuando hay una versión nueva (ver obtener_fuente).
API_DE_KAGGLE = "https://www.kaggle.com/api/v1/datasets/download/"
FUENTES_DE_KAGGLE = {
    "ventas": "rush4ratio/video-game-sales-with-ratings",
    "steam": "fronkongames/steam-games-dataset",
}
# Archivo que se descarga de cada conjunto. De Steam solo se baja games.csv: el
# conjunto completo también trae games.json, que pesa mucho más y no hace falta.
ARCHIVOS_DE_KAGGLE = {
    "ventas": "Video_Games_Sales_as_at_22_Dec_2016.csv",
    "steam": "games.csv",
}
NOMBRE_DEL_REGISTRO_DE_KAGGLE = "versiones_kaggle.json"  # Versión de la última descarga de cada catálogo.
DIAS_SIN_HUELLA = 30   # Si Kaggle no informa la versión, se vuelve a descargar cada 30 días.
NOMBRES_DE_FUENTE = {"ventas": "ventas (Video Game Sales with Ratings)",
                     "steam": "Steam (Steam Games Dataset)"}

# Columnas de las copias reducidas de datos_juegos. Usan los nombres internos del
# programa, así que las dos fuentes quedan con el mismo formato.
COLUMNAS_DE_LA_COPIA = ("identificador", "titulo", "anio", "plataformas", "windows", "mac", "linux",
                        "genero", "etiquetas", "desarrollador", "saga", "positivas", "negativas",
                        "ventas", "usuarios", "nota", "critica", "revision_contenido")
ERRORES_DE_DATOS = (OSError, ValueError, EOFError, HTTPException, csv.Error, zipfile.BadZipFile, zlib.error)
ERRORES_DE_EJECUCION = ERRORES_DE_DATOS + (sqlite3.Error,)
LIMITE_DE_REGISTRO = 32 * 1024 * 1024  # Tamaño máximo, en caracteres, de la ficha JSON de un juego.

# Una configuración evolutiva es una tupla de cuatro genes, en este orden:
#   poblacion: individuos que viven en cada generación.
#   descendientes: hijos nuevos por generación; debe ser menor que la población,
#       para que sobreviva al menos el mejor individuo (elitismo).
#   torneo: individuos que compiten para ser el padre de cada hijo.
#   dirigida: probabilidad de que una mutación sea dirigida. En una lista de juegos
#       elige un juego de mayor afinidad; en una configuración mueve un gen a un
#       valor vecino.
NOMBRES_DE_PARAMETROS = ("poblacion", "descendientes", "torneo", "dirigida")
VALORES_DE_AJUSTE = [       # Valores que puede tomar cada gen, en el mismo orden.
    [12, 18, 24, 30, 36],
    [6, 9, 12, 15, 18, 24],
    [2, 3, 4, 5],
    [0.20, 0.45, 0.70, 0.90],
]
AJUSTE_INICIAL = (30, 18, 3, 0.45)          # Ajuste manual del diseño original.
CONFIGURACION_DEL_META = (12, 6, 2, 0.45)   # Parámetros del propio meta-evolutivo.


# ----------------------------------------------------------------------
# Conocimiento del dominio: géneros, etiquetas y plataformas.
# ----------------------------------------------------------------------

# Traducción de los géneros de los dos catálogos (texto normalizado) a su nombre en español.
NOMBRES_DE_GENERO = {
    "action": "Acción", "adventure": "Aventura", "fighting": "Lucha",
    "misc": "Misceláneo", "platform": "Plataformas", "platformer": "Plataformas",
    "puzzle": "Rompecabezas", "racing": "Carreras", "rpg": "Rol",
    "role playing": "Rol", "shooter": "Disparos", "simulation": "Simulación",
    "sports": "Deportes", "strategy": "Estrategia", "horror": "Terror",
    "casual": "Casual", "indie": "Independiente",
    "massively multiplayer": "Multijugador masivo", "free to play": "Gratuito",
    "early access": "Acceso anticipado", "violent": "Violento", "gore": "Sangriento",
}

# Steam guarda muchos géneros como etiquetas (por ejemplo, Shooter o Horror). Esta tabla
# les asigna el mismo género que usa el catálogo de ventas, para que el cuestionario
# funcione igual en los dos catálogos.
ETIQUETAS_DE_GENERO = {
    "action": ["Acción"], "adventure": ["Aventura"], "rpg": ["Rol"],
    "jrpg": ["Rol"], "action rpg": ["Rol"], "strategy": ["Estrategia"],
    "rts": ["Estrategia"], "turn based strategy": ["Estrategia"],
    "shooter": ["Disparos"], "fps": ["Disparos"], "third person shooter": ["Disparos"],
    "sports": ["Deportes"], "racing": ["Carreras"], "simulation": ["Simulación"],
    "puzzle": ["Rompecabezas"], "platformer": ["Plataformas"],
    "2d platformer": ["Plataformas"], "3d platformer": ["Plataformas"],
    "fighting": ["Lucha"], "beat em up": ["Lucha"],
    "horror": ["Terror"], "survival horror": ["Terror"],
    "psychological horror": ["Terror", "Terror psicológico"],
    "casual": ["Casual"], "indie": ["Independiente"],
}

# Nombres en español de etiquetas frecuentes de Steam. Solo se usan al explicar una recomendación.
NOMBRES_DE_ETIQUETA = {
    "singleplayer": "un jugador", "multiplayer": "multijugador",
    "co op": "cooperativo", "online co op": "cooperativo en línea",
    "local multiplayer": "multijugador local", "open world": "mundo abierto",
    "story rich": "historia profunda", "atmospheric": "atmosférico",
    "great soundtrack": "gran banda sonora", "survival": "supervivencia",
    "sci fi": "ciencia ficción", "fantasy": "fantasía", "difficult": "difícil",
    "exploration": "exploración", "pixel graphics": "gráficos de píxeles",
    "female protagonist": "protagonista femenina", "first person": "primera persona",
    "third person": "tercera persona", "funny": "humor", "mystery": "misterio",
    "zombies": "zombis", "sandbox": "mundo libre", "turn based": "por turnos",
    "survival horror": "terror de supervivencia", "psychological horror": "terror psicológico",
    "dark": "oscuro", "classic": "clásico", "choices matter": "decisiones importantes",
    "multiple endings": "varios finales", "fps": "disparos en primera persona",
}

# Géneros que ofrece el cuestionario, en el orden en que se muestran.
GENEROS_DEL_CUESTIONARIO = (
    "Acción", "Aventura", "Rol", "Estrategia", "Disparos", "Deportes", "Carreras",
    "Simulación", "Rompecabezas", "Plataformas", "Lucha", "Terror",
    "Terror psicológico", "Casual", "Independiente", "Multijugador masivo",
)

# Géneros o etiquetas (normalizados) que excluyen un título: contenido para adultos y
# programas que no son juegos. Así una demostración en clase no muestra esos títulos.
CONTENIDO_EXCLUIDO = frozenset({
    "sexual content", "nudity", "hentai", "nsfw", "software", "utilities",
    "design illustration", "animation modeling", "software training",
    "audio production", "video production", "web publishing", "photo editing",
    "accounting", "game development", "movie", "documentary", "360 video",
})

# Buscamos palabras completas para que, por ejemplo, «Sussex» siga siendo un nombre válido.
INDICIOS_SEXUALES = re.compile(
    r"\b(?:hentai\w*|nsfw|porn\w*|eroge|ecchi|lewd\w*|erotic\w*|erótic\w*|xxx|sex|sexo|sexual(?:ly|es)?|"
    r"nudity|nudes?|naked|desnud[oa]\w*|fetish\w*|bdsm|hardcore pornography|"
    r"adult[\s_-]+(?:only|game|content|visual novel)|adults[\s_-]+only|"
    r"solo para adultos|contenido para adultos|explicit adult|strip[\s_-]+(?:poker|club))\b",
    re.IGNORECASE,
)


def hay_contenido_sexual(*campos):
    # La normalización también reconoce títulos publicados con letras de ancho completo.
    return any(INDICIOS_SEXUALES.search(unicodedata.normalize("NFKC", str(campo)).replace("_", " "))
               for campo in campos if campo)

# Anotaciones del programa original para juegos que el catálogo de ventas clasifica en
# géneros más amplios; por ejemplo, Silent Hill 2 aparece como Acción.
SAGAS_DE_TERROR = (
    "silent hill", "resident evil", "fatal frame", "dead space",
    "clock tower", "alone in the dark", "the evil within",
)
TITULOS_DE_TERROR_PSICOLOGICO = {
    "silent hill", "silent hill 2", "silent hill 3", "silent hill 4 the room",
    "silent hill origins", "silent hill downpour", "silent hill shattered memories",
    "silent hill homecoming", "the evil within", "haunting ground",
}
OTROS_TITULOS_DE_TERROR = {
    "alien isolation", "haunting ground", "siren", "siren blood curse", "forbidden siren 2",
}
EDICIONES_EQUIVALENTES = {
    "resident evil 2 dual shock edition": "resident evil 2",
    "silent hill 2 restless dreams": "silent hill 2",
}

# El estudio tiene poca influencia. La editora no interviene.
PESO_POR_TIPO = {"genero": 1.5, "tema": 0.5, "estudio": 0.10}

# Claves compactas que unen nombres completos y abreviaturas de la misma consola.
ALIAS_DE_PLATAFORMAS = {
    "microsoftwindows": "pc", "windows": "pc", "computadora": "pc",
    "macos": "mac", "osx": "mac", "playstation": "ps", "playstation1": "ps", "ps1": "ps",
    "playstation2": "ps2", "playstation3": "ps3", "playstation4": "ps4",
    "playstation5": "ps5", "playstationvita": "psv", "psvita": "psv",
    "playstationportable": "psp", "xbox360": "x360", "xboxone": "xone", "xboxoriginal": "xb", "xboxconsole": "xb", "xboxseriesx": "xboxseriesxs",
    "xboxseriess": "xboxseriesxs", "xboxseries": "xboxseriesxs", "xsx": "xboxseriesxs",
    "nintendoswitch2": "switch2",
    "nintendowii": "wii", "nintendowiiu": "wiiu", "nintendogamecube": "gc",
    "nintendods": "ds", "nintendo3ds": "3ds", "nintendoswitch": "switch",
    "gamecube": "gc", "nintendo64": "n64", "gameboyadvance": "gba",
    "supernintendo": "snes", "megadrive": "gen", "genesis": "gen", "dreamcast": "dc",
}

# Un nombre de familia permite buscar en varios modelos. Un modelo concreto exige coincidencia exacta.
MODELOS = {"pc": "PC", "mac": "Mac", "ps2": "PS2", "ps3": "PS3", "ps4": "PS4", "ps5": "PS5",
           "xb": "Xbox original", "x360": "Xbox 360", "xone": "Xbox One", "xboxseriesxs": "Xbox Series X/S",
           "switch": "Nintendo Switch", "switch2": "Nintendo Switch 2", "xbox": "Xbox", "nintendo": "Nintendo"}
FAMILIAS = {"xbox": {"xb", "x360", "xone", "xboxseriesxs"},
            "nintendo": {"switch", "switch2", "wii", "wiiu", "ds", "3ds", "gc", "n64", "nes", "snes",
                         "gb", "gbc", "gba"}}
PAGINAS_DE_CONSOLAS = {"PlayStation_2": "PS2", "PlayStation_3": "PS3", "PlayStation_4": "PS4",
                       "PlayStation_5": "PS5", "Xbox_(console)": "Xbox original", "Xbox_360": "Xbox 360",
                       "Xbox_One": "Xbox One", "Xbox_Series_X_and_Series_S": "Xbox Series X/S",
                       "Nintendo_Switch": "Nintendo Switch", "Nintendo_Switch_2": "Nintendo Switch 2"}

# Nombres que pueden tener en cada catálogo las columnas que usa el programa.
COLUMNAS_DEL_CATALOGO = {
    "titulo": ("name", "title", "titulo", "game name", "game"),
    "genero": ("genres", "genre", "generos", "genero"),
    "plataformas": ("platform", "platforms", "plataformas", "plataforma"),
    "anio": ("year of release", "release date", "anio", "year", "fecha de lanzamiento"),
    "etiquetas": ("tags", "steamspy tags", "etiquetas", "categories"),
    "desarrollador": ("developer", "developers", "desarrollador"),
    "identificador": ("appid", "app id", "steam appid", "steam app id"),
    "positivas": ("positive", "positive ratings", "recommendations positive"),
    "negativas": ("negative", "negative ratings", "recommendations negative"),
    "ventas": ("global sales",),
    "usuarios": ("user count",),
    "nota": ("user score",),
    "critica": ("critic score", "metacritic score"),
    "saga": ("saga",),
    "windows": ("windows",),
    "mac": ("mac", "macos"),
    "linux": ("linux",),
    "revision_contenido": ("revision_contenido",),
    "aviso_contenido": ("notes", "mature content description"),
    "clasificacion": ("rating", "esrb rating"),
}


# ----------------------------------------------------------------------
# Utilidades de texto.
# ----------------------------------------------------------------------

# Diccionario que recuerda los textos ya normalizados. Los catálogos repiten muchas
# veces los mismos géneros y etiquetas, así que guardar el resultado ahorra trabajo.
textos_normalizados = {}


def normalizar(texto):
    # Convierte un texto en una clave comparable.

    # Parámetros:
    #     texto (str): cualquier cadena, incluso vacía.

    # Devuelve:
    #     str: el texto en minúsculas, sin acentos ni símbolos y con las
    #     palabras separadas por un solo espacio. Por ejemplo,
    #     "Silent Hill® 2: Restless Dreams" se convierte en
    #     "silent hill 2 restless dreams".
    if texto not in textos_normalizados:
        limpio = texto.replace("®", "").replace("™", "").replace("©", "").lower()
        # NFKD separa cada acento de su letra; después se descartan los acentos sueltos.
        letras = unicodedata.normalize("NFKD", limpio)
        sin_acentos = "".join(c for c in letras if not unicodedata.combining(c))
        # Se conservan las secuencias de letras y dígitos, unidas por un solo espacio.
        textos_normalizados[texto] = " ".join(re.findall(r"[^\W_]+", sin_acentos))
    return textos_normalizados[texto]


def clave_titulo(titulo):
    # Devuelve la clave con la que el catálogo identifica un título.

    # Parámetros:
    #     titulo (str): nombre del juego tal como aparece en un archivo.

    # Devuelve:
    #     str: el título normalizado. Las ediciones documentadas en
    #     EDICIONES_EQUIVALENTES se convierten en la clave del juego base.
    clave = normalizar(titulo)
    return EDICIONES_EQUIVALENTES.get(clave, clave)


def numero(texto):
    # Convierte un texto en un número real no negativo.

    # Parámetros:
    #     texto (str, int o float): valor leído de un archivo.

    # Devuelve:
    #     float o None: el número si es finito y mayor o igual que cero;
    #     None si el texto está vacío, no es numérico (por ejemplo "tbd")
    #     o es negativo.
    valor = None
    try:
        medido = float(texto)
        if math.isfinite(medido) and medido >= 0:
            valor = medido
    except (TypeError, ValueError):
        valor = None
    return valor


def primero_presente(opciones, disponibles):
    # Busca la primera opción que aparece en una colección.

    # Parámetros:
    #     opciones (sequence): opciones en orden de preferencia.
    #     disponibles (colección): valores con los que se comparan.

    # Devuelve:
    #     La primera opción que está en disponibles, o None si ninguna está.
    elegida = None
    for opcion in opciones:
        if elegida is None and opcion in disponibles:
            elegida = opcion
    return elegida


def detectar_separador(encabezado):
    # Elige el separador de un CSV a partir de su primera línea.

    # Parámetros:
    #     encabezado (str): primera línea del archivo.

    # Devuelve:
    #     str: ",", ";" o tabulador; el que divide el encabezado en más columnas.
    mejor = ","
    columnas_del_mejor = 0
    for separador in (",", ";", "\t"):
        columnas = len(list(csv.reader([encabezado], delimiter=separador))[0])
        if columnas > columnas_del_mejor:
            mejor = separador
            columnas_del_mejor = columnas
    return mejor


def nombres_de_campo(texto):
    # Separa los valores de un campo que contiene una lista.

    # Parámetros:
    #     texto (str): lista separada por comas, punto y coma o barras
    #         ("Action, Adventure"), o arreglo JSON ('["Action","RPG"]').

    # Devuelve:
    #     list[str]: los valores sin espacios ni comillas en los extremos,
    #     en su orden original y sin cadenas vacías.
    valores = re.split(r"[;,|]", texto)
    if texto.startswith("[") and texto.endswith("]"):
        try:
            arreglo = json.loads(texto)
        except json.JSONDecodeError:
            # Algunas exportaciones usan comillas simples dentro de la lista.
            arreglo = re.split(r"[;,|]", texto[1:-1])
        if isinstance(arreglo, list):
            valores = [v for v in arreglo if isinstance(v, str)]
    return [v.strip(" '\"") for v in valores if v.strip(" '\"")]


def etiquetas_de_campo(texto):
    # Devuelve hasta ocho etiquetas de un juego.

    # Parámetros:
    #     texto (str): lista de etiquetas, o un objeto JSON que asocia cada
    #         etiqueta con su cantidad de votos ('{"Horror": 120, "Indie": 80}').

    # Devuelve:
    #     list[str]: como máximo ocho etiquetas; si hay votos, las más
    #     votadas van primero.
    if texto.startswith("{") and texto.endswith("}"):
        try:
            recuentos = json.loads(texto)
        except json.JSONDecodeError:
            recuentos = {}
        valores = sorted(recuentos, key=lambda etiqueta: -(numero(recuentos[etiqueta]) or 0))
    else:
        valores = nombres_de_campo(texto)
    return valores[:8]


def clave_de_plataforma(texto):
    # Devuelve una clave común para los nombres de una misma plataforma.

    # Parámetros:
    #     texto (str o None): nombre escrito por la persona o leído de un
    #         catálogo, por ejemplo "PS 4", "PlayStation 4" o "ps4".

    # Devuelve:
    #     str: clave compacta, por ejemplo "ps4"; cadena vacía si el texto
    #     está vacío.
    compacto = normalizar(texto or "").replace(" ", "")
    return ALIAS_DE_PLATAFORMAS.get(compacto, compacto)


# ----------------------------------------------------------------------
# Lectura del archivo JSON de Steam sin cargarlo completo en memoria.
# ----------------------------------------------------------------------

class LectorDeObjetos:
    # Lee el objeto JSON de Steam un juego a la vez.

    # El archivo games.json pesa más de un gigabyte, así que no se puede
    # cargar entero con json.load. Esta clase guarda en memoria solo el
    # bloque de texto que falta por decodificar.

    # Uso:
    #     lector = LectorDeObjetos(archivo)
    #     lector.empezar()
    #     par = lector.siguiente_juego()
    #     while par is not None:
    #         ...                         # par es (AppID, ficha del juego)
    #         par = lector.siguiente_juego()

    # Atributos:
    #     archivo: archivo de texto abierto que contiene el objeto JSON.
    #     pendiente (str): texto leído que aún no se ha decodificado.
    #     indice (int): posición, dentro de pendiente, del siguiente carácter.
    #     decodificador (json.JSONDecoder): decodifica un valor a partir de
    #         una posición del texto.
    #     quedan_juegos (bool): True mientras falten juegos por leer.

    def __init__(self, archivo):
        # Prepara la lectura.

        # Parámetros:
        #     archivo: objeto de archivo de texto abierto para lectura.
        self.archivo = archivo
        self.pendiente = ""
        self.indice = 0
        self.decodificador = json.JSONDecoder()
        self.quedan_juegos = False

    def leer_bloque(self):
        # Descarta el texto ya decodificado y añade el siguiente bloque.

        # Devuelve:
        #     bool: True si se leyó texto nuevo; False si el archivo terminó.
        bloque = self.archivo.read(1024 * 1024)
        self.pendiente = self.pendiente[self.indice:] + bloque
        self.indice = 0
        return len(bloque) > 0

    def saltar_espacios(self):
        # Avanza el índice sobre los espacios del bloque actual.

        # Devuelve:
        #     bool: True si después de los espacios queda un carácter en el
        #     bloque actual.
        while self.indice < len(self.pendiente) and self.pendiente[self.indice] in " \t\r\n":
            self.indice += 1
        return self.indice < len(self.pendiente)

    def mirar(self):
        # Devuelve el siguiente carácter visible sin consumirlo.

        # Devuelve:
        #     str: un carácter, o cadena vacía si el documento terminó.
        quedan_datos = True
        # Mientras el bloque actual solo tenga espacios, se lee el siguiente bloque.
        while not self.saltar_espacios() and quedan_datos:
            quedan_datos = self.leer_bloque()
        siguiente = ""
        if self.indice < len(self.pendiente):
            siguiente = self.pendiente[self.indice]
        return siguiente

    def consumir(self, signo):
        # Consume un delimitador exigido por la estructura JSON.

        # Parámetros:
        #     signo (str): carácter esperado, por ejemplo "{" o ":".

        # Errores:
        #     ValueError: si el siguiente carácter visible es otro.
        aparente = self.mirar()
        if aparente != signo:
            raise ValueError(f"Se esperaba '{signo}' y apareció '{aparente}'.")
        self.indice += 1

    def valor(self, inicio):
        # Decodifica el siguiente valor JSON.

        # Parámetros:
        #     inicio (str): primer carácter que debe tener el valor; '"' para
        #         una cadena o "{" para un objeto.

        # Devuelve:
        #     str o dict: el valor decodificado.

        # Errores:
        #     ValueError: si el valor no empieza con inicio o supera
        #         LIMITE_DE_REGISTRO caracteres; json.JSONDecodeError si el
        #         archivo termina antes de completar el valor.
        if self.mirar() != inicio:
            raise ValueError(f"El registro no comienza con '{inicio}'.")
        resultado = None
        decodificado = False
        # Si la ficha quedó partida entre dos bloques, se añade texto hasta completarla.
        while not decodificado:
            try:
                resultado, fin = self.decodificador.raw_decode(self.pendiente, self.indice)
                self.indice = fin
                decodificado = True
            except json.JSONDecodeError:
                if len(self.pendiente) - self.indice > LIMITE_DE_REGISTRO:
                    raise ValueError("Un registro JSON supera 32 MiB.")
                if not self.leer_bloque():
                    raise
        return resultado

    def empezar(self):
        # Consume la llave que abre el objeto principal de games.json.

        # Errores:
        #     ValueError: si el archivo no empieza con un objeto JSON.
        self.consumir("{")
        self.quedan_juegos = self.mirar() != "}"
        if not self.quedan_juegos:
            self.consumir("}")

    def siguiente_juego(self):
        # Lee el siguiente par del objeto principal.

        # Devuelve:
        #     tuple o None: (identificador de Steam, ficha del juego), o None
        #     cuando ya no quedan juegos.

        # Errores:
        #     ValueError: si el archivo no es un único objeto JSON.
        par = None
        if self.quedan_juegos:
            appid = self.valor('"')
            self.consumir(":")
            ficha = self.valor("{")
            par = (appid, ficha)
            # Después de cada juego viene una coma (otro juego) o la llave de cierre.
            self.quedan_juegos = self.mirar() == ","
            if self.quedan_juegos:
                self.consumir(",")
            else:
                self.consumir("}")
                if self.mirar() != "":
                    raise ValueError("El JSON contiene datos después del objeto de juegos.")
        return par


def arreglo(valores):
    # Serializa como arreglo JSON las cadenas no vacías de un valor.

    # Parámetros:
    #     valores (list, tuple, str u otro): valor de la ficha de Steam.

    # Devuelve:
    #     str: arreglo JSON, por ejemplo '["Action","Indie"]'; cadena vacía
    #     si no hay cadenas útiles.
    elementos = []
    if isinstance(valores, (list, tuple)):
        elementos = [v for v in valores if isinstance(v, str) and v.strip()]
    elif isinstance(valores, str) and valores.strip():
        elementos = [valores.strip()]
    texto = ""
    if elementos:
        texto = json.dumps(elementos, ensure_ascii=False, separators=(",", ":"))
    return texto


def elegir_etiquetas(juego, limite=8):
    # Selecciona las etiquetas más representativas de una ficha de Steam.

    # Parámetros:
    #     juego (dict): ficha de games.json. Su campo tags puede ser un
    #         diccionario etiqueta → votos o una lista.
    #     limite (int): cantidad máxima de etiquetas (entero positivo).

    # Devuelve:
    #     list[str]: las etiquetas, sin pasar del límite indicado; con votos,
    #     las más votadas primero. Si no hay etiquetas, usa las categorías.
    originales = juego.get("tags")
    etiquetas = []
    if isinstance(originales, dict):
        etiquetas = sorted(originales, key=lambda etiqueta: -(numero(originales[etiqueta]) or 0))
    elif isinstance(originales, list):
        etiquetas = originales
    if not etiquetas and isinstance(juego.get("categories"), list):
        etiquetas = juego.get("categories")
    return etiquetas[:limite]


def proyectar_juego(appid, juego):
    # Conserva solo los campos de una ficha de games.json que usa el modelo.

    # Parámetros:
    #     appid (str): identificador de Steam del juego.
    #     juego (dict): ficha completa de games.json.

    # Devuelve:
    #     dict: una fila para la copia reducida, con los nombres de
    #     COLUMNAS_DE_LA_COPIA. Omite imágenes, videos y descripciones; las
    #     columnas que faltan se escriben vacías.
    avisos = juego.get("content_descriptors") or {}
    ids = avisos.get("ids", []) if isinstance(avisos, dict) else []
    restringido = any(str(valor) in ("1", "3", "4") for valor in (ids or [])) or hay_contenido_sexual(
        juego.get("name"), juego.get("genres"), juego.get("tags"), juego.get("categories"), juego.get("notes"), avisos)
    return {
        "revision_contenido": "excluir" if restringido else "",
        "identificador": appid, "titulo": juego.get("name"), "anio": juego.get("release_date"),
        "windows": juego.get("windows"), "mac": juego.get("mac"), "linux": juego.get("linux"),
        "genero": arreglo(juego.get("genres")), "etiquetas": arreglo(elegir_etiquetas(juego)),
        "desarrollador": arreglo(juego.get("developers")),
        "positivas": juego.get("positive"), "negativas": juego.get("negative"),
        "critica": juego.get("metacritic_score"), "nota": juego.get("user_score"),
    }


# ----------------------------------------------------------------------
# Lectura de archivos CSV de cualquiera de los dos catálogos.
# ----------------------------------------------------------------------

def reparar_encabezado(nombres, valores):
    # Corrige un defecto conocido del games.csv de Steam.

    # En algunas versiones del archivo, los encabezados «Discount» y
    # «DLC count» aparecen unidos como «DiscountDLC count», aunque cada fila
    # tiene los dos valores. Sin esta corrección, todas las columnas que
    # siguen quedarían desplazadas un lugar.

    # Parámetros:
    #     nombres (list[str]): encabezados leídos del archivo.
    #     valores (list[str]): primera fila de datos.

    # Devuelve:
    #     list[str]: los encabezados corregidos; una copia sin cambios si el
    #     archivo no tiene el defecto.
    reparados = list(nombres)
    if "DiscountDLC count" in reparados and len(valores) == len(reparados) + 1:
        indice = reparados.index("DiscountDLC count")
        reparados[indice:indice + 1] = ["Discount", "DLC count"]
    return reparados


def recorrer_csv(entrada, nombre, procesar):
    # Lee un catálogo CSV fila por fila sin cargarlo completo en memoria.

    # Cada fila se estandariza: sus columnas se renombran con los nombres
    # internos de COLUMNAS_DEL_CATALOGO, de modo que el resto del programa no
    # depende de cómo se llame cada columna en cada catálogo.

    # Parámetros:
    #     entrada: archivo de texto abierto, colocado al inicio.
    #     nombre (str): nombre del archivo; solo se usa en los mensajes.
    #     procesar (función): recibe cada fila estandarizada (dict) que tiene
    #         título.

    # Devuelve:
    #     tuple: (filas con título, filas omitidas por tener columnas de más).

    # Errores:
    #     ValueError: si el archivo no tiene columna de título.
    con_titulo = 0
    omitidas = 0
    # Algunas celdas de Steam (las descripciones) son muy largas; el límite se amplía
    # solo durante la lectura y después se restablece.
    limite_anterior = csv.field_size_limit(LIMITE_DE_REGISTRO)
    try:
        encabezado = entrada.readline()
        separador = detectar_separador(encabezado)
        nombres = list(csv.reader([encabezado], delimiter=separador))[0]
        campos = None
        for valores in csv.reader(entrada, delimiter=separador):
            # La primera fila con datos permite reparar el encabezado y ubicar las columnas.
            if campos is None and valores:
                nombres = reparar_encabezado(nombres, valores)
                campos = columnas_del_archivo(nombres)
                if campos["titulo"] is None:
                    raise ValueError(f"{nombre} necesita una columna Name, Title o titulo.")
            if len(valores) > len(nombres):
                omitidas += 1
            elif valores:
                cruda = dict(zip(nombres, valores))
                fila = {}
                for destino, campo in campos.items():
                    fila[destino] = cruda.get(campo, "").strip()
                if clave_titulo(fila["titulo"]):
                    procesar(fila)
                    con_titulo += 1
    finally:
        csv.field_size_limit(limite_anterior)
    return con_titulo, omitidas


def clasificar_fila(fila):
    # Leemos todas las etiquetas y las notas antes de reducir la ficha a ocho etiquetas.
    clasificacion = normalizar(fila.get("clasificacion", ""))
    if (clasificacion in ("ao", "adults only") or
            hay_contenido_sexual(fila["titulo"], fila["genero"], fila["etiquetas"], fila.get("aviso_contenido"))):
        return "excluir"
    if fila.get("revision_contenido"):
        return fila["revision_contenido"]
    if not fila["identificador"] and clasificacion in ("ec", "e", "e10", "everyone", "everyone 10"):
        return "revisado"
    return ""


def fila_de_copia(fila):
    # Prepara una fila estandarizada para escribirla en la copia reducida.

    # Parámetros:
    #     fila (dict): fila con las claves de COLUMNAS_DEL_CATALOGO.

    # Devuelve:
    #     dict: la misma fila con las etiquetas reducidas a las ocho más
    #     representativas; así la copia ocupa mucho menos que el original.
    copia = {campo: fila.get(campo, "") for campo in COLUMNAS_DE_LA_COPIA}
    copia["revision_contenido"] = clasificar_fila(fila)
    copia["etiquetas"] = arreglo(etiquetas_de_campo(fila["etiquetas"]))
    return copia


# ----------------------------------------------------------------------
# Localización de los catálogos en la computadora.
# ----------------------------------------------------------------------

class OrigenDeDatos:
    # Archivo original de un catálogo encontrado en la computadora.

    # Atributos:
    #     fuente (str): "ventas" o "steam".
    #     ruta (Path): archivo encontrado (CSV, JSON o ZIP).
    #     miembro (str): nombre del archivo dentro del ZIP; cadena vacía si
    #         ruta no es un ZIP.
    #     formato (str): "csv" o "json".

    def __init__(self, fuente, ruta, miembro, formato):
        # Guarda la ubicación (ver los atributos de la clase).
        self.fuente = fuente
        self.ruta = ruta
        self.miembro = miembro
        self.formato = formato

    def descripcion(self):
        # Devuelve el nombre visible, por ejemplo "archive.zip › games.csv".
        texto = self.ruta.name
        if self.miembro:
            texto += f" › {self.miembro}"
        return texto


def clasificar_contenido(inicio):
    # Reconoce un catálogo por el principio de su contenido.

    # Se usa el contenido y no el nombre porque Kaggle entrega los archivos
    # con nombres variables, por ejemplo archive.zip o archive (1).zip.

    # Parámetros:
    #     inicio (str): primeros caracteres del archivo.

    # Devuelve:
    #     tuple o None: (fuente, formato), por ejemplo ("steam", "csv");
    #     None si el contenido no corresponde a ningún catálogo conocido.
    resultado = None
    if inicio.lstrip().startswith("{"):
        # games.json es un objeto cuyos valores son fichas con nombre y fecha de lanzamiento.
        if '"release_date"' in inicio and '"name"' in inicio:
            resultado = ("steam", "json")
    elif inicio.strip():
        encabezado = inicio.splitlines()[0]
        separador = detectar_separador(encabezado)
        columnas = {normalizar(c) for c in list(csv.reader([encabezado], delimiter=separador))[0]}
        campos = columnas_del_archivo(columnas)
        if campos["titulo"] and "global sales" in columnas:
            resultado = ("ventas", "csv")
        elif campos["titulo"] and campos["identificador"] and campos["genero"] and campos["anio"]:
            resultado = ("steam", "csv")
    return resultado


def leer_inicio(binario):
    # Lee los primeros 64 KiB de un archivo binario abierto y los decodifica.

    # Parámetros:
    #     binario: archivo abierto en modo binario.

    # Devuelve:
    #     str: el texto inicial; los bytes inválidos se ignoran.
    return binario.read(65536).decode("utf-8-sig", errors="ignore")


def examinar_archivo(ruta):
    # Busca catálogos dentro de un archivo.

    # Parámetros:
    #     ruta (Path): archivo .csv, .json o .zip.

    # Devuelve:
    #     list[OrigenDeDatos]: los catálogos reconocidos; lista vacía si el
    #     archivo no contiene ninguno o no se puede leer.
    hallados = []
    sufijo = ruta.suffix.lower()
    try:
        if sufijo in (".csv", ".json"):
            with ruta.open("rb") as binario:
                tipo = clasificar_contenido(leer_inicio(binario))
            if tipo is not None:
                hallados.append(OrigenDeDatos(tipo[0], ruta, "", tipo[1]))
        elif sufijo == ".zip" and zipfile.is_zipfile(ruta):
            with zipfile.ZipFile(ruta) as paquete:
                for miembro in paquete.namelist():
                    util = miembro.lower().endswith((".csv", ".json")) and not miembro.startswith("__MACOSX/")
                    if util:
                        # Solo se descomprime el principio de cada archivo interno.
                        with paquete.open(miembro) as binario:
                            tipo = clasificar_contenido(leer_inicio(binario))
                        if tipo is not None:
                            hallados.append(OrigenDeDatos(tipo[0], ruta, miembro, tipo[1]))
    except ERRORES_DE_DATOS:
        # Un archivo dañado o en uso no impide buscar en los demás.
        hallados = []
    return hallados


# ----------------------------------------------------------------------
# Copias reducidas de los catálogos.
# ----------------------------------------------------------------------

def unico_archivo_del_zip(paquete, ruta, terminacion):
    # Busca dentro de un ZIP el único archivo con cierta terminación.

    # Parámetros:
    #     paquete (zipfile.ZipFile): ZIP abierto.
    #     ruta (Path): ruta del ZIP; solo se usa en el mensaje de error.
    #     terminacion (str): por ejemplo ".csv".

    # Devuelve:
    #     str: nombre interno del archivo.

    # Errores:
    #     ValueError: si no hay exactamente un archivo con esa terminación.
    nombres = [n for n in paquete.namelist()
               if n.lower().endswith(terminacion) and not n.startswith("__MACOSX/")]
    if len(nombres) != 1:
        raise ValueError(f"{ruta.name} debe contener un único archivo {terminacion}.")
    return nombres[0]


def abrir_csv(ruta):
    # Abre un CSV suelto o el único CSV de una copia reducida (ZIP).

    # Se usa con with, igual que open: «with abrir_csv(ruta) as datos:».
    # Del ZIP se lee el CSV completo a memoria, porque las copias reducidas
    # son pequeñas.

    # Parámetros:
    #     ruta (Path): archivo .csv, o archivo .zip con exactamente un CSV.

    # Devuelve:
    #     Archivo de texto UTF-8 listo para leer.

    # Errores:
    #     ValueError: si el ZIP no contiene exactamente un CSV.
    if ruta.suffix.lower() == ".csv":
        archivo = ruta.open(encoding="utf-8-sig", newline="")
    else:
        with zipfile.ZipFile(ruta) as paquete:
            nombre = unico_archivo_del_zip(paquete, ruta, ".csv")
            texto = paquete.read(nombre).decode("utf-8-sig")
        archivo = io.StringIO(texto, newline="")
    return archivo


def escribir_copia(entrada, formato, destino, nombre):
    # Escribe la copia reducida de un catálogo a partir de su original.

    # Parámetros:
    #     entrada: archivo de texto abierto con el catálogo original.
    #     formato (str): "csv" o "json".
    #     destino (Path): archivo ZIP que se crea con un único catalogo.csv.
    #     nombre (str): nombre del original; solo se usa en los mensajes.

    # Devuelve:
    #     int: cantidad de juegos copiados.

    # Errores:
    #     ValueError: si el original no contiene juegos.
    registros = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zip_salida:
        with zip_salida.open("catalogo.csv", "w") as binario:
            # TextIOWrapper convierte el texto del CSV en bytes para el ZIP.
            with io.TextIOWrapper(binario, encoding="utf-8", newline="") as salida:
                escritor = csv.DictWriter(salida, fieldnames=COLUMNAS_DE_LA_COPIA)
                escritor.writeheader()
                if formato == "json":
                    lector = LectorDeObjetos(entrada)
                    lector.empezar()
                    par = lector.siguiente_juego()
                    while par is not None:
                        escritor.writerow(proyectar_juego(par[0], par[1]))
                        registros += 1
                        par = lector.siguiente_juego()
                else:
                    registros = recorrer_csv(entrada, nombre, lambda fila: escritor.writerow(fila_de_copia(fila)))[0]
    if registros == 0:
        raise ValueError(f"{nombre} no contiene juegos.")
    return registros


def preparar_copia(origen, destino):
    # Crea la copia reducida de un catálogo original.

    # El original se lee por bloques, aunque esté dentro de un ZIP, sin
    # descomprimirlo en el disco. La copia se escribe con un nombre temporal
    # y solo al terminar recibe su nombre definitivo, para que una ejecución
    # interrumpida no deje una copia incompleta.

    # Parámetros:
    #     origen (OrigenDeDatos): archivo original.
    #     destino (Path): copia que se crea en datos_juegos.
    print(f"Preparando la copia local del catálogo de {NOMBRES_DE_FUENTE[origen.fuente]} "
          f"a partir de {origen.descripcion()}…", flush=True)
    with tempfile.TemporaryDirectory(dir=destino.parent) as carpeta_temporal:
        temporal = Path(carpeta_temporal) / "catalogo.zip"
        if origen.miembro:
            with zipfile.ZipFile(origen.ruta) as paquete:
                with paquete.open(origen.miembro) as binario:
                    with io.TextIOWrapper(binario, encoding="utf-8-sig", errors="replace", newline="") as entrada:
                        escribir_copia(entrada, origen.formato, temporal, origen.descripcion())
        else:
            with origen.ruta.open(encoding="utf-8-sig", errors="replace", newline="") as entrada:
                escribir_copia(entrada, origen.formato, temporal, origen.descripcion())
        temporal.replace(destino)


def copia_legible(ruta, fuente):
    # Verifica la integridad y el contenido. Las dos copias usan el mismo encabezado,
    # pero Steam tiene AppID por juego y ventas tiene cifras de ventas por plataforma.
    valida = False
    if ruta.is_file():
        try:
            with zipfile.ZipFile(ruta) as paquete:
                nombre = unico_archivo_del_zip(paquete, ruta, ".csv")
                with paquete.open(nombre) as binario, io.TextIOWrapper(binario, encoding="utf-8-sig", newline="") as texto:
                    lector = csv.DictReader(texto)
                    campos = columnas_del_archivo(lector.fieldnames or [])
                    clave = campos["identificador"] if fuente == "steam" else campos["ventas"]
                    if campos["titulo"] and clave:
                        for fila in islice(lector, 64):
                            valor = (fila.get(clave) or "").strip()
                            coincide = valor.isascii() and valor.isdigit() if fuente == "steam" else numero(valor) is not None
                            valida = valida or bool(fila.get(campos["titulo"]) and coincide)
                valida = valida and paquete.testzip() is None
        except ERRORES_DE_DATOS:
            valida = False
    return valida


def nombre_de_copia(origen):
    # Devuelve el nombre de la copia reducida de un original.

    # El nombre incluye una suma de comprobación de la ruta, el tamaño y la
    # fecha del original: si el archivo cambia, se prepara una copia nueva.

    # Parámetros:
    #     origen (OrigenDeDatos): archivo original.

    # Devuelve:
    #     str: por ejemplo "steam_local_1a2b3c4d.csv.zip".
    datos = origen.ruta.stat()
    marca = f"contenido1|{origen.ruta.resolve()}|{origen.miembro}|{datos.st_size}|{datos.st_mtime_ns}"
    return f"{origen.fuente}_local_{zlib.crc32(marca.encode('utf-8')):08x}.csv.zip"


def copia_anterior(copias, fuente):
    # Busca la copia reducida más reciente que ya exista de una fuente.

    # Sirve, por ejemplo, cuando la carpeta datos_juegos se copió a otra
    # computadora sin los archivos originales.

    # Parámetros:
    #     copias (Path): carpeta datos_juegos.
    #     fuente (str): "ventas" o "steam".

    # Devuelve:
    #     Path o None: la copia legible más reciente.
    anteriores = sorted(copias.glob(f"{fuente}_*.csv.zip"), key=lambda r: r.stat().st_mtime, reverse=True)
    elegida = None
    for ruta in anteriores:
        if elegida is None and copia_legible(ruta, fuente):
            elegida = ruta
    return elegida


def descargar_respuesta(respuesta, destino, fuente):
    # Guarda en un archivo el contenido de una descarga ya abierta.

    # Se copia en bloques de 1 MiB para no cargar el catálogo completo en memoria.

    # Parámetros:
    #     respuesta: conexión abierta con urlopen.
    #     destino (Path): archivo donde se escribe el contenido (CSV o ZIP).
    #     fuente (str): "ventas" o "steam"; solo se usa en los mensajes.

    # Errores:
    #     ValueError: si la descarga se interrumpe antes de terminar.
    print(f"Descargando el catálogo de {NOMBRES_DE_FUENTE[fuente]} desde Kaggle…", flush=True)
    total = int(respuesta.headers.get("Content-Length") or 0)
    recibidos = 0
    siguiente_aviso = 10
    with destino.open("wb") as archivo:
        bloque = respuesta.read(1024 * 1024)
        while bloque:
            archivo.write(bloque)
            recibidos += len(bloque)
            # El avance se muestra cada 10 % solo en archivos grandes, como el de Steam.
            if total > 10_000_000 and recibidos * 100 >= total * siguiente_aviso:
                print(f"  {siguiente_aviso} % ({recibidos // 1_000_000:,} de {total // 1_000_000:,} MB)",
                      flush=True)
                siguiente_aviso += 10
            bloque = respuesta.read(1024 * 1024)
    if total and recibidos != total:
        raise ValueError(f"La descarga se interrumpió al recibir {recibidos} de {total} bytes.")


def credenciales_de_kaggle():
    # Busca credenciales de Kaggle por si la descarga anónima es rechazada.

    # Kaggle permite descargar sin cuenta los conjuntos públicos, así que
    # normalmente no se usan. Si se usan, se leen de las variables de entorno
    # KAGGLE_USERNAME y KAGGLE_KEY o del archivo ~/.kaggle/kaggle.json. La
    # clave nunca se escribe en este programa.

    # Devuelve:
    #     str: encabezado de autorización ("Basic …"); cadena vacía si no hay
    #     credenciales.
    usuario = os.environ.get("KAGGLE_USERNAME", "")
    clave = os.environ.get("KAGGLE_KEY", "")
    if not (usuario and clave):
        try:
            datos = json.loads((Path.home() / ".kaggle" / "kaggle.json").read_text(encoding="utf-8"))
            usuario = str(datos.get("username", ""))
            clave = str(datos.get("key", ""))
        except (OSError, ValueError, AttributeError):
            usuario, clave = "", ""
    autorizacion = ""
    if usuario and clave:
        autorizacion = "Basic " + base64.b64encode(f"{usuario}:{clave}".encode("utf-8")).decode("ascii")
    return autorizacion


def abrir_descarga(url):
    # Abre la conexión con Kaggle sin leer todavía el contenido.

    # Parámetros:
    #     url (str): dirección de un archivo del conjunto de datos.

    # Devuelve:
    #     Conexión abierta; se usa con with.

    # Errores:
    #     OSError (incluye HTTPError): si no hay conexión o Kaggle rechaza la
    #     petición incluso con credenciales.
    peticion = Request(url, headers={"User-Agent": "RecomendadorVideojuegos/4.0"})
    try:
        respuesta = urlopen(peticion, timeout=60)
    except HTTPError as error:
        autorizacion = credenciales_de_kaggle()
        if error.code not in (401, 403) or not autorizacion:
            raise
        # Kaggle redirige la descarga a otro servidor. add_unredirected_header evita
        # que la clave viaje también a ese servidor.
        peticion = Request(url, headers={"User-Agent": "RecomendadorVideojuegos/4.0"})
        peticion.add_unredirected_header("Authorization", autorizacion)
        respuesta = urlopen(peticion, timeout=60)
    return respuesta


def huella_de_respuesta(respuesta):
    # Identifica la versión del archivo que Kaggle está ofreciendo.

    # Los encabezados de la respuesta llegan antes que el contenido. ETag y
    # Last-Modified cambian cuando el autor publica una versión nueva, así que
    # comparar esta huella con la guardada permite saber si hay datos nuevos
    # sin descargar el archivo.

    # Parámetros:
    #     respuesta: conexión abierta con abrir_descarga.

    # Devuelve:
    #     str: la huella; cadena vacía si Kaggle no envió esos encabezados.
    etiqueta = respuesta.headers.get("ETag", "")
    modificado = respuesta.headers.get("Last-Modified", "")
    tamano = respuesta.headers.get("Content-Length", "")
    huella = ""
    if etiqueta or modificado:
        huella = f"{etiqueta}|{modificado}|{tamano}"
    return huella


def leer_registro(copias):
    # Lee qué versión de cada catálogo se descargó por última vez.

    # Parámetros:
    #     copias (Path): carpeta datos_juegos.

    # Devuelve:
    #     dict: fuente → {"huella": str, "copia": nombre del archivo, "fecha": segundos}.
    #     Diccionario vacío si todavía no se ha descargado nada.
    registro = {}
    try:
        leido = json.loads((copias / NOMBRE_DEL_REGISTRO_DE_KAGGLE).read_text(encoding="utf-8"))
        if isinstance(leido, dict):
            registro = {f: d for f, d in leido.items() if f in FUENTES_DE_KAGGLE and isinstance(d, dict)}
    except (OSError, ValueError):
        registro = {}
    return registro


def guardar_registro(copias, registro):
    # Guarda el registro de descargas; se escribe con un nombre temporal y después
    # se renombra, para que un corte de luz no deje un archivo a medias.
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=copias, delete=False) as temporal:
            json.dump(registro, temporal, ensure_ascii=False, indent=2)
        Path(temporal.name).replace(copias / NOMBRE_DEL_REGISTRO_DE_KAGGLE)
    except OSError as error:
        print(f"No se pudo guardar el registro de descargas. {error}")


def actualizar_desde_kaggle(copias, fuente, registro):
    # Consulta Kaggle y descarga el catálogo solo si hay una versión nueva.

    # Cada ejecución abre la descarga y lee primero sus encabezados (la
    # huella). Si coincide con la de la última descarga, cierra la conexión
    # sin bajar el archivo y usa la copia guardada. Si Kaggle no envía huella,
    # se vuelve a descargar cuando la copia tiene más de DIAS_SIN_HUELLA días.

    # Parámetros:
    #     copias (Path): carpeta datos_juegos.
    #     fuente (str): "ventas" o "steam".
    #     registro (dict): registro de descargas; se actualiza si se descarga.

    # Devuelve:
    #     Path: copia reducida lista para leer.

    # Errores:
    #     OSError o ValueError: si no hay conexión o la descarga no sirve.
    url = f"{API_DE_KAGGLE}{FUENTES_DE_KAGGLE[fuente]}/{ARCHIVOS_DE_KAGGLE[fuente]}"
    anterior = registro.get(fuente, {})
    copia = copias / str(anterior.get("copia", "") or f"{fuente}_kaggle.csv.zip")
    copia_valida = bool(anterior) and copia_legible(copia, fuente)
    print(f"Consultando en Kaggle el catálogo de {NOMBRES_DE_FUENTE[fuente]}…", flush=True)
    with abrir_descarga(url) as respuesta:
        huella = huella_de_respuesta(respuesta)
        if huella:
            sin_cambios = copia_valida and huella == anterior.get("huella")
        else:
            antiguedad = time.time() - (numero(anterior.get("fecha")) or 0)
            sin_cambios = copia_valida and antiguedad < DIAS_SIN_HUELLA * 86400
        if sin_cambios:
            # Al salir del with se cierra la conexión sin descargar el contenido.
            print("  Kaggle no tiene una versión nueva; se usa la descarga guardada.", flush=True)
            destino = copia
        else:
            destino = copias / f"{fuente}_kaggle.csv.zip"
            # La descarga se guarda en una carpeta temporal que se borra al terminar.
            with tempfile.TemporaryDirectory(dir=copias) as temporal:
                descarga = Path(temporal) / ARCHIVOS_DE_KAGGLE[fuente]
                descargar_respuesta(respuesta, descarga, fuente)
                # Kaggle puede entregar el CSV suelto o comprimido en un ZIP.
                if zipfile.is_zipfile(descarga):
                    comprimido = descarga.with_suffix(".zip")
                    descarga.rename(comprimido)
                    descarga = comprimido
                hallados = [o for o in examinar_archivo(descarga) if o.fuente == fuente]
                if not hallados:
                    raise ValueError("La descarga no contiene el catálogo esperado.")
                # Si el ZIP trae CSV y JSON, se usa el CSV, que se lee más rápido.
                hallados.sort(key=lambda origen: origen.formato == "json")
                preparar_copia(hallados[0], destino)
            if not copia_legible(destino, fuente):
                raise ValueError("La descarga no produjo una copia utilizable.")
            registro[fuente] = {"huella": huella, "copia": destino.name, "fecha": int(time.time())}
    return destino


def originales_junto_al_programa(carpeta):
    # Busca catálogos descargados a mano en la carpeta del programa.

    # Es el último respaldo, por si no hay internet ni copias guardadas. Solo
    # se revisa la carpeta del programa (no sus subcarpetas ni Descargas), para
    # que un archivo viejo en otra carpeta nunca se use sin que lo sepamos.

    # Parámetros:
    #     carpeta (Path): carpeta del programa.

    # Devuelve:
    #     dict[str, list[OrigenDeDatos]]: fuente → originales; primero los CSV.
    encontrados = {}
    for ruta in sorted(carpeta.iterdir()):
        if ruta.is_file() and ruta.suffix.lower() in (".csv", ".json", ".zip"):
            for origen in examinar_archivo(ruta):
                encontrados.setdefault(origen.fuente, []).append(origen)
    for lista in encontrados.values():
        lista.sort(key=lambda origen: origen.formato == "json")
    return encontrados


def obtener_fuente(carpeta, fuente, registro):
    # Devuelve la copia reducida de un catálogo, lista para leer.

    # Orden de prioridad:
    #   1. Kaggle: se consulta en cada ejecución y se descarga si hay versión nueva.
    #   2. Si Kaggle no responde: la última copia guardada en datos_juegos.
    #   3. Si nunca se ha descargado: un archivo de Kaggle junto al programa.

    # Parámetros:
    #     carpeta (Path): carpeta del programa.
    #     fuente (str): "ventas" o "steam".
    #     registro (dict): registro de descargas.

    # Devuelve:
    #     Path: copia reducida (ZIP con un CSV).

    # Errores:
    #     ValueError: si ninguna de las tres opciones funcionó.
    copias = carpeta / NOMBRE_DE_LAS_COPIAS
    ruta = None
    try:
        ruta = actualizar_desde_kaggle(copias, fuente, registro)
    except ERRORES_DE_DATOS as error:
        print(f"  No se pudo consultar Kaggle. {error}")
    if ruta is None:
        ruta = copia_anterior(copias, fuente)
        if ruta is not None:
            fecha = time.strftime("%d/%m/%Y", time.localtime(ruta.stat().st_mtime))
            print(f"  Se usará la copia guardada el {fecha}.")
    if ruta is None:
        for original in originales_junto_al_programa(carpeta).get(fuente, []):
            if ruta is None:
                destino = copias / nombre_de_copia(original)
                try:
                    if not copia_legible(destino, fuente):
                        preparar_copia(original, destino)
                    if copia_legible(destino, fuente):
                        ruta = destino
                except ERRORES_DE_DATOS as error:
                    print(f"  No se pudo leer {original.descripcion()}. {error}")
    if ruta is None:
        raise ValueError("No hay conexión con Kaggle ni una copia guardada.")
    return ruta


def localizar_catalogos(carpeta):
    # Prepara las dos fuentes de datos y devuelve las que estén disponibles.

    # Parámetros:
    #     carpeta (Path): carpeta del programa.

    # Devuelve:
    #     dict[str, Path]: fuente → copia reducida, con una o dos fuentes.

    # Errores:
    #     ValueError: si no se pudo preparar el catálogo de Steam.
    copias = carpeta / NOMBRE_DE_LAS_COPIAS
    copias.mkdir(exist_ok=True)
    registro = leer_registro(copias)
    disponibles = {}
    for fuente in FUENTES_DE_KAGGLE:
        try:
            disponibles[fuente] = obtener_fuente(carpeta, fuente, registro)
        except ERRORES_DE_DATOS as error:
            print(f"No se pudo preparar el catálogo de {NOMBRES_DE_FUENTE[fuente]}. {error}")
            print("  Revisa tu conexión a internet y vuelve a ejecutar. Sin internet, también puedes "
                  f"descargarlo de https://www.kaggle.com/datasets/{FUENTES_DE_KAGGLE[fuente]} "
                  f"y dejar el archivo en {carpeta}.")
    guardar_registro(copias, registro)
    if "steam" not in disponibles:
        raise ValueError("Falta el catálogo de Steam, que es el que se usa para armar las listas.")
    return disponibles


# ----------------------------------------------------------------------
# Catálogo unificado de videojuegos.
# ----------------------------------------------------------------------

def fecha_del_catalogo(texto):
    # Steam escribe las fechas en inglés aunque Spyder esté en español.
    coincidencia = re.search(r"\b(?:19[5-9]\d|20\d{2})\b", texto)
    if not coincidencia:
        return None, None
    anio = int(coincidencia.group())
    meses = "jan feb mar apr may jun jul aug sep oct nov dec".split()
    partes = re.findall(r"[a-z]+|\d+", texto.lower())
    # Un año o un trimestre anunciado no nos dice el día del estreno.
    resultado = (anio, None)
    try:
        if len(partes) == 3:
            if partes[0] == str(anio):
                resultado = (anio, date.fromisoformat(texto.strip()))
            elif partes[-1] == str(anio):
                mes, dia = partes[:2]
                if mes.isdigit():
                    dia, mes = mes, dia
                resultado = (anio, date(anio, meses.index(mes[:3]) + 1, int(dia)))
    except ValueError:
        # Una fecha imposible (por ejemplo, 31 de febrero) se trata como día desconocido.
        resultado = (anio, None)
    return resultado


def consultar_tienda(url):
    solicitud = Request(url, headers={"User-Agent": "RecomendadorDeJuegos/1.0"})
    with urlopen(solicitud, timeout=7) as respuesta:
        return json.load(respuesta)


def consolas_de_wikidata(carpeta):
    # La misma ficha de Wikidata debe contener el AppID de Steam y la consola.
    archivo = carpeta / NOMBRE_DE_LAS_COPIAS / "consolas_wikidata.json"
    anteriores = {}
    try:
        guardados = json.loads(archivo.read_text(encoding="utf-8"))
        if isinstance(guardados, dict):
            anteriores = {a: ps for a, ps in guardados.items() if a.isdigit() and isinstance(ps, list)
                          and all(p in PAGINAS_DE_CONSOLAS.values() for p in ps)}
        if anteriores and time.time() - archivo.stat().st_mtime < 7 * 86400:
            return anteriores
    except (OSError, ValueError):
        # Sin una copia legible, las consolas se consultan de nuevo en Wikidata.
        anteriores = {}
    paginas = " ".join(f"<https://en.wikipedia.org/wiki/{p}>" for p in PAGINAS_DE_CONSOLAS)
    consulta = (f"SELECT DISTINCT ?app ?pagina WHERE {{ VALUES ?pagina {{ {paginas} }} "
                "?pagina schema:about ?plataforma . ?juego wdt:P400 ?plataforma; wdt:P1733 ?app; wdt:P577 ?fecha . "
                f'FILTER(?fecha >= "{ANIO_DESDE}-01-01T00:00:00Z"^^xsd:dateTime) }}')
    url = "https://query.wikidata.org/sparql?" + urlencode({"query": consulta, "format": "json"})
    try:
        peticion = Request(url, headers={"User-Agent": "RecomendadorDeJuegos/1.0"})
        with urlopen(peticion, timeout=20) as respuesta:
            filas = json.load(respuesta)["results"]["bindings"]
        consolas = {}
        for fila in filas:
            appid = fila["app"]["value"]
            modelo = PAGINAS_DE_CONSOLAS.get(fila["pagina"]["value"].rsplit("/", 1)[-1])
            if appid.isdigit() and modelo:
                consolas.setdefault(appid, []).append(modelo)
        if not consolas:
            raise ValueError("consulta vacía")
    except (OSError, ValueError, KeyError, TypeError, HTTPException) as error:
        print(f"No se pudo actualizar Wikidata. Se usarán las plataformas documentadas disponibles. {error}")
        return anteriores
    try:
        with tempfile.TemporaryDirectory(dir=archivo.parent) as carpeta_temporal:
            temporal = Path(carpeta_temporal) / archivo.name
            temporal.write_text(json.dumps(consolas), encoding="utf-8")
            temporal.replace(archivo)
    except OSError as error:
        print(f"No se pudo guardar la copia de plataformas. {error}")
    return consolas


# Identificadores públicos de las etiquetas de género y de contenido de Steam.
GENEROS_POR_TAG = {9: "Estrategia", 19: "Acción", 21: "Aventura", 122: "Rol", 492: "Independiente",
                   597: "Casual", 599: "Simulación", 699: "Carreras", 701: "Deportes", 1625: "Plataformas",
                   1664: "Rompecabezas", 1667: "Terror", 1721: "Terror psicológico", 1743: "Lucha",
                   1774: "Disparos", 3978: "Terror"}


def completar_generos(juegos, carpeta):
    # Kaggle puede traer géneros amplios y ninguna etiqueta. Steam devuelve las etiquetas por AppID.
    actuales = {j.appid: j for j in juegos.values() if j.appid and j.es_recomendable()}
    ahora = int(time.time())
    conexion = sqlite3.connect(carpeta / "etiquetas_steam.sqlite3", timeout=10)
    try:
        conexion.execute("CREATE TABLE IF NOT EXISTS etiquetas (appid TEXT PRIMARY KEY, tags TEXT, fecha INTEGER)")
        guardadas = {appid: (json.loads(tags), fecha) for appid, tags, fecha in
                     conexion.execute("SELECT appid, tags, fecha FROM etiquetas")}
        pendientes = [a for a in actuales if a not in guardadas or ahora - guardadas[a][1] > 30 * 86400]
        if pendientes:
            print("Actualizando las etiquetas de género de Steam…", flush=True)
        # Se consulta en lotes de 50 juegos; si Steam deja de responder, se detienen las consultas.
        steam_responde = True
        inicio = 0
        while inicio < len(pendientes) and steam_responde:
            lote = pendientes[inicio:inicio + 50]
            inicio += 50
            peticion = {"ids": [{"appid": int(a)} for a in lote],
                        "context": {"language": "english", "country_code": "US"},
                        "data_request": {"include_tag_count": 20}}
            url = "https://api.steampowered.com/IStoreBrowseService/GetItems/v1/?" + urlencode(
                {"input_json": json.dumps(peticion, separators=(",", ":"))})
            try:
                productos = consultar_tienda(url)["response"]["store_items"]
            except (OSError, HTTPException, ValueError, TypeError, KeyError):
                print("Steam no respondió. Se usarán los géneros del catálogo y las etiquetas guardadas.")
                productos = []
                steam_responde = False
            for producto in productos:
                appid = str(producto.get("id"))
                if appid in lote and producto.get("success") == 1:
                    tags = producto.get("tagids", [])
                    guardadas[appid] = tags, ahora
                    conexion.execute("INSERT OR REPLACE INTO etiquetas VALUES (?, ?, ?)",
                                     (appid, json.dumps(tags), ahora))
            conexion.commit()
        for appid, juego in actuales.items():
            tags = set(guardadas.get(appid, ([], 0))[0])
            if tags & {6650, 9130, 12095}:
                juego.apto = False
            nuevos = {GENEROS_POR_TAG[t] for t in tags if t in GENEROS_POR_TAG}
            if "Terror psicológico" in nuevos:
                nuevos.add("Terror")
            juego.generos.update(nuevos)
            juego.atributos.update(("genero", normalizar(g)) for g in nuevos)
    finally:
        conexion.close()


def producto_de_steam(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=english"
    respuesta = consultar_tienda(url)
    return respuesta.get(appid, {}).get("data", {})


def revisar_producto(producto):
    # Steam distingue desnudez/sexo (1, 3 y 4) de violencia (2) y madurez general (5).
    if not producto or not producto.get("name"):
        return ""
    avisos = producto.get("content_descriptors") or {}
    esrb = (producto.get("ratings") or {}).get("esrb") or {}
    if (producto.get("type") != "game" or normalizar(str(esrb.get("rating", ""))) in ("ao", "adults only")
            or hay_contenido_sexual(producto["name"], avisos.get("notes"), esrb.get("descriptors"),
                                    producto.get("genres"), producto.get("short_description"))):
        return "excluir"
    ids = avisos.get("ids")
    if not isinstance(ids, list):
        return ""
    indicadores = {str(valor) for valor in ids}
    if indicadores & {"1", "3", "4"}:
        return "excluir"
    # Una lista vacía también es una respuesta de Steam. Un código desconocido queda pendiente.
    return "revisado" if indicadores <= {"2", "5"} else ""


def ficha_de_la_tienda(appid):
    # Usamos la ficha pública para distinguir juegos, DLC y anuncios sin fecha.
    producto = producto_de_steam(appid)
    if producto.get("type") != "game" or not producto.get("name"):
        return None
    lanzamiento = producto.get("release_date", {})
    if not isinstance(lanzamiento.get("coming_soon"), bool):
        return None
    fila = dict.fromkeys(COLUMNAS_DE_LA_COPIA, "")
    fila.update(identificador=appid, titulo=producto["name"], anio=lanzamiento.get("date") or "",
                anunciado=lanzamiento["coming_soon"], revision_contenido=revisar_producto(producto),
                genero=json.dumps([g["description"] for g in producto.get("genres", [])]),
                desarrollador=json.dumps(producto.get("developers", [])))
    for plataforma in ("windows", "mac", "linux"):
        fila[plataforma] = str(producto.get("platforms", {}).get(plataforma, False))
    return fila


def anuncios_de_steam(carpeta):
    # La lista de deseos pública incluye juegos anunciados después de la exportación de Kaggle.
    archivo = carpeta / NOMBRE_DE_LAS_COPIAS / "lanzamientos_steam.json"
    anteriores = {}
    try:
        registros = json.loads(archivo.read_text(encoding="utf-8"))
        vigente = time.time() - archivo.stat().st_mtime < 7 * 86400
        if isinstance(registros, list):
            for fila in registros:
                if isinstance(fila, dict):
                    # Las versiones anteriores guardaban el anuncio sin sus avisos.
                    fila.setdefault("revision_contenido", "")
                    if not vigente and fila["revision_contenido"] == "revisado":
                        fila["revision_contenido"] = ""
                if (isinstance(fila, dict) and isinstance(fila.get("anunciado"), bool)
                        and all(isinstance(fila.get(campo), str) for campo in COLUMNAS_DE_LA_COPIA)):
                    anteriores[fila["identificador"]] = fila
        if vigente and anteriores and all(f["revision_contenido"] for f in anteriores.values()):
            return list(anteriores.values())
    except ERRORES_DE_DATOS:
        # Sin una copia legible, los anuncios se consultan de nuevo en la tienda.
        anteriores = {}
    print("Consultando los próximos lanzamientos en la tienda de Steam…", flush=True)
    url = ("https://store.steampowered.com/search/results/?filter=popularwishlist"
           "&category1=998&infinite=1&count=16&cc=us&l=english")
    try:
        pagina = consultar_tienda(url)
        ids = re.findall(r'data-ds-appid="(\d+)"', pagina["results_html"])
        if not ids:
            raise ValueError("La tienda no devolvió su lista de próximos lanzamientos.")
        fichas = []
        consultas_exitosas = 0
        with ThreadPoolExecutor(max_workers=4) as consultas:
            pendientes = {k: consultas.submit(ficha_de_la_tienda, k) for k in dict.fromkeys(ids[:16])}
            for appid, consulta in pendientes.items():
                try:
                    fila = consulta.result()
                    consultas_exitosas += 1
                except (OSError, ValueError, HTTPException, KeyError, TypeError, AttributeError):
                    fila = anteriores.get(appid)
                if fila:
                    fichas.append(fila)
        if not fichas or not consultas_exitosas:
            raise ValueError("Ninguna ficha de la tienda estuvo disponible.")
    except (OSError, ValueError, HTTPException, KeyError, TypeError, AttributeError) as error:
        print(f"No se pudieron actualizar los anuncios de Steam. Se usarán los datos guardados. {error}")
        return list(anteriores.values())
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=archivo.parent, delete=False) as temporal:
            json.dump(fichas, temporal, ensure_ascii=False)
        Path(temporal.name).replace(archivo)
    except OSError as error:
        print(f"No se pudo guardar la copia de los anuncios para otra sesión. {error}")
    return fichas


class FichaDeJuego:
    # Ficha de un título que reúne los datos de todas sus ediciones.

    # Atributos:
    #     titulo (str): nombre visible, tal como aparece en el primer catálogo
    #         que lo menciona.
    #     anio (int o None): año del primer lanzamiento conocido.
    #     saga (str): nombre normalizado de la saga, o cadena vacía.
    #     generos (set[str]): géneros visibles, en español cuando hay traducción.
    #     plataformas (set[str]): plataformas visibles, por ejemplo {"PS2", "PC"}.
    #     atributos (set[tuple]): pares (tipo, valor) que usa el modelo; tipo es
    #         "genero", "tema" o "estudio" y valor está normalizado.
    #     calidad_publica (float): nota pública suavizada en [0, 1]; vale 0.65
    #         mientras no haya opiniones.
    #     evidencia_publica (float): cantidad de opiniones que respaldan la nota.
    #     popularidad (float): logaritmo escalado de ventas o reseñas, en [0, 1].
    #     con_ventas (bool): True si el catálogo de ventas registra el título.
    #     apto (bool): False si es contenido para adultos o un programa que no
    #         es un juego.

    def __init__(self, titulo):
        # Crea una ficha vacía.

        # Parámetros:
        #     titulo (str): nombre visible del juego.
        self.titulo = titulo
        self.anio = None
        self.fecha = None
        self.anunciado = False
        self.periodo = ""
        self.saga = ""
        self.generos = set()
        self.plataformas = set()
        self.atributos = set()
        self.calidad_publica = 0.65
        self.evidencia_publica = 0.0
        self.popularidad = 0.0
        self.en_steam = False
        self.appid = ""
        self.contenido_revisado = False
        self.con_ventas = False
        self.apto = True

    def es_recomendable(self):
        # Para un estreno basta con conocer su género y plataforma. Las reseñas ajustan la nota.
        reciente = self.anio >= ANIO_DESDE if self.anio is not None else self.anunciado
        return bool(reciente and self.apto and self.generos and self.plataformas)


def resena_publica(fila):
    # Calcula la nota pública, su evidencia y la popularidad de una fila.

    # Las notas con pocas opiniones se acercan a 0.65 (suavizado bayesiano:
    # equivale a sumar 20 opiniones ficticias, 13 de ellas favorables).

    # Parámetros:
    #     fila (dict): fila estandarizada con las claves de COLUMNAS_DEL_CATALOGO.

    # Devuelve:
    #     tuple: (nota, opiniones, popularidad). nota es un float en [0, 1] o
    #     None si la fila no tiene opiniones; opiniones es la cantidad de
    #     opiniones (0 si no hay); popularidad está en [0, 1].
    positivas = numero(fila["positivas"])
    negativas = numero(fila["negativas"])
    nota_usuario = numero(fila["nota"])
    critica = numero(fila["critica"])
    ventas = numero(fila["ventas"])
    votos_de_steam = (positivas or 0.0) + (negativas or 0.0)
    nota = None
    opiniones = 0.0
    # Cada fuente usa su propia escala; se toma la más informativa que exista.
    if positivas is not None and votos_de_steam > 0:
        opiniones = votos_de_steam
        nota = (positivas + 13) / (votos_de_steam + 20)
    elif nota_usuario is not None and 0 < nota_usuario <= 10:
        opiniones = numero(fila["usuarios"]) or 1.0
        nota = (opiniones * nota_usuario / 10 + 13) / (opiniones + 20)
    elif critica is not None and 0 < critica <= 100:
        opiniones = 0.5  # La crítica es una señal de respaldo, equivalente a media opinión.
        nota = 0.5 * (critica / 100 + 0.65)
    # La popularidad crece con el logaritmo para que los grandes éxitos no dominen.
    popularidad = 0.0
    if ventas is not None:
        popularidad = min(1.0, math.log1p(ventas) / math.log1p(30))
    elif votos_de_steam > 0:
        popularidad = min(1.0, math.log1p(votos_de_steam) / math.log1p(25000))
    return nota, opiniones, popularidad


def columnas_del_archivo(nombres):
    # Relaciona las columnas que usa el programa con las del archivo.

    # Parámetros:
    #     nombres (list[str]): encabezados del archivo.

    # Devuelve:
    #     dict[str, str o None]: nombre interno (por ejemplo "titulo") →
    #     encabezado del archivo (por ejemplo "Name"), o None si falta.
    disponibles = {}
    for columna in nombres:
        disponibles[normalizar(columna)] = columna
    campos = {}
    for destino, alias in COLUMNAS_DEL_CATALOGO.items():
        # El nombre interno va primero porque es el que usan las copias de datos_juegos.
        encontrado = primero_presente((destino,) + alias, disponibles)
        campos[destino] = disponibles[encontrado] if encontrado else None
    return campos


class CatalogoDeJuegos:
    # Catálogo unificado de los dos conjuntos de datos.

    # Atributos:
    #     fuentes (list[Path]): archivos leídos.
    #     filas_por_fuente (dict[Path, int]): filas con título leídas de cada
    #         archivo; permite comprobar que se usaron los dos catálogos.
    #     juegos (dict[str, FichaDeJuego]): fichas indexadas por clave de título.
    #     por_appid (dict[str, str]): identificador de Steam → clave de título.
    #     plataformas (dict[str, str]): clave de plataforma → nombre visible.
    #     por_texto_compacto (dict[str, str o None]): título sin espacios →
    #         clave; None cuando dos títulos distintos se escriben igual.
    #     claves_recomendables (list[str]): claves de los juegos recomendables.
    #     frecuencia_de_generos (Counter): juegos recomendables por género.
    #     frecuencia_de_plataformas (Counter): juegos recomendables por plataforma.
    #     frecuencia_de_atributos (Counter): juegos recomendables por atributo;
    #         un atributo poco frecuente describe mejor lo que comparten dos juegos.

    def __init__(self, fuentes, anuncios=(), consolas=None, carpeta_etiquetas=None):
        # Lee todos los catálogos y construye los índices.

        # Parámetros:
        #     fuentes (list[Path]): archivos CSV o ZIP con un CSV.

        # Errores:
        #     ValueError: si ningún archivo contiene títulos utilizables.
        self.fuentes = list(fuentes)
        self.juegos = {}
        self.por_appid = {}
        self.filas_por_fuente = {}
        self.hoy = date.today()
        self.ids_de_la_tienda = {fila["identificador"] for fila in anuncios}
        for fuente in self.fuentes:
            self.leer(fuente)
        for fila in anuncios:
            self.agregar_fila(fila)
        # Añade las opciones recién descubiertas al final del menú para conservar su numeración anterior.
        generos_originales = {g for j in self.juegos.values() if j.es_recomendable() for g in j.generos}
        self.orden_generos = sorted(GENEROS_DEL_CUESTIONARIO, key=lambda g: g not in generos_originales)
        if carpeta_etiquetas is not None:
            completar_generos(self.juegos, carpeta_etiquetas)
        # Aplicamos el veto después de unir las fuentes. Otra fila del mismo juego no puede deshacerlo.
        self.juegos = {clave: juego for clave, juego in self.juegos.items() if juego.apto}
        self.por_appid = {appid: clave for appid, clave in self.por_appid.items() if clave in self.juegos}
        if not self.juegos and not (self.filas_por_fuente or anuncios):
            raise ValueError("Los archivos no contienen títulos utilizables.")

        # Índices y conteos que usan el cuestionario, los filtros y las explicaciones.
        for appid, modelos in (consolas or {}).items():
            if appid in self.por_appid:
                self.juegos[self.por_appid[appid]].plataformas.update(modelos)
        self.plataformas = dict(MODELOS)
        self.claves_recomendables = []
        self.frecuencia_de_generos = Counter()
        self.frecuencia_de_plataformas = Counter()
        self.frecuencia_de_atributos = Counter()
        for clave, juego in self.juegos.items():
            for plataforma in juego.plataformas:
                self.plataformas[clave_de_plataforma(plataforma)] = plataforma
            if juego.es_recomendable():
                self.claves_recomendables.append(clave)
                self.frecuencia_de_generos.update(juego.generos)
                self.frecuencia_de_plataformas.update(juego.plataformas)
                self.frecuencia_de_atributos.update(juego.atributos)
        self.indexar_nombres()

    def leer(self, fuente):
        # Agrega al catálogo las filas de un archivo.

        # Parámetros:
        #     fuente (Path): CSV o ZIP con un CSV; el separador puede ser coma,
        #         punto y coma o tabulador.

        # Errores:
        #     ValueError: si el archivo no tiene columna de título o no tiene
        #         filas con título.
        with abrir_csv(fuente) as datos:
            filas_con_titulo, filas_omitidas = recorrer_csv(datos, fuente.name, self.agregar_fila)
        self.filas_por_fuente[fuente] = filas_con_titulo
        if filas_omitidas:
            print(f"{fuente.name}: se omitieron {filas_omitidas} filas con columnas de más.")
        if filas_con_titulo == 0:
            raise ValueError(f"{fuente.name} no tiene filas con título.")

    def agregar_fila(self, fila):
        # Agrega una fila estandarizada a la ficha de su título.

        # Parámetros:
        #     fila (dict): fila con las claves de COLUMNAS_DEL_CATALOGO y un
        #         título no vacío. Si el título ya existe (por ejemplo, el mismo
        #         juego en los dos catálogos), sus datos se suman a la misma ficha.
        clave = clave_titulo(fila["titulo"])
        anio, fecha = fecha_del_catalogo(fila["anio"])
        appid = fila["identificador"]
        # Una reedición puede tener el mismo nombre que el original y otra fecha o plataforma.
        anterior = self.juegos.get(clave)
        otra_edicion = anterior and (anterior.appid and anterior.appid != appid or
                                     anterior.anio and anio and abs(anterior.anio - anio) > 2)
        if appid.isdigit() and (otra_edicion or (anio and anio >= ANIO_DESDE) or appid in self.ids_de_la_tienda):
            clave = self.por_appid.get(appid, f"{clave} steam {appid}")
        if clave not in self.juegos:
            self.juegos[clave] = FichaDeJuego(fila["titulo"])
        juego = self.juegos[clave]
        if "anunciado" in fila:
            # La ficha de la tienda prevalece si se aplaza el estreno o desaparece su fecha.
            juego.anio, juego.fecha = anio, fecha
            juego.anunciado = fila["anunciado"]
            juego.periodo = fila["anio"]
        elif anio and (juego.anio is None or anio < juego.anio or (anio == juego.anio and fecha)):
            juego.anio, juego.fecha = anio, fecha
            juego.anunciado = fecha > self.hoy if fecha else anio > self.hoy.year
        self.agregar_ficha(clave, fila)

    def agregar_ficha(self, clave, fila):
        # Agrega los rasgos de una fila a la ficha de su título.

        # Parámetros:
        #     clave (str): clave del título, ya presente en self.juegos.
        #     fila (dict): fila estandarizada con las claves de COLUMNAS_DEL_CATALOGO.
        juego = self.juegos[clave]
        if fila["identificador"].isascii() and fila["identificador"].isdigit():
            juego.en_steam = True
            juego.appid = fila["identificador"]
            self.por_appid[fila["identificador"]] = clave

        # Steam informa sobre PC y Mac. Ventas y Wikidata aportan las consolas.
        plataformas = nombres_de_campo(fila["plataformas"])
        for campo, etiqueta in (("windows", "PC"), ("mac", "Mac")):
            if fila[campo].lower() in ("true", "yes", "1", "si"):
                plataformas.append(etiqueta)
        for plataforma in plataformas:
            if normalizar(plataforma) not in ("", "n a", "unknown", "linux", "gnu linux", "steamos"):
                juego.plataformas.add(MODELOS.get(clave_de_plataforma(plataforma), plataforma))

        # Contenido excluido: géneros o etiquetas de adultos o de programas que no son juegos.
        revision = clasificar_fila(fila)
        if revision == "excluir":
            juego.apto = False
        elif revision == "revisado":
            juego.contenido_revisado = True
        originales = nombres_de_campo(fila["genero"])
        temas = [normalizar(t) for t in etiquetas_de_campo(fila["etiquetas"])]
        for texto in [normalizar(g) for g in originales] + temas:
            if texto in CONTENIDO_EXCLUIDO:
                juego.apto = False

        # Géneros: los del catálogo, los que se deducen de las etiquetas y las anotaciones de terror.
        generos = set()
        for genero in originales:
            if normalizar(genero) not in ("", "n a", "unknown"):
                generos.add(NOMBRES_DE_GENERO.get(normalizar(genero), genero))
        for tema in temas:
            generos.update(ETIQUETAS_DE_GENERO.get(tema, []))
        nombre = clave_titulo(fila["titulo"])
        if nombre in TITULOS_DE_TERROR_PSICOLOGICO:
            generos.update(["Terror", "Terror psicológico"])
        saga_manual = ""
        for saga in SAGAS_DE_TERROR:
            if nombre == saga or nombre.startswith(saga + " "):
                saga_manual = saga
        if saga_manual or nombre in OTROS_TITULOS_DE_TERROR:
            generos.add("Terror")
        saga_declarada = normalizar(fila["saga"])
        if not juego.saga:
            juego.saga = saga_manual or (saga_declarada if saga_declarada != "ninguna" else "")

        # Los gustos se aprenden a partir de los géneros, las etiquetas, la saga y el estudio.
        juego.generos.update(generos)
        for genero in generos:
            juego.atributos.add(("genero", normalizar(genero)))
        for tema in temas:
            if tema:
                juego.atributos.add(("tema", tema))
        if juego.saga:
            juego.atributos.add(("tema", juego.saga))
        for nombre in nombres_de_campo(fila["desarrollador"])[:4]:
            estudio = normalizar(nombre)
            if estudio not in ("", "n a", "unknown"):
                juego.atributos.add(("estudio", estudio))

        # Reseñas: se conserva la nota de la fuente con más opiniones.
        nota, opiniones, popularidad = resena_publica(fila)
        if nota is not None and opiniones > juego.evidencia_publica:
            juego.calidad_publica = nota
            juego.evidencia_publica = opiniones
        juego.popularidad = max(juego.popularidad, popularidad)
        if numero(fila["ventas"]) is not None:
            juego.con_ventas = True

    def indexar_nombres(self):
        # Construye el índice de títulos escritos sin espacios.

        # Permite escribir, por ejemplo, SilentHill2. Si dos títulos distintos
        # se escriben igual sin espacios, el índice guarda None para no elegir
        # uno al azar.
        self.por_texto_compacto = {}
        pares = [(clave, clave) for clave in self.juegos] + list(EDICIONES_EQUIVALENTES.items())
        for clave, ficha in self.juegos.items():
            nombre = clave_titulo(ficha.titulo)
            if nombre != clave:
                pares.append((nombre, clave))
            if ficha.anio:
                pares.append((f"{nombre} {ficha.anio}", clave))
        for nombre, clave in pares:
            if clave in self.juegos:
                compacto = nombre.replace(" ", "")
                anterior = self.por_texto_compacto.get(compacto, clave)
                if anterior == clave:
                    self.por_texto_compacto[compacto] = clave
                else:
                    self.por_texto_compacto[compacto] = None

    def resolver_titulo(self, texto):
        # Identifica un único título del catálogo.

        # Parámetros:
        #     texto (str o None): título escrito por la persona o guardado en
        #         el perfil.

        # Devuelve:
        #     str o None: la clave del título; None si no existe o si la
        #     escritura sin espacios corresponde a varios títulos.
        clave = clave_titulo(texto or "")
        if clave not in self.juegos:
            clave = self.por_texto_compacto.get(clave.replace(" ", ""))
        return clave

    def buscar_titulos(self, texto, limite=6):
        # Busca títulos que contengan todas las palabras escritas.

        # Parámetros:
        #     texto (str): parte de un título, por ejemplo "zelda ocarina".
        #     limite (int): cantidad máxima de resultados (entero positivo).

        # Devuelve:
        #     list[str]: claves ordenadas: primero la coincidencia exacta,
        #     después los juegos recomendables y más populares. Si ninguna
        #     clave contiene las palabras, sugiere títulos de escritura
        #     parecida (por ejemplo, con una letra equivocada).
        palabras = normalizar(texto or "").split()
        exacta = self.resolver_titulo(texto)
        claves = []
        if palabras:
            coincidencias = [k for k in self.juegos if all(p in k for p in palabras)]
            if exacta and exacta not in coincidencias:
                coincidencias.append(exacta)
            if not coincidencias:
                parecidos = difflib.get_close_matches("".join(palabras), list(self.por_texto_compacto),
                                                      n=limite, cutoff=0.72)
                coincidencias = [self.por_texto_compacto[n] for n in parecidos if self.por_texto_compacto[n]]
            coincidencias.sort(key=lambda k: (k != exacta, not self.juegos[k].es_recomendable(),
                                              -self.juegos[k].popularidad, len(k), k))
            for clave in coincidencias:
                if len(claves) < limite and clave not in claves:
                    claves.append(clave)
        return claves

    def describir(self, clave):
        # Devuelve una descripción corta de un título.

        # Parámetros:
        #     clave (str): clave presente en self.juegos.

        # Devuelve:
        #     str: por ejemplo "Silent Hill 2 (2001) · PS2, PC".
        ficha = self.juegos[clave]
        periodo = str(ficha.anio or "")
        if ficha.fecha:
            periodo = ficha.fecha.strftime("%d/%m/%Y")
        elif ficha.anunciado and ficha.anio and ficha.periodo:
            periodo = ficha.periodo
        anio = f" ({periodo})" if periodo else ""
        if ficha.anunciado:
            if ficha.fecha and ficha.fecha < self.hoy:
                periodo = "fecha por actualizar"
            anio = f" · Próximamente ({periodo or 'fecha por confirmar'})"
        plataformas = ", ".join(sorted(ficha.plataformas)) or "plataforma sin registrar"
        return f"{ficha.titulo}{anio} · {plataformas}"

    def buscar_plataforma(self, texto):
        # Reconoce el nombre de una plataforma del catálogo.

        # Parámetros:
        #     texto (str o None): por ejemplo "PS4", "ps 4" o "PlayStation 4".

        # Devuelve:
        #     str o None: el nombre visible de la plataforma; None si el texto
        #     está vacío o no corresponde a ninguna plataforma.
        plataforma = None
        if texto:
            plataforma = self.plataformas.get(clave_de_plataforma(texto))
        return plataforma

    def resolver_plataforma(self, texto):
        # Igual que buscar_plataforma, pero rechaza los nombres desconocidos.

        # Parámetros:
        #     texto (str o None): nombre de plataforma; vacío significa «todas».

        # Devuelve:
        #     str o None: nombre visible, o None si el texto está vacío.

        # Errores:
        #     ValueError: si el texto no corresponde a ninguna plataforma.
        plataforma = self.buscar_plataforma(texto)
        if texto and plataforma is None:
            conocidas = ", ".join(self.plataformas_frecuentes(20))
            raise ValueError(f"Plataforma desconocida: '{texto}'. Puedes usar {conocidas}.")
        return plataforma

    def plataformas_frecuentes(self, cantidad=12):
        # Devuelve las plataformas con más juegos recomendables.

        # Parámetros:
        #     cantidad (int): máximo de plataformas (entero positivo).

        # Devuelve:
        #     list[str]: nombres visibles, de la más frecuente a la menos.
        return [plataforma for plataforma, _ in self.frecuencia_de_plataformas.most_common(cantidad)]

    def generos_del_cuestionario(self):
        # Devuelve los géneros del cuestionario que existen en el catálogo.

        # Devuelve:
        #     list[str]: géneros de GENEROS_DEL_CUESTIONARIO con al menos un
        #     juego recomendable, en el mismo orden.
        return [genero for genero in self.orden_generos if self.frecuencia_de_generos[genero] > 0]

    def candidatos(self, plataforma="", excluidos=(), evitados=(), historicos=False):
        # Filtra los juegos que se pueden recomendar.

        # Parámetros:
        #     plataforma (str o None): nombre visible; vacío acepta todas.
        #     excluidos (set[str]): claves ya jugadas, valoradas o favoritas.
        #     evitados (list[str]): géneros que la persona no quiere ver.

        # Devuelve:
        #     list[str]: claves recomendables que cumplen los tres filtros.
        filtro = clave_de_plataforma(plataforma) if plataforma else ""
        evitar = [normalizar(genero) for genero in evitados]
        elegidos = []
        modelos = FAMILIAS.get(filtro, {filtro})
        for clave in (self.juegos if historicos else self.claves_recomendables):
            juego = self.juegos[clave]
            # En la búsqueda histórica solo cuentan juegos anteriores a ANIO_DESDE con género.
            fuera_del_periodo = historicos and not (filtro and juego.anio and juego.anio < ANIO_DESDE
                                                    and juego.generos)
            plataforma_correcta = not filtro or any(clave_de_plataforma(p) in modelos for p in juego.plataformas)
            genero_evitado = any(normalizar(g) in evitar for g in juego.generos)
            if not fuera_del_periodo and clave not in excluidos and plataforma_correcta and not genero_evitado:
                elegidos.append(clave)
        return elegidos


# ----------------------------------------------------------------------
# Perfil persistente del jugador (SQLite).
# ----------------------------------------------------------------------

class Preferencias:
    # Respuestas del cuestionario inicial.

    # Atributos:
    #     generos (list[str]): géneros que le gustan a la persona.
    #     evitados (list[str]): géneros que nunca se le deben recomendar.
    #     favoritos (list[str]): claves de los juegos que declaró como favoritos.
    #     plataforma (str): plataforma preferida; cadena vacía si le da igual.
    #     respondido (bool): True si ya contestó el cuestionario.

    def __init__(self):
        # Crea unas preferencias vacías, como las de alguien que aún no contesta.
        self.generos = []
        self.evitados = []
        self.favoritos = []
        self.plataforma = ""
        self.respondido = False


def crear_tablas(conexion):
    # Crea las tablas del perfil si todavía no existen.

    # Tablas:
    #     perfil: una sola fila con las respuestas del cuestionario (listas en
    #         JSON).
    #     valoraciones: «me interesa» (1) o «no me interesa» (-1) por título.
    #     configuraciones: parámetros que eligió el meta-evolutivo para cada
    #         combinación de catálogos y longitud de lista.
    # Todo lo que guarda el perfil lo escribió la persona en la consola.

    # Parámetros:
    #     conexion (sqlite3.Connection): conexión abierta al archivo del perfil.
    conexion.executescript(
        "CREATE TABLE IF NOT EXISTS perfil ( "
        "id INTEGER PRIMARY KEY CHECK (id=1), "
        "generos TEXT NOT NULL, evitados TEXT NOT NULL, favoritos TEXT NOT NULL, "
        "plataforma TEXT NOT NULL, respondido INTEGER NOT NULL, "
        "alta INTEGER NOT NULL "
        "); "
        "CREATE TABLE IF NOT EXISTS valoraciones ( "
        "titulo TEXT PRIMARY KEY, valor INTEGER NOT NULL CHECK (valor IN (-1, 1)), "
        "fecha INTEGER NOT NULL "
        "); "
        "CREATE TABLE IF NOT EXISTS configuraciones ( "
        "clave TEXT PRIMARY KEY, parametros TEXT NOT NULL "
        "); "
        "CREATE TABLE IF NOT EXISTS resumen_resenas ("
        "appid TEXT PRIMARY KEY, total INTEGER NOT NULL, porcentaje INTEGER NOT NULL, fecha INTEGER NOT NULL"
        "); "
        "CREATE TABLE IF NOT EXISTS revision_steam ("
        "appid TEXT PRIMARY KEY, resultado TEXT NOT NULL, fecha INTEGER NOT NULL"
        ");"
    )
    # INSERT OR IGNORE crea el perfil vacío la primera vez y respeta el existente después.
    conexion.execute(
        "INSERT OR IGNORE INTO perfil(id, generos, evitados, favoritos, plataforma, respondido, alta) "
        "VALUES(1, '[]', '[]', '[]', '', 0, ?)",
        (int(time.time()),))
    conexion.commit()


def leer_preferencias(conexion):
    # Lee las respuestas guardadas del cuestionario.

    # Parámetros:
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.

    # Devuelve:
    #     Preferencias: las respuestas; vacías si nunca se contestó.
    fila = conexion.execute(
        "SELECT generos, evitados, favoritos, plataforma, respondido FROM perfil WHERE id=1").fetchone()
    preferencias = Preferencias()
    preferencias.generos = json.loads(fila[0])
    preferencias.evitados = json.loads(fila[1])
    preferencias.favoritos = json.loads(fila[2])
    preferencias.plataforma = fila[3]
    preferencias.respondido = fila[4] == 1
    return preferencias


def guardar_preferencias(conexion, preferencias):
    # Guarda las respuestas del cuestionario en el perfil.

    # Parámetros:
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.
    #     preferencias (Preferencias): respuestas que sustituyen a las anteriores.
    conexion.execute(
        "UPDATE perfil SET generos=?, evitados=?, favoritos=?, plataforma=?, respondido=? "
        "WHERE id=1",
        (json.dumps(preferencias.generos, ensure_ascii=False),
          json.dumps(preferencias.evitados, ensure_ascii=False),
          json.dumps(preferencias.favoritos, ensure_ascii=False),
          preferencias.plataforma, int(preferencias.respondido)))
    conexion.commit()


def guardar_valoraciones(conexion, valoraciones):
    # Guarda o corrige valoraciones de juegos recomendados.

    # Parámetros:
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.
    #     valoraciones (dict[str, int]): clave de título → 1 («me interesa»)
    #         o -1 («no me interesa»).
    ahora = int(time.time())
    for clave, valor in valoraciones.items():
        # Si el juego ya tenía valoración, la nueva la sustituye.
        conexion.execute(
            "INSERT INTO valoraciones(titulo, valor, fecha) VALUES(?, ?, ?) "
            "ON CONFLICT(titulo) DO UPDATE SET valor=excluded.valor, fecha=excluded.fecha",
            (clave, valor, ahora))
    conexion.commit()


# ----------------------------------------------------------------------
# Señales personales: lo que la persona escribió en la consola.
# ----------------------------------------------------------------------

class ActividadDeJuego:
    # Señales personales sobre un juego.

    # El programa no lee cuentas de Steam ni historiales de juego: solo sabe
    # lo que la persona escribe en la consola. Por eso las únicas señales son
    # los favoritos del cuestionario y las valoraciones de las listas.

    # Atributos:
    #     favorito (bool): declarado como favorito en el cuestionario, o
    #         juego de referencia de esta ejecución.
    #     valoracion (int): 1 «me interesa», -1 «no me interesa», 0 sin valorar.

    def __init__(self):
        # Crea una actividad vacía: no es favorito ni tiene valoración.
        self.favorito = False
        self.valoracion = 0

    def interesa(self):
        # Indica si hay interés claro en el juego.

        # Devuelve:
        #     bool: True si es favorito o si tiene «me interesa».
        return self.favorito or self.valoracion > 0

    def rechazado(self):
        # Devuelve True si la persona marcó «no me interesa».
        return self.valoracion < 0


def obtener_actividad(actividad, clave):
    # Devuelve la actividad de un juego y la crea vacía si no existía.

    # Parámetros:
    #     actividad (dict[str, ActividadDeJuego]): señales por título.
    #     clave (str): clave del título.

    # Devuelve:
    #     ActividadDeJuego: el objeto guardado en el diccionario; modificarlo
    #     modifica la actividad.
    if clave not in actividad:
        actividad[clave] = ActividadDeJuego()
    return actividad[clave]


def actividad_personal(conexion, catalogo, preferencias):
    # Combina por título los favoritos y las valoraciones guardadas.

    # Parámetros:
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     preferencias (Preferencias): respuestas del cuestionario.

    # Devuelve:
    #     dict[str, ActividadDeJuego]: clave de título → señales. Solo
    #     incluye títulos que existen en el catálogo cargado.
    actividad = {}
    for favorito in preferencias.favoritos:
        clave = catalogo.resolver_titulo(favorito)
        if clave in catalogo.juegos:
            obtener_actividad(actividad, clave).favorito = True
    for nombre, valor in conexion.execute("SELECT titulo, valor FROM valoraciones").fetchall():
        clave = catalogo.resolver_titulo(nombre)
        if clave in catalogo.juegos:
            obtener_actividad(actividad, clave).valoracion = valor
    return actividad


def hay_informacion_personal(preferencias, actividad):
    # Indica si hay gustos suficientes para no recomendar solo por popularidad.

    # Parámetros:
    #     preferencias (Preferencias): respuestas del cuestionario.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.

    # Devuelve:
    #     bool: True si hay al menos un género favorito, un juego de interés
    #     o una valoración.
    return len(preferencias.generos) > 0 or any(uso.interesa() or uso.rechazado() for uso in actividad.values())


# ----------------------------------------------------------------------
# Aprendizaje del perfil de gustos (regresión logística).
# ----------------------------------------------------------------------

class PerfilDeGustos:
    # Modelo lineal de los gustos de una persona.

    # Atributos:
    #     pesos (dict[tuple, float]): peso de cada atributo (tipo, valor); un
    #         valor positivo favorece los juegos que tienen ese atributo, por
    #         ejemplo ("genero", "terror").
    #     intercepto (float): término independiente del modelo.
    #     evidencia (int): cantidad de señales personales usadas (ejemplos de
    #         entrenamiento y géneros declarados).

    def __init__(self, pesos, intercepto, evidencia):
        # Guarda los valores aprendidos (ver los atributos de la clase).
        self.pesos = pesos
        self.intercepto = intercepto
        self.evidencia = evidencia
        self.generos_declarados = set()
        self.con_historial = False
        self.favoritos = {}
        self.frecuencia_personal = {}


def sigmoide(valor):
    # Convierte un número real en una probabilidad.

    # Parámetros:
    #     valor (float): suma lineal del modelo.

    # Devuelve:
    #     float: 1 / (1 + e^-valor), en (0, 1). La fórmula se evalúa de dos
    #     formas para evitar desbordamientos con valores grandes.
    exponencial = math.exp(-abs(valor))
    return 1 / (1 + exponencial) if valor >= 0 else exponencial / (1 + exponencial)


def pesos_previos(preferencias):
    # Traduce los géneros del cuestionario en pesos iniciales del modelo.

    # Parámetros:
    #     preferencias (Preferencias): respuestas del cuestionario.

    # Devuelve:
    #     dict[tuple, float]: ("genero", nombre normalizado) → PESO_PREVIO_GUSTA.
    previos = {}
    for genero in preferencias.generos:
        previos[("genero", normalizar(genero))] = PESO_PREVIO_GUSTA
    return previos


def ejemplos_aprendizaje(catalogo, actividad, fondo, semilla):
    # Construye los ejemplos ponderados de la regresión logística.

    # Clase 1: juegos de interés (favoritos y «me interesa»). Clase 0: juegos
    # rechazados («no me interesa») y una muestra de hasta 48 juegos típicos
    # del catálogo, que permite comparar los rasgos de la persona con los
    # rasgos comunes. Si no hay juegos de interés pero sí rechazos, los juegos
    # típicos pasan a la clase 1: así se aprende qué tienen de peor los
    # rechazados que un juego cualquiera.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    #     fondo (sequence[str]): claves de las que se toma la muestra típica.
    #     semilla (int): semilla de la muestra, para que sea reproducible.

    # Devuelve:
    #     list[tuple]: (atributos ordenados, clase, peso). Los pesos de cada
    #     clase suman 0.5, aunque una clase tenga más juegos que la otra.
    positivos = []
    negativos = []
    # Dentro de los ejemplos positivos, un favorito ya jugado pesa el doble que «me interesa».
    for clave in sorted(actividad):
        uso = actividad[clave]
        atributos = tuple(sorted(catalogo.juegos[clave].atributos))
        if uso.interesa():
            positivos.append((atributos, 4.0 if uso.favorito else 2.0))
        elif uso.rechazado():
            negativos.append((atributos, 2.0))

    # Muestra reproducible de juegos típicos que la persona no ha mencionado.
    disponibles = [clave for clave in fondo if clave not in actividad]
    muestra = random.Random(semilla).sample(disponibles, min(48, len(disponibles)))
    tipicos = [tuple(sorted(catalogo.juegos[clave].atributos)) for clave in muestra]

    grupos = ()
    if positivos:
        masa_tipica = max(1.0, sum(peso for _, peso in negativos) / 3)
        clase_cero = negativos + [(atributos, masa_tipica / len(tipicos)) for atributos in tipicos]
        grupos = ((1, positivos), (0, clase_cero))
    elif any(uso.rechazado() for uso in actividad.values()):
        grupos = ((1, [(atributos, 1.0) for atributos in tipicos]), (0, negativos))

    # Cada clase recibe el mismo peso total.
    ejemplos = []
    for clase, grupo in grupos:
        masa = sum(peso for _, peso in grupo)
        if masa > 0:
            ejemplos.extend((atributos, clase, peso / (2 * masa)) for atributos, peso in grupo)
    return ejemplos


def aprender_perfil(catalogo, actividad, preferencias, fondo, semilla=SEMILLA_PREDETERMINADA):
    # Aprende el perfil de gustos con regresión logística regularizada.

    # Con historial, la regresión aprende de favoritos y valoraciones. Los géneros declarados
    # se combinan después para poder controlar cuánto pesa cada fuente de información.
    # Sin historial, los géneros declarados dan los pesos iniciales.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    #     preferencias (Preferencias): respuestas del cuestionario.
    #     fondo (sequence[str]): claves para la muestra de juegos típicos.
    #     semilla (int): semilla de esa muestra.

    # Devuelve:
    #     PerfilDeGustos: pesos, intercepto y cantidad de evidencia.
    ejemplos = ejemplos_aprendizaje(catalogo, actividad, fondo, semilla)
    declarados = pesos_previos(preferencias)
    previos = {} if ejemplos else declarados
    pesos = dict(previos)
    for rasgos, _, _ in ejemplos:
        for rasgo in rasgos:
            if rasgo not in pesos:
                pesos[rasgo] = 0.0
    intercepto = 0.0

    for _ in range(ITERACIONES_DE_APRENDIZAJE if ejemplos else 0):
        # Cada vuelta acumula cuánto contribuyó cada rasgo al error en todos los ejemplos.
        gradientes = {rasgo: 0.0 for rasgo in pesos}
        gradiente_del_intercepto = 0.0
        for rasgos, observado, peso_del_ejemplo in ejemplos:
            # La suma lineal se convierte en una estimación entre 0 y 1.
            estimado = sigmoide(intercepto + sum(PESO_POR_TIPO[r[0]] * pesos[r] for r in rasgos))
            # Si un ejemplo de clase 1 solo obtiene 0.3, el error es negativo y sus rasgos ganan peso.
            error = peso_del_ejemplo * (estimado - observado)
            gradiente_del_intercepto += error
            for rasgo in rasgos:
                gradientes[rasgo] += error * PESO_POR_TIPO[rasgo[0]]
        # Restar el gradiente reduce el error; la regularización acerca cada peso a su valor previo.
        intercepto -= TASA_DE_APRENDIZAJE * gradiente_del_intercepto
        for rasgo in pesos:
            diferencia = pesos[rasgo] - previos.get(rasgo, 0.0)
            pesos[rasgo] -= TASA_DE_APRENDIZAJE * (gradientes[rasgo] + REGULARIZACION * diferencia)

    perfil = PerfilDeGustos(pesos, intercepto, len(ejemplos) + len(declarados))
    perfil.generos_declarados = set(declarados)
    perfil.con_historial = bool(ejemplos)
    frecuencias = Counter()
    peso_total = 0
    juegos_con_generos = 0
    for clave in sorted(actividad):
        uso = actividad[clave]
        if uso.interesa():
            rasgos = rasgos_para_comparar(catalogo.juegos[clave])
            if rasgos and uso.favorito:
                perfil.favoritos[clave] = rasgos
            familias = [g for tipo, g in rasgos if tipo == "genero"]
            if familias:
                peso = 2 if uso.favorito else 1
                for genero in familias:
                    frecuencias[genero] += peso
                peso_total += peso
                juegos_con_generos += 1
    if juegos_con_generos > 1:
        perfil.frecuencia_personal = {g: n / peso_total for g, n in frecuencias.items()}
    return perfil


def familia_del_genero(genero):
    # Una etiqueta más específica sigue describiendo la misma experiencia.
    return "terror" if genero == "terror psicologico" else genero


def gustos_coincidentes(juego, perfil):
    # Se cuenta cada familia elegida una sola vez, aunque coincidan un género y su subgénero.
    return {familia_del_genero(g) for _, g in perfil.generos_declarados & juego.atributos}


def rasgos_para_comparar(juego):
    # Un género y su traducción en las etiquetas de Steam cuentan una sola vez.
    rasgos = set()
    for tipo, nombre in juego.atributos:
        if tipo == "genero":
            rasgos.add((tipo, familia_del_genero(nombre)))
        elif tipo == "tema" and nombre not in ETIQUETAS_DE_GENERO:
            rasgos.add((tipo, nombre))
    return rasgos


def parecido_al_favorito(rasgos, favorito):
    # La similitud de Jaccard compara los rasgos compartidos con el total de rasgos distintos.
    return len(rasgos & favorito) / len(rasgos | favorito)


def muestra_variada(catalogo, ordenados, perfil, limite):
    # Partimos del orden de afinidad. Buscamos combinaciones distintas entre los gustos declarados.
    gustos = {familia_del_genero(g) for _, g in perfil.generos_declarados}
    if len(gustos) < 2 and not perfil.favoritos:
        return []
    mejores = {}
    ejemplos = {}

    for clave in ordenados:
        coincidencias = frozenset(gustos_coincidentes(catalogo.juegos[clave], perfil))
        if len(gustos) > 1 and coincidencias:
            mejores.setdefault(coincidencias, clave)
        if perfil.favoritos:
            rasgos = rasgos_para_comparar(catalogo.juegos[clave])
            for titulo, favorito in perfil.favoritos.items():
                parecido = parecido_al_favorito(rasgos, favorito)
                if parecido > ejemplos.get(titulo, (0, None))[0]:
                    ejemplos[titulo] = (parecido, clave)
    # Si varias combinaciones aportan la misma novedad, gana la de mayor afinidad.
    muestra = list(dict.fromkeys(clave for _, clave in ejemplos.values()))[:limite]
    representados = set()
    for clave in muestra:
        representados.update(gustos_coincidentes(catalogo.juegos[clave], perfil))
    while mejores and len(muestra) < limite:
        combinacion = max(mejores, key=lambda rasgos: len(rasgos - representados))
        clave = mejores.pop(combinacion)
        if clave not in muestra:
            muestra.append(clave)
        representados.update(combinacion)
    return muestra


def estimar_afinidad(juego, perfil):
    # Estima cuánto le gustará un juego a la persona.

    # Parámetros:
    #     juego (FichaDeJuego): ficha del juego.
    #     perfil (PerfilDeGustos): perfil aprendido.

    # Devuelve:
    #     float: afinidad en [0, 1]. Las reseñas aportan un 20 % a partir de 101 opiniones.
    if perfil.generos_declarados:
        coincidencias = len(gustos_coincidentes(juego, perfil))
        por_generos = sigmoide(coincidencias * PESO_PREVIO_GUSTA * PESO_POR_TIPO["genero"])
    if perfil.con_historial or not perfil.generos_declarados:
        # Recorremos los rasgos en un orden estable para que la suma sea reproducible.
        valor = perfil.intercepto
        for rasgo in sorted(juego.atributos):
            valor += PESO_POR_TIPO[rasgo[0]] * perfil.pesos.get(rasgo, 0.0)
        personal = sigmoide(valor)
        if perfil.generos_declarados:
            personal = PESO_DEL_HISTORIAL * personal + (1 - PESO_DEL_HISTORIAL) * por_generos
    else:
        personal = por_generos
    if juego.evidencia_publica < MINIMO_DE_RESENAS:
        return personal
    return (1 - PESO_DE_LA_RESENA) * personal + PESO_DE_LA_RESENA * juego.calidad_publica


# ----------------------------------------------------------------------
# Algoritmo evolutivo genérico que solo usa mutación.
# ----------------------------------------------------------------------

def estructura_valida(configuracion, presupuesto):
    # Comprueba que una configuración se pueda ejecutar.

    # Parámetros:
    #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida).
    #     presupuesto (int): evaluaciones disponibles.

    # Devuelve:
    #     bool: True si 1 <= descendientes < poblacion <= presupuesto,
    #     1 <= torneo <= poblacion y 0 <= dirigida <= 1.
    poblacion, descendientes, torneo, dirigida = configuracion
    return (1 <= descendientes < poblacion <= presupuesto
            and 1 <= torneo <= poblacion
            and 0 <= dirigida <= 1)


def configuracion_valida(configuracion, presupuesto=PRESUPUESTO_DE_BUSQUEDA):
    # Comprueba que una configuración pertenezca al dominio del ajuste.

    # Parámetros:
    #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida).
    #     presupuesto (int): evaluaciones disponibles.

    # Devuelve:
    #     bool: True si cada gen tiene uno de los valores de VALORES_DE_AJUSTE
    #     y la estructura es ejecutable.
    en_el_dominio = len(configuracion) == len(VALORES_DE_AJUSTE)
    if en_el_dominio:
        for posicion in range(len(configuracion)):
            if configuracion[posicion] not in VALORES_DE_AJUSTE[posicion]:
                en_el_dominio = False
    return en_el_dominio and estructura_valida(configuracion, presupuesto)


class ResultadoEvolutivo:
    # Resultado de una ejecución de AlgoritmoEvolutivo.

    # Atributos:
    #     mejor (tuple): mejor individuo encontrado.
    #     aptitud (float): aptitud de ese individuo.
    #     mejoras (list[tuple]): curva de convergencia; una terna (generación,
    #         número de evaluación, aptitud) por cada mejora estricta del mejor
    #         individuo. La primera terna es el mejor de la población inicial
    #         (generación 0).
    #     generaciones (int): generaciones completadas con el presupuesto.
    #     evaluaciones (int): individuos evaluados.
    #     diversidad (float): diversidad genética media de todas las
    #         generaciones, en [0, 1].

    def __init__(self, mejor, aptitud, mejoras, generaciones, evaluaciones, diversidad):
        # Guarda las medidas de la ejecución (ver los atributos de la clase).
        self.mejor = mejor
        self.aptitud = aptitud
        self.mejoras = mejoras
        self.generaciones = generaciones
        self.evaluaciones = evaluaciones
        self.diversidad = diversidad

    def momento_de_convergencia(self, objetivo):
        # Indica cuándo la búsqueda alcanzó una aptitud objetivo.

        # Parámetros:
        #     objetivo (float): aptitud que se considera convergencia.

        # Devuelve:
        #     tuple: (generación, número de evaluación) de la primera mejora
        #     con aptitud mayor o igual que el objetivo; si nunca lo alcanzó,
        #     (generaciones, evaluaciones), es decir, todo el presupuesto.
        momento = (self.generaciones, self.evaluaciones)
        encontrado = False
        for generacion, evaluacion, aptitud in self.mejoras:
            if not encontrado and aptitud >= objetivo - 1e-12:
                momento = (generacion, evaluacion)
                encontrado = True
        return momento


def diversidad_genetica(individuos):
    # Mide la diversidad de una población con la distancia de Hamming.

    # Parámetros:
    #     individuos (list[tuple]): individuos de la misma longitud.

    # Devuelve:
    #     float: fracción media de posiciones distintas entre cada par de
    #     individuos, en [0, 1]; 0 si hay menos de dos individuos.
    cantidad = len(individuos)
    diversidad = 0.0
    if cantidad > 1 and len(individuos[0]) > 0:
        genes = len(individuos[0])
        pares_iguales = 0
        # En cada posición se cuentan los pares de individuos que tienen el mismo gen:
        # si un valor aparece n veces, forma n·(n-1) pares ordenados iguales.
        for posicion in range(genes):
            frecuencias = Counter(individuo[posicion] for individuo in individuos)
            for repeticiones in frecuencias.values():
                pares_iguales += repeticiones * (repeticiones - 1)
        diversidad = 1 - pares_iguales / (cantidad * (cantidad - 1) * genes)
    return diversidad


class AlgoritmoEvolutivo:
    # Estrategia evolutiva con elitismo, torneo y un solo padre por hijo.

    # No depende del tipo de individuo: recibe la función de aptitud y el
    # operador de mutación como parámetros. Así se usa igual para evolucionar
    # listas de juegos y para evolucionar configuraciones del propio algoritmo.

    # Atributos:
    #     poblacion, descendientes, torneo, dirigida: los cuatro genes de la
    #         configuración (ver NOMBRES_DE_PARAMETROS).
    #     evaluar (función): individuo → aptitud (float, mayor es mejor).
    #     mutar (función): (padre, dirigida, azar) → hijo válido.
    #     presupuesto (int): evaluaciones máximas, incluida la población inicial.
    #     azar (random.Random): generador de números aleatorios.

    def __init__(self, configuracion, evaluar, mutar, presupuesto, azar):
        # Guarda los componentes de la búsqueda.

        # Parámetros:
        #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida).
        #     evaluar, mutar, presupuesto, azar: ver los atributos de la clase.

        # Errores:
        #     ValueError: si la configuración no es ejecutable con el presupuesto.
        if not estructura_valida(configuracion, presupuesto):
            raise ValueError(f"La configuración {configuracion} no es válida con {presupuesto} evaluaciones.")
        self.poblacion, self.descendientes, self.torneo, self.dirigida = configuracion
        self.evaluar = evaluar
        self.mutar = mutar
        self.presupuesto = presupuesto
        self.azar = azar

    def seleccionar_padre(self, poblacion):
        # Elige un padre por torneo.

        # Parámetros:
        #     poblacion (list[tuple]): pares (aptitud, individuo).

        # Devuelve:
        #     tuple: el individuo con mayor aptitud entre los del torneo.
        competidores = self.azar.sample(poblacion, self.torneo)
        ganador = max(competidores, key=lambda par: par[0])
        return ganador[1]

    def ejecutar(self, iniciales):
        # Evoluciona la población hasta agotar el presupuesto.

        # Parámetros:
        #     iniciales (list[tuple]): exactamente self.poblacion individuos válidos.

        # Devuelve:
        #     ResultadoEvolutivo: mejor individuo y medidas de la ejecución.

        # Errores:
        #     ValueError: si la población inicial no tiene el tamaño indicado.
        if len(iniciales) != self.poblacion:
            raise ValueError("La población inicial no tiene el tamaño de la configuración.")
        # Cada miembro de la población es un par (aptitud, individuo).
        poblacion = [(self.evaluar(individuo), individuo) for individuo in iniciales]
        evaluaciones = len(poblacion)
        mejor = max(poblacion, key=lambda par: par[0])
        mejoras = [(0, poblacion.index(mejor) + 1, mejor[0])]
        generacion = 0
        diversidades = [diversidad_genetica(iniciales)]

        # En cada generación sobreviven los mejores y cada hijo nuevo nace de una mutación.
        while evaluaciones < self.presupuesto:
            generacion += 1
            cantidad = min(self.descendientes, self.presupuesto - evaluaciones)
            ordenada = sorted(poblacion, key=lambda par: par[0], reverse=True)
            nueva = ordenada[:self.poblacion - cantidad]
            for _ in range(cantidad):
                padre = self.seleccionar_padre(poblacion)
                dirigida = self.azar.random() < self.dirigida
                hijo = self.mutar(padre, dirigida, self.azar)
                par = (self.evaluar(hijo), hijo)
                evaluaciones += 1
                # Solo una mejora estricta se registra en la curva de convergencia.
                if par[0] > mejor[0] + 1e-12:
                    mejor = par
                    mejoras.append((generacion, evaluaciones, par[0]))
                nueva.append(par)
            poblacion = nueva
            diversidades.append(diversidad_genetica([individuo for _, individuo in poblacion]))
        return ResultadoEvolutivo(mejor[1], mejor[0], mejoras, generacion, evaluaciones,
                                  statistics.mean(diversidades))


# ----------------------------------------------------------------------
# Problema de configuración: armar una lista de juegos.
# ----------------------------------------------------------------------

class MedidasDeRuta:
    # Criterios de calidad de una lista, todos en [0, 1].

    # Atributos:
    #     afinidad (float): combina la afinidad individual con lo que representa la ruta del perfil.
    #     variedad (float): mide las diferencias entre juegos y la cobertura de los géneros elegidos.
    #     continuidad (float): parecido medio entre juegos consecutivos.

    def __init__(self, afinidad, variedad, continuidad):
        # Guarda los tres criterios (ver los atributos de la clase).
        self.afinidad = afinidad
        self.variedad = variedad
        self.continuidad = continuidad

    def aptitud(self):
        # Devuelve 0.60 afinidad + 0.20 variedad + 0.20 continuidad.

        # Los gustos pesan más que variar la lista o enlazar vecinos.
        return 0.60 * self.afinidad + 0.20 * self.variedad + 0.20 * self.continuidad


class ProblemaDeRuta:
    # Problema de configuración que resuelve el evolutivo base.

    # Un individuo es una tupla de claves distintas de longitud fija; el
    # orden importa, porque la continuidad mira los juegos vecinos.

    # Atributos:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     afinidades (dict[str, float]): afinidad de cada candidato de la reserva.
    #     candidatos (list[str]): reserva de los TAMANO_DE_RESERVA candidatos
    #         de mayor afinidad, ordenados de mayor a menor.
    #     preferidos (list[str]): primeros candidatos, que usa la mutación dirigida.
    #     longitud (int): juegos por lista; como máximo, el número de candidatos.
    #     parecidos (dict): memoria del parecido de cada pareja ya calculada.

    def __init__(self, catalogo, candidatos, longitud, perfil):
        # Calcula las afinidades y prepara la reserva de candidatos.

        # Parámetros:
        #     catalogo (CatalogoDeJuegos): catálogo cargado.
        #     candidatos (list[str]): al menos una clave, sin repetir.
        #     longitud (int): juegos por lista (entero positivo).
        #     perfil (PerfilDeGustos): perfil aprendido.
        self.catalogo = catalogo
        todas = {}
        for clave in candidatos:
            todas[clave] = estimar_afinidad(catalogo.juegos[clave], perfil)
        ordenados = sorted(candidatos, key=lambda clave: (-todas[clave], clave))
        self.candidatos = ordenados[:max(TAMANO_DE_RESERVA, longitud)]
        # La reserva también debe incluir un anuncio aunque su juego todavía no tenga reseñas.
        self.longitud = min(longitud, len(self.candidatos))
        self.representantes = {}
        if self.longitud > 1:
            # Se busca el mejor publicado y el mejor anunciado; basta con encontrar uno de cada tipo.
            indice = 0
            while len(self.representantes) < 2 and indice < len(ordenados):
                clave = ordenados[indice]
                self.representantes.setdefault(catalogo.juegos[clave].anunciado, clave)
                indice += 1
            for clave in self.representantes.values():
                if clave not in self.candidatos:
                    self.candidatos[-1] = clave
        variados = muestra_variada(catalogo, ordenados, perfil, max(16, 3 * longitud))
        self.candidatos.extend(k for k in variados if k not in self.candidatos)
        self.afinidades = {clave: todas[clave] for clave in self.candidatos}
        self.preferidos = self.candidatos[:max(self.longitud + 1, TAMANO_DE_PREFERIDOS)]
        self.parecidos = {}
        self.gustos_para_variedad = {familia_del_genero(g) for _, g in perfil.generos_declarados}
        self.familias = {k: gustos_coincidentes(catalogo.juegos[k], perfil)
                         for k in self.candidatos}

        self.frecuencia_personal = perfil.frecuencia_personal
        self.generos_del_candidato = {
            k: {familia_del_genero(g) for tipo, g in catalogo.juegos[k].atributos if tipo == "genero"}
            for k in self.candidatos
        }
        # Guardamos el parecido una vez. Muchas rutas reutilizan los mismos juegos.
        self.parecidos_a_favoritos = {}
        for titulo, favorito in perfil.favoritos.items():
            self.parecidos_a_favoritos[titulo] = {
                k: parecido_al_favorito(rasgos_para_comparar(catalogo.juegos[k]), favorito)
                for k in self.candidatos
            }

        # Una ruta inicial se arma paso a paso. Cada nuevo juego compite por lo que aporta
        # junto a los ya elegidos. El evolutivo también prueba otras rutas y muta su orden.
        self.inicial_por_gustos = None

    def ruta_por_gustos(self):
        if self.inicial_por_gustos is None:
            ruta = []
            for _ in range(self.longitud):
                opciones = (k for k in self.candidatos if k not in ruta)
                mejor = max(opciones, key=lambda k: self.aptitud(ruta + [k]))
                ruta.append(mejor)
            self.inicial_por_gustos = self.combinar_lanzamientos(ruta)
        return self.inicial_por_gustos

    def combinar_lanzamientos(self, ruta):
        # Cuando hay opciones de ambos tipos, deja al menos un lugar para cada tipo.
        if len(self.representantes) == 2:
            estado = self.catalogo.juegos[ruta[0]].anunciado
            if all(self.catalogo.juegos[k].anunciado == estado for k in ruta):
                ruta[-1] = self.representantes[not estado]
        return tuple(ruta)

    def parecido(self, a, b):
        # Mide el parecido entre dos juegos y lo recuerda.

        # Parámetros:
        #     a, b (str): claves de la reserva.

        # Devuelve:
        #     tuple: (similitud de Jaccard en [0, 1], True si son de la misma saga).
        pareja = (a, b) if a < b else (b, a)
        if pareja not in self.parecidos:
            primero = self.catalogo.juegos[a]
            segundo = self.catalogo.juegos[b]
            union = primero.atributos | segundo.atributos
            # Jaccard divide los rasgos compartidos entre los rasgos distintos de la pareja.
            similitud = 0.0
            if union:
                similitud = len(primero.atributos & segundo.atributos) / len(union)
            misma_saga = primero.saga != "" and primero.saga == segundo.saga
            self.parecidos[pareja] = (similitud, misma_saga)
        return self.parecidos[pareja]

    def medir(self, ruta):
        # Calcula los criterios de una lista.

        # Parámetros:
        #     ruta (tuple[str]): al menos una clave de la reserva, sin repetir.

        # Devuelve:
        #     MedidasDeRuta: afinidad, variedad y continuidad.
        afinidad = sum(self.afinidades[clave] for clave in ruta) / len(ruta)
        senales = [afinidad]
        if len(self.parecidos_a_favoritos) > 1:
            # Para cada favorito buscamos su mejor coincidencia entre todos los juegos de la ruta.
            cobertura = sum(max(parecidos[k] for k in ruta) for parecidos in self.parecidos_a_favoritos.values())
            senales.append(cobertura / len(self.parecidos_a_favoritos))
        if self.frecuencia_personal and len(ruta) > 1:
            # Si un género aparece en toda la ruta y en pocos de tus juegos, la ruta pierde puntos.
            # La referencia es la frecuencia de tus propios favoritos y valoraciones positivas.
            cantidades = Counter(g for k in ruta for g in self.generos_del_candidato[k])
            exceso = max((n / len(ruta) - self.frecuencia_personal.get(g, 0.0)
                          for g, n in cantidades.items()), default=0.0)
            senales.append(1 - max(0.0, exceso))
        afinidad = sum(senales) / len(senales)
        variedad = 1.0
        continuidad = 1.0
        if len(ruta) > 1:
            suma_pares = 0.0
            suma_vecinos = 0.0
            for i in range(len(ruta)):
                for j in range(i + 1, len(ruta)):
                    similitud, misma_saga = self.parecido(ruta[i], ruta[j])
                    # Dos juegos de la misma saga restan variedad aunque compartan pocos rasgos.
                    suma_pares += similitud + (0.5 if misma_saga else 0.0)
                    if j == i + 1:
                        suma_vecinos += similitud
            # La variedad considera todas las parejas; la continuidad, solo los vecinos.
            total_pares = len(ruta) * (len(ruta) - 1) / 2
            variedad = max(0.0, 1 - suma_pares / total_pares)
            continuidad = suma_vecinos / (len(ruta) - 1)
            if len(self.gustos_para_variedad) > 1:
                # La variedad también premia que la lista cubra varios intereses declarados.
                coincidencias = [self.familias[k] for k in ruta]
                cobertura = len(set().union(*coincidencias)) / len(self.gustos_para_variedad)
                distancia = 0.0
                for i, unos in enumerate(coincidencias):
                    for otros in coincidencias[i + 1:]:
                        union = unos | otros
                        if unos and otros:
                            distancia += len(unos ^ otros) / len(union)
                variedad = (variedad + cobertura + distancia / total_pares) / 3
        return MedidasDeRuta(afinidad, variedad, continuidad)

    def aptitud(self, ruta):
        # Devuelve la aptitud de una lista (la función que maximiza el evolutivo base).
        return self.medir(ruta).aptitud()

    def mutar(self, padre, dirigida, azar):
        # Produce una lista hija cambiando un solo gen del padre.

        # Con probabilidad PROBABILIDAD_DE_INTERCAMBIO intercambia dos
        # posiciones (cambia el orden). En otro caso sustituye un juego por
        # otro que no esté en la lista: uno de los preferidos si la mutación es
        # dirigida, o cualquiera de la reserva si no lo es.

        # Parámetros:
        #     padre (tuple[str]): lista válida.
        #     dirigida (bool): si la sustitución se restringe a los preferidos.
        #     azar (random.Random): generador de números aleatorios.

        # Devuelve:
        #     tuple[str]: lista válida de la misma longitud y sin repetidos.
        ruta = list(padre)
        hay_sustitutos = self.longitud < len(self.candidatos)
        intercambiar = self.longitud > 1 and (not hay_sustitutos or azar.random() < PROBABILIDAD_DE_INTERCAMBIO)
        if intercambiar:
            a, b = azar.sample(range(self.longitud), 2)
            ruta[a], ruta[b] = ruta[b], ruta[a]
        elif hay_sustitutos:
            opciones = self.preferidos if dirigida else self.candidatos
            if len(opciones) <= max(TAMANO_DE_PREFERIDOS, 2 * self.longitud):
                nuevo = azar.choice([clave for clave in opciones if clave not in padre])
            else:
                # Con más del doble de opciones que juegos en la lista, cada intento acierta al
                # menos la mitad de las veces; es más rápido que filtrar toda la reserva.
                nuevo = azar.choice(opciones)
                while nuevo in padre:
                    nuevo = azar.choice(opciones)
            posicion = azar.randrange(self.longitud)
            ruta[posicion] = nuevo
            # Si se perdería el único anunciado o publicado, conserva la lista del padre.
            if len(self.representantes) == 2:
                estado_anterior = self.catalogo.juegos[padre[posicion]].anunciado
                if not any(self.catalogo.juegos[k].anunciado == estado_anterior for k in ruta):
                    return padre
        return tuple(ruta)

    def poblacion_inicial(self, cantidad, azar):
        # Crea la población inicial del evolutivo base.

        # Parámetros:
        #     cantidad (int): individuos (entero positivo).
        #     azar (random.Random): generador de números aleatorios.

        # Devuelve:
        #     list[tuple[str]]: una ruta por afinidad, otra por gustos si hay varios y el resto al azar.
        iniciales = [self.combinar_lanzamientos(self.candidatos[:self.longitud])]
        if cantidad > 1 and (len(self.gustos_para_variedad) > 1 or len(self.parecidos_a_favoritos) > 1):
            iniciales.append(self.ruta_por_gustos())
        for _ in range(cantidad - len(iniciales)):
            iniciales.append(self.combinar_lanzamientos(azar.sample(self.candidatos, self.longitud)))
        return iniciales


def evolucionar_ruta(problema, configuracion, semilla, presupuesto=PRESUPUESTO_DE_BUSQUEDA):
    # Ejecuta el evolutivo base sobre un problema de lista.

    # Parámetros:
    #     problema (ProblemaDeRuta): problema con al menos un candidato.
    #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida) válida.
    #     semilla (int): semilla de los números aleatorios.
    #     presupuesto (int): evaluaciones permitidas; al menos la población.

    # Devuelve:
    #     ResultadoEvolutivo: la mejor lista y las medidas de la ejecución.
    azar = random.Random(semilla)
    if len(problema.candidatos) == 1:
        # Con un solo candidato no hay nada que evolucionar.
        ruta = tuple(problema.candidatos)
        aptitud = problema.aptitud(ruta)
        resultado = ResultadoEvolutivo(ruta, aptitud, [(0, 1, aptitud)], 0, 1, 0.0)
    else:
        algoritmo = AlgoritmoEvolutivo(configuracion, problema.aptitud, problema.mutar, presupuesto, azar)
        resultado = algoritmo.ejecutar(problema.poblacion_inicial(configuracion[0], azar))
    return resultado


# ----------------------------------------------------------------------
# Meta-evolutivo: un algoritmo evolutivo que diseña al evolutivo base.
# ----------------------------------------------------------------------

class EscenarioDeAjuste:
    # Problema típico con un jugador simulado cuyos gustos se conocen.

    # Atributos:
    #     problema (ProblemaDeRuta): problema construido con el perfil que el
    #         recomendador aprendió del jugador simulado.
    #     gusto_oculto (dict[str, float]): interés verdadero del jugador en
    #         cada candidato; el recomendador no lo ve y solo sirve para medir.
    #     semillas (list[int]): una semilla por cada ejecución repetida.
    #     aptitud_inicial (float): aptitud de la lista voraz (los juegos de
    #         mayor afinidad), que siempre está en la población inicial.
    #     aptitud_de_referencia (float): mejor aptitud conocida, obtenida con
    #         ejecuciones diez veces más largas.

    def __init__(self, problema, gusto_oculto, semillas, aptitud_inicial, aptitud_de_referencia):
        # Guarda los datos del escenario (ver los atributos de la clase).
        self.problema = problema
        self.gusto_oculto = gusto_oculto
        self.semillas = semillas
        self.aptitud_inicial = aptitud_inicial
        self.aptitud_de_referencia = aptitud_de_referencia

    def calidad(self, aptitud):
        # Convierte la aptitud de una lista en la fracción de la mejora posible.

        # Parámetros:
        #     aptitud (float): aptitud de la mejor lista de una ejecución.

        # Devuelve:
        #     float: 0 si la ejecución no mejoró la lista voraz, 1 si alcanzó
        #     la mejor aptitud conocida; se limita a [0, 1].
        mejora_posible = self.aptitud_de_referencia - self.aptitud_inicial
        fraccion = 1.0
        if mejora_posible > 1e-12:
            fraccion = (aptitud - self.aptitud_inicial) / mejora_posible
        return min(1.0, max(0.0, fraccion))

    def objetivo(self):
        # Devuelve la aptitud que representa el OBJETIVO_DE_CONVERGENCIA de la mejora posible.
        mejora_posible = self.aptitud_de_referencia - self.aptitud_inicial
        return self.aptitud_inicial + OBJETIVO_DE_CONVERGENCIA * mejora_posible


def generar_escenarios(catalogo, disponibles, longitud, cantidad, repeticiones, semilla):
    # Crea jugadores simulados para medir configuraciones del evolutivo base.

    # Cada jugador prefiere dos géneros frecuentes. Su interés oculto en un
    # juego es mayor si el juego tiene uno de esos géneros y si su nota
    # pública es buena. El jugador declara solo uno de los dos géneros en el
    # cuestionario y valora 14 juegos con «me interesa» o «no me interesa»,
    # igual que una persona real en la consola; el recomendador aprende el
    # perfil con esa información incompleta.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     disponibles (list[str]): claves recomendables (al menos longitud + 1).
    #     longitud (int): juegos por lista.
    #     cantidad (int): jugadores simulados.
    #     repeticiones (int): ejecuciones por jugador.
    #     semilla (int): semilla que hace reproducibles los escenarios.

    # Devuelve:
    #     list[EscenarioDeAjuste]: cantidad escenarios.
    origen = random.Random(semilla)
    escenarios = []
    for _ in range(cantidad):
        azar = random.Random(origen.getrandbits(64))
        muestra = azar.sample(disponibles, min(514, len(disponibles)))
        total_observados = min(14, max(0, len(muestra) - longitud))
        observados = muestra[:total_observados]
        candidatos = muestra[total_observados:]

        # Gustos ocultos: dos géneros frecuentes en la muestra.
        frecuencias = Counter()
        for clave in muestra:
            for genero in catalogo.juegos[clave].generos:
                frecuencias[normalizar(genero)] += 1
        frecuentes = sorted(g for g, n in frecuencias.items() if n >= min(6, len(muestra)))
        preferidos = sorted(azar.sample(frecuentes, min(2, len(frecuentes))))
        gustos = {}
        for clave in muestra:
            juego = catalogo.juegos[clave]
            coincide = any(normalizar(g) in preferidos for g in juego.generos)
            ventaja = 0.45 if coincide else 0.0
            gustos[clave] = 0.12 + ventaja + 0.22 * juego.calidad_publica + azar.uniform(0, 0.12)

        # Lo que ve el recomendador: un género declarado y las valoraciones de los juegos observados.
        # Cuanto mayor es el gusto oculto, más probable es que el jugador marque «me interesa».
        declarados = Preferencias()
        declarados.generos = preferidos[:1]
        declarados.respondido = True
        actividad = {}
        for clave in observados:
            uso = ActividadDeJuego()
            uso.valoracion = 1 if azar.random() < gustos[clave] else -1
            actividad[clave] = uso
        en_la_muestra = set(muestra)
        fondo = [clave for clave in disponibles if clave not in en_la_muestra]
        perfil = aprender_perfil(catalogo, actividad, declarados, fondo, semilla)
        problema = ProblemaDeRuta(catalogo, candidatos, longitud, perfil)
        semillas = [azar.getrandbits(64) for _ in range(repeticiones)]

        # Límites de la calidad: la lista voraz y la mejor lista de tres búsquedas largas.
        inicial = problema.aptitud(problema.combinar_lanzamientos(problema.candidatos[:problema.longitud]))
        referencia = inicial
        for _ in range(3):
            larga = evolucionar_ruta(problema, AJUSTE_INICIAL, azar.getrandbits(64), 10 * PRESUPUESTO_DE_BUSQUEDA)
            referencia = max(referencia, larga.aptitud)
        gusto_oculto = {clave: gustos[clave] for clave in problema.candidatos}
        escenarios.append(EscenarioDeAjuste(problema, gusto_oculto, semillas, inicial, referencia))
    return escenarios


class DesempenoEvolutivo:
    # Medidas medias de un algoritmo evolutivo sobre varias ejecuciones.

    # Atributos:
    #     calidad (float): fracción media de la mejora posible que logran las
    #         soluciones, en [0, 1].
    #     convergencia (float): generación media en que cada ejecución alcanzó
    #         el OBJETIVO_DE_CONVERGENCIA; una ejecución que no lo alcanza
    #         cuenta todas sus generaciones. Es la medida de eficiencia que
    #         pide el enunciado.
    #     rapidez (float): media de 1 - evaluaciones hasta el objetivo /
    #         evaluaciones totales, en [0, 1]; vale 0 si no se alcanzó. Usa
    #         evaluaciones porque, con el mismo presupuesto, una configuración
    #         con menos descendientes tiene más generaciones.
    #     diversidad (float): diversidad genética media, en [0, 1].
    #     ejecuciones (int): cantidad de ejecuciones promediadas.
    #     interes (float): interés oculto medio de los jugadores simulados en
    #         las listas encontradas; solo se informa, no entra en la aptitud.

    def __init__(self, calidad, convergencia, rapidez, diversidad, ejecuciones, interes):
        # Guarda las medidas medias (ver los atributos de la clase).
        self.calidad = calidad
        self.convergencia = convergencia
        self.rapidez = rapidez
        self.diversidad = diversidad
        self.ejecuciones = ejecuciones
        self.interes = interes

    def aptitud(self):
        # Devuelve 0.70 calidad + 0.15 rapidez + 0.15 diversidad.

        # Los tres criterios del enunciado están en [0, 1]. La calidad pesa
        # más; la rapidez premia converger pronto y la diversidad premia
        # explorar. Sin la calidad normalizada, la diversidad dominaría,
        # porque varía cien veces más que la aptitud bruta de las listas.
        return 0.70 * self.calidad + 0.15 * self.rapidez + 0.15 * self.diversidad


def resumir_ejecuciones(resultados, calidades, objetivos, intereses):
    # Promedia las medidas de varias ejecuciones.

    # Parámetros:
    #     resultados (list[ResultadoEvolutivo]): al menos una ejecución.
    #     calidades (list[float]): calidad de la solución de cada ejecución.
    #     objetivos (list[float]): aptitud de convergencia de cada ejecución.
    #     intereses (list[float]): interés oculto de cada solución; puede estar
    #         vacía si no se conoce.

    # Devuelve:
    #     DesempenoEvolutivo: medias de las medidas.
    generaciones = []
    rapideces = []
    for resultado, objetivo in zip(resultados, objetivos):
        generacion, evaluacion = resultado.momento_de_convergencia(objetivo)
        generaciones.append(generacion)
        rapideces.append(1 - evaluacion / resultado.evaluaciones)
    interes = statistics.mean(intereses) if intereses else 0.0
    return DesempenoEvolutivo(statistics.mean(calidades), statistics.mean(generaciones),
                              statistics.mean(rapideces),
                              statistics.mean(r.diversidad for r in resultados),
                              len(resultados), interes)


def medir_configuracion(configuracion, escenarios):
    # Mide una configuración del evolutivo base con todas las ejecuciones.

    # Parámetros:
    #     configuracion (tuple): configuración válida del evolutivo base.
    #     escenarios (list[EscenarioDeAjuste]): escenarios con sus semillas;
    #         en total, EJECUCIONES_POR_CONFIGURACION ejecuciones.

    # Devuelve:
    #     DesempenoEvolutivo: medias de las ejecuciones. La calidad de cada
    #     ejecución es la fracción de la mejora posible que logró
    #     (EscenarioDeAjuste.calidad).
    resultados = []
    calidades = []
    objetivos = []
    intereses = []
    for escenario in escenarios:
        for semilla in escenario.semillas:
            resultado = evolucionar_ruta(escenario.problema, configuracion, semilla)
            resultados.append(resultado)
            calidades.append(escenario.calidad(resultado.aptitud))
            objetivos.append(escenario.objetivo())
            intereses.append(statistics.mean(escenario.gusto_oculto[clave] for clave in resultado.mejor))
    return resumir_ejecuciones(resultados, calidades, objetivos, intereses)


class EvaluadorDeConfiguraciones:
    # Función de aptitud del meta-evolutivo, con memoria de resultados.

    # Como los escenarios y las semillas son fijos, medir dos veces la misma
    # configuración da el mismo resultado; la memoria evita repetir el trabajo.

    # Atributos:
    #     escenarios (list[EscenarioDeAjuste]): problemas típicos.
    #     desempenos (dict): configuración (tupla) → DesempenoEvolutivo medido.
    #     avisar_cada (int): cada cuántas configuraciones nuevas se informa del
    #         avance; 0 no informa.

    def __init__(self, escenarios, avisar_cada=0):
        # Guarda los escenarios y prepara la memoria vacía.
        self.escenarios = escenarios
        self.desempenos = {}
        self.avisar_cada = avisar_cada

    def desempeno(self, configuracion):
        # Devuelve el DesempenoEvolutivo de una configuración válida (tupla).
        if configuracion not in self.desempenos:
            self.desempenos[configuracion] = medir_configuracion(configuracion, self.escenarios)
            if self.avisar_cada > 0 and len(self.desempenos) % self.avisar_cada == 0:
                print(f"  {len(self.desempenos)} configuraciones medidas…", flush=True)
        return self.desempenos[configuracion]

    def aptitud(self, configuracion):
        # Devuelve la aptitud (float) de una configuración válida.
        return self.desempeno(configuracion).aptitud()


def configuraciones_posibles(presupuesto=PRESUPUESTO_DE_BUSQUEDA):
    # Enumera el dominio completo del ajuste.

    # Parámetros:
    #     presupuesto (int): evaluaciones con las que se ejecutarán.

    # Devuelve:
    #     list[tuple]: todas las combinaciones válidas de VALORES_DE_AJUSTE.
    posibles = []
    for poblacion in VALORES_DE_AJUSTE[0]:
        for descendientes in VALORES_DE_AJUSTE[1]:
            for torneo in VALORES_DE_AJUSTE[2]:
                for dirigida in VALORES_DE_AJUSTE[3]:
                    configuracion = (poblacion, descendientes, torneo, dirigida)
                    if configuracion_valida(configuracion, presupuesto):
                        posibles.append(configuracion)
    return posibles


def vecinas_de_configuracion(padre, dirigida):
    # Lista las configuraciones que se obtienen cambiando un solo gen.

    # Parámetros:
    #     padre (tuple): configuración del dominio.
    #     dirigida (bool): True solo acepta el valor anterior o el siguiente
    #         del gen en su lista de VALORES_DE_AJUSTE; False acepta cualquier
    #         otro valor.

    # Devuelve:
    #     list[tuple]: vecinas válidas; si la mutación dirigida no tiene
    #     vecinas válidas, devuelve las de la no dirigida.
    cercanas = []
    todas = []
    for gen in range(len(padre)):
        valores = VALORES_DE_AJUSTE[gen]
        actual = valores.index(padre[gen])
        for posicion in range(len(valores)):
            vecina = list(padre)
            vecina[gen] = valores[posicion]
            vecina = tuple(vecina)
            if posicion != actual and configuracion_valida(vecina):
                todas.append(vecina)
                if abs(posicion - actual) == 1:
                    cercanas.append(vecina)
    elegidas = todas
    if dirigida and cercanas:
        elegidas = cercanas
    return elegidas


def mutar_configuracion(padre, dirigida, azar):
    # Operador de mutación del meta-evolutivo.

    # Parámetros:
    #     padre (tuple): configuración del dominio.
    #     dirigida (bool): si el cambio es a un valor vecino.
    #     azar (random.Random): generador de números aleatorios.

    # Devuelve:
    #     tuple: hija válida que difiere del padre en un gen.
    return azar.choice(vecinas_de_configuracion(padre, dirigida))


def ajustar_parametros(evaluador, configuracion_meta, semilla, presupuesto=PRESUPUESTO_DEL_META):
    # Ejecuta el meta-evolutivo para elegir los parámetros del evolutivo base.

    # La población inicial incluye el ajuste manual (AJUSTE_INICIAL), de
    # modo que el resultado nunca es peor que él.

    # Parámetros:
    #     evaluador (EvaluadorDeConfiguraciones): función de aptitud con memoria.
    #     configuracion_meta (tuple): parámetros del propio meta-evolutivo; su
    #         población debe caber en el presupuesto.
    #     semilla (int): semilla de los números aleatorios.
    #     presupuesto (int): configuraciones que se pueden evaluar.

    # Devuelve:
    #     ResultadoEvolutivo: la mejor configuración y las medidas de la búsqueda.
    azar = random.Random(semilla)
    posibles = [c for c in configuraciones_posibles() if c != AJUSTE_INICIAL]
    iniciales = [AJUSTE_INICIAL] + azar.sample(posibles, configuracion_meta[0] - 1)
    algoritmo = AlgoritmoEvolutivo(configuracion_meta, evaluador.aptitud, mutar_configuracion, presupuesto, azar)
    return algoritmo.ejecutar(iniciales)


def escenarios_tipicos(catalogo, longitud, semilla):
    # Crea los escenarios estándar del ajuste: 5 jugadores × 10 ejecuciones.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     longitud (int): juegos por lista.
    #     semilla (int): semilla base del programa.

    # Devuelve:
    #     list[EscenarioDeAjuste]: escenarios con EJECUCIONES_POR_CONFIGURACION
    #     ejecuciones en total.
    repeticiones = max(1, EJECUCIONES_POR_CONFIGURACION // ESCENARIOS_DE_AJUSTE)
    return generar_escenarios(catalogo, catalogo.claves_recomendables, longitud,
                              ESCENARIOS_DE_AJUSTE, repeticiones, semilla + 1000)


def firma_del_ajuste(catalogo, longitud, semilla):
    # Identifica las condiciones de un ajuste guardado.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     longitud (int): juegos por lista.
    #     semilla (int): semilla base del programa.

    # Devuelve:
    #     str: texto JSON con la versión, la longitud, la semilla y el tamaño
    #     y la fecha de cada archivo de datos. Si algo cambia, se ajusta de nuevo.
    archivos = []
    for ruta in catalogo.fuentes:
        datos = ruta.stat()
        archivos.append([str(ruta.resolve()), datos.st_size, datos.st_mtime_ns])
    anuncios = sorted(k for k in catalogo.claves_recomendables if catalogo.juegos[k].anunciado)
    return json.dumps([VERSION_DEL_AJUSTE, ANIO_DESDE, longitud, semilla, archivos, anuncios], ensure_ascii=False)


def parametros_para_recomendar(conexion, catalogo, longitud, semilla):
    # Recupera los parámetros ajustados o ejecuta el meta-evolutivo.

    # Parámetros:
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     longitud (int): juegos por lista.
    #     semilla (int): semilla base del programa.

    # Devuelve:
    #     tuple: (poblacion, descendientes, torneo, dirigida) válida para el
    #     evolutivo base.
    clave = firma_del_ajuste(catalogo, longitud, semilla)
    fila = conexion.execute("SELECT parametros FROM configuraciones WHERE clave=?", (clave,)).fetchone()
    if fila is None:
        print("Ajustando el evolutivo con el meta-evolutivo (solo la primera vez con esta longitud)…", flush=True)
        evaluador = EvaluadorDeConfiguraciones(escenarios_tipicos(catalogo, longitud, semilla), avisar_cada=10)
        parametros = ajustar_parametros(evaluador, CONFIGURACION_DEL_META, semilla + 2000).mejor
        desempeno = evaluador.desempeno(parametros)
        poblacion, descendientes, torneo, dirigida = parametros
        print(f"Parámetros elegidos: población {poblacion}, {descendientes} descendientes, "
              f"torneo de {torneo}, mutación dirigida {dirigida:.0%}. "
              f"En {desempeno.ejecuciones} ejecuciones logra el {desempeno.calidad:.0%} de la mejora posible, "
              f"llega al {OBJETIVO_DE_CONVERGENCIA:.0%} en la generación {desempeno.convergencia:.1f} "
              f"y su diversidad genética es {desempeno.diversidad:.3f}.")
        conexion.execute("INSERT OR REPLACE INTO configuraciones VALUES (?, ?)",
                         (clave, json.dumps(list(parametros))))
        conexion.commit()
    else:
        parametros = tuple(json.loads(fila[0]))
        if not configuracion_valida(parametros):
            parametros = AJUSTE_INICIAL
    return parametros


# ----------------------------------------------------------------------
# Conversación con la persona: cuestionario y valoraciones.
# ----------------------------------------------------------------------

class Consola:
    # Lee las respuestas de la persona.

    # Atributos:
    #     cerrada (bool): True si no se debe preguntar nada, porque se pidió
    #         --sin-preguntas o porque la entrada terminó. Entonces cada
    #         pregunta devuelve una cadena vacía, que significa «omitir».

    def __init__(self, interactiva=True):
        # Parámetros:
        # interactiva (bool): False desactiva todas las preguntas.
        self.cerrada = not interactiva

    def preguntar(self, mensaje):
        # Muestra una pregunta y lee una línea.

        # Parámetros:
        #     mensaje (str): texto de la pregunta.

        # Devuelve:
        #     str: la respuesta sin espacios en los extremos; cadena vacía si
        #     la consola está cerrada.
        respuesta = ""
        if not self.cerrada:
            try:
                respuesta = input(mensaje).strip()
            except EOFError:
                self.cerrada = True
                print()
        return respuesta

    def confirmar(self, mensaje):
        # Hace una pregunta de sí o no.

        # Devuelve:
        #     bool: True si la respuesta empieza con «s».
        return normalizar(self.preguntar(mensaje)).startswith("s")


def mostrar_opciones(opciones, columnas=4):
    # Imprime una lista numerada en columnas.

    # Parámetros:
    #     opciones (list[str]): textos que se numeran desde 1.
    #     columnas (int): opciones por renglón (entero positivo).
    celdas = [f"{i:>3}) {texto:<20}" for i, texto in enumerate(opciones, 1)]
    for inicio in range(0, len(celdas), columnas):
        print("".join(celdas[inicio:inicio + columnas]).rstrip())


def interpretar_lista(texto, opciones):
    # Interpreta una respuesta con números o nombres separados por comas.

    # Parámetros:
    #     texto (str): por ejemplo "1, 3 12, terror".
    #     opciones (list[str]): opciones numeradas desde 1.

    # Devuelve:
    #     tuple: (elegidas, desconocidas). elegidas son las opciones
    #     reconocidas, sin repetir y en el orden escrito; desconocidas son los
    #     fragmentos que no corresponden a ninguna opción.
    por_nombre = {normalizar(opcion): opcion for opcion in opciones}
    reconocidas = []
    desconocidas = []
    for parte in texto.split(","):
        palabras = parte.split()
        if palabras and all(p.isdigit() for p in palabras):
            # Una parte con solo números puede traer varios separados por espacios.
            for palabra in palabras:
                indice = int(palabra)
                if 1 <= indice <= len(opciones):
                    reconocidas.append(opciones[indice - 1])
                else:
                    desconocidas.append(palabra)
        elif palabras:
            nombre = por_nombre.get(normalizar(parte))
            if nombre:
                reconocidas.append(nombre)
            else:
                desconocidas.append(parte.strip())
    # Si una opción se escribió dos veces, se conserva solo la primera.
    elegidas = []
    for opcion in reconocidas:
        if opcion not in elegidas:
            elegidas.append(opcion)
    return elegidas, desconocidas


def elegir_generos(consola, opciones, mensaje):
    # Pregunta una lista de géneros hasta recibir una respuesta válida.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     opciones (list[str]): géneros numerados desde 1.
    #     mensaje (str): pregunta.

    # Devuelve:
    #     list[str]: géneros elegidos; lista vacía si la persona pulsa Enter.
    elegidos = []
    pendiente = True
    while pendiente:
        respuesta = consola.preguntar(mensaje)
        elegidos, desconocidos = interpretar_lista(respuesta, opciones)
        if desconocidos:
            print(f"   No reconocí: {', '.join(desconocidos)}. Usa los números de la lista o los nombres.")
        pendiente = bool(desconocidos)
    return elegidos


def elegir_titulo(consola, catalogo, texto):
    # Busca un título y deja que la persona elija el correcto.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     texto (str): parte del título escrita por la persona.

    # Devuelve:
    #     str o None: la clave elegida; None si no hubo resultados o la
    #     persona eligió «ninguno».
    claves = catalogo.buscar_titulos(texto)
    elegida = None
    if not claves:
        print("   No encontré ese juego. Prueba con otra parte del título.")
    elif len(claves) == 1:
        elegida = claves[0]
    else:
        for indice, clave in enumerate(claves, 1):
            print(f"     {indice}) {catalogo.describir(clave)}")
        print("     0) Ninguno de estos")
        respuesta = consola.preguntar("   ¿Cuál es? ")
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(claves):
            elegida = claves[int(respuesta) - 1]
    return elegida


def elegir_juegos(consola, catalogo):
    # Pregunta los juegos favoritos, uno por renglón.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.

    # Devuelve:
    #     list[str]: hasta MAXIMO_DE_FAVORITOS claves distintas.
    print(f"3. Escribe juegos que ya jugaste y te gustaron, uno por renglón (hasta {MAXIMO_DE_FAVORITOS}). "
          "Enter para terminar.")
    favoritos = []
    seguir = True
    while seguir and len(favoritos) < MAXIMO_DE_FAVORITOS:
        texto = consola.preguntar("   Juego: ")
        seguir = bool(texto)
        if seguir:
            clave = elegir_titulo(consola, catalogo, texto)
            if clave and clave not in favoritos:
                favoritos.append(clave)
                print(f"   Añadido: {catalogo.describir(clave)}")
    return favoritos


def elegir_plataforma(consola, catalogo):
    # Pregunta la plataforma preferida hasta reconocerla o recibir Enter.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.

    # Devuelve:
    #     str: nombre visible de la plataforma; cadena vacía si le da igual.
    comunes = "PC, Mac, PS2, PS3, PS4, PS5, Xbox, Nintendo; también puedes escribir el modelo exacto"
    plataforma = ""
    pendiente = True
    while pendiente:
        respuesta = consola.preguntar(f"4. ¿En qué plataforma juegas? ({comunes}; Enter si te da igual): ")
        plataforma = catalogo.buscar_plataforma(respuesta) or ""
        pendiente = bool(respuesta) and not plataforma
        if pendiente:
            print(f"   No conozco «{respuesta}». Escribe una de estas: {comunes}.")
    return plataforma


def aplicar_cuestionario(consola, catalogo):
    # Hace el cuestionario inicial de gustos.

    # Exige al menos un género favorito o un juego, para que la primera lista
    # ya sea personal y no una clasificación por popularidad.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.

    # Devuelve:
    #     Preferencias: respuestas; respondido es False si la entrada terminó
    #     sin datos suficientes.
    print("\nCuéntame qué te gusta. Solo te lo preguntaré esta vez; después aprenderé de tus valoraciones.")
    opciones = catalogo.generos_del_cuestionario()
    preferencias = Preferencias()
    suficiente = False
    while not suficiente and not consola.cerrada:
        mostrar_opciones(opciones)
        preferencias.generos = elegir_generos(
            consola, opciones, "1. ¿Qué géneros te gustan? Escríbelos en cualquier orden, separados por comas: ")
        evitados = elegir_generos(
            consola, opciones, "2. ¿Hay géneros que prefieras evitar? (Enter para omitir): ")
        repetidos = [g for g in evitados if g in preferencias.generos]
        if repetidos:
            print(f"   {', '.join(repetidos)} ya está entre tus favoritos; no lo evitaré.")
        preferencias.evitados = [g for g in evitados if g not in preferencias.generos]
        preferencias.favoritos = elegir_juegos(consola, catalogo)
        suficiente = bool(preferencias.generos or preferencias.favoritos)
        if not suficiente and not consola.cerrada:
            print("Necesito al menos un género o un juego para no recomendarte solo por popularidad. "
                  "Intentémoslo otra vez.\n")
    if suficiente:
        preferencias.plataforma = elegir_plataforma(consola, catalogo)
    preferencias.respondido = suficiente
    return preferencias


def describir_preferencias(catalogo, preferencias):
    # Resume en una línea las respuestas guardadas.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     preferencias (Preferencias): respuestas del cuestionario.

    # Devuelve:
    #     str: por ejemplo "te gusta Terror, Rol · favoritos: Silent Hill 2 · plataforma PS2".
    partes = []
    if preferencias.generos:
        partes.append("géneros que te gustan: " + ", ".join(sorted(preferencias.generos)))
    if preferencias.evitados:
        partes.append("evitas " + ", ".join(preferencias.evitados))
    if preferencias.favoritos:
        titulos = []
        for clave in preferencias.favoritos:
            disponible = catalogo.resolver_titulo(clave)
            if disponible:
                titulos.append(catalogo.juegos[disponible].titulo)
        if titulos:
            partes.append("favoritos: " + ", ".join(titulos))
    if preferencias.plataforma:
        partes.append(f"plataforma {preferencias.plataforma}")
    else:
        partes.append("cualquier plataforma")
    return " · ".join(partes)


def preparar_preferencias(consola, conexion, catalogo, cambiar):
    # Obtiene los gustos: los guardados o los de un cuestionario nuevo.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     cambiar (bool): True repite el cuestionario sin preguntar antes.

    # Devuelve:
    #     Preferencias: las respuestas vigentes, ya guardadas en el perfil.
    preferencias = leer_preferencias(conexion)
    if preferencias.respondido and not cambiar and not consola.cerrada:
        print(f"\nTus gustos guardados: {describir_preferencias(catalogo, preferencias)}.")
        respuesta = consola.preguntar("Pulsa Enter para continuar o escribe C para cambiarlos: ")
        cambiar = normalizar(respuesta) in ("c", "cambiar")
    if (cambiar or not preferencias.respondido) and not consola.cerrada:
        nuevas = aplicar_cuestionario(consola, catalogo)
        if nuevas.respondido:
            guardar_preferencias(conexion, nuevas)
            preferencias = nuevas
    return preferencias


def nombrar_atributo(juego, atributo):
    # Devuelve el nombre visible de un atributo para explicar una recomendación.

    # Parámetros:
    #     juego (FichaDeJuego): ficha que contiene el atributo.
    #     atributo (tuple): par (tipo, valor normalizado).

    # Devuelve:
    #     str: por ejemplo "Terror", "atmosférico" o "estudio Konami".
    tipo, valor = atributo
    nombre = valor
    if tipo == "genero":
        for genero in juego.generos:
            if normalizar(genero) == valor:
                nombre = genero
    elif tipo == "tema" and valor == juego.saga:
        nombre = f"saga {valor.title()}"
    elif tipo == "tema":
        if valor in NOMBRES_DE_ETIQUETA:
            nombre = NOMBRES_DE_ETIQUETA[valor]
        elif valor in ETIQUETAS_DE_GENERO:
            # Una etiqueta que equivale a un género se muestra con el nombre del género.
            nombre = ETIQUETAS_DE_GENERO[valor][-1]
    else:
        nombre = f"{tipo} {valor.title()}"
    return nombre


def mostrar_recomendaciones(problema, resultado, perfil, numero_de_lista):
    # Imprime la lista recomendada con una razón breve por juego.

    # Parámetros:
    #     problema (ProblemaDeRuta): problema resuelto.
    #     resultado (ResultadoEvolutivo): resultado del evolutivo base.
    #     perfil (PerfilDeGustos): perfil aprendido.
    #     numero_de_lista (int): número de la lista en esta sesión (desde 1).
    cantidad = len(resultado.mejor)
    palabra = "juego" if cantidad == 1 else "juegos"
    print(f"\nTus recomendaciones · lista {numero_de_lista} ({cantidad} {palabra})")
    frecuencias = problema.catalogo.frecuencia_de_atributos
    total = len(problema.catalogo.claves_recomendables)

    def relevancia(rasgo):
        aprendido = perfil.pesos.get(rasgo, 0.0)
        if perfil.con_historial and perfil.generos_declarados:
            aprendido *= PESO_DEL_HISTORIAL
            if rasgo in perfil.generos_declarados:
                aprendido += (1 - PESO_DEL_HISTORIAL) * PESO_PREVIO_GUSTA
        return aprendido * PESO_POR_TIPO[rasgo[0]] * math.log1p(total / (1 + frecuencias[rasgo]))

    anterior = None
    for posicion, clave in enumerate(resultado.mejor, 1):
        ficha = problema.catalogo.juegos[clave]
        fuentes = [nombre for nombre, presente in (("Steam", ficha.en_steam), ("ventas", ficha.con_ventas)) if presente]
        print(f"{posicion}. {problema.catalogo.describir(clave)} · Catálogo: {' y '.join(fuentes)}")
        # Razón principal: el género y el otro rasgo más relevantes. La relevancia multiplica el peso
        # en el perfil por la rareza del rasgo, para no explicar con rasgos casi universales.
        positivos = [r for r in ficha.atributos if perfil.pesos.get(r, 0.0) > 0.05 or r in perfil.generos_declarados]
        positivos = sorted((r for r in positivos if relevancia(r) > 0), key=lambda r: (-relevancia(r), r))
        generos = [r for r in positivos if r[0] == "genero"]
        otros = [r for r in positivos if r[0] != "genero"]
        if generos and otros:
            elegidos = [generos[0], otros[0]]
        else:
            elegidos = positivos[:2]
        motivos = []
        for rasgo in elegidos:
            nombre = nombrar_atributo(ficha, rasgo)
            if nombre not in motivos:
                motivos.append(nombre)
        if motivos:
            print(f"   Coincide con tu perfil: {', '.join(motivos)}.")
        else:
            print("   Aporta variedad a la lista.")
        if perfil.favoritos:
            parecido = problema.parecidos_a_favoritos
            favorito = max(perfil.favoritos, key=lambda k: parecido[k][clave])
            compartidos = rasgos_para_comparar(ficha) & perfil.favoritos[favorito]
            if compartidos:
                rasgo = min(compartidos, key=lambda r: (frecuencias[r], r))
                titulo = problema.catalogo.juegos[favorito].titulo
                print(f"   Comparte «{nombrar_atributo(ficha, rasgo)}» con tu favorito {titulo}.")
        if ficha.evidencia_publica >= MINIMO_DE_RESENAS:
            print(f"   Se consideraron {int(ficha.evidencia_publica):,} reseñas del juego.")
        # Razón secundaria: el rasgo menos frecuente que comparte con el juego anterior.
        if anterior is not None:
            comunes = sorted(anterior.atributos & ficha.atributos, key=lambda r: (frecuencias[r], r))
            if comunes:
                print(f"   Comparte «{nombrar_atributo(ficha, comunes[0])}» con el juego anterior.")
        anterior = ficha


def interpretar_valoraciones(texto, cantidad):
    # Interpreta una respuesta como «1 3 -2».

    # Parámetros:
    #     texto (str): números separados por espacios o comas; el signo menos
    #         indica «no me interesa».
    #     cantidad (int): juegos de la lista.

    # Devuelve:
    #     tuple: (valoraciones, errores). valoraciones asocia cada posición
    #     (desde 1) con 1 o -1; errores son los fragmentos inválidos.
    valoraciones = {}
    errores = []
    for token in re.split(r"[\s,;]+", texto):
        coincide = re.fullmatch(r"([+-]?)(\d+)", token)
        if coincide and 1 <= int(coincide.group(2)) <= cantidad:
            valoraciones[int(coincide.group(2))] = -1 if coincide.group(1) == "-" else 1
        elif token:
            errores.append(token)
    return valoraciones, errores


def pedir_valoraciones(consola, conexion, ruta):
    # Pide y guarda las valoraciones de una lista recomendada.

    # Parámetros:
    #     consola (Consola): entrada de la persona.
    #     conexion (sqlite3.Connection): perfil con las tablas creadas.
    #     ruta (tuple[str]): claves de la lista mostrada.

    # Devuelve:
    #     bool: True si se guardó al menos una valoración; False si la
    #     persona omitió la valoración o la consola está cerrada.
    if not consola.cerrada:
        print("\n¿Qué te parecen? Escribe los números que te interesan y, con signo menos, los que no "
              "(por ejemplo: 1 3 -2). Enter para omitir.")
    valoraciones = {}
    pendiente = not consola.cerrada
    while pendiente:
        valoraciones, errores = interpretar_valoraciones(consola.preguntar("Tu valoración: "), len(ruta))
        if errores:
            print(f"   No entendí: {', '.join(errores)}. Usa números del 1 al {len(ruta)}.")
        pendiente = bool(errores)
    if valoraciones:
        guardar_valoraciones(conexion, {ruta[p - 1]: v for p, v in valoraciones.items()})
        interesan = sum(v > 0 for v in valoraciones.values())
        print(f"Guardé {interesan} «me interesa» y {len(valoraciones) - interesan} «no me interesa». "
              "Las próximas listas aprenderán de esto.")
    return bool(valoraciones)


# ----------------------------------------------------------------------
# Flujo de recomendación.
# ----------------------------------------------------------------------

def resolver_referencia(catalogo, texto):
    # Identifica el juego de referencia de esta ejecución.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     texto (str): título escrito por la persona; puede estar vacío.

    # Devuelve:
    #     str o None: la clave del juego; None si no se indicó o no se
    #     identificó (en ese caso muestra títulos parecidos).
    referencia = None
    if texto:
        referencia = catalogo.resolver_titulo(texto)
    if texto and referencia is None:
        print(f"No pude identificar un único juego con '{texto}'.")
        sugerencias = [catalogo.juegos[k].titulo for k in catalogo.buscar_titulos(texto, 3)]
        if sugerencias:
            print("Títulos parecidos: " + ", ".join(sugerencias) + ".")
    elif referencia:
        print(f"Juego de referencia para esta ejecución: {catalogo.juegos[referencia].titulo}.")
    return referencia


def plataforma_de_la_ejecucion(catalogo, opciones, preferencias):
    # Decide qué plataforma filtra esta ejecución.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     opciones (argparse.Namespace): la plataforma escrita en la terminal o
    #         en PLATAFORMA_PREFERIDA tiene prioridad.
    #     preferencias (Preferencias): plataforma del cuestionario.

    # Devuelve:
    #     str: nombre visible; cadena vacía para todas.

    # Errores:
    #     ValueError: si la plataforma de las opciones no existe.
    plataforma = catalogo.resolver_plataforma(opciones.plataforma) or ""
    if not plataforma and preferencias.plataforma:
        plataforma = catalogo.buscar_plataforma(preferencias.plataforma) or ""
        if not plataforma:
            print(f"La plataforma guardada ({preferencias.plataforma}) no está en este catálogo; "
                  "usaré todas.")
    return plataforma


def actualizar_resenas(catalogo, claves, perfil, longitud, conexion):
    # La tienda devuelve el número real de reseñas y el porcentaje positivo redondeado.
    ahora = int(time.time())
    guardadas = {a: (n, p) for a, n, p in conexion.execute(
        "SELECT appid, total, porcentaje FROM resumen_resenas WHERE fecha >= ?", (ahora - 7 * 86400,))}
    ordenadas = sorted(claves, key=lambda k: (-estimar_afinidad(catalogo.juegos[k], perfil), k))
    pendientes = [catalogo.juegos[k].appid for k in ordenadas if catalogo.juegos[k].appid
                  and catalogo.juegos[k].appid not in guardadas and not catalogo.juegos[k].anunciado]
    ids = pendientes[:max(12, 2 * longitud)]
    if ids:
        peticion = {"ids": [{"appid": int(a)} for a in ids],
                    "context": {"language": "english", "country_code": "US"},
                    "data_request": {"include_reviews": True}}
        url = "https://api.steampowered.com/IStoreBrowseService/GetItems/v1/?" + urlencode(
            {"input_json": json.dumps(peticion, separators=(",", ":"))})
        try:
            productos = consultar_tienda(url)["response"]["store_items"]
            for producto in productos:
                appid = str(producto.get("id", ""))
                resumen = producto.get("reviews", {}).get("summary_filtered", {})
                total, porcentaje = resumen.get("review_count"), resumen.get("percent_positive")
                if (appid in ids and type(total) is int and total >= 0 and type(porcentaje) is int
                        and 0 <= porcentaje <= 100):
                    guardadas[appid] = total, porcentaje
                    conexion.execute("INSERT OR REPLACE INTO resumen_resenas VALUES (?, ?, ?, ?)",
                                     (appid, total, porcentaje, ahora))
            conexion.commit()
        except (OSError, ValueError, HTTPException, AttributeError, KeyError, TypeError):
            print("Steam no devolvió el resumen de reseñas. Usaré los datos disponibles del catálogo.")
    for clave in claves:
        juego = catalogo.juegos[clave]
        if juego.appid in guardadas:
            total, porcentaje = guardadas[juego.appid]
            juego.evidencia_publica = total
            juego.calidad_publica = (total * porcentaje / 100 + 13) / (total + 20)


def candidatos_revisados(catalogo, candidatos, perfil, longitud, conexion):
    # Conservamos las revisiones durante 30 días para poder reutilizarlas incluso sin conexión.
    ahora = int(time.time())
    anteriores = dict(conexion.execute("SELECT appid, resultado FROM revision_steam WHERE fecha >= ?",
                                       (ahora - 30 * 86400,)))
    ordenados = sorted(candidatos, key=lambda k: (-estimar_afinidad(catalogo.juegos[k], perfil), k))
    admitidos = []
    pendientes = set()
    for clave in ordenados:
        juego = catalogo.juegos[clave]
        estado = anteriores.get(juego.appid, "")
        # Un juego que Steam ya marcó como no apto no se admite ni se vuelve a consultar.
        if estado != "excluir":
            if juego.contenido_revisado or estado == "revisado":
                admitidos.append(clave)
            elif juego.appid:
                pendientes.add(clave)

    # Revisamos primero los mejores candidatos de cada tipo para poder mezclar estrenos y anuncios.
    # Limitamos las consultas a la tienda. Los juegos sin datos suficientes se quedan fuera.
    por_revisar = []
    for anunciado in (False, True):
        grupo = [k for k in ordenados if catalogo.juegos[k].anunciado == anunciado
                 and (catalogo.juegos[k].appid or catalogo.juegos[k].contenido_revisado)
                 and anteriores.get(catalogo.juegos[k].appid) != "excluir"]
        cupo = max(12, 2 * longitud)
        variados = muestra_variada(catalogo, grupo, perfil, max(16, 3 * longitud))
        # Alternamos alta afinidad y combinaciones de gustos antes de consultar Steam.
        turnos = zip_longest(grupo[:cupo], variados)
        seleccion = dict.fromkeys(k for turno in turnos for k in turno if k is not None)
        por_revisar.extend(islice((k for k in seleccion if k in pendientes), max(16, 3 * longitud)))
    if por_revisar:
        print("Comprobando los avisos de contenido de Steam…", flush=True)
        with ThreadPoolExecutor(max_workers=4) as consultas:
            trabajos = {k: consultas.submit(producto_de_steam, catalogo.juegos[k].appid) for k in por_revisar}
            for clave, trabajo in trabajos.items():
                try:
                    estado = revisar_producto(trabajo.result())
                except (OSError, ValueError, HTTPException, KeyError, TypeError, AttributeError):
                    # Sin respuesta de Steam, el juego queda sin revisar y no se recomienda.
                    estado = ""
                if estado:
                    conexion.execute("INSERT OR REPLACE INTO revision_steam VALUES (?, ?, ?)",
                                     (catalogo.juegos[clave].appid, estado, ahora))
                if estado == "revisado":
                    admitidos.append(clave)
        conexion.commit()
    return admitidos


def recomendar_una_lista(catalogo, preferencias, actividad, vistos, plataforma, parametros, opciones,
                         numero_de_lista, conexion):
    # Aprende el perfil, evoluciona una lista y la muestra.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     preferencias (Preferencias): respuestas del cuestionario.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    #     vistos (set[str]): juegos ya mostrados en esta sesión; no se repiten.
    #     plataforma (str): filtro de plataforma; vacío acepta todas.
    #     parametros (tuple): (poblacion, descendientes, torneo, dirigida) del evolutivo base.
    #     opciones (argparse.Namespace): opciones de la ejecución.
    #     numero_de_lista (int): número de la lista en esta sesión.

    # Devuelve:
    #     tuple[str]: claves recomendadas; tupla vacía si no quedan candidatos.
    candidatos = catalogo.candidatos(plataforma, set(actividad) | vistos, preferencias.evitados)
    perfil = aprender_perfil(catalogo, actividad, preferencias, catalogo.claves_recomendables, opciones.semilla)
    candidatos = candidatos_revisados(catalogo, candidatos, perfil, opciones.longitud, conexion)
    if not candidatos and plataforma and plataforma not in ("PC", "Mac"):
        print(f"No hay estrenos verificables con tus filtros en {plataforma}. Buscando en su catálogo histórico…")
        historicos = catalogo.candidatos(plataforma, set(actividad) | vistos, preferencias.evitados, historicos=True)
        candidatos = candidatos_revisados(catalogo, historicos, perfil, opciones.longitud, conexion)
    ruta = ()
    if not candidatos:
        print("No quedan juegos con compatibilidad y contenido comprobados que cumplan tus filtros.")
    else:
        actualizar_resenas(catalogo, candidatos, perfil, opciones.longitud, conexion)
        problema = ProblemaDeRuta(catalogo, candidatos, opciones.longitud, perfil)
        resultado = evolucionar_ruta(problema, parametros, opciones.semilla + numero_de_lista)
        mostrar_recomendaciones(problema, resultado, perfil, numero_de_lista)
        ruta = resultado.mejor
    return ruta


def archivo_del_jugador(consola, opciones):
    # --perfil y las ejecuciones sin preguntas siguen usando el archivo indicado.
    if not opciones.elegir_jugador:
        return opciones.perfil
    apodo = consola.preguntar("¿Quién juega? Escribe tu apodo (Enter para el perfil de siempre): ").strip()
    if not apodo:
        return opciones.perfil
    # El apodo nunca se usa como ruta. Su clave estable admite acentos, espacios y símbolos.
    nombre = " ".join(unicodedata.normalize("NFKC", apodo).casefold().split())
    clave = hashlib.sha256(nombre.encode("utf-8")).hexdigest()
    carpeta = opciones.carpeta / "perfiles"
    carpeta.mkdir(exist_ok=True)
    print(f"Perfil de {apodo}.")
    return carpeta / (clave + ".sqlite3")


def recomendar(catalogo, opciones):
    # Sesión completa de recomendación.

    # Lee o pregunta los gustos, ajusta el evolutivo base si hace falta y muestra listas mientras la persona las valore y
    # pida otra.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     opciones (argparse.Namespace): opciones de la ejecución.
    consola = Consola(opciones.interactivo)
    conexion = sqlite3.connect(archivo_del_jugador(consola, opciones), timeout=10)
    # try/finally garantiza que el archivo del perfil se cierre aunque ocurra un error.
    try:
        crear_tablas(conexion)
        preferencias = preparar_preferencias(consola, conexion, catalogo, opciones.cambiar_gustos)
        if not opciones.plataforma and clave_de_plataforma(preferencias.plataforma) == "linux":
            print("Tu perfil guardaba Linux. Elige tu plataforma actual.")
            if consola.cerrada:
                print("Indícala con --plataforma o ejecuta el cuestionario.")
                return
            preferencias.plataforma = elegir_plataforma(consola, catalogo)
            guardar_preferencias(conexion, preferencias)
        referencia = resolver_referencia(catalogo, opciones.titulo)
        plataforma = plataforma_de_la_ejecucion(catalogo, opciones, preferencias)
        actividad = actividad_personal(conexion, catalogo, preferencias)
        if referencia:
            obtener_actividad(actividad, referencia).favorito = True

        if not hay_informacion_personal(preferencias, actividad):
            # Sin gustos no se recomienda: la lista sería solo una clasificación por popularidad.
            print("Todavía no conozco tus gustos. Ejecuta el programa con preguntas (HACER_PREGUNTAS = True) "
                  "o indica un juego de referencia.")
        else:
            parametros = (parametros_para_recomendar(conexion, catalogo, opciones.longitud, opciones.semilla)
                          if catalogo.claves_recomendables else AJUSTE_INICIAL)
            numero_de_lista = 1
            vistos = set()
            otra_lista = True
            # Cada vuelta recalcula el perfil con las valoraciones de la vuelta anterior.
            while otra_lista:
                ruta = recomendar_una_lista(catalogo, preferencias, actividad, vistos, plataforma,
                                            parametros, opciones, numero_de_lista, conexion)
                vistos.update(ruta)
                valoro = len(ruta) > 0 and pedir_valoraciones(consola, conexion, ruta)
                otra_lista = valoro and consola.confirmar("¿Quieres otra lista con lo que acabas de valorar? (S/N): ")
                if otra_lista:
                    numero_de_lista += 1
                    actividad = actividad_personal(conexion, catalogo, preferencias)
                    if referencia:
                        obtener_actividad(actividad, referencia).favorito = True
            print("\n¡Hasta la próxima! Tus gustos y valoraciones quedaron guardados.")
    finally:
        conexion.close()


# ----------------------------------------------------------------------
# Experimentos del reporte.
# ----------------------------------------------------------------------

def formato_de_configuracion(configuracion):
    # Devuelve una configuración (tupla) como texto breve, por ejemplo "(30, 18, 3, 0.45)".
    poblacion, descendientes, torneo, dirigida = configuracion
    return f"({poblacion}, {descendientes}, {torneo}, {dirigida:.2f})"


def imprimir_tabla(filas, desempenos, con_interes=True):
    # Imprime una tabla de configuraciones y sus medidas.

    # Parámetros:
    #     filas (list[tuple]): (nombre de la fila, configuración en tupla).
    #     desempenos (dict): configuración → DesempenoEvolutivo.
    #     con_interes (bool): si se muestra la columna del interés simulado.
    encabezado = (f"  {'Configuración':<36}{'(pob, desc, torneo, dirig)':<28}{'Calidad':>9}"
                  f"{'Conv. (gen)':>13}{'Rapidez':>9}{'Diversidad':>12}{'Aptitud':>9}")
    if con_interes:
        encabezado += f"{'Interés':>9}"
    print(encabezado)
    for nombre, configuracion in filas:
        d = desempenos[configuracion]
        renglon = (f"  {nombre:<36}{formato_de_configuracion(configuracion):<28}{d.calidad:>9.4f}"
                   f"{d.convergencia:>13.2f}{d.rapidez:>9.4f}{d.diversidad:>12.4f}{d.aptitud():>9.4f}")
        if con_interes:
            renglon += f"{d.interes:>9.4f}"
        print(renglon)


def repetir_meta(evaluador, configuracion_meta, repeticiones, semilla, peor, optima):
    # Ejecuta varias veces el meta-evolutivo con los mismos parámetros.

    # Parámetros:
    #     evaluador (EvaluadorDeConfiguraciones): aptitud con memoria; en los
    #         experimentos ya contiene todas las configuraciones medidas.
    #     configuracion_meta (tuple): parámetros del meta-evolutivo.
    #     repeticiones (int): ejecuciones (entero positivo).
    #     semilla (int): semilla base; cada ejecución usa semilla + i.
    #     peor, optima (float): aptitudes de la peor y la mejor configuración
    #         del paisaje completo; normalizan la calidad del meta.

    # Devuelve:
    #     tuple: (DesempenoEvolutivo del meta, lista de las mejores
    #     configuraciones encontradas en cada ejecución). La calidad de cada
    #     ejecución es (aptitud encontrada - peor) / (óptima - peor).
    resultados = [ajustar_parametros(evaluador, configuracion_meta, semilla + i) for i in range(repeticiones)]
    escala = optima - peor
    if escala <= 1e-12:
        escala = 1.0
    calidades = [(r.aptitud - peor) / escala for r in resultados]
    objetivo = peor + OBJETIVO_DE_CONVERGENCIA * escala
    desempeno = resumir_ejecuciones(resultados, calidades, [objetivo] * len(resultados), [])
    return desempeno, [r.mejor for r in resultados]


def ejecutar_experimentos(catalogo, opciones):
    # Ejecuta los tres experimentos del reporte y muestra sus tablas.

    # 1. Paisaje completo: mide con 50 ejecuciones todas las configuraciones
    #    válidas del evolutivo base y compara la óptima con el ajuste manual.
    # 2. Meta-evolutivo: lo ejecuta 50 veces con CONFIGURACION_DEL_META y
    #    cuenta cuántas veces encuentra la configuración óptima.
    # 3. Pregunta del enunciado: usa cada configuración válida como parámetros
    #    del meta-evolutivo (50 ejecuciones cada una) y compara la mejor para
    #    el meta con la mejor para el evolutivo base.

    # Parámetros:
    #     catalogo (CatalogoDeJuegos): catálogo cargado.
    #     opciones (argparse.Namespace): longitud y semilla de la ejecución.
    inicio = time.time()
    repeticiones = EJECUCIONES_POR_CONFIGURACION
    evaluador = EvaluadorDeConfiguraciones(escenarios_tipicos(catalogo, opciones.longitud, opciones.semilla),
                                           avisar_cada=25)
    posibles = configuraciones_posibles()

    print(f"\nExperimento 1. Paisaje completo del evolutivo base: {len(posibles)} configuraciones × "
          f"{repeticiones} ejecuciones (listas de {opciones.longitud} juegos, "
          f"{PRESUPUESTO_DE_BUSQUEDA} evaluaciones por ejecución).", flush=True)
    desempenos = {configuracion: evaluador.desempeno(configuracion) for configuracion in posibles}
    ordenadas = sorted(posibles, key=lambda c: (-desempenos[c].aptitud(), c))
    optima = ordenadas[0]
    posicion_manual = ordenadas.index(AJUSTE_INICIAL) + 1
    imprimir_tabla([("Óptima (búsqueda exhaustiva)", optima), ("Segunda", ordenadas[1]),
                    (f"Ajuste manual (lugar {posicion_manual})", AJUSTE_INICIAL),
                    ("Mediana", ordenadas[len(ordenadas) // 2]), ("Peor", ordenadas[-1])], desempenos)

    print(f"  Calidad: fracción de la mejora posible sobre la lista voraz. Conv. (gen): generación en que se "
          f"alcanza el {OBJETIVO_DE_CONVERGENCIA:.0%} de esa mejora.\n  Interés: gusto oculto medio del jugador "
          f"simulado (solo informativo).")

    print(f"\nExperimento 2. Meta-evolutivo con sus parámetros {formato_de_configuracion(CONFIGURACION_DEL_META)}, "
          f"{repeticiones} ejecuciones de {PRESUPUESTO_DEL_META} evaluaciones.", flush=True)
    peor = desempenos[ordenadas[-1]].aptitud()
    mejor = desempenos[optima].aptitud()
    meta, encontradas = repetir_meta(evaluador, CONFIGURACION_DEL_META, repeticiones, opciones.semilla + 3000,
                                     peor, mejor)
    aciertos = sum(c == optima for c in encontradas)
    lugares = [ordenadas.index(c) + 1 for c in encontradas]
    print(f"  Encontró la óptima en {aciertos} de {repeticiones} ejecuciones; lugar medio del resultado "
          f"{statistics.mean(lugares):.1f} de {len(ordenadas)} (mediana {statistics.median(lugares):.0f}).")
    print(f"  Calidad media {meta.calidad:.4f} (1 = siempre la óptima, 0 = la peor); convergencia media en la "
          f"generación {meta.convergencia:.2f}; diversidad genética media {meta.diversidad:.4f}.")
    print(f"  Configuración encontrada con más frecuencia: "
          f"{formato_de_configuracion(Counter(encontradas).most_common(1)[0][0])}.")

    print(f"\nExperimento 3. ¿Los mejores parámetros del evolutivo base también son los mejores para el "
          f"meta-evolutivo? Cada configuración se usa como parámetros del meta ({repeticiones} ejecuciones).",
          flush=True)
    candidatas_meta = [c for c in posibles if estructura_valida(c, PRESUPUESTO_DEL_META)]
    desempenos_meta = {c: repetir_meta(evaluador, c, repeticiones, opciones.semilla + 4000, peor, mejor)[0]
                       for c in candidatas_meta}
    ordenadas_meta = sorted(candidatas_meta, key=lambda c: (-desempenos_meta[c].aptitud(), c))
    optima_meta = ordenadas_meta[0]
    filas = [("Óptima para el meta", optima_meta), ("Segunda para el meta", ordenadas_meta[1])]
    if CONFIGURACION_DEL_META in desempenos_meta:
        filas.append((f"Usada por el programa (lugar {ordenadas_meta.index(CONFIGURACION_DEL_META) + 1})",
                      CONFIGURACION_DEL_META))
    if optima in desempenos_meta:
        filas.append((f"Óptima del base (lugar {ordenadas_meta.index(optima) + 1})", optima))
    filas.append(("Peor para el meta", ordenadas_meta[-1]))
    print("  Calidad: posición de la configuración encontrada entre la peor (0) y la óptima (1) del paisaje.")
    imprimir_tabla(filas, desempenos_meta, con_interes=False)
    coinciden = "sí coinciden" if optima_meta == optima else "no coinciden"
    lugar = ""
    if optima in desempenos_meta:
        lugar = (f" Como parámetros del meta, la óptima del base ocupa el lugar "
                 f"{ordenadas_meta.index(optima) + 1} de {len(ordenadas_meta)}.")
    print(f"\nConclusión: la mejor configuración para el evolutivo base es {formato_de_configuracion(optima)} y "
          f"la mejor para el meta-evolutivo es {formato_de_configuracion(optima_meta)}; {coinciden}.{lugar}")
    print(f"Tiempo total: {time.time() - inicio:.0f} s.")


# ----------------------------------------------------------------------
# Opciones y punto de entrada.
# ----------------------------------------------------------------------

def leer_opciones(argumentos=None):
    # Lee los argumentos de la terminal y aplica las constantes de Spyder.

    # Parámetros:
    #     argumentos (list[str] o None): argumentos; None usa los de la
    #         terminal (en Spyder no hay ninguno).

    # Devuelve:
    #     argparse.Namespace: titulo (str), plataforma (str), longitud (int de
    #     1 a LONGITUD_MAXIMA), carpeta (Path existente), perfil (Path),
    #     cambiar_gustos, interactivo y experimentos (bool) y
    #     semilla (int).
    lector = argparse.ArgumentParser(description="Recomendador evolutivo de videojuegos.")
    lector.add_argument("titulo", nargs="*", help="Juego de referencia opcional, por ejemplo Silent Hill 2.")
    lector.add_argument("--plataforma", nargs="+", help="Por ejemplo PC, PS4 o PlayStation 4.")
    lector.add_argument("--longitud", type=int, default=LONGITUD_DE_RUTA, metavar="N", help="Juegos por lista.")
    lector.add_argument("--carpeta", type=Path, default=CARPETA_DEL_PROGRAMA,
                        help="Carpeta donde están los catálogos.")
    lector.add_argument("--perfil", type=Path, help="Archivo SQLite del jugador.")
    lector.add_argument("--cambiar-gustos", action="store_true", help="Repite el cuestionario de gustos.")
    lector.add_argument("--sin-preguntas", action="store_true", default=not HACER_PREGUNTAS,
                        help="Usa lo guardado y no hace preguntas.")
    lector.add_argument("--experimentos", action="store_true", default=MODO_EXPERIMENTOS,
                        help="Ejecuta los experimentos del reporte.")
    lector.add_argument("--semilla", type=int, default=SEMILLA_PREDETERMINADA, help="Semilla aleatoria.")
    opciones = lector.parse_args(argumentos)
    opciones.titulo = (" ".join(opciones.titulo) or JUEGO_DE_REFERENCIA).strip()
    if opciones.plataforma:
        opciones.plataforma = " ".join(opciones.plataforma)
    else:
        opciones.plataforma = PLATAFORMA_PREFERIDA
    opciones.interactivo = not opciones.sin_preguntas
    if not 1 <= opciones.longitud <= LONGITUD_MAXIMA:
        lector.error(f"La longitud debe ser un entero de 1 a {LONGITUD_MAXIMA}.")
    if not opciones.carpeta.is_dir():
        lector.error("La carpeta indicada debe existir.")
    opciones.elegir_jugador = opciones.interactivo and opciones.perfil is None
    if opciones.perfil is None:
        opciones.perfil = opciones.carpeta / NOMBRE_DEL_PERFIL
    return opciones


def principal(argumentos=None):
    # Prepara los datos y ejecuta la recomendación o los experimentos.

    # Parámetros:
    #     argumentos (list[str] o None): argumentos de la terminal.
    opciones = leer_opciones(argumentos)
    print("Preparando los catálogos de videojuegos…", flush=True)
    copias = localizar_catalogos(opciones.carpeta)
    anuncios = anuncios_de_steam(opciones.carpeta)
    catalogo = CatalogoDeJuegos(list(copias.values()), anuncios, consolas_de_wikidata(opciones.carpeta),
                               opciones.carpeta / NOMBRE_DE_LAS_COPIAS)
    # El resumen por fuente permite comprobar que se usaron los dos catálogos.
    for fuente, ruta in copias.items():
        print(f"  {NOMBRES_DE_FUENTE[fuente]}: {catalogo.filas_por_fuente[ruta]:,} juegos leídos.")
    for fuente in FUENTES_DE_KAGGLE:
        if fuente not in copias:
            print(f"  Aviso: falta el catálogo de {NOMBRES_DE_FUENTE[fuente]}; se recomienda con el otro.")
    steam = sum(catalogo.juegos[k].en_steam for k in catalogo.claves_recomendables)
    print(f"Steam aporta {steam:,} títulos que cumplen los requisitos antes del filtro de plataforma.")
    proximos = sum(catalogo.juegos[k].anunciado for k in catalogo.claves_recomendables)
    print(f"Recomendaciones desde {ANIO_DESDE}. Próximos lanzamientos disponibles en el catálogo: {proximos}.")
    print(f"Catálogo listo: {len(catalogo.juegos):,} títulos distintos, "
          f"{len(catalogo.claves_recomendables):,} recomendables.", flush=True)
    if opciones.experimentos and not catalogo.claves_recomendables:
        print(f"Esta copia no contiene juegos recomendables desde {ANIO_DESDE}. Puedes actualizar el CSV de Steam.")
    elif opciones.experimentos:
        ejecutar_experimentos(catalogo, opciones)
    else:
        recomendar(catalogo, opciones)


if __name__ == "__main__":
    try:
        principal()
    except ERRORES_DE_EJECUCION as error:
        print(f"No se pudo completar la ejecución. {error}")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida. Tus gustos y valoraciones guardados se conservan.")
