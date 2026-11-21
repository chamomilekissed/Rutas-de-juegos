# -*- coding: utf-8 -*-
# RECOMENDADOR EVOLUTIVO DE VIDEOJUEGOS
# Proyecto de Programación 2 de Inteligencia Artificial.
# Adaptado del proyecto original de nattfernandez.

# ======================================================================
# MANUAL DE USUARIO
# ======================================================================

# 1. ¿Qué hace este programa?
#    Recomienda listas cortas de videojuegos, parecido a como una plataforma de series
#    te sugiere qué ver. La primera vez te hace unas preguntas sobre tus gustos. Después
#    aprende de lo que opinas de cada lista: escribes «me interesa» o «no me interesa».
#    El programa solo sabe de ti lo que escribes en la consola; no entra a tu cuenta de
#    Steam ni lee archivos de tu computadora. Tus respuestas se guardan en un perfil, así
#    que no tienes que contestar lo mismo cada vez que lo abres.
# 2. ¿Cómo funciona por dentro? (explicado sin tecnicismos)
#    El programa usa dos ideas de la inteligencia artificial:
#    a) Aprender tus gustos. Con tus géneros, tus juegos favoritos y tus valoraciones,
#       calcula una «afinidad» para cada juego: un número entre 0 y 1 que estima qué
#       tanto te va a gustar. Para eso usa una regresión logística, que es un modelo que
#       aprende cuánto pesa cada rasgo (por ejemplo, «terror» o «mundo abierto») en tus
#       decisiones.
#    b) Armar la mejor lista con un algoritmo evolutivo. Funciona como la evolución de
#       los seres vivos: se crea un grupo de listas al azar (la «población»), se califica
#       cada una (su «aptitud») y las mejores tienen hijos. Un hijo nace de una de dos
#       formas: por «mutación», cuando se copia una lista y se le cambia un juego o el
#       orden de dos juegos, o por «cruzamiento», cuando se mezclan dos listas. Cada ronda
#       de hijos es una «generación». Después de muchas generaciones queda una lista muy
#       buena. Una lista buena tiene juegos afines a ti, variados entre sí y con cierta
#       relación entre un juego y el siguiente.
#    Además hay un segundo algoritmo evolutivo, el «meta-evolutivo», que no arma listas:
#    busca la mejor manera de configurar al primero. Prueba distintos tamaños de
#    población, cantidades de hijos por generación, tamaños de torneo (cuántas listas
#    compiten para ser padre), probabilidades de mutación dirigida y porcentajes de hijos
#    por cruzamiento. Cada configuración se califica con 50 ejecuciones del primer
#    algoritmo: qué tan buenas son sus listas, en qué generación llega a una buena lista y
#    qué tan distintas son entre sí las listas de su población (diversidad genética).
#    Los dos niveles usan la misma clase AlgoritmoEvolutivo, porque la forma de evolucionar
#    es igual sin importar si lo que evoluciona es una lista de juegos o una configuración.
#    Otros detalles: todos los géneros que eliges empiezan con el mismo peso; si das varios
#    favoritos, la lista busca juegos parecidos a cada uno; Steam aporta etiquetas que
#    faltan en Kaggle y se guardan 30 días.
# 3. ¿Qué necesito?
#    Python 3.10 o más reciente, por ejemplo el que trae Anaconda con Spyder. Solo usa
#    la biblioteca estándar de Python, así que no hay que instalar nada más.
# 4. ¿Cómo lo ejecuto?
#    Abre este archivo en Spyder y pulsa F5. Las preguntas aparecen en la consola: escribe
#    tu respuesta y pulsa Enter.
# 5. La primera vez
#    a) Datos. No tienes que descargar nada a mano ni tener cuenta de Kaggle.
#       - La primera vez el programa descarga los catálogos de Kaggle (sección 11) y
#         guarda una copia más pequeña en la carpeta datos_juegos. El catálogo de Steam
#         pesa cientos de megabytes, así que puede tardar varios minutos; la consola
#         muestra el avance.
#       - Después revisa Kaggle como máximo una vez cada siete días y solo vuelve a
#         descargar si el autor publicó una versión nueva.
#       - Si no hay internet, usa la última copia guardada y lo avisa.
#       - La primera vez también pide a Steam las etiquetas de los juegos recientes; las
#         guarda 30 días. Al terminar cada etapa, la consola dice cuántos segundos tardó.
#       Necesitas internet al menos la primera vez.
#       Las recomendaciones son de juegos de 2026 en adelante (tus favoritos pueden ser de
#       cualquier año). El programa también consulta en la tienda de Steam hasta 16 juegos
#       anunciados y guarda esa lista siete días. Wikidata dice en qué consolas está cada
#       juego. Si no hay estrenos confirmados para tu consola, el programa te avisa y busca
#       en sus juegos anteriores. «Nintendo» y «Xbox» incluyen todas sus consolas; escribe
#       el modelo exacto si solo tienes una.
#       El programa descarta los juegos con indicios de contenido sexual o desnudez. Antes
#       de recomendar un juego de Steam revisa los avisos de su ficha en la tienda; si no
#       puede revisarlos, prefiere mostrar una lista más corta.
#    b) Perfil y cuestionario. Escribe tu apodo para guardar tus respuestas; cada persona
#       debe usar un apodo distinto. Si ya tenías un perfil de una versión anterior, pulsa
#       Enter para abrirlo. Después responde:
#       - los géneros que te gustan, con sus números separados por comas (por ejemplo
#         1, 3, 12) o con sus nombres (por ejemplo terror, rol);
#       - los géneros que prefieres evitar (Enter para omitir); esos juegos nunca aparecen;
#       - hasta cinco juegos que te hayan gustado: escribe parte del título, por ejemplo
#         zelda, y elige uno de los resultados por su número; no importan las mayúsculas,
#         los acentos ni los espacios;
#       - tu plataforma, por ejemplo PC, PS4 o Wii (Enter si te da igual).
#       Debes dar al menos un género o un juego, porque el programa no arma listas solo
#       con los juegos más populares.
#    c) Ajuste. El meta-evolutivo busca la mejor configuración del algoritmo que arma las
#       listas. Tarda alrededor de un minuto. El resultado se guarda en datos_juegos y lo
#       usan todos los perfiles mientras no cambien la longitud de la lista ni los
#       catálogos de Kaggle.
# 6. Las siguientes veces
#    El programa muestra tus gustos guardados. Pulsa Enter para seguir o escribe C para
#    contestar otra vez el cuestionario.
# 7. ¿Cómo valoro una lista?
#    Debajo de cada lista escribe los números de los juegos que te interesan y, con un
#    signo menos, los que no. Por ejemplo, «1 3 -2» quiere decir que te interesan el 1 y
#    el 3 y que el 2 no. Enter salta la valoración. Los juegos que valoras ya no se te
#    vuelven a recomendar, y el programa recalcula tus gustos con esa información. Luego
#    puedes pedir otra lista. Si la lista tiene dos o más juegos, incluye un juego que
#    todavía no sale y uno que ya salió, siempre que los dos cumplan tus filtros. Steam
#    puede cambiar la fecha de un juego anunciado o dejarla por confirmar.
# 8. Opciones
#    Antes de pulsar F5 puedes cambiar estas constantes de la sección «Opciones de
#    ejecución», que está más abajo:
#        JUEGO_DE_REFERENCIA     juego que orienta solo esta ejecución, por ejemplo "Silent Hill 2".
#        PLATAFORMA_PREFERIDA    plataforma solo para esta ejecución, por ejemplo "PS4".
#        LONGITUD_DE_RUTA        cuántos juegos tiene cada lista, de 1 a 10.
#        SEMILLA_PREDETERMINADA  número que fija el azar; con la misma semilla sale lo mismo.
#        HACER_PREGUNTAS         False usa lo guardado y no pregunta nada.
#        MODO_EXPERIMENTOS       True ejecuta los experimentos del reporte (sección 9).
#    Para contestar otra vez el cuestionario, escribe C cuando el programa muestre tus
#    gustos. Para usar otro perfil, escribe otro apodo.
# 9. Modo de experimentos
#    Con MODO_EXPERIMENTOS = True el programa no recomienda. Califica con 50 ejecuciones
#    cada configuración posible del algoritmo que arma las listas, ejecuta 50 veces el
#    meta-evolutivo y compara cuáles configuraciones son mejores para cada uno. Tarda unos
#    minutos y escribe tablas listas para el reporte.
# 10. Archivos que crea
#    datos_juegos/                  copias reducidas de los catálogos, versiones_kaggle.json
#                                   (versión de cada descarga), etiquetas, anuncios y
#                                   consolas guardados, y ajustes_evolutivos.sqlite3 (la
#                                   configuración que eligió el meta-evolutivo).
#    perfil_recomendador.sqlite3    perfil que se usa si no escribes apodo.
#    perfiles/                      un archivo por apodo.
#    Borrar un perfil borra esos gustos y valoraciones. Borrar datos_juegos obliga a
#    descargar otra vez los catálogos. Para usar el programa en una computadora sin
#    internet, copia la carpeta datos_juegos junto a este archivo.
# 11. ¿De dónde salen los datos? (Kaggle, una página pública de conjuntos de datos)
#    - Video Game Sales with Ratings, de rush4ratio (se descarga
#      Video_Games_Sales_as_at_22_Dec_2016.csv):
#      https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings
#    - Steam Games Dataset, de FronkonGames (se descarga solo games.csv):
#      https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
#    El programa busca cada catálogo en este orden:
#      1. En Kaggle (descarga solo si hay una versión nueva).
#      2. Si Kaggle no responde, en la última copia guardada en datos_juegos.
#      3. Si nunca se descargó, en un archivo de Kaggle colocado junto a este programa.
#    Kaggle deja descargar estos datos sin cuenta. Si algún día pidiera cuenta, el
#    programa usa las credenciales de ~/.kaggle/kaggle.json o de las variables
#    KAGGLE_USERNAME y KAGGLE_KEY; este archivo no contiene ninguna clave.
#    Al iniciar, el programa dice de dónde salió cada catálogo y cuántos juegos leyó.
#    Las listas se arman con el catálogo de Steam.
# 12. Problemas frecuentes
#    - «No se pudo consultar Kaggle»: revisa tu conexión y vuelve a pulsar F5. Sin
#      internet, descarga games.csv desde la página de la sección 11 y déjalo junto al
#      programa.
#    - «Plataforma desconocida»: usa uno de los nombres que sugiere el mensaje.
#    - Para empezar de cero, borra perfil_recomendador.sqlite3 o la carpeta perfiles.

import argparse
import base64
import csv
import difflib
import hashlib
import io
import json
import math
import os
from itertools import islice, product, zip_longest
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
# Opciones de ejecución. Se pueden cambiar antes de pulsar F5 (ver la sección 8 del manual).
# ----------------------------------------------------------------------
JUEGO_DE_REFERENCIA = ""            # Juego que orienta solo esta ejecución, por ejemplo "Silent Hill 2".
PLATAFORMA_PREFERIDA = ""           # Plataforma solo para esta ejecución; vacía usa la del cuestionario.
LONGITUD_DE_RUTA = 5                # Cuántos juegos tiene cada lista recomendada (de 1 a 10).
SEMILLA_PREDETERMINADA = 2026       # Fija el azar: con los mismos datos y la misma semilla sale lo mismo.
HACER_PREGUNTAS = True              # False usa solo lo guardado, sin cuestionario ni valoraciones.
MODO_EXPERIMENTOS = False           # True ejecuta los experimentos del reporte en lugar de recomendar.
# Carpeta donde está este archivo; ahí se crean datos_juegos y los perfiles.
CARPETA_DEL_PROGRAMA = Path(__file__).resolve().parent


# ----------------------------------------------------------------------
# Números que controlan el modelo de gustos y los algoritmos evolutivos.
# ----------------------------------------------------------------------
PRESUPUESTO_DE_BUSQUEDA = 480       # Cuántas listas puede calificar el algoritmo de las listas en una ejecución.
PRESUPUESTO_DEL_META = 40           # Cuántas configuraciones puede calificar el meta-evolutivo en un ajuste.
EJECUCIONES_POR_CONFIGURACION = 50  # Ejecuciones con las que se califica cada configuración.
ESCENARIOS_DE_AJUSTE = 5            # Jugadores simulados; cada uno recibe 50 / 5 = 10 ejecuciones.
OBJETIVO_DE_CONVERGENCIA = 0.95     # Una ejecución «ya llegó» cuando logra el 95 % de la mejora posible.
TAMANO_DE_RESERVA = 200             # Cuántos juegos de mayor afinidad forman la reserva de donde salen las listas.
TAMANO_DE_PREFERIDOS = 24           # Cuántos juegos de mayor afinidad usa la mutación dirigida.
PROBABILIDAD_DE_INTERCAMBIO = 0.28  # Probabilidad de que una mutación cambie de lugar dos juegos.
ANIO_DESDE = 2026                   # Primer año de las recomendaciones; los favoritos pueden ser de antes.
PESO_DE_LA_RESENA = 0.20            # Parte de la afinidad que sale de las reseñas del público (20 %).
PESO_DEL_HISTORIAL = 0.70           # Si hay historial y géneros elegidos: 70 % historial y 30 % géneros.
MINIMO_DE_RESENAS = 101             # Las reseñas solo cuentan si son más de cien.
PESO_PREVIO_GUSTA = 1.2             # Peso inicial de cada género elegido en el cuestionario.
ITERACIONES_DE_APRENDIZAJE = 70     # Vueltas que da la regresión logística para aprender los pesos.
TASA_DE_APRENDIZAJE = 0.7           # Qué tan grande es cada corrección de los pesos en cada vuelta.
REGULARIZACION = 0.06               # Qué tanto se acerca cada peso a su valor inicial, para evitar pesos extremos.
MAXIMO_DE_FAVORITOS = 5             # Cuántos juegos favoritos se pueden dar en el cuestionario.
ETIQUETAS_QUE_DEFINEN_GENERO = 5    # Solo las 5 etiquetas más votadas de un juego le asignan un género.
LONGITUD_MAXIMA = 10                # Lista más larga permitida; más juegos hacen lento el primer ajuste.
VERSION_DEL_AJUSTE = 13             # Al cambiar este número se ignoran los ajustes guardados por versiones anteriores.
# Nombres del perfil que se usa sin apodo y de la carpeta de copias de los catálogos.
NOMBRE_DEL_PERFIL = "perfil_recomendador.sqlite3"
NOMBRE_DE_LAS_COPIAS = "datos_juegos"

# Los dos catálogos se descargan de Kaggle. Antes de descargar, el programa revisa si hay
# una versión nueva, para no bajar lo mismo otra vez (ver obtener_fuente).
API_DE_KAGGLE = "https://www.kaggle.com/api/v1/datasets/download/"
# Nombre de cada catálogo dentro de Kaggle (autor/conjunto de datos).
FUENTES_DE_KAGGLE = {
    "ventas": "rush4ratio/video-game-sales-with-ratings",
    "steam": "fronkongames/steam-games-dataset",
}
# Archivo que se descarga de cada catálogo. De Steam solo se baja games.csv; el catálogo
# también trae games.json, que pesa mucho más y no hace falta.
ARCHIVOS_DE_KAGGLE = {
    "ventas": "Video_Games_Sales_as_at_22_Dec_2016.csv",
    "steam": "games.csv",
}
NOMBRE_DEL_REGISTRO_DE_KAGGLE = "versiones_kaggle.json"  # Guarda qué versión de cada catálogo se descargó.
DIAS_SIN_HUELLA = 30                # Si Kaggle no informa la versión, se vuelve a descargar cada 30 días.
DIAS_ENTRE_CONSULTAS = 7            # Con una copia que sirve, Kaggle se revisa como máximo cada 7 días.
NOMBRE_DE_LOS_AJUSTES = "ajustes_evolutivos.sqlite3"  # Configuración elegida por el meta-evolutivo, común a todos los perfiles.
# Nombres de los catálogos que se muestran en los mensajes.
NOMBRES_DE_FUENTE = {"ventas": "ventas (Video Game Sales with Ratings)",
                     "steam": "Steam (Steam Games Dataset)"}

# Columnas de las copias reducidas que se guardan en datos_juegos. Las dos fuentes usan
# los mismos nombres de columna, así el resto del programa las lee igual.
COLUMNAS_DE_LA_COPIA = ("identificador", "titulo", "anio", "plataformas", "windows", "mac", "linux",
                        "genero", "etiquetas", "desarrollador", "saga", "positivas", "negativas",
                        "ventas", "usuarios", "nota", "critica", "revision_contenido")
# Errores que pueden pasar al leer archivos o descargar (archivo dañado, sin internet…).
# El programa los atiende con un mensaje claro en vez de detenerse con un error largo.
ERRORES_DE_DATOS = (OSError, ValueError, EOFError, HTTPException, csv.Error, zipfile.BadZipFile, zlib.error)
ERRORES_DE_EJECUCION = ERRORES_DE_DATOS + (sqlite3.Error,)
LIMITE_DE_REGISTRO = 32 * 1024 * 1024  # Tamaño máximo de una ficha o celda: 32 millones de caracteres.

# Una configuración del algoritmo evolutivo es una tupla de cinco números («genes»), en
# este orden:
#   poblacion: cuántas listas viven en cada generación.
#   descendientes: cuántos hijos nuevos nacen en cada generación. Debe ser menor que la
#       población para que siempre sobreviva la mejor lista (a esto se le llama elitismo).
#   torneo: cuántos individuos compiten para ser padre; gana el mejor de ellos.
#   dirigida: probabilidad de que una mutación sea «dirigida». En una lista, el juego
#       nuevo sale de los de mayor afinidad; en una configuración, un número cambia solo
#       a un valor vecino.
#   cruzamiento: qué fracción de los hijos nace mezclando dos padres; los demás nacen por
#       mutación de un padre. Con 0 el algoritmo solo muta.
NOMBRES_DE_PARAMETROS = ("poblacion", "descendientes", "torneo", "dirigida", "cruzamiento")
VALORES_DE_AJUSTE = [               # Valores que puede tomar cada gen, en el mismo orden.
    [12, 18, 24, 30, 36],
    [6, 9, 12, 15, 18, 24],
    [2, 3, 4, 5],
    [0.20, 0.45, 0.70, 0.90],
    [0.0, 0.25, 0.50, 0.75],
]
AJUSTE_INICIAL = (30, 18, 3, 0.45, 0.0)  # Configuración hecha a mano en el diseño original (solo mutación).
CONFIGURACION_DEL_META = (12, 6, 2, 0.45, 0.25)  # Configuración del propio meta-evolutivo.


# ----------------------------------------------------------------------
# Lo que el programa sabe de videojuegos: géneros, etiquetas y plataformas.
# ----------------------------------------------------------------------
# Traduce al español los géneros que traen los catálogos (escritos sin mayúsculas ni acentos).
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
# convierte esas etiquetas en los mismos géneros del catálogo de ventas, para que el
# cuestionario funcione igual con los dos catálogos.
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

# Nombres en español de etiquetas comunes de Steam. Solo sirven para explicar por qué se
# recomienda un juego.
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

# Géneros que ofrece el cuestionario, en el orden en que aparecen en pantalla.
GENEROS_DEL_CUESTIONARIO = (
    "Acción", "Aventura", "Rol", "Estrategia", "Disparos", "Deportes", "Carreras",
    "Simulación", "Rompecabezas", "Plataformas", "Lucha", "Terror",
    "Terror psicológico", "Casual", "Independiente", "Multijugador masivo",
)

# Géneros o etiquetas que sacan a un título del catálogo: contenido para adultos y
# programas que no son juegos (por ejemplo, programas de dibujo). Así una demostración
# en clase nunca muestra esos títulos.
CONTENIDO_EXCLUIDO = frozenset({
    "sexual content", "nudity", "hentai", "nsfw", "software", "utilities",
    "design illustration", "animation modeling", "software training",
    "audio production", "video production", "web publishing", "photo editing",
    "accounting", "game development", "movie", "documentary", "360 video",
})

# Palabras que indican contenido sexual. \b significa «palabra completa», para que un
# nombre como «Sussex» no se confunda con «sex».
INDICIOS_SEXUALES = re.compile(
    r"\b(?:hentai\w*|nsfw|porn\w*|eroge|ecchi|lewd\w*|erotic\w*|erótic\w*|xxx|sex|sexo|sexual(?:ly|es)?|"
    r"nudity|nudes?|naked|desnud[oa]\w*|fetish\w*|bdsm|hardcore pornography|"
    r"adult[\s_-]+(?:only|game|content|visual novel)|adults[\s_-]+only|"
    r"solo para adultos|contenido para adultos|explicit adult|strip[\s_-]+(?:poker|club))\b",
    re.IGNORECASE,
)


def hay_contenido_sexual(*campos):
    # Dice si algún texto tiene palabras de contenido sexual (ver INDICIOS_SEXUALES).
    # NFKC convierte las letras «anchas» de algunos títulos asiáticos en letras normales,
    # para que también se reconozcan.
    # Recibe:
    #     campos: cualquier cantidad de textos o valores; los vacíos se saltan.
    # Devuelve:
    #     bool: True si alguno tiene una de esas palabras.
    return any(INDICIOS_SEXUALES.search(unicodedata.normalize("NFKC", str(campo)).replace("_", " "))
               for campo in campos if campo)

# Notas del programa original para juegos de terror que el catálogo de ventas clasifica
# con un género más general; por ejemplo, Silent Hill 2 aparece como Acción.
SAGAS_DE_TERROR = (
    "silent hill", "resident evil", "fatal frame", "dead space",
    "clock tower", "alone in the dark", "the evil within",
)
# Títulos que se marcan como terror psicológico y otros títulos de terror conocidos.
TITULOS_DE_TERROR_PSICOLOGICO = {
    "silent hill", "silent hill 2", "silent hill 3", "silent hill 4 the room",
    "silent hill origins", "silent hill downpour", "silent hill shattered memories",
    "silent hill homecoming", "the evil within", "haunting ground",
}
OTROS_TITULOS_DE_TERROR = {
    "alien isolation", "haunting ground", "siren", "siren blood curse", "forbidden siren 2",
}
# Ediciones especiales que se tratan como el juego original.
EDICIONES_EQUIVALENTES = {
    "resident evil 2 dual shock edition": "resident evil 2",
    "silent hill 2 restless dreams": "silent hill 2",
}

# Cuánto pesa cada tipo de rasgo al calcular la afinidad: el género es lo que más importa,
# las etiquetas (temas) importan menos y el estudio que hizo el juego casi no influye. La
# editora no se toma en cuenta.
PESO_POR_TIPO = {"genero": 1.5, "tema": 0.5, "estudio": 0.10}

# Nombres que la gente escribe para una misma consola y la clave corta que usa el
# programa; por ejemplo, «PlayStation 4» y «ps4» se convierten en «ps4».
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

# Nombres visibles de cada consola. «Xbox» y «Nintendo» son familias: al elegirlas se
# buscan juegos de todos sus modelos. Un modelo concreto, como «PS4», solo busca ese.
MODELOS = {"pc": "PC", "mac": "Mac", "ps2": "PS2", "ps3": "PS3", "ps4": "PS4", "ps5": "PS5",
           "xb": "Xbox original", "x360": "Xbox 360", "xone": "Xbox One", "xboxseriesxs": "Xbox Series X/S",
           "switch": "Nintendo Switch", "switch2": "Nintendo Switch 2", "xbox": "Xbox", "nintendo": "Nintendo"}
# Modelos que incluye cada familia de consolas.
FAMILIAS = {"xbox": {"xb", "x360", "xone", "xboxseriesxs"},
            "nintendo": {"switch", "switch2", "wii", "wiiu", "ds", "3ds", "gc", "n64", "nes", "snes",
                         "gb", "gbc", "gba"}}
# Página de Wikipedia de cada consola, con la que se pregunta a Wikidata, y su nombre en el programa.
PAGINAS_DE_CONSOLAS = {"PlayStation_2": "PS2", "PlayStation_3": "PS3", "PlayStation_4": "PS4",
                       "PlayStation_5": "PS5", "Xbox_(console)": "Xbox original", "Xbox_360": "Xbox 360",
                       "Xbox_One": "Xbox One", "Xbox_Series_X_and_Series_S": "Xbox Series X/S",
                       "Nintendo_Switch": "Nintendo Switch", "Nintendo_Switch_2": "Nintendo Switch 2"}

# Cada catálogo llama distinto a sus columnas (por ejemplo, «Name» o «Title»). Esta tabla
# dice qué nombres puede tener cada columna que usa el programa.
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
# Herramientas para comparar textos.
# ----------------------------------------------------------------------
# Memoria de los textos que ya se normalizaron. Los catálogos repiten muchas veces los
# mismos géneros y etiquetas, así que recordar el resultado ahorra tiempo.
textos_normalizados = {}


def normalizar(texto):
    # Convierte un texto en una «clave» fácil de comparar, para que «Silent Hill® 2:
    # Restless Dreams» y «silent hill 2 restless dreams» se reconozcan como lo mismo.
    # Recibe:
    #     texto (str): cualquier texto, incluso vacío.
    # Devuelve:
    #     str: el texto en minúsculas, sin acentos ni símbolos y con las palabras
    #     separadas por un solo espacio.
    if texto not in textos_normalizados:
        limpio = texto.replace("®", "").replace("™", "").replace("©", "").lower()
        # NFKD separa cada letra de su acento (á queda como a + ´); luego se quitan los acentos.
        letras = unicodedata.normalize("NFKD", limpio)
        sin_acentos = "".join(c for c in letras if not unicodedata.combining(c))
        # Se quedan solo las letras y los números, unidos por un espacio, y se guarda en la memoria.
        textos_normalizados[texto] = " ".join(re.findall(r"[^\W_]+", sin_acentos))
    return textos_normalizados[texto]


def clave_titulo(titulo):
    # Devuelve la clave con la que el catálogo reconoce un título.
    # Recibe:
    #     titulo (str): nombre del juego tal como aparece en un archivo.
    # Devuelve:
    #     str: el título normalizado. Si es una edición especial conocida (ver
    #     EDICIONES_EQUIVALENTES), devuelve la clave del juego original.
    clave = normalizar(titulo)
    return EDICIONES_EQUIVALENTES.get(clave, clave)


def numero(texto):
    # Convierte un texto leído de un archivo en un número que no sea negativo.
    # Recibe:
    #     texto (str, int o float): el valor leído.
    # Devuelve:
    #     float o None: el número; None si el texto está vacío, no es un número (por
    #     ejemplo «tbd», «por definir») o es negativo.
    valor = None
    try:
        medido = float(texto)
        if math.isfinite(medido) and medido >= 0:
            valor = medido
    except (TypeError, ValueError):
        valor = None
    return valor


def primero_presente(opciones, disponibles):
    # Busca la primera opción de una lista que también aparece en otra colección.
    # Recibe:
    #     opciones (lista o tupla): opciones en orden de preferencia.
    #     disponibles (colección): valores contra los que se compara.
    # Devuelve:
    #     La primera opción que está en disponibles, o None si no hay ninguna.
    elegida = None
    for opcion in opciones:
        if elegida is None and opcion in disponibles:
            elegida = opcion
    return elegida


def detectar_separador(encabezado):
    # Adivina con qué símbolo se separan las columnas de un archivo CSV (una tabla en
    # texto). Prueba la coma, el punto y coma y el tabulador.
    # Recibe:
    #     encabezado (str): primera línea del archivo, la de los nombres de columna.
    # Devuelve:
    #     str: el separador que divide esa línea en más columnas.
    mejor = ","
    columnas_del_mejor = 0
    for separador in (",", ";", "\t"):
        columnas = len(list(csv.reader([encabezado], delimiter=separador))[0])
        if columnas > columnas_del_mejor:
            mejor = separador
            columnas_del_mejor = columnas
    return mejor


def nombres_de_campo(texto):
    # Separa los valores de una celda que contiene una lista, como «Action, Adventure».
    # Recibe:
    #     texto (str): lista separada por comas, punto y coma o barras, o una lista en
    #         formato JSON, como '["Action","RPG"]'.
    # Devuelve:
    #     list[str]: los valores sin espacios ni comillas sobrantes, en su orden original
    #     y sin textos vacíos.
    valores = re.split(r"[;,|]", texto)
    if texto.startswith("[") and texto.endswith("]"):
        try:
            arreglo = json.loads(texto)
        except json.JSONDecodeError:
            # Algunos archivos usan comillas simples, que JSON no acepta; se separa a mano.
            arreglo = re.split(r"[;,|]", texto[1:-1])
        if isinstance(arreglo, list):
            valores = [v for v in arreglo if isinstance(v, str)]
    return [v.strip(" '\"") for v in valores if v.strip(" '\"")]


def etiquetas_de_campo(texto):
    # Devuelve hasta ocho etiquetas de un juego.
    # Recibe:
    #     texto (str): lista de etiquetas, o un objeto JSON que dice cuántos votos tiene
    #         cada etiqueta, como '{"Horror": 120, "Indie": 80}'.
    # Devuelve:
    #     list[str]: como máximo ocho etiquetas; si hay votos, primero las más votadas.
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
    # Da una misma clave a los distintos nombres de una plataforma.
    # Recibe:
    #     texto (str o None): nombre escrito por la persona o leído de un catálogo, por
    #         ejemplo «PS 4», «PlayStation 4» o «ps4».
    # Devuelve:
    #     str: la clave corta, por ejemplo «ps4»; texto vacío si no se escribió nada.
    compacto = normalizar(texto or "").replace(" ", "")
    return ALIAS_DE_PLATAFORMAS.get(compacto, compacto)


# ----------------------------------------------------------------------
# Lectura del archivo JSON de Steam por partes, sin cargarlo completo en memoria.
# ----------------------------------------------------------------------
class LectorDeObjetos:
    # Lee el archivo games.json de Steam un juego a la vez.
    # Ese archivo pesa más de un gigabyte; abrirlo completo llenaría la memoria. Por eso
    # esta clase lee pedazos de 1 MB y solo guarda el texto que todavía no ha convertido
    # en datos. Hoy el programa descarga games.csv, así que solo se usa si alguien deja un
    # games.json junto al programa.
    # Forma de usarla:
    #     lector = LectorDeObjetos(archivo)
    #     lector.empezar()
    #     par = lector.siguiente_juego()
    #     while par is not None:
    #         ...                         # par es (AppID, ficha del juego)
    #         par = lector.siguiente_juego()
    # Atributos:
    #     archivo: el archivo de texto abierto.
    #     pendiente (str): texto leído que todavía no se convierte en datos.
    #     indice (int): posición, dentro de pendiente, del siguiente carácter por leer.
    #     decodificador (json.JSONDecoder): herramienta de Python que convierte texto JSON
    #         en datos a partir de una posición.
    #     quedan_juegos (bool): True mientras falten juegos por leer.

    def __init__(self, archivo):
        # Prepara la lectura.
        # Recibe:
        #     archivo: archivo de texto abierto para leer.
        self.archivo = archivo
        self.pendiente = ""
        self.indice = 0
        self.decodificador = json.JSONDecoder()
        self.quedan_juegos = False

    def leer_bloque(self):
        # Tira el texto que ya se leyó y agrega el siguiente pedazo de 1 MB.
        # Devuelve:
        #     bool: True si había más texto; False si el archivo ya terminó.
        bloque = self.archivo.read(1024 * 1024)
        self.pendiente = self.pendiente[self.indice:] + bloque
        self.indice = 0
        return len(bloque) > 0

    def saltar_espacios(self):
        # Avanza sobre los espacios y saltos de línea del pedazo actual.
        # Devuelve:
        #     bool: True si después de los espacios todavía queda algún carácter.
        while self.indice < len(self.pendiente) and self.pendiente[self.indice] in " \t\r\n":
            self.indice += 1
        return self.indice < len(self.pendiente)

    def mirar(self):
        # Mira cuál es el siguiente carácter visible, sin avanzar.
        # Devuelve:
        #     str: ese carácter, o texto vacío si el archivo terminó.
        quedan_datos = True
        # Si el pedazo actual solo tiene espacios, se lee el siguiente pedazo.
        while not self.saltar_espacios() and quedan_datos:
            quedan_datos = self.leer_bloque()
        siguiente = ""
        if self.indice < len(self.pendiente):
            siguiente = self.pendiente[self.indice]
        return siguiente

    def consumir(self, signo):
        # Avanza sobre un símbolo que la estructura JSON exige, como «{» o «:».
        # Recibe:
        #     signo (str): el símbolo que debe aparecer.
        # Puede fallar:
        #     ValueError: si aparece otro símbolo, porque el archivo está mal formado.
        aparente = self.mirar()
        if aparente != signo:
            raise ValueError(f"Se esperaba '{signo}' y apareció '{aparente}'.")
        self.indice += 1

    def valor(self, inicio):
        # Convierte en datos el siguiente valor del archivo.
        # Recibe:
        #     inicio (str): con qué debe empezar el valor: '"' para un texto o «{» para la
        #         ficha de un juego.
        # Devuelve:
        #     str o dict: el valor ya convertido.
        # Puede fallar:
        #     ValueError: si el valor empieza con otro símbolo o mide más de
        #         LIMITE_DE_REGISTRO caracteres; json.JSONDecodeError si el archivo se
        #         corta antes de terminar el valor.
        if self.mirar() != inicio:
            raise ValueError(f"El registro no comienza con '{inicio}'.")
        resultado = None
        decodificado = False
        # Si la ficha quedó partida entre dos pedazos, se lee el siguiente pedazo y se vuelve a intentar.
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
        # Avanza sobre la llave «{» con la que empieza todo el archivo games.json.
        # Puede fallar:
        #     ValueError: si el archivo no empieza con «{».
        self.consumir("{")
        self.quedan_juegos = self.mirar() != "}"
        if not self.quedan_juegos:
            self.consumir("}")

    def siguiente_juego(self):
        # Lee el siguiente juego del archivo.
        # Devuelve:
        #     tuple o None: (número de Steam del juego, ficha del juego), o None cuando ya
        #     no quedan juegos.
        # Puede fallar:
        #     ValueError: si el archivo no tiene la forma esperada.
        par = None
        if self.quedan_juegos:
            appid = self.valor('"')
            self.consumir(":")
            ficha = self.valor("{")
            par = (appid, ficha)
            # Después de cada juego viene una coma (hay otro juego) o la llave «}» (se acabó).
            self.quedan_juegos = self.mirar() == ","
            if self.quedan_juegos:
                self.consumir(",")
            else:
                self.consumir("}")
                if self.mirar() != "":
                    raise ValueError("El JSON contiene datos después del objeto de juegos.")
        return par


def arreglo(valores):
    # Convierte en una lista JSON los textos no vacíos de un valor, para guardarlos en una
    # sola celda del CSV.
    # Recibe:
    #     valores (lista, tupla, texto u otro): valor tomado de la ficha de Steam.
    # Devuelve:
    #     str: la lista en JSON, por ejemplo '["Action","Indie"]'; texto vacío si no hay
    #     ningún texto útil.
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
    # Elige las etiquetas que mejor describen un juego de games.json.
    # Recibe:
    #     juego (dict): ficha de games.json. Sus etiquetas pueden venir como diccionario
    #         etiqueta → votos o como lista.
    #     limite (int): cuántas etiquetas como máximo (número entero positivo).
    # Devuelve:
    #     list[str]: las etiquetas, sin pasar del límite; si hay votos, primero las más
    #     votadas. Si el juego no tiene etiquetas, usa sus categorías.
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
    # Se queda solo con los datos de una ficha de games.json que el programa usa.
    # Recibe:
    #     appid (str): número con el que Steam identifica al juego.
    #     juego (dict): ficha completa del juego.
    # Devuelve:
    #     dict: una fila para la copia reducida, con las columnas de COLUMNAS_DE_LA_COPIA.
    #     Deja fuera imágenes, videos y descripciones. Si Steam marca desnudez o contenido
    #     sexual (avisos 1, 3 y 4) o hay palabras de ese tipo, la fila queda marcada como
    #     «excluir».
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
# Lectura de las tablas CSV de los dos catálogos.
# ----------------------------------------------------------------------
def reparar_encabezado(nombres, valores):
    # Corrige un error conocido del games.csv de Steam.
    # En algunas versiones, los nombres de columna «Discount» y «DLC count» aparecen
    # pegados como «DiscountDLC count», aunque cada fila sí trae los dos valores. Sin esta
    # corrección, todas las columnas siguientes quedarían desplazadas un lugar.
    # Recibe:
    #     nombres (list[str]): nombres de columna leídos del archivo.
    #     valores (list[str]): primera fila de datos.
    # Devuelve:
    #     list[str]: los nombres corregidos; una copia igual si el archivo no tiene el error.
    reparados = list(nombres)
    if "DiscountDLC count" in reparados and len(valores) == len(reparados) + 1:
        indice = reparados.index("DiscountDLC count")
        reparados[indice:indice + 1] = ["Discount", "DLC count"]
    return reparados


def recorrer_csv(entrada, nombre, procesar):
    # Lee un catálogo CSV renglón por renglón, sin cargarlo completo en memoria.
    # A cada renglón se le cambian los nombres de columna por los nombres internos del
    # programa (ver COLUMNAS_DEL_CATALOGO). Así el resto del programa no depende de cómo
    # llama cada catálogo a sus columnas.
    # Recibe:
    #     entrada: archivo de texto abierto, desde el principio.
    #     nombre (str): nombre del archivo; solo se usa en los mensajes.
    #     procesar (función): se llama con cada renglón (dict) que tenga título.
    # Devuelve:
    #     tuple: (renglones con título, renglones descartados por tener columnas de más).
    # Puede fallar:
    #     ValueError: si el archivo no tiene una columna de título.
    con_titulo = 0
    omitidas = 0
    # Algunas celdas de Steam (las descripciones) son muy largas. El límite de tamaño de
    # celda se amplía solo mientras se lee y después se regresa a su valor anterior.
    limite_anterior = csv.field_size_limit(LIMITE_DE_REGISTRO)
    try:
        encabezado = entrada.readline()
        separador = detectar_separador(encabezado)
        nombres = list(csv.reader([encabezado], delimiter=separador))[0]
        campos = None
        for valores in csv.reader(entrada, delimiter=separador):
            # Con el primer renglón de datos se corrige el encabezado y se ubican las columnas.
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
    # Decide si un renglón del catálogo es apto para mostrarse.
    # Se revisan todas las etiquetas y notas del renglón antes de recortarlas a ocho.
    # Recibe:
    #     fila (dict): renglón con las columnas de COLUMNAS_DEL_CATALOGO.
    # Devuelve:
    #     str: «excluir» si es solo para adultos o tiene indicios de contenido sexual;
    #     la revisión que ya traía la fila, si tiene una; «revisado» si es un juego del
    #     catálogo de ventas con clasificación para todo público; texto vacío si todavía
    #     no se sabe (entonces se revisará en la tienda de Steam antes de recomendarlo).
    clasificacion = normalizar(fila.get("clasificacion", ""))
    # Las condiciones se revisan en orden: la primera que se cumple decide el resultado.
    resultado = ""
    if (clasificacion in ("ao", "adults only") or
            hay_contenido_sexual(fila["titulo"], fila["genero"], fila["etiquetas"], fila.get("aviso_contenido"))):
        resultado = "excluir"
    elif fila.get("revision_contenido"):
        resultado = fila["revision_contenido"]
    elif not fila["identificador"] and clasificacion in ("ec", "e", "e10", "everyone", "everyone 10"):
        resultado = "revisado"
    return resultado


def fila_de_copia(fila):
    # Prepara un renglón para escribirlo en la copia reducida.
    # Recibe:
    #     fila (dict): renglón con las columnas de COLUMNAS_DEL_CATALOGO.
    # Devuelve:
    #     dict: el mismo renglón con su revisión de contenido y solo sus ocho etiquetas
    #     principales; así la copia ocupa mucho menos que el original.
    copia = {campo: fila.get(campo, "") for campo in COLUMNAS_DE_LA_COPIA}
    copia["revision_contenido"] = clasificar_fila(fila)
    copia["etiquetas"] = arreglo(etiquetas_de_campo(fila["etiquetas"]))
    return copia


# ----------------------------------------------------------------------
# Búsqueda de los catálogos en la computadora.
# ----------------------------------------------------------------------
class OrigenDeDatos:
    # Describe dónde está el archivo original de un catálogo en la computadora.
    # Atributos:
    #     fuente (str): «ventas» o «steam».
    #     ruta (Path): el archivo encontrado (CSV, JSON o ZIP).
    #     miembro (str): nombre del archivo dentro del ZIP; texto vacío si no es un ZIP.
    #     formato (str): «csv» o «json».

    def __init__(self, fuente, ruta, miembro, formato):
        # Guarda la ubicación (ver los atributos de la clase).
        self.fuente = fuente
        self.ruta = ruta
        self.miembro = miembro
        self.formato = formato

    def descripcion(self):
        # Devuelve el nombre que se muestra en pantalla, por ejemplo «archive.zip › games.csv».
        texto = self.ruta.name
        if self.miembro:
            texto += f" › {self.miembro}"
        return texto


def clasificar_contenido(inicio):
    # Reconoce de qué catálogo se trata leyendo el principio del archivo.
    # Se mira el contenido y no el nombre porque Kaggle entrega archivos con nombres que
    # cambian, como archive.zip o archive (1).zip.
    # Recibe:
    #     inicio (str): los primeros caracteres del archivo.
    # Devuelve:
    #     tuple o None: (fuente, formato), por ejemplo («steam», «csv»); None si no se
    #     parece a ningún catálogo conocido.
    resultado = None
    if inicio.lstrip().startswith("{"):
        # games.json es un gran objeto cuyos valores son fichas con nombre y fecha de lanzamiento.
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
    # Lee los primeros 64 KB de un archivo y los convierte en texto.
    # Recibe:
    #     binario: archivo abierto en modo binario (bytes).
    # Devuelve:
    #     str: el texto inicial; los bytes que no son texto válido se ignoran.
    return binario.read(65536).decode("utf-8-sig", errors="ignore")


def examinar_archivo(ruta):
    # Busca catálogos dentro de un archivo, que puede ser un ZIP con varios archivos.
    # Recibe:
    #     ruta (Path): archivo .csv, .json o .zip.
    # Devuelve:
    #     list[OrigenDeDatos]: los catálogos reconocidos; lista vacía si no hay ninguno o
    #     el archivo no se puede leer.
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
        # Un archivo dañado o abierto por otro programa no impide buscar en los demás.
        hallados = []
    return hallados


# ----------------------------------------------------------------------
# Copias reducidas de los catálogos.
# ----------------------------------------------------------------------
def unico_archivo_del_zip(paquete, ruta, terminacion):
    # Busca dentro de un ZIP el único archivo que termina de cierta forma.
    # Recibe:
    #     paquete (zipfile.ZipFile): el ZIP ya abierto.
    #     ruta (Path): ruta del ZIP; solo se usa en el mensaje de error.
    #     terminacion (str): por ejemplo «.csv».
    # Devuelve:
    #     str: el nombre del archivo dentro del ZIP.
    # Puede fallar:
    #     ValueError: si no hay exactamente un archivo con esa terminación.
    nombres = [n for n in paquete.namelist()
               if n.lower().endswith(terminacion) and not n.startswith("__MACOSX/")]
    if len(nombres) != 1:
        raise ValueError(f"{ruta.name} debe contener un único archivo {terminacion}.")
    return nombres[0]


def abrir_csv(ruta):
    # Abre un CSV suelto o el único CSV que hay dentro de una copia reducida (ZIP).
    # Se usa igual que open: «with abrir_csv(ruta) as datos:». Las copias reducidas son
    # pequeñas, así que su CSV se lee completo en memoria.
    # Recibe:
    #     ruta (Path): archivo .csv, o archivo .zip con exactamente un CSV.
    # Devuelve:
    #     Archivo de texto listo para leer.
    # Puede fallar:
    #     ValueError: si el ZIP no tiene exactamente un CSV.
    if ruta.suffix.lower() == ".csv":
        archivo = ruta.open(encoding="utf-8-sig", newline="")
    else:
        with zipfile.ZipFile(ruta) as paquete:
            nombre = unico_archivo_del_zip(paquete, ruta, ".csv")
            texto = paquete.read(nombre).decode("utf-8-sig")
        archivo = io.StringIO(texto, newline="")
    return archivo


def escribir_copia(entrada, formato, destino, nombre):
    # Escribe la copia reducida de un catálogo a partir del archivo original.
    # Recibe:
    #     entrada: archivo de texto abierto con el catálogo original.
    #     formato (str): «csv» o «json».
    #     destino (Path): archivo ZIP que se crea, con un solo catalogo.csv adentro.
    #     nombre (str): nombre del original; solo se usa en los mensajes.
    # Devuelve:
    #     int: cuántos juegos se copiaron.
    # Puede fallar:
    #     ValueError: si el original no tiene juegos.
    registros = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zip_salida:
        with zip_salida.open("catalogo.csv", "w") as binario:
            # TextIOWrapper convierte el texto del CSV en bytes, que es lo que guarda el ZIP.
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
                    # Se cuentan los juegos copiados para avisar cada 25 000, porque el CSV de
                    # Steam tarda en leerse. Se usa una lista para que la función copiar pueda
                    # cambiar el contador.
                    copiados = [0]

                    def copiar(fila):
                        # Escribe un renglón en la copia y avisa cada 25 000 juegos.
                        # Recibe:
                        #     fila (dict): renglón con las columnas de COLUMNAS_DEL_CATALOGO.
                        escritor.writerow(fila_de_copia(fila))
                        copiados[0] += 1
                        if copiados[0] % 25000 == 0:
                            print(f"  {copiados[0]:,} juegos preparados…", flush=True)
                    registros = recorrer_csv(entrada, nombre, copiar)[0]
    if registros == 0:
        raise ValueError(f"{nombre} no contiene juegos.")
    return registros


def preparar_copia(origen, destino):
    # Crea la copia reducida de un catálogo original.
    # El original se lee por pedazos, aunque esté dentro de un ZIP, sin descomprimirlo en
    # el disco. La copia se escribe primero con un nombre temporal y solo al final recibe
    # su nombre definitivo; así, si el programa se interrumpe, no queda una copia a medias.
    # Recibe:
    #     origen (OrigenDeDatos): el archivo original.
    #     destino (Path): la copia que se crea en datos_juegos.
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
    # Comprueba que una copia reducida esté completa y sea del catálogo correcto.
    # Las dos copias tienen las mismas columnas, pero en la de Steam cada juego tiene su
    # número de Steam (AppID) y en la de ventas cada juego tiene cifras de ventas.
    # Recibe:
    #     ruta (Path): la copia (ZIP).
    #     fuente (str): «ventas» o «steam».
    # Devuelve:
    #     bool: True si el ZIP no está dañado y alguno de sus primeros 64 juegos tiene
    #     título y el dato que corresponde a esa fuente.
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
    # Inventa el nombre de la copia reducida de un archivo original.
    # El nombre incluye un código calculado con la ruta, el tamaño y la fecha del original:
    # si el archivo cambia, el código cambia y se prepara una copia nueva.
    # Recibe:
    #     origen (OrigenDeDatos): el archivo original.
    # Devuelve:
    #     str: por ejemplo «steam_local_1a2b3c4d.csv.zip».
    datos = origen.ruta.stat()
    marca = f"contenido1|{origen.ruta.resolve()}|{origen.miembro}|{datos.st_size}|{datos.st_mtime_ns}"
    return f"{origen.fuente}_local_{zlib.crc32(marca.encode('utf-8')):08x}.csv.zip"


def copia_anterior(copias, fuente):
    # Busca la copia reducida más reciente que ya exista de una fuente.
    # Sirve, por ejemplo, cuando la carpeta datos_juegos se copió a otra computadora sin
    # los archivos originales.
    # Recibe:
    #     copias (Path): la carpeta datos_juegos.
    #     fuente (str): «ventas» o «steam».
    # Devuelve:
    #     Path o None: la copia legible más reciente, o None si no hay ninguna.
    anteriores = sorted(copias.glob(f"{fuente}_*.csv.zip"), key=lambda r: r.stat().st_mtime, reverse=True)
    elegida = None
    for ruta in anteriores:
        if elegida is None and copia_legible(ruta, fuente):
            elegida = ruta
    return elegida


def descargar_respuesta(respuesta, destino, fuente):
    # Guarda en un archivo lo que va llegando de una descarga.
    # Se escribe en pedazos de 1 MB para no tener el catálogo completo en memoria.
    # Recibe:
    #     respuesta: la conexión de descarga ya abierta.
    #     destino (Path): archivo donde se guarda (CSV o ZIP).
    #     fuente (str): «ventas» o «steam»; solo se usa en los mensajes.
    # Puede fallar:
    #     ValueError: si la descarga se corta antes de terminar.
    print(f"Descargando el catálogo de {NOMBRES_DE_FUENTE[fuente]} desde Kaggle…", flush=True)
    total = int(respuesta.headers.get("Content-Length") or 0)
    recibidos = 0
    siguiente_aviso = 10
    siguiente_megas = 25
    inicio = time.time()
    with destino.open("wb") as archivo:
        bloque = respuesta.read(1024 * 1024)
        while bloque:
            archivo.write(bloque)
            recibidos += len(bloque)
            transcurrido = max(time.time() - inicio, 1e-6)
            velocidad = recibidos / 1_000_000 / transcurrido
            # En archivos grandes, como el de Steam, se avisa cada 10 % con la velocidad y el
            # tiempo que falta. Si Kaggle no dice el tamaño, se avisa cada 25 MB.
            if total > 10_000_000 and recibidos * 100 >= total * siguiente_aviso:
                faltan = (total - recibidos) / 1_000_000 / velocidad
                print(f"  {siguiente_aviso} % ({recibidos // 1_000_000:,} de {total // 1_000_000:,} MB, "
                      f"{velocidad:.1f} MB/s, faltan unos {faltan:.0f} s)", flush=True)
                siguiente_aviso += 10
            elif not total and recibidos >= siguiente_megas * 1_000_000:
                print(f"  {recibidos // 1_000_000:,} MB recibidos ({velocidad:.1f} MB/s)", flush=True)
                siguiente_megas += 25
            bloque = respuesta.read(1024 * 1024)
    if total and recibidos != total:
        raise ValueError(f"La descarga se interrumpió al recibir {recibidos} de {total} bytes.")


def credenciales_de_kaggle():
    # Busca una cuenta de Kaggle por si algún día Kaggle no deja descargar sin cuenta.
    # Hoy Kaggle deja descargar sin cuenta estos catálogos, así que normalmente no se usa.
    # Si se usa, se lee de las variables KAGGLE_USERNAME y KAGGLE_KEY o del archivo
    # ~/.kaggle/kaggle.json. La clave nunca se escribe en este programa.
    # Devuelve:
    #     str: el texto de autorización («Basic …»); texto vacío si no hay cuenta.
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
    # Abre la conexión con Kaggle, sin descargar todavía el contenido.
    # Recibe:
    #     url (str): dirección del archivo en Kaggle.
    # Devuelve:
    #     La conexión abierta; se usa con with.
    # Puede fallar:
    #     OSError (incluye HTTPError): si no hay internet o Kaggle rechaza la petición
    #     incluso con cuenta.
    peticion = Request(url, headers={"User-Agent": "RecomendadorVideojuegos/4.0"})
    try:
        respuesta = urlopen(peticion, timeout=60)
    except HTTPError as error:
        autorizacion = credenciales_de_kaggle()
        if error.code not in (401, 403) or not autorizacion:
            raise
        # Kaggle manda la descarga a otro servidor. add_unredirected_header hace que la
        # clave solo vaya a Kaggle y no a ese otro servidor.
        peticion = Request(url, headers={"User-Agent": "RecomendadorVideojuegos/4.0"})
        peticion.add_unredirected_header("Authorization", autorizacion)
        respuesta = urlopen(peticion, timeout=60)
    return respuesta


def huella_de_respuesta(respuesta):
    # Calcula una «huella» de la versión del archivo que ofrece Kaggle.
    # Los datos de la respuesta (encabezados) llegan antes que el archivo. ETag y
    # Last-Modified cambian cuando el autor publica una versión nueva; comparar la huella
    # con la guardada dice si hay datos nuevos sin tener que descargar nada.
    # Recibe:
    #     respuesta: la conexión abierta con abrir_descarga.
    # Devuelve:
    #     str: la huella; texto vacío si Kaggle no envió esos datos.
    etiqueta = respuesta.headers.get("ETag", "")
    modificado = respuesta.headers.get("Last-Modified", "")
    tamano = respuesta.headers.get("Content-Length", "")
    huella = ""
    if etiqueta or modificado:
        huella = f"{etiqueta}|{modificado}|{tamano}"
    return huella


def leer_registro(copias):
    # Lee qué versión de cada catálogo se descargó la última vez.
    # Recibe:
    #     copias (Path): la carpeta datos_juegos.
    # Devuelve:
    #     dict: fuente → {«huella», «copia» (nombre del archivo), «fecha» y «consulta»
    #     (en segundos)}. Diccionario vacío si todavía no se descargó nada.
    registro = {}
    try:
        leido = json.loads((copias / NOMBRE_DEL_REGISTRO_DE_KAGGLE).read_text(encoding="utf-8"))
        if isinstance(leido, dict):
            registro = {f: d for f, d in leido.items() if f in FUENTES_DE_KAGGLE and isinstance(d, dict)}
    except (OSError, ValueError):
        registro = {}
    return registro


def guardar_registro(copias, registro):
    # Guarda el registro de descargas. Se escribe con un nombre temporal y luego se le
    # cambia el nombre, para que un apagón no deje el archivo a medias.
    # Recibe:
    #     copias (Path): la carpeta datos_juegos.
    #     registro (dict): lo que devolvió leer_registro, ya actualizado.
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=copias, delete=False) as temporal:
            json.dump(registro, temporal, ensure_ascii=False, indent=2)
        Path(temporal.name).replace(copias / NOMBRE_DEL_REGISTRO_DE_KAGGLE)
    except OSError as error:
        print(f"No se pudo guardar el registro de descargas. {error}")


def actualizar_desde_kaggle(copias, fuente, registro):
    # Decide si hay que revisar Kaggle y, si hay una versión nueva, la descarga.
    # Si la copia guardada sirve y Kaggle se revisó hace menos de DIAS_ENTRE_CONSULTAS
    # días, no se usa internet. Si no, se revisa Kaggle con consultar_kaggle.
    # Recibe:
    #     copias (Path): la carpeta datos_juegos.
    #     fuente (str): «ventas» o «steam».
    #     registro (dict): registro de descargas; se actualiza si se consulta Kaggle.
    # Devuelve:
    #     Path: la copia reducida lista para leer.
    # Puede fallar:
    #     OSError o ValueError: si no hay internet o la descarga no sirve.
    url = f"{API_DE_KAGGLE}{FUENTES_DE_KAGGLE[fuente]}/{ARCHIVOS_DE_KAGGLE[fuente]}"
    anterior = registro.get(fuente, {})
    copia = copias / str(anterior.get("copia", "") or f"{fuente}_kaggle.csv.zip")
    copia_valida = bool(anterior) and copia_legible(copia, fuente)
    # Los registros de versiones anteriores solo guardaban la fecha de la descarga.
    ultima_consulta = numero(anterior.get("consulta")) or numero(anterior.get("fecha")) or 0
    if copia_valida and time.time() - ultima_consulta < DIAS_ENTRE_CONSULTAS * 86400:
        dias = (time.time() - ultima_consulta) / 86400
        print(f"Catálogo de {NOMBRES_DE_FUENTE[fuente]}: se usa la copia guardada "
              f"(Kaggle se revisó hace {dias:.1f} días).", flush=True)
        destino = copia
    else:
        destino = consultar_kaggle(copias, fuente, registro, url, copia, copia_valida)
    return destino


def consultar_kaggle(copias, fuente, registro, url, copia, copia_valida):
    # Compara la huella de Kaggle con la guardada y descarga el catálogo si cambió.
    # Si Kaggle no envía huella, se vuelve a descargar cuando la copia tiene más de
    # DIAS_SIN_HUELLA días.
    # Recibe:
    #     copias (Path): la carpeta datos_juegos.
    #     fuente (str): «ventas» o «steam».
    #     registro (dict): registro de descargas; se actualiza con esta consulta.
    #     url (str): dirección del archivo en Kaggle.
    #     copia (Path): la copia guardada de la última descarga.
    #     copia_valida (bool): True si esa copia se puede leer.
    # Devuelve:
    #     Path: la copia reducida lista para leer.
    # Puede fallar:
    #     OSError o ValueError: si no hay internet o la descarga no sirve.
    anterior = registro.get(fuente, {})
    print(f"Consultando en Kaggle el catálogo de {NOMBRES_DE_FUENTE[fuente]}…", flush=True)
    with abrir_descarga(url) as respuesta:
        huella = huella_de_respuesta(respuesta)
        if huella:
            sin_cambios = copia_valida and huella == anterior.get("huella")
        else:
            antiguedad = time.time() - (numero(anterior.get("fecha")) or 0)
            sin_cambios = copia_valida and antiguedad < DIAS_SIN_HUELLA * 86400
        if sin_cambios:
            # No hay versión nueva: al salir del with se cierra la conexión sin descargar nada.
            print("  Kaggle no tiene una versión nueva; se usa la descarga guardada.", flush=True)
            destino = copia
            registro[fuente] = dict(anterior, consulta=int(time.time()))
        else:
            destino = copias / f"{fuente}_kaggle.csv.zip"
            # Hay versión nueva: se descarga en una carpeta temporal que se borra al terminar.
            with tempfile.TemporaryDirectory(dir=copias) as temporal:
                descarga = Path(temporal) / ARCHIVOS_DE_KAGGLE[fuente]
                descargar_respuesta(respuesta, descarga, fuente)
                # Kaggle puede entregar el CSV suelto o dentro de un ZIP.
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
            ahora = int(time.time())
            registro[fuente] = {"huella": huella, "copia": destino.name, "fecha": ahora, "consulta": ahora}
    return destino


def originales_junto_al_programa(carpeta):
    # Busca catálogos que alguien haya descargado a mano y dejado junto al programa.
    # Es el último recurso, si no hay internet ni copias guardadas. Solo se revisa la
    # carpeta del programa (no sus subcarpetas ni Descargas), para no usar sin querer un
    # archivo viejo de otra carpeta.
    # Recibe:
    #     carpeta (Path): la carpeta del programa.
    # Devuelve:
    #     dict[str, list[OrigenDeDatos]]: fuente → archivos encontrados; primero los CSV.
    encontrados = {}
    for ruta in sorted(carpeta.iterdir()):
        if ruta.is_file() and ruta.suffix.lower() in (".csv", ".json", ".zip"):
            for origen in examinar_archivo(ruta):
                encontrados.setdefault(origen.fuente, []).append(origen)
    for lista in encontrados.values():
        lista.sort(key=lambda origen: origen.formato == "json")
    return encontrados


def obtener_fuente(carpeta, fuente, registro):
    # Consigue la copia reducida de un catálogo, lista para leer.
    # Se intenta en este orden:
    #   1. Kaggle: se descarga si hay versión nueva.
    #   2. Si Kaggle no responde: la última copia guardada en datos_juegos.
    #   3. Si nunca se descargó: un archivo de Kaggle dejado junto al programa.
    # Recibe:
    #     carpeta (Path): la carpeta del programa.
    #     fuente (str): «ventas» o «steam».
    #     registro (dict): registro de descargas.
    # Devuelve:
    #     Path: la copia reducida (un ZIP con un CSV).
    # Puede fallar:
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
    # Prepara los dos catálogos y devuelve los que se pudieron conseguir.
    # Recibe:
    #     carpeta (Path): la carpeta del programa.
    # Devuelve:
    #     dict[str, Path]: fuente → copia reducida, con uno o dos catálogos.
    # Puede fallar:
    #     ValueError: si no se consiguió el catálogo de Steam, que es el que arma las listas.
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
# Catálogo unificado: junta los dos catálogos en una sola colección de juegos.
# ----------------------------------------------------------------------
def fecha_del_catalogo(texto):
    # Lee el año y, si se puede, el día exacto de una fecha del catálogo.
    # Steam escribe las fechas en inglés («Mar 5, 2026») aunque Spyder esté en español.
    # Recibe:
    #     texto (str): fecha tal como viene, por ejemplo «Mar 5, 2026», «2026-03-05»,
    #         «2026» o «Q3 2026».
    # Devuelve:
    #     tuple: (año o None, fecha completa o None). Si solo se anuncia el año o el
    #     trimestre, la fecha completa es None.
    coincidencia = re.search(r"\b(?:19[5-9]\d|20\d{2})\b", texto)
    # Si el texto no tiene ningún año, no se sabe nada de la fecha.
    resultado = (None, None)
    if coincidencia:
        anio = int(coincidencia.group())
        meses = "jan feb mar apr may jun jul aug sep oct nov dec".split()
        partes = re.findall(r"[a-z]+|\d+", texto.lower())
        # Un año o un trimestre anunciado no dice el día del estreno; se intenta leer el día.
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
    # Pide datos a la tienda de Steam y los devuelve ya convertidos de JSON.
    # Recibe:
    #     url (str): dirección de la consulta.
    # Devuelve:
    #     dict: la respuesta de Steam.
    # Puede fallar:
    #     OSError o HTTPException: si no hay internet o Steam no responde en 7 segundos;
    #     ValueError: si la respuesta no es JSON.
    solicitud = Request(url, headers={"User-Agent": "RecomendadorDeJuegos/1.0"})
    with urlopen(solicitud, timeout=7) as respuesta:
        datos = json.load(respuesta)
    return datos


def guardar_json(archivo, datos, fecha=None):
    # Guarda datos en un archivo JSON sin riesgo de dejarlo a medias: primero se escribe
    # con un nombre temporal y al final se le cambia el nombre.
    # Recibe:
    #     archivo (Path): el archivo de destino dentro de datos_juegos.
    #     datos (dict o list): lo que se guarda.
    #     fecha (float o None): fecha de modificación que se le pone al archivo, en
    #         segundos; None deja la fecha actual. Sirve para que, después de una consulta
    #         fallida, se vuelva a intentar antes de lo normal.
    # Puede fallar:
    #     OSError: si no se puede escribir en la carpeta.
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=archivo.parent, delete=False) as temporal:
        json.dump(datos, temporal, ensure_ascii=False)
    Path(temporal.name).replace(archivo)
    if fecha is not None:
        os.utime(archivo, (fecha, fecha))


def consolas_de_wikidata(carpeta):
    # Pregunta a Wikidata (una enciclopedia de datos abierta) en qué consolas salió cada
    # juego de Steam. Solo cuenta una ficha de Wikidata que tenga a la vez el número de
    # Steam del juego y la consola. La respuesta se guarda siete días.
    # Recibe:
    #     carpeta (Path): la carpeta del programa.
    # Devuelve:
    #     dict[str, list[str]]: número de Steam → consolas, por ejemplo
    #     {"2362050": ["PS5", "Xbox Series X/S"]}. Si Wikidata no responde, devuelve lo
    #     último que se guardó (puede estar vacío).
    archivo = carpeta / NOMBRE_DE_LAS_COPIAS / "consolas_wikidata.json"
    consolas, vigente = copia_de_consolas(archivo)
    # Solo se pregunta a Wikidata si la copia guardada tiene siete días o más.
    if not vigente:
        try:
            consolas = preguntar_a_wikidata()
            fecha = None
        except (OSError, ValueError, KeyError, TypeError, HTTPException) as error:
            print(f"No se pudo actualizar Wikidata. Se usarán las plataformas documentadas disponibles. {error}")
            # Se guarda lo que había con una fecha de hace seis días, para volver a intentar
            # dentro de un día y no cada vez que se abre el programa.
            fecha = time.time() - 6 * 86400
        try:
            guardar_json(archivo, consolas, fecha)
        except OSError as error:
            print(f"No se pudo guardar la copia de plataformas. {error}")
    return consolas


def copia_de_consolas(archivo):
    # Lee la copia guardada de las consolas de Wikidata.
    # Recibe:
    #     archivo (Path): el archivo consolas_wikidata.json de datos_juegos.
    # Devuelve:
    #     tuple: (consolas guardadas, True si la copia tiene menos de siete días). Si la
    #     copia no existe o no se puede leer, devuelve ({}, False).
    anteriores = {}
    vigente = False
    try:
        guardados = json.loads(archivo.read_text(encoding="utf-8"))
        if isinstance(guardados, dict):
            # Solo se conservan los juegos con número de Steam y consolas conocidas.
            anteriores = {a: ps for a, ps in guardados.items() if a.isdigit() and isinstance(ps, list)
                          and all(p in PAGINAS_DE_CONSOLAS.values() for p in ps)}
            # Una copia de menos de siete días se usa aunque esté vacía; así una consulta que
            # falló no se repite cada vez que se abre el programa.
            vigente = time.time() - archivo.stat().st_mtime < 7 * 86400
    except (OSError, ValueError):
        # Si la copia no se puede leer, se pregunta otra vez a Wikidata.
        anteriores = {}
        vigente = False
    return anteriores, vigente


def preguntar_a_wikidata():
    # Pregunta a Wikidata en qué consolas salió cada juego reciente de Steam.
    # Devuelve:
    #     dict[str, list[str]]: número de Steam → consolas.
    # Puede fallar:
    #     OSError o HTTPException: si no hay internet o Wikidata no responde en 45 segundos;
    #     ValueError, KeyError o TypeError: si la respuesta viene vacía o con otra forma.
    # Se arma la pregunta: juegos de las consolas de PAGINAS_DE_CONSOLAS que tengan número
    # de Steam y fecha de salida desde ANIO_DESDE.
    paginas = " ".join(f"<https://en.wikipedia.org/wiki/{p}>" for p in PAGINAS_DE_CONSOLAS)
    consulta = (f"SELECT DISTINCT ?app ?pagina WHERE {{ VALUES ?pagina {{ {paginas} }} "
                "?pagina schema:about ?plataforma . ?juego wdt:P400 ?plataforma; wdt:P1733 ?app; wdt:P577 ?fecha . "
                f'FILTER(?fecha >= "{ANIO_DESDE}-01-01T00:00:00Z"^^xsd:dateTime) }}')
    url = "https://query.wikidata.org/sparql?" + urlencode({"query": consulta, "format": "json"})
    print("Consultando en Wikidata las consolas de cada juego…", flush=True)
    peticion = Request(url, headers={"User-Agent": "RecomendadorDeJuegos/1.0"})
    with urlopen(peticion, timeout=45) as respuesta:
        filas = json.load(respuesta)["results"]["bindings"]
    # Cada respuesta une un número de Steam con una consola; se agrupan por juego.
    consolas = {}
    for fila in filas:
        appid = fila["app"]["value"]
        modelo = PAGINAS_DE_CONSOLAS.get(fila["pagina"]["value"].rsplit("/", 1)[-1])
        if appid.isdigit() and modelo:
            consolas.setdefault(appid, []).append(modelo)
    if not consolas:
        raise ValueError("consulta vacía")
    return consolas


# Números con los que Steam identifica sus etiquetas de género (por ejemplo, 1667 es
# «Horror») y el género del cuestionario que les corresponde.
GENEROS_POR_TAG = {9: "Estrategia", 19: "Acción", 21: "Aventura", 122: "Rol", 492: "Independiente",
                   597: "Casual", 599: "Simulación", 699: "Carreras", 701: "Deportes", 1625: "Plataformas",
                   1664: "Rompecabezas", 1667: "Terror", 1721: "Terror psicológico", 1743: "Lucha",
                   1774: "Disparos", 3978: "Terror"}


def pedir_etiquetas(lote):
    # Pide a la tienda de Steam las etiquetas de un grupo de juegos.
    # Recibe:
    #     lote (list[str]): hasta 50 números de Steam.
    # Devuelve:
    #     dict[str, list[int]]: número de Steam → sus etiquetas, de la más votada a la
    #     menos votada. Solo incluye los juegos que Steam devolvió bien.
    # Puede fallar:
    #     OSError, HTTPException, ValueError, TypeError o KeyError: si Steam no responde o
    #     la respuesta no tiene la forma esperada.
    peticion = {"ids": [{"appid": int(a)} for a in lote],
                "context": {"language": "english", "country_code": "US"},
                "data_request": {"include_tag_count": 20}}
    url = "https://api.steampowered.com/IStoreBrowseService/GetItems/v1/?" + urlencode(
        {"input_json": json.dumps(peticion, separators=(",", ":"))})
    recibidas = {}
    for producto in consultar_tienda(url)["response"]["store_items"]:
        appid = str(producto.get("id"))
        if appid in lote and producto.get("success") == 1:
            recibidas[appid] = etiquetas_por_votos(producto)
    return recibidas


def etiquetas_por_votos(producto):
    # Ordena las etiquetas de un juego de la más votada a la menos votada.
    # En Steam las etiquetas las ponen los jugadores. Las últimas suelen tener muy pocos
    # votos y a veces son bromas: por ejemplo, un juego de peleas tenía «Psychological
    # Horror» en el lugar 11. Por eso importa el orden.
    # Recibe:
    #     producto (dict): ficha de Steam. Su campo tags es una lista de {tagid, weight}
    #         (etiqueta y peso, es decir, votos); si falta, se usa tagids, la lista simple.
    # Devuelve:
    #     list[int]: números de etiqueta, del mayor peso al menor.
    pesadas = [t for t in (producto.get("tags") or []) if isinstance(t, dict) and "tagid" in t]
    ordenadas = list(producto.get("tagids") or [])
    if pesadas:
        # sorted no cambia el orden de Steam entre dos etiquetas con el mismo peso.
        ordenadas = [t["tagid"] for t in sorted(pesadas, key=lambda t: -(numero(t.get("weight")) or 0))]
    return ordenadas


def completar_generos(juegos, carpeta):
    # Agrega a cada juego reciente los géneros que salen de sus etiquetas de Steam.
    # Kaggle a veces trae solo géneros muy generales (como «Acción») y ninguna etiqueta;
    # Steam sí da las etiquetas de cada juego. Se guardan 30 días en el archivo
    # etiquetas_steam.sqlite3. También se guarda que Steam no devolvió un juego, para no
    # volver a preguntarlo cada vez.
    # Recibe:
    #     juegos (dict[str, FichaDeJuego]): las fichas del catálogo. Se les agregan
    #         géneros, y apto se vuelve False si Steam marca contenido sexual.
    #     carpeta (Path): la carpeta datos_juegos.
    actuales = {j.appid: j for j in juegos.values() if j.appid and j.es_recomendable()}
    ahora = int(time.time())
    conexion = sqlite3.connect(carpeta / "etiquetas_steam.sqlite3", timeout=10)
    try:
        # Las versiones anteriores guardaban las etiquetas en la tabla «etiquetas», sin el
        # orden de votos; por eso ahora se usa una tabla nueva.
        conexion.execute("CREATE TABLE IF NOT EXISTS etiquetas_por_votos "
                         "(appid TEXT PRIMARY KEY, tags TEXT, fecha INTEGER)")
        guardadas = {appid: (json.loads(tags), fecha) for appid, tags, fecha in
                     conexion.execute("SELECT appid, tags, fecha FROM etiquetas_por_votos")}
        # Juegos sin etiquetas guardadas o con etiquetas de hace más de 30 días, en grupos de 50.
        pendientes = [a for a in actuales if a not in guardadas or ahora - guardadas[a][1] > 30 * 86400]
        lotes = [pendientes[i:i + 50] for i in range(0, len(pendientes), 50)]
        if lotes:
            print(f"Actualizando las etiquetas de género de Steam de {len(pendientes):,} juegos "
                  "(solo la primera vez o cada 30 días)…", flush=True)
        # Se hacen cuatro consultas de 50 juegos al mismo tiempo (una «ronda»). Si en una
        # ronda no responde ninguna, se deja de preguntar y se usan los datos guardados.
        steam_responde = True
        indice = 0
        siguiente_aviso = 10
        with ThreadPoolExecutor(max_workers=4) as consultas:
            while indice < len(lotes) and steam_responde:
                ronda = lotes[indice:indice + 4]
                indice += len(ronda)
                trabajos = [(lote, consultas.submit(pedir_etiquetas, lote)) for lote in ronda]
                respondidas = 0
                for lote, trabajo in trabajos:
                    try:
                        recibidas = trabajo.result()
                        respondidas += 1
                    except (OSError, HTTPException, ValueError, TypeError, KeyError):
                        recibidas = None
                    if recibidas is not None:
                        for appid in lote:
                            # Si Steam no devolvió el juego, se conservan sus etiquetas anteriores.
                            tags = recibidas.get(appid, guardadas.get(appid, ([], 0))[0])
                            guardadas[appid] = tags, ahora
                            conexion.execute("INSERT OR REPLACE INTO etiquetas_por_votos VALUES (?, ?, ?)",
                                             (appid, json.dumps(tags), ahora))
                conexion.commit()
                steam_responde = respondidas > 0
                if len(lotes) >= 10 and indice * 100 >= len(lotes) * siguiente_aviso:
                    print(f"  {indice * 100 // len(lotes)} % de las etiquetas", flush=True)
                    siguiente_aviso = indice * 100 // len(lotes) // 10 * 10 + 10
        if not steam_responde:
            print("Steam no respondió. Se usarán los géneros del catálogo y las etiquetas guardadas.")
        # Con las etiquetas ya guardadas se completa cada ficha.
        for appid, juego in actuales.items():
            tags = guardadas.get(appid, ([], 0))[0]
            # Para sacar un juego por contenido sexual basta cualquier etiqueta, aunque tenga
            # pocos votos (6650, 9130 y 12095 son desnudez y contenido sexual).
            if set(tags) & {6650, 9130, 12095}:
                juego.apto = False
            # Para asignar un género solo cuentan las etiquetas más votadas.
            principales = tags[:ETIQUETAS_QUE_DEFINEN_GENERO]
            nuevos = {GENEROS_POR_TAG[t] for t in principales if t in GENEROS_POR_TAG}
            if "Terror psicológico" in nuevos:
                nuevos.add("Terror")
            juego.generos.update(nuevos)
            juego.atributos.update(("genero", normalizar(g)) for g in nuevos)
    finally:
        conexion.close()


def producto_de_steam(appid):
    # Pide a la tienda de Steam la ficha pública de un juego.
    # Recibe:
    #     appid (str): número de Steam del juego.
    # Devuelve:
    #     dict: la ficha (nombre, tipo, fecha, géneros, avisos de contenido…); diccionario
    #     vacío si Steam no la tiene.
    # Puede fallar:
    #     Los mismos errores que consultar_tienda.
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=english"
    respuesta = consultar_tienda(url)
    return respuesta.get(appid, {}).get("data", {})


def revisar_producto(producto):
    # Revisa los avisos de contenido de la ficha de un juego en la tienda de Steam.
    # Steam usa números: 1, 3 y 4 son desnudez o contenido sexual, 2 es violencia y 5 es
    # contenido para mayores en general.
    # Recibe:
    #     producto (dict): ficha de producto_de_steam.
    # Devuelve:
    #     str: «excluir» si no es un juego, es solo para adultos o tiene desnudez o
    #     contenido sexual; «revisado» si sus avisos son solo de violencia o madurez (o no
    #     tiene avisos); texto vacío si no se puede saber.
    # Si la ficha está vacía o no tiene nombre, no se puede saber nada.
    resultado = ""
    if producto and producto.get("name"):
        avisos = producto.get("content_descriptors") or {}
        esrb = (producto.get("ratings") or {}).get("esrb") or {}
        # Primero se descarta lo que no es un juego, lo que es solo para adultos y lo que
        # tiene palabras de contenido sexual.
        if (producto.get("type") != "game" or normalizar(str(esrb.get("rating", ""))) in ("ao", "adults only")
                or hay_contenido_sexual(producto["name"], avisos.get("notes"), esrb.get("descriptors"),
                                        producto.get("genres"), producto.get("short_description"))):
            resultado = "excluir"
        else:
            # Después se revisan los números de aviso, si Steam los envió como lista.
            ids = avisos.get("ids")
            if isinstance(ids, list):
                indicadores = {str(valor) for valor in ids}
                # Una lista de avisos vacía también es una respuesta válida de Steam. Un
                # número de aviso desconocido deja el juego sin revisar.
                if indicadores & {"1", "3", "4"}:
                    resultado = "excluir"
                elif indicadores <= {"2", "5"}:
                    resultado = "revisado"
    return resultado


def ficha_de_la_tienda(appid):
    # Convierte la ficha de la tienda de un juego anunciado en un renglón del catálogo.
    # La ficha sirve para distinguir juegos de contenidos adicionales (DLC) y anuncios sin
    # fecha.
    # Recibe:
    #     appid (str): número de Steam del juego.
    # Devuelve:
    #     dict o None: renglón con las columnas de COLUMNAS_DE_LA_COPIA más «anunciado»
    #     (True si todavía no sale); None si no es un juego o Steam no dice si ya salió.
    producto = producto_de_steam(appid)
    fila = None
    # Solo sirven los juegos con nombre que dicen si ya salieron o todavía no.
    if producto.get("type") == "game" and producto.get("name"):
        lanzamiento = producto.get("release_date", {})
        if isinstance(lanzamiento.get("coming_soon"), bool):
            fila = dict.fromkeys(COLUMNAS_DE_LA_COPIA, "")
            fila.update(identificador=appid, titulo=producto["name"], anio=lanzamiento.get("date") or "",
                        anunciado=lanzamiento["coming_soon"], revision_contenido=revisar_producto(producto),
                        genero=json.dumps([g["description"] for g in producto.get("genres", [])]),
                        desarrollador=json.dumps(producto.get("developers", [])))
            for plataforma in ("windows", "mac", "linux"):
                fila[plataforma] = str(producto.get("platforms", {}).get(plataforma, False))
    return fila


def anuncios_de_steam(carpeta):
    # Consigue los próximos lanzamientos más deseados de Steam, porque el catálogo de
    # Kaggle no trae juegos anunciados después de que se armó. La lista se guarda siete días.
    # Recibe:
    #     carpeta (Path): la carpeta del programa.
    # Devuelve:
    #     list[dict]: hasta 16 renglones como los de ficha_de_la_tienda. Si la tienda no
    #     responde, devuelve los últimos que se guardaron.
    archivo = carpeta / NOMBRE_DE_LAS_COPIAS / "lanzamientos_steam.json"
    anteriores, vigente = copia_de_anuncios(archivo)
    fichas = list(anteriores.values())
    # Un anuncio sin revisión también se acepta: candidatos_revisados lo revisa antes de
    # recomendarlo. Solo se pregunta a la tienda si la copia es vieja o está vacía.
    if not (vigente and anteriores):
        try:
            nuevas = preguntar_por_anuncios(anteriores)
        except (OSError, ValueError, HTTPException, KeyError, TypeError, AttributeError) as error:
            print(f"No se pudieron actualizar los anuncios de Steam. Se usarán los datos guardados. {error}")
            nuevas = None
        # Si la tienda respondió, se usan y se guardan los anuncios nuevos.
        if nuevas is not None:
            fichas = nuevas
            try:
                guardar_json(archivo, fichas)
            except OSError as error:
                print(f"No se pudo guardar la copia de los anuncios para otra sesión. {error}")
    return fichas


def copia_de_anuncios(archivo):
    # Lee la copia guardada de los anuncios de la tienda de Steam.
    # Recibe:
    #     archivo (Path): el archivo lanzamientos_steam.json de datos_juegos.
    # Devuelve:
    #     tuple: (número de Steam → renglón del anuncio, True si la copia tiene menos de
    #     siete días). Si la copia no existe o no se puede leer, devuelve ({}, False).
    anteriores = {}
    vigente = False
    try:
        registros = json.loads(archivo.read_text(encoding="utf-8"))
        vigente = time.time() - archivo.stat().st_mtime < 7 * 86400
        if isinstance(registros, list):
            for fila in registros:
                if isinstance(fila, dict):
                    # Las versiones anteriores guardaban el anuncio sin su revisión de contenido.
                    # Una revisión de más de siete días se vuelve a hacer.
                    fila.setdefault("revision_contenido", "")
                    if not vigente and fila["revision_contenido"] == "revisado":
                        fila["revision_contenido"] = ""
                # Solo se conservan los renglones completos.
                if (isinstance(fila, dict) and isinstance(fila.get("anunciado"), bool)
                        and all(isinstance(fila.get(campo), str) for campo in COLUMNAS_DE_LA_COPIA)):
                    anteriores[fila["identificador"]] = fila
    except ERRORES_DE_DATOS:
        # Si la copia no se puede leer, se pregunta otra vez a la tienda.
        anteriores = {}
        vigente = False
    return anteriores, vigente


def preguntar_por_anuncios(anteriores):
    # Pide a la tienda de Steam los 16 juegos por salir más agregados a listas de deseos, y
    # la ficha de cada uno (cuatro consultas al mismo tiempo).
    # Recibe:
    #     anteriores (dict): anuncios guardados; se usan para un juego cuya ficha no llegó.
    # Devuelve:
    #     list[dict]: renglones como los de ficha_de_la_tienda.
    # Puede fallar:
    #     OSError, HTTPException, KeyError, TypeError o AttributeError: si la tienda no
    #     responde bien; ValueError: si no llegó la lista o ninguna ficha.
    print("Consultando los próximos lanzamientos en la tienda de Steam…", flush=True)
    url = ("https://store.steampowered.com/search/results/?filter=popularwishlist"
           "&category1=998&infinite=1&count=16&cc=us&l=english")
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
                # Si una ficha no llega, se usa la guardada de ese juego, si había.
                fila = anteriores.get(appid)
            if fila:
                fichas.append(fila)
    if not fichas or not consultas_exitosas:
        raise ValueError("Ninguna ficha de la tienda estuvo disponible.")
    return fichas


class FichaDeJuego:
    # Ficha de un juego que junta los datos de todos los renglones que hablan de él.
    # Atributos:
    #     titulo (str): nombre que se muestra, como aparece en el primer catálogo.
    #     anio (int o None): año de su primer lanzamiento conocido.
    #     fecha (date o None): día exacto del estreno, si se conoce.
    #     anunciado (bool): True si todavía no sale.
    #     periodo (str): fecha anunciada tal como la escribe la tienda, por ejemplo «Q3 2026».
    #     saga (str): nombre de la saga sin mayúsculas ni acentos, o texto vacío.
    #     generos (set[str]): géneros que se muestran, en español cuando hay traducción.
    #     plataformas (set[str]): plataformas que se muestran, por ejemplo {«PS2», «PC»}.
    #     atributos (set[tuple]): los rasgos con los que el modelo aprende gustos; cada uno
    #         es (tipo, valor), con tipo «genero», «tema» (etiqueta o saga) o «estudio».
    #     calidad_publica (float): nota de las reseñas, entre 0 y 1; vale 0.65 mientras
    #         no haya opiniones.
    #     evidencia_publica (float): cuántas opiniones respaldan esa nota.
    #     popularidad (float): qué tan vendido o reseñado es, entre 0 y 1.
    #     en_steam (bool): True si el juego está en Steam.
    #     appid (str): número de Steam del juego; texto vacío si no está en Steam.
    #     contenido_revisado (bool): True si ya se comprobó que no tiene contenido sexual.
    #     con_ventas (bool): True si aparece en el catálogo de ventas.
    #     apto (bool): False si es contenido para adultos o un programa que no es un juego.

    def __init__(self, titulo):
        # Crea una ficha vacía.
        # Recibe:
        #     titulo (str): nombre del juego.
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
        # Dice si el juego se puede recomendar.
        # Devuelve:
        #     bool: True si es de ANIO_DESDE en adelante (o está anunciado sin año), es apto
        #     y se conocen su género y su plataforma. Para un estreno no hacen falta
        #     reseñas; si las tiene, ajustan su nota.
        reciente = self.anio >= ANIO_DESDE if self.anio is not None else self.anunciado
        return bool(reciente and self.apto and self.generos and self.plataformas)


def resena_publica(fila):
    # Calcula la nota de las reseñas de un renglón, cuántas opiniones la respaldan y qué
    # tan popular es el juego.
    # Una nota con pocas opiniones no es confiable, así que se acerca a 0.65: es como sumar
    # 20 opiniones inventadas, 13 a favor y 7 en contra (a esto se le llama suavizado
    # bayesiano). Por ejemplo, 2 opiniones a favor de 2 dan (2 + 13) / (2 + 20) ≈ 0.68,
    # no 1.0.
    # Recibe:
    #     fila (dict): renglón con las columnas de COLUMNAS_DEL_CATALOGO.
    # Devuelve:
    #     tuple: (nota, opiniones, popularidad). nota está entre 0 y 1, o es None si no
    #     hay opiniones; opiniones es cuántas hay (0 si ninguna); popularidad está entre
    #     0 y 1.
    positivas = numero(fila["positivas"])
    negativas = numero(fila["negativas"])
    nota_usuario = numero(fila["nota"])
    critica = numero(fila["critica"])
    ventas = numero(fila["ventas"])
    votos_de_steam = (positivas or 0.0) + (negativas or 0.0)
    nota = None
    opiniones = 0.0
    # Cada catálogo califica distinto: votos de Steam, nota de usuarios o nota de la
    # crítica. Se usa la primera que exista, en ese orden.
    if positivas is not None and votos_de_steam > 0:
        opiniones = votos_de_steam
        nota = (positivas + 13) / (votos_de_steam + 20)
    elif nota_usuario is not None and 0 < nota_usuario <= 10:
        opiniones = numero(fila["usuarios"]) or 1.0
        nota = (opiniones * nota_usuario / 10 + 13) / (opiniones + 20)
    elif critica is not None and 0 < critica <= 100:
        opiniones = 0.5  # La nota de la crítica cuenta como media opinión: es solo un respaldo.
        nota = 0.5 * (critica / 100 + 0.65)
    # La popularidad crece despacio (logaritmo) para que los grandes éxitos no opaquen a
    # los demás juegos.
    popularidad = 0.0
    if ventas is not None:
        popularidad = min(1.0, math.log1p(ventas) / math.log1p(30))
    elif votos_de_steam > 0:
        popularidad = min(1.0, math.log1p(votos_de_steam) / math.log1p(25000))
    return nota, opiniones, popularidad


def columnas_del_archivo(nombres):
    # Busca en un archivo las columnas que usa el programa.
    # Recibe:
    #     nombres (list[str]): los nombres de columna del archivo.
    # Devuelve:
    #     dict[str, str o None]: nombre interno (por ejemplo «titulo») → nombre en el
    #     archivo (por ejemplo «Name»), o None si el archivo no tiene esa columna.
    disponibles = {}
    for columna in nombres:
        disponibles[normalizar(columna)] = columna
    campos = {}
    for destino, alias in COLUMNAS_DEL_CATALOGO.items():
        # El nombre interno se busca primero porque es el que usan las copias de datos_juegos.
        encontrado = primero_presente((destino,) + alias, disponibles)
        campos[destino] = disponibles[encontrado] if encontrado else None
    return campos


class CatalogoDeJuegos:
    # Catálogo que junta los dos conjuntos de datos en una sola colección de juegos.
    # Atributos:
    #     fuentes (list[Path]): archivos leídos.
    #     filas_por_fuente (dict[Path, int]): renglones con título leídos de cada archivo;
    #         sirve para comprobar que se usaron los dos catálogos.
    #     hoy (date): fecha de hoy; decide si un juego ya salió o todavía no.
    #     ids_de_la_tienda (set[str]): números de Steam de los anuncios de la tienda.
    #     juegos (dict[str, FichaDeJuego]): las fichas, cada una con su clave de título.
    #     por_appid (dict[str, str]): número de Steam → clave de título.
    #     orden_generos (list[str]): orden de los géneros en el cuestionario.
    #     plataformas (dict[str, str]): clave de plataforma → nombre que se muestra.
    #     por_texto_compacto (dict[str, str o None]): título sin espacios → clave; None si
    #         dos títulos distintos se escriben igual sin espacios.
    #     claves_recomendables (list[str]): claves de los juegos que se pueden recomendar.
    #     frecuencia_de_generos (Counter): cuántos juegos recomendables hay de cada género.
    #     frecuencia_de_plataformas (Counter): cuántos hay en cada plataforma.
    #     frecuencia_de_atributos (Counter): cuántos tienen cada rasgo. Un rasgo poco común
    #         explica mejor qué tienen en común dos juegos.

    def __init__(self, fuentes, anuncios=(), consolas=None, carpeta_etiquetas=None):
        # Lee todos los catálogos y prepara las búsquedas.
        # Recibe:
        #     fuentes (list[Path]): archivos CSV o ZIP con un CSV.
        #     anuncios (list[dict]): renglones de los anuncios de la tienda de Steam.
        #     consolas (dict o None): número de Steam → consolas, de Wikidata.
        #     carpeta_etiquetas (Path o None): dónde se guardan las etiquetas de Steam;
        #         None no pregunta a Steam.
        # Puede fallar:
        #     ValueError: si ningún archivo tiene títulos que se puedan usar.
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
        # Los géneros que aparecen nuevos se agregan al final del menú, para que los
        # números de los demás no cambien.
        generos_originales = {g for j in self.juegos.values() if j.es_recomendable() for g in j.generos}
        self.orden_generos = sorted(GENEROS_DEL_CUESTIONARIO, key=lambda g: g not in generos_originales)
        if carpeta_etiquetas is not None:
            completar_generos(self.juegos, carpeta_etiquetas)
        # Los juegos no aptos se quitan hasta el final, después de juntar todas las fuentes;
        # así otro renglón del mismo juego no puede volver a hacerlo apto.
        self.juegos = {clave: juego for clave, juego in self.juegos.items() if juego.apto}
        self.por_appid = {appid: clave for appid, clave in self.por_appid.items() if clave in self.juegos}
        if not self.juegos and not (self.filas_por_fuente or anuncios):
            raise ValueError("Los archivos no contienen títulos utilizables.")
        # Se agregan las consolas de Wikidata y se cuentan géneros, plataformas y rasgos,
        # que usan el cuestionario, los filtros y las explicaciones.
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
        # Agrega al catálogo todos los renglones de un archivo.
        # Recibe:
        #     fuente (Path): CSV o ZIP con un CSV; las columnas pueden estar separadas por
        #         coma, punto y coma o tabulador.
        # Puede fallar:
        #     ValueError: si el archivo no tiene columna de título o ningún renglón con título.
        with abrir_csv(fuente) as datos:
            filas_con_titulo, filas_omitidas = recorrer_csv(datos, fuente.name, self.agregar_fila)
        self.filas_por_fuente[fuente] = filas_con_titulo
        if filas_omitidas:
            print(f"{fuente.name}: se omitieron {filas_omitidas} filas con columnas de más.")
        if filas_con_titulo == 0:
            raise ValueError(f"{fuente.name} no tiene filas con título.")

    def agregar_fila(self, fila):
        # Agrega un renglón a la ficha de su juego.
        # Recibe:
        #     fila (dict): renglón con las columnas de COLUMNAS_DEL_CATALOGO y un título. Si
        #         el juego ya tiene ficha (por ejemplo, porque está en los dos catálogos),
        #         sus datos se suman a esa ficha.
        clave = clave_titulo(fila["titulo"])
        anio, fecha = fecha_del_catalogo(fila["anio"])
        appid = fila["identificador"]
        # Una reedición puede llamarse igual que el original y tener otra fecha o plataforma;
        # en ese caso, y para los juegos recientes de Steam, la clave incluye su número de
        # Steam para que sean fichas separadas.
        anterior = self.juegos.get(clave)
        otra_edicion = anterior and (anterior.appid and anterior.appid != appid or
                                     anterior.anio and anio and abs(anterior.anio - anio) > 2)
        if appid.isdigit() and (otra_edicion or (anio and anio >= ANIO_DESDE) or appid in self.ids_de_la_tienda):
            clave = self.por_appid.get(appid, f"{clave} steam {appid}")
        if clave not in self.juegos:
            self.juegos[clave] = FichaDeJuego(fila["titulo"])
        juego = self.juegos[clave]
        if "anunciado" in fila:
            # Para un anuncio manda la ficha de la tienda, por si el estreno se pospuso o
            # quedó sin fecha.
            juego.anio, juego.fecha = anio, fecha
            juego.anunciado = fila["anunciado"]
            juego.periodo = fila["anio"]
        elif anio and (juego.anio is None or anio < juego.anio or (anio == juego.anio and fecha)):
            juego.anio, juego.fecha = anio, fecha
            juego.anunciado = fecha > self.hoy if fecha else anio > self.hoy.year
        self.agregar_ficha(clave, fila)

    def agregar_ficha(self, clave, fila):
        # Agrega a una ficha los datos de un renglón: plataformas, géneros, rasgos y reseñas.
        # Recibe:
        #     clave (str): clave del juego, que ya está en self.juegos.
        #     fila (dict): renglón con las columnas de COLUMNAS_DEL_CATALOGO.
        juego = self.juegos[clave]
        if fila["identificador"].isascii() and fila["identificador"].isdigit():
            juego.en_steam = True
            juego.appid = fila["identificador"]
            self.por_appid[fila["identificador"]] = clave
        # Steam dice si el juego funciona en PC y Mac. Ventas y Wikidata aportan las consolas.
        plataformas = nombres_de_campo(fila["plataformas"])
        for campo, etiqueta in (("windows", "PC"), ("mac", "Mac")):
            if fila[campo].lower() in ("true", "yes", "1", "si"):
                plataformas.append(etiqueta)
        for plataforma in plataformas:
            if normalizar(plataforma) not in ("", "n a", "unknown", "linux", "gnu linux", "steamos"):
                juego.plataformas.add(MODELOS.get(clave_de_plataforma(plataforma), plataforma))
        # Se sacan del catálogo el contenido para adultos y los programas que no son juegos.
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
        # Géneros: los del catálogo, los que salen de las etiquetas y las notas de terror
        # del programa original.
        generos = set()
        for genero in originales:
            if normalizar(genero) not in ("", "n a", "unknown"):
                generos.add(NOMBRES_DE_GENERO.get(normalizar(genero), genero))
        # Igual que con las etiquetas de la tienda, solo las más votadas asignan un género.
        for tema in temas[:ETIQUETAS_QUE_DEFINEN_GENERO]:
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
        # Se guardan los rasgos con los que se aprenden los gustos: géneros, etiquetas,
        # saga y estudio.
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
        # Reseñas: si hay varias fuentes, se queda la nota de la que tiene más opiniones.
        nota, opiniones, popularidad = resena_publica(fila)
        if nota is not None and opiniones > juego.evidencia_publica:
            juego.calidad_publica = nota
            juego.evidencia_publica = opiniones
        juego.popularidad = max(juego.popularidad, popularidad)
        if numero(fila["ventas"]) is not None:
            juego.con_ventas = True

    def indexar_nombres(self):
        # Prepara una búsqueda de títulos escritos sin espacios.
        # Así se puede escribir, por ejemplo, SilentHill2. Si dos títulos distintos se
        # escriben igual sin espacios, se guarda None para no elegir uno al azar.
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
        # Encuentra un único juego a partir de su título.
        # Recibe:
        #     texto (str o None): título escrito por la persona o guardado en el perfil.
        # Devuelve:
        #     str o None: la clave del juego; None si no existe o si sin espacios se
        #     parece a varios juegos.
        clave = clave_titulo(texto or "")
        if clave not in self.juegos:
            clave = self.por_texto_compacto.get(clave.replace(" ", ""))
        return clave

    def buscar_titulos(self, texto, limite=6):
        # Busca juegos cuyo título tenga todas las palabras escritas.
        # Recibe:
        #     texto (str): parte de un título, por ejemplo «zelda ocarina».
        #     limite (int): cuántos resultados como máximo (número entero positivo).
        # Devuelve:
        #     list[str]: claves ordenadas: primero el título exacto, luego los juegos
        #     recomendables y los más populares. Si ningún título tiene esas palabras,
        #     sugiere títulos que se escriben parecido (por ejemplo, con una letra mal).
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
        # Escribe una descripción corta de un juego para mostrarla en pantalla.
        # Recibe:
        #     clave (str): clave de un juego del catálogo.
        # Devuelve:
        #     str: por ejemplo «Silent Hill 2 (2001) · PS2, PC». Si todavía no sale, dice
        #     «Próximamente» con su fecha.
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
        # Reconoce el nombre de una plataforma.
        # Recibe:
        #     texto (str o None): por ejemplo «PS4», «ps 4» o «PlayStation 4».
        # Devuelve:
        #     str o None: el nombre que se muestra; None si no se escribió nada o no se
        #     reconoce.
        plataforma = None
        if texto:
            plataforma = self.plataformas.get(clave_de_plataforma(texto))
        return plataforma

    def resolver_plataforma(self, texto):
        # Igual que buscar_plataforma, pero avisa si el nombre no existe.
        # Recibe:
        #     texto (str o None): nombre de plataforma; vacío quiere decir «todas».
        # Devuelve:
        #     str o None: el nombre que se muestra, o None si no se escribió nada.
        # Puede fallar:
        #     ValueError: si el nombre no es de ninguna plataforma conocida.
        plataforma = self.buscar_plataforma(texto)
        if texto and plataforma is None:
            conocidas = ", ".join(self.plataformas_frecuentes(20))
            raise ValueError(f"Plataforma desconocida: '{texto}'. Puedes usar {conocidas}.")
        return plataforma

    def plataformas_frecuentes(self, cantidad=12):
        # Devuelve las plataformas con más juegos recomendables.
        # Recibe:
        #     cantidad (int): cuántas como máximo (número entero positivo).
        # Devuelve:
        #     list[str]: nombres, de la que tiene más juegos a la que tiene menos.
        return [plataforma for plataforma, _ in self.frecuencia_de_plataformas.most_common(cantidad)]

    def generos_del_cuestionario(self):
        # Devuelve los géneros del cuestionario que sí tienen juegos.
        # Devuelve:
        #     list[str]: géneros de GENEROS_DEL_CUESTIONARIO con al menos un juego
        #     recomendable, en el orden del menú.
        return [genero for genero in self.orden_generos if self.frecuencia_de_generos[genero] > 0]

    def candidatos(self, plataforma="", excluidos=(), evitados=(), historicos=False):
        # Escoge los juegos que se pueden recomendar con los filtros de la persona.
        # Recibe:
        #     plataforma (str o None): plataforma elegida; vacía acepta todas.
        #     excluidos (set[str]): claves de juegos favoritos, valorados o ya mostrados.
        #     evitados (list[str]): géneros que la persona no quiere ver.
        #     historicos (bool): True busca juegos anteriores a ANIO_DESDE, para consolas
        #         que ya casi no tienen estrenos.
        # Devuelve:
        #     list[str]: claves que pasan los filtros de plataforma, excluidos y géneros evitados.
        filtro = clave_de_plataforma(plataforma) if plataforma else ""
        evitar = [normalizar(genero) for genero in evitados]
        elegidos = []
        modelos = FAMILIAS.get(filtro, {filtro})
        for clave in (self.juegos if historicos else self.claves_recomendables):
            juego = self.juegos[clave]
            # En la búsqueda de juegos anteriores solo cuentan los de antes de ANIO_DESDE con género.
            fuera_del_periodo = historicos and not (filtro and juego.anio and juego.anio < ANIO_DESDE
                                                    and juego.generos)
            plataforma_correcta = not filtro or any(clave_de_plataforma(p) in modelos for p in juego.plataformas)
            genero_evitado = any(normalizar(g) in evitar for g in juego.generos)
            if not fuera_del_periodo and clave not in excluidos and plataforma_correcta and not genero_evitado:
                elegidos.append(clave)
        return elegidos


# ----------------------------------------------------------------------
# Perfil del jugador, guardado en un archivo SQLite (una pequeña base de datos).
# ----------------------------------------------------------------------
class Preferencias:
    # Respuestas del cuestionario.
    # Atributos:
    #     generos (list[str]): géneros que le gustan a la persona.
    #     evitados (list[str]): géneros que nunca se le deben recomendar.
    #     favoritos (list[str]): claves de los juegos que dijo que le gustaron.
    #     plataforma (str): su plataforma; texto vacío si le da igual.
    #     respondido (bool): True si ya contestó el cuestionario.

    def __init__(self):
        # Crea respuestas vacías, como las de alguien que todavía no contesta.
        self.generos = []
        self.evitados = []
        self.favoritos = []
        self.plataforma = ""
        self.respondido = False


def crear_tablas(conexion):
    # Crea las tablas del perfil si todavía no existen.
    # Tablas:
    #     perfil: un solo renglón con las respuestas del cuestionario.
    #     valoraciones: 1 («me interesa») o -1 («no me interesa») por juego.
    #     configuraciones: la usaban versiones anteriores; hoy la configuración del
    #         meta-evolutivo se guarda en NOMBRE_DE_LOS_AJUSTES y la tabla queda por compatibilidad.
    #     resumen_resenas: número de reseñas y porcentaje positivo de cada juego, según Steam.
    #     revision_steam: resultado de revisar el contenido de cada juego en Steam.
    # Todo lo personal que guarda el perfil lo escribió la persona en la consola.
    # Recibe:
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
    # INSERT OR IGNORE crea el perfil vacío la primera vez y no toca el que ya existe.
    conexion.execute(
        "INSERT OR IGNORE INTO perfil(id, generos, evitados, favoritos, plataforma, respondido, alta) "
        "VALUES(1, '[]', '[]', '[]', '', 0, ?)",
        (int(time.time()),))
    conexion.commit()


def leer_preferencias(conexion):
    # Lee las respuestas guardadas del cuestionario.
    # Recibe:
    #     conexion (sqlite3.Connection): perfil con sus tablas.
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
    # Guarda en el perfil las respuestas del cuestionario.
    # Recibe:
    #     conexion (sqlite3.Connection): perfil con sus tablas.
    #     preferencias (Preferencias): respuestas que reemplazan a las anteriores.
    conexion.execute(
        "UPDATE perfil SET generos=?, evitados=?, favoritos=?, plataforma=?, respondido=? "
        "WHERE id=1",
        (json.dumps(preferencias.generos, ensure_ascii=False),
          json.dumps(preferencias.evitados, ensure_ascii=False),
          json.dumps(preferencias.favoritos, ensure_ascii=False),
          preferencias.plataforma, int(preferencias.respondido)))
    conexion.commit()


def guardar_valoraciones(conexion, valoraciones):
    # Guarda o corrige las valoraciones de los juegos recomendados.
    # Recibe:
    #     conexion (sqlite3.Connection): perfil con sus tablas.
    #     valoraciones (dict[str, int]): clave del juego → 1 («me interesa») o -1 («no me
    #         interesa»).
    ahora = int(time.time())
    for clave, valor in valoraciones.items():
        # Si el juego ya tenía valoración, la nueva la reemplaza.
        conexion.execute(
            "INSERT INTO valoraciones(titulo, valor, fecha) VALUES(?, ?, ?) "
            "ON CONFLICT(titulo) DO UPDATE SET valor=excluded.valor, fecha=excluded.fecha",
            (clave, valor, ahora))
    conexion.commit()


# ----------------------------------------------------------------------
# Señales personales: lo que la persona escribió en la consola.
# ----------------------------------------------------------------------
class ActividadDeJuego:
    # Lo que la persona ha dicho de un juego.
    # El programa no lee cuentas de Steam ni historiales: solo sabe lo que la persona
    # escribe. Por eso las únicas señales son sus favoritos del cuestionario y sus
    # valoraciones de las listas.
    # Atributos:
    #     favorito (bool): True si lo dio como favorito en el cuestionario o si es el
    #         juego de referencia de esta ejecución.
    #     valoracion (int): 1 «me interesa», -1 «no me interesa», 0 sin valorar.

    def __init__(self):
        # Empieza sin señales: no es favorito ni tiene valoración.
        self.favorito = False
        self.valoracion = 0

    def interesa(self):
        # Dice si a la persona le interesa el juego.
        # Devuelve:
        #     bool: True si es favorito o si marcó «me interesa».
        return self.favorito or self.valoracion > 0

    def rechazado(self):
        # Devuelve True si la persona marcó «no me interesa».
        return self.valoracion < 0


def obtener_actividad(actividad, clave):
    # Devuelve las señales de un juego; si no tenía, las crea vacías.
    # Recibe:
    #     actividad (dict[str, ActividadDeJuego]): señales de cada juego.
    #     clave (str): clave del juego.
    # Devuelve:
    #     ActividadDeJuego: el objeto que está guardado en el diccionario, así que
    #     cambiarlo cambia también la actividad guardada.
    if clave not in actividad:
        actividad[clave] = ActividadDeJuego()
    return actividad[clave]


def actividad_personal(conexion, catalogo, preferencias):
    # Junta, juego por juego, los favoritos y las valoraciones guardadas.
    # Recibe:
    #     conexion (sqlite3.Connection): perfil con sus tablas.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     preferencias (Preferencias): respuestas del cuestionario.
    # Devuelve:
    #     dict[str, ActividadDeJuego]: clave del juego → sus señales. Solo incluye juegos
    #     que existen en el catálogo.
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
    # Dice si ya se conocen los gustos de la persona, para no recomendar solo los juegos
    # más populares.
    # Recibe:
    #     preferencias (Preferencias): respuestas del cuestionario.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    # Devuelve:
    #     bool: True si hay al menos un género favorito, un juego de interés o una valoración.
    return len(preferencias.generos) > 0 or any(uso.interesa() or uso.rechazado() for uso in actividad.values())


# ----------------------------------------------------------------------
# Aprendizaje de los gustos (regresión logística).
# La idea: cada rasgo de un juego (su género, sus etiquetas, su estudio) tiene un «peso».
# Si un rasgo aparece mucho en los juegos que te gustan y poco en los demás, su peso sube;
# si aparece en los que rechazas, baja. La afinidad de un juego se calcula sumando los
# pesos de sus rasgos y convirtiendo esa suma en un número entre 0 y 1.
# ----------------------------------------------------------------------
class PerfilDeGustos:
    # Los gustos aprendidos de una persona.
    # Atributos:
    #     pesos (dict[tuple, float]): peso de cada rasgo (tipo, valor). Un peso positivo
    #         sube la afinidad de los juegos que tienen ese rasgo, por ejemplo
    #         («genero», «terror»); uno negativo la baja.
    #     intercepto (float): punto de partida de la suma, antes de agregar los rasgos.
    #     evidencia (int): cuántas señales personales se usaron (ejemplos y géneros).
    #     generos_declarados (set[tuple]): géneros elegidos en el cuestionario, como rasgos.
    #     con_historial (bool): True si hay favoritos o valoraciones de donde aprender.
    #     favoritos (dict[str, set]): clave de cada favorito → sus rasgos, para buscar
    #         juegos parecidos a él.
    #     frecuencia_personal (dict[str, float]): en qué fracción de los juegos que te
    #         gustan aparece cada género; vacío si hay menos de dos juegos para calcularla.

    def __init__(self, pesos, intercepto, evidencia):
        # Guarda lo aprendido (ver los atributos de la clase).
        self.pesos = pesos
        self.intercepto = intercepto
        self.evidencia = evidencia
        self.generos_declarados = set()
        self.con_historial = False
        self.favoritos = {}
        self.frecuencia_personal = {}


def sigmoide(valor):
    # Convierte cualquier número en uno entre 0 y 1 (función sigmoide). Los números muy
    # positivos dan casi 1, los muy negativos casi 0, y el 0 da 0.5.
    # Recibe:
    #     valor (float): la suma de los pesos.
    # Devuelve:
    #     float: 1 / (1 + e^-valor). Se calcula de dos maneras según el signo para que
    #     la computadora no se desborde con números muy grandes.
    exponencial = math.exp(-abs(valor))
    return 1 / (1 + exponencial) if valor >= 0 else exponencial / (1 + exponencial)


def pesos_previos(preferencias):
    # Convierte los géneros elegidos en el cuestionario en pesos iniciales del modelo.
    # Recibe:
    #     preferencias (Preferencias): respuestas del cuestionario.
    # Devuelve:
    #     dict[tuple, float]: («genero», nombre) → PESO_PREVIO_GUSTA; todos los géneros
    #     elegidos empiezan con el mismo peso.
    previos = {}
    for genero in preferencias.generos:
        previos[("genero", normalizar(genero))] = PESO_PREVIO_GUSTA
    return previos


def ejemplos_aprendizaje(catalogo, actividad, fondo, semilla):
    # Prepara los ejemplos de los que aprende la regresión logística.
    # Cada ejemplo es un juego con su respuesta: 1 «le interesa» o 0 «no le interesa».
    # Respuesta 1: los favoritos y los «me interesa». Respuesta 0: los «no me interesa» y
    # hasta 48 juegos comunes del catálogo que la persona no ha mencionado; compararlos
    # muestra qué rasgos distinguen sus gustos de un juego cualquiera. Si solo hay
    # rechazos, los juegos comunes pasan a tener respuesta 1, para aprender qué tienen de
    # peor los rechazados que un juego cualquiera.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    #     fondo (lista de str): claves de donde se sacan los juegos comunes.
    #     semilla (int): fija el azar, para que la muestra sea siempre la misma.
    # Devuelve:
    #     list[tuple]: (rasgos ordenados, respuesta, peso). Los pesos de cada respuesta
    #     suman 0.5, aunque una tenga más juegos que la otra; así ninguna domina.
    positivos = []
    negativos = []
    # Entre los ejemplos con respuesta 1, un favorito ya jugado pesa el doble que un «me interesa».
    for clave in sorted(actividad):
        uso = actividad[clave]
        atributos = tuple(sorted(catalogo.juegos[clave].atributos))
        if uso.interesa():
            positivos.append((atributos, 4.0 if uso.favorito else 2.0))
        elif uso.rechazado():
            negativos.append((atributos, 2.0))
    # Muestra al azar, pero siempre igual con la misma semilla, de juegos que la persona no mencionó.
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
    # Se reparte el peso para que las dos respuestas tengan el mismo peso total.
    ejemplos = []
    for clase, grupo in grupos:
        masa = sum(peso for _, peso in grupo)
        if masa > 0:
            ejemplos.extend((atributos, clase, peso / (2 * masa)) for atributos, peso in grupo)
    return ejemplos


def aprender_perfil(catalogo, actividad, preferencias, fondo, semilla=SEMILLA_PREDETERMINADA):
    # Aprende los gustos con una regresión logística.
    # Si hay historial (favoritos o valoraciones), la regresión aprende de él; los géneros
    # del cuestionario se combinan después, en estimar_afinidad, para controlar cuánto pesa
    # cada fuente. Si no hay historial, los géneros del cuestionario son los pesos.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    #     preferencias (Preferencias): respuestas del cuestionario.
    #     fondo (lista de str): claves para la muestra de juegos comunes.
    #     semilla (int): semilla de esa muestra.
    # Devuelve:
    #     PerfilDeGustos: los pesos aprendidos y los datos para comparar con los favoritos.
    ejemplos = ejemplos_aprendizaje(catalogo, actividad, fondo, semilla)
    declarados = pesos_previos(preferencias)
    # Todos los rasgos que aparecen en los ejemplos empiezan con peso 0 (o con su peso del
    # cuestionario si no hay historial).
    previos = {} if ejemplos else declarados
    pesos = dict(previos)
    for rasgos, _, _ in ejemplos:
        for rasgo in rasgos:
            if rasgo not in pesos:
                pesos[rasgo] = 0.0
    intercepto = 0.0
    # Descenso de gradiente: se repiten ITERACIONES_DE_APRENDIZAJE vueltas. En cada vuelta se
    # mide cuánto se equivoca el modelo en cada ejemplo y se corrigen un poco los pesos en
    # la dirección que reduce ese error, como quien baja una montaña paso a paso.
    for _ in range(ITERACIONES_DE_APRENDIZAJE if ejemplos else 0):
        # Se suma cuánto contribuyó cada rasgo al error en todos los ejemplos.
        gradientes = {rasgo: 0.0 for rasgo in pesos}
        gradiente_del_intercepto = 0.0
        for rasgos, observado, peso_del_ejemplo in ejemplos:
            # La suma de pesos se convierte en una estimación entre 0 y 1.
            estimado = sigmoide(intercepto + sum(PESO_POR_TIPO[r[0]] * pesos[r] for r in rasgos))
            # Error = estimación − respuesta real. Si un juego que le interesa (1) solo
            # obtiene 0.3, el error es negativo y sus rasgos ganarán peso.
            error = peso_del_ejemplo * (estimado - observado)
            gradiente_del_intercepto += error
            for rasgo in rasgos:
                gradientes[rasgo] += error * PESO_POR_TIPO[rasgo[0]]
        # Se resta el gradiente para reducir el error. La regularización (REGULARIZACION)
        # acerca cada peso a su valor inicial, para que ningún peso crezca demasiado
        # con tan pocos ejemplos.
        intercepto -= TASA_DE_APRENDIZAJE * gradiente_del_intercepto
        for rasgo in pesos:
            diferencia = pesos[rasgo] - previos.get(rasgo, 0.0)
            pesos[rasgo] -= TASA_DE_APRENDIZAJE * (gradientes[rasgo] + REGULARIZACION * diferencia)
    # Se guarda el perfil y se calcula en qué fracción de los juegos que le gustan a la
    # persona aparece cada género (los favoritos cuentan doble). Esa fracción sirve para
    # que una lista no repita un género mucho más de lo que la persona lo juega.
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
    # Agrupa un subgénero con su género principal: «terror psicológico» cuenta como «terror».
    # Recibe:
    #     genero (str): género sin mayúsculas ni acentos.
    # Devuelve:
    #     str: el género principal.
    return "terror" if genero == "terror psicologico" else genero


def gustos_coincidentes(juego, perfil):
    # Dice qué géneros elegidos por la persona tiene un juego.
    # Cada familia de géneros cuenta una sola vez, aunque el juego tenga el género y su subgénero.
    # Recibe:
    #     juego (FichaDeJuego): ficha del juego.
    #     perfil (PerfilDeGustos): gustos aprendidos.
    # Devuelve:
    #     set[str]: las familias de géneros que coinciden.
    return {familia_del_genero(g) for _, g in perfil.generos_declarados & juego.atributos}


def rasgos_para_comparar(juego):
    # Prepara los rasgos de un juego para compararlo con otro.
    # Un género y la etiqueta de Steam que significa lo mismo cuentan una sola vez.
    # Recibe:
    #     juego (FichaDeJuego): ficha del juego.
    # Devuelve:
    #     set[tuple]: rasgos (tipo, valor) de tipo «genero» o «tema».
    rasgos = set()
    for tipo, nombre in juego.atributos:
        if tipo == "genero":
            rasgos.add((tipo, familia_del_genero(nombre)))
        elif tipo == "tema" and nombre not in ETIQUETAS_DE_GENERO:
            rasgos.add((tipo, nombre))
    return rasgos


def parecido_al_favorito(rasgos, favorito):
    # Mide qué tanto se parece un juego a un favorito con la similitud de Jaccard: rasgos
    # en común divididos entre todos los rasgos distintos de los dos. Da 1 si son iguales
    # y 0 si no comparten nada.
    # Recibe:
    #     rasgos (set): rasgos del juego.
    #     favorito (set): rasgos del favorito; no puede estar vacío.
    # Devuelve:
    #     float: el parecido, entre 0 y 1.
    return len(rasgos & favorito) / len(rasgos | favorito)


def muestra_variada(catalogo, ordenados, perfil, limite):
    # Escoge juegos que representen gustos distintos de la persona, para que la lista no
    # salga toda de un mismo género. Se recorre la lista de mayor a menor afinidad y se
    # guarda el mejor juego de cada combinación de géneros elegidos y el más parecido a
    # cada favorito.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     ordenados (list[str]): claves de mayor a menor afinidad.
    #     perfil (PerfilDeGustos): gustos aprendidos.
    #     limite (int): cuántos juegos como máximo.
    # Devuelve:
    #     list[str]: los juegos elegidos; lista vacía si hay un solo gusto y ningún favorito.
    gustos = {familia_del_genero(g) for _, g in perfil.generos_declarados}
    # «mejores» guarda el primer juego (el de más afinidad) de cada combinación de gustos;
    # «ejemplos» guarda el juego más parecido a cada favorito. Con un solo gusto y ningún
    # favorito no hay nada que variar, así que no se recorre la lista y la muestra queda vacía.
    mejores = {}
    ejemplos = {}
    if len(gustos) > 1 or perfil.favoritos:
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
    # Primero entra el más parecido a cada favorito. Después se agregan combinaciones de
    # gustos, empezando por la que aporta más gustos que todavía no están en la muestra;
    # si varias aportan lo mismo, gana la de mayor afinidad.
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
    # Estima cuánto le gustará un juego a la persona (su afinidad).
    # Combina tres fuentes: lo aprendido de su historial (70 %), los géneros que eligió
    # (30 %) y, si el juego tiene más de 100 reseñas, la opinión del público (20 % del total).
    # Recibe:
    #     juego (FichaDeJuego): ficha del juego.
    #     perfil (PerfilDeGustos): gustos aprendidos.
    # Devuelve:
    #     float: la afinidad, entre 0 y 1.
    if perfil.generos_declarados:
        # Por géneros: cuantos más géneros elegidos tenga el juego, más alta la afinidad.
        coincidencias = len(gustos_coincidentes(juego, perfil))
        por_generos = sigmoide(coincidencias * PESO_PREVIO_GUSTA * PESO_POR_TIPO["genero"])
    if perfil.con_historial or not perfil.generos_declarados:
        # Por historial: se suman los pesos de los rasgos del juego, siempre en el mismo
        # orden para que el resultado sea idéntico cada vez.
        valor = perfil.intercepto
        for rasgo in sorted(juego.atributos):
            valor += PESO_POR_TIPO[rasgo[0]] * perfil.pesos.get(rasgo, 0.0)
        personal = sigmoide(valor)
        if perfil.generos_declarados:
            personal = PESO_DEL_HISTORIAL * personal + (1 - PESO_DEL_HISTORIAL) * por_generos
    else:
        personal = por_generos
    # Las reseñas solo cuentan si hay suficientes (MINIMO_DE_RESENAS) para confiar en ellas.
    afinidad = personal
    if juego.evidencia_publica >= MINIMO_DE_RESENAS:
        afinidad = (1 - PESO_DE_LA_RESENA) * personal + PESO_DE_LA_RESENA * juego.calidad_publica
    return afinidad


# ----------------------------------------------------------------------
# Algoritmo evolutivo general, con mutación y cruzamiento. Sirve para cualquier tipo de
# individuo: listas de juegos o configuraciones del propio algoritmo.
# ----------------------------------------------------------------------
def estructura_valida(configuracion, presupuesto):
    # Comprueba que una configuración se pueda ejecutar.
    # Recibe:
    #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida, cruzamiento).
    #     presupuesto (int): cuántas evaluaciones se permiten.
    # Devuelve:
    #     bool: True si tiene cinco genes, hay menos descendientes que población, la
    #     población cabe en el presupuesto, el torneo no es mayor que la población y las
    #     dos probabilidades están entre 0 y 1.
    valida = len(configuracion) == len(NOMBRES_DE_PARAMETROS)
    if valida:
        poblacion, descendientes, torneo, dirigida, cruzamiento = configuracion
        valida = (1 <= descendientes < poblacion <= presupuesto
                  and 1 <= torneo <= poblacion
                  and 0 <= dirigida <= 1
                  and 0 <= cruzamiento <= 1)
    return valida


def configuracion_valida(configuracion, presupuesto=PRESUPUESTO_DE_BUSQUEDA):
    # Comprueba que una configuración sea una de las que el meta-evolutivo puede probar.
    # Recibe:
    #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida, cruzamiento).
    #     presupuesto (int): cuántas evaluaciones se permiten.
    # Devuelve:
    #     bool: True si cada gen tiene uno de los valores de VALORES_DE_AJUSTE y además se
    #     puede ejecutar.
    en_el_dominio = len(configuracion) == len(VALORES_DE_AJUSTE)
    if en_el_dominio:
        for posicion in range(len(configuracion)):
            if configuracion[posicion] not in VALORES_DE_AJUSTE[posicion]:
                en_el_dominio = False
    return en_el_dominio and estructura_valida(configuracion, presupuesto)


class ResultadoEvolutivo:
    # Resultado de una ejecución de AlgoritmoEvolutivo.
    # Atributos:
    #     mejor (tuple): el mejor individuo encontrado.
    #     aptitud (float): su calificación.
    #     mejoras (list[tuple]): historia de las mejoras. Cada vez que aparece un individuo
    #         mejor que todos los anteriores se anota (generación, número de evaluación,
    #         aptitud). La primera anotación es el mejor de la población inicial (generación 0).
    #     generaciones (int): cuántas generaciones alcanzó a hacer con su presupuesto.
    #     evaluaciones (int): cuántos individuos calificó.
    #     diversidad (float): qué tan distintos fueron entre sí sus individuos, en
    #         promedio de todas las generaciones, entre 0 y 1.

    def __init__(self, mejor, aptitud, mejoras, generaciones, evaluaciones, diversidad):
        # Guarda las medidas de la ejecución (ver los atributos de la clase).
        self.mejor = mejor
        self.aptitud = aptitud
        self.mejoras = mejoras
        self.generaciones = generaciones
        self.evaluaciones = evaluaciones
        self.diversidad = diversidad

    def momento_de_convergencia(self, objetivo):
        # Dice en qué momento la búsqueda llegó a una calificación objetivo (convergencia).
        # Recibe:
        #     objetivo (float): la calificación que se considera «ya llegó».
        # Devuelve:
        #     tuple: (generación, número de evaluación) de la primera mejora que alcanzó el
        #     objetivo; si nunca lo alcanzó, (generaciones, evaluaciones), es decir, todo
        #     su presupuesto.
        momento = (self.generaciones, self.evaluaciones)
        encontrado = False
        for generacion, evaluacion, aptitud in self.mejoras:
            if not encontrado and aptitud >= objetivo - 1e-12:
                momento = (generacion, evaluacion)
                encontrado = True
        return momento


def diversidad_genetica(individuos):
    # Mide qué tan distintos son entre sí los individuos de una población (diversidad
    # genética), con la distancia de Hamming: cuántas posiciones son diferentes entre dos
    # individuos. Por ejemplo, (A, B, C) y (A, D, C) difieren en 1 de 3 posiciones.
    # Recibe:
    #     individuos (list[tuple]): individuos del mismo tamaño.
    # Devuelve:
    #     float: fracción promedio de posiciones distintas entre cada par de individuos,
    #     entre 0 (todos iguales) y 1; 0 si hay menos de dos individuos.
    cantidad = len(individuos)
    diversidad = 0.0
    if cantidad > 1 and len(individuos[0]) > 0:
        genes = len(individuos[0])
        pares_iguales = 0
        # Para no comparar todos los pares uno por uno, en cada posición se cuenta cuántas
        # veces aparece cada valor: si un valor aparece n veces, forma n·(n−1) pares iguales.
        for posicion in range(genes):
            frecuencias = Counter(individuo[posicion] for individuo in individuos)
            for repeticiones in frecuencias.values():
                pares_iguales += repeticiones * (repeticiones - 1)
        diversidad = 1 - pares_iguales / (cantidad * (cantidad - 1) * genes)
    return diversidad


class AlgoritmoEvolutivo:
    # Algoritmo evolutivo con elitismo (los mejores siempre sobreviven) y selección por
    # torneo (para elegir un padre, compiten algunos individuos al azar y gana el mejor).
    # Cada hijo nace por cruzamiento de dos padres, con probabilidad «cruzamiento», o por
    # mutación de un padre en los demás casos. La clase no sabe qué tipo de individuo
    # evoluciona: recibe como parámetros la función que lo califica y las funciones que lo
    # mutan y lo cruzan. Por eso sirve igual para listas de juegos y para configuraciones.
    # Atributos:
    #     poblacion, descendientes, torneo, dirigida, cruzamiento: los cinco genes de la
    #         configuración (ver NOMBRES_DE_PARAMETROS).
    #     evaluar (función): individuo → aptitud (número; cuanto mayor, mejor).
    #     mutar (función): (padre, dirigida, azar) → hijo válido.
    #     cruzar (función): (padre, madre, azar) → hijo válido.
    #     presupuesto (int): cuántos individuos puede calificar en total, contando la
    #         población inicial.
    #     azar (random.Random): generador de números al azar.

    def __init__(self, configuracion, evaluar, mutar, cruzar, presupuesto, azar):
        # Guarda las piezas de la búsqueda.
        # Recibe:
        #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida, cruzamiento).
        #     evaluar, mutar, cruzar, presupuesto, azar: ver los atributos de la clase.
        # Puede fallar:
        #     ValueError: si la configuración no se puede ejecutar con ese presupuesto.
        if not estructura_valida(configuracion, presupuesto):
            raise ValueError(f"La configuración {configuracion} no es válida con {presupuesto} evaluaciones.")
        self.poblacion, self.descendientes, self.torneo, self.dirigida, self.cruzamiento = configuracion
        self.evaluar = evaluar
        self.mutar = mutar
        self.cruzar = cruzar
        self.presupuesto = presupuesto
        self.azar = azar

    def seleccionar_padre(self, poblacion):
        # Elige un padre por torneo: toma algunos individuos al azar y gana el mejor.
        # Recibe:
        #     poblacion (list[tuple]): pares (aptitud, individuo).
        # Devuelve:
        #     tuple: el individuo ganador.
        competidores = self.azar.sample(poblacion, self.torneo)
        ganador = max(competidores, key=lambda par: par[0])
        return ganador[1]

    def ejecutar(self, iniciales):
        # Hace evolucionar la población hasta gastar el presupuesto.
        # Recibe:
        #     iniciales (list[tuple]): exactamente self.poblacion individuos válidos.
        # Devuelve:
        #     ResultadoEvolutivo: el mejor individuo y las medidas de la ejecución.
        # Puede fallar:
        #     ValueError: si la población inicial no tiene el tamaño de la configuración.
        if len(iniciales) != self.poblacion:
            raise ValueError("La población inicial no tiene el tamaño de la configuración.")
        # Se califica la población inicial. Cada miembro se guarda como (aptitud, individuo).
        poblacion = [(self.evaluar(individuo), individuo) for individuo in iniciales]
        evaluaciones = len(poblacion)
        mejor = max(poblacion, key=lambda par: par[0])
        mejoras = [(0, poblacion.index(mejor) + 1, mejor[0])]
        generacion = 0
        diversidades = [diversidad_genetica(iniciales)]
        # Cada vuelta es una generación: sobreviven los mejores y nacen los hijos nuevos,
        # por cruzamiento o por mutación; los padres se eligen por torneo.
        while evaluaciones < self.presupuesto:
            generacion += 1
            cantidad = min(self.descendientes, self.presupuesto - evaluaciones)
            # Los mejores pasan directo a la siguiente generación (elitismo); los hijos
            # ocupan los lugares que quedan.
            ordenada = sorted(poblacion, key=lambda par: par[0], reverse=True)
            nueva = ordenada[:self.poblacion - cantidad]
            for _ in range(cantidad):
                padre = self.seleccionar_padre(poblacion)
                # Con cruzamiento 0 no se sortea nada; así, con la misma semilla, se repite
                # exactamente la búsqueda que solo usa mutación.
                por_cruzamiento = self.cruzamiento > 0 and self.azar.random() < self.cruzamiento
                if por_cruzamiento:
                    madre = self.seleccionar_padre(poblacion)
                    hijo = self.cruzar(padre, madre, self.azar)
                else:
                    dirigida = self.azar.random() < self.dirigida
                    hijo = self.mutar(padre, dirigida, self.azar)
                par = (self.evaluar(hijo), hijo)
                evaluaciones += 1
                # Solo se anota en la historia un hijo que supera al mejor hasta ahora.
                if par[0] > mejor[0] + 1e-12:
                    mejor = par
                    mejoras.append((generacion, evaluaciones, par[0]))
                nueva.append(par)
            poblacion = nueva
            diversidades.append(diversidad_genetica([individuo for _, individuo in poblacion]))
        return ResultadoEvolutivo(mejor[1], mejor[0], mejoras, generacion, evaluaciones,
                                  statistics.mean(diversidades))


# ----------------------------------------------------------------------
# El problema de configuración: armar una lista de juegos. Elegir y ordenar N juegos de
# entre cientos, cumpliendo condiciones (sin repetir, con un estreno y un anuncio), es
# un problema de configuración, como acomodar muebles en un cuarto.
# ----------------------------------------------------------------------
class MedidasDeRuta:
    # Las tres calificaciones de una lista, todas entre 0 y 1.
    # Atributos:
    #     afinidad (float): qué tanto le gustará la lista a la persona; también premia
    #         que represente a sus distintos favoritos.
    #     variedad (float): qué tan distintos son los juegos entre sí y cuántos de los
    #         géneros elegidos cubre.
    #     continuidad (float): qué tanto se parece cada juego al siguiente.

    def __init__(self, afinidad, variedad, continuidad):
        # Guarda las tres calificaciones (ver los atributos de la clase).
        self.afinidad = afinidad
        self.variedad = variedad
        self.continuidad = continuidad

    def aptitud(self):
        # Junta las tres calificaciones en una sola. Los gustos pesan más que variar la
        # lista o enlazar los juegos.
        # Devuelve:
        #     float: 0.60 afinidad + 0.20 variedad + 0.20 continuidad, entre 0 y 1.
        return 0.60 * self.afinidad + 0.20 * self.variedad + 0.20 * self.continuidad


class ProblemaDeRuta:
    # El problema que resuelve el algoritmo evolutivo de las listas.
    # Un individuo es una tupla de claves de juego, sin repetir y siempre del mismo tamaño.
    # El orden importa, porque la continuidad mira qué juego va después de cuál.
    # Atributos:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     candidatos (list[str]): la «reserva»: los TAMANO_DE_RESERVA juegos de mayor
    #         afinidad (más algunos que representan gustos distintos), de mayor a menor.
    #     longitud (int): juegos por lista; como máximo, cuántos candidatos hay.
    #     representantes (dict[bool, str]): el mejor juego ya publicado (False) y el mejor
    #         anunciado (True), para que la lista tenga uno de cada tipo.
    #     afinidades (dict[str, float]): afinidad de cada candidato.
    #     preferidos (list[str]): los primeros candidatos, que usa la mutación dirigida.
    #     parecidos (dict): memoria del parecido de cada pareja ya comparada.
    #     gustos_para_variedad (set[str]): familias de géneros elegidas en el cuestionario.
    #     familias (dict[str, set]): candidato → géneros elegidos que tiene.
    #     frecuencia_personal (dict[str, float]): ver PerfilDeGustos.
    #     generos_del_candidato (dict[str, set]): candidato → todas sus familias de géneros.
    #     parecidos_a_favoritos (dict[str, dict]): favorito → (candidato → parecido).
    #     inicial_por_gustos (tuple o None): lista armada paso a paso por ruta_por_gustos;
    #         None hasta que se calcula.

    def __init__(self, catalogo, candidatos, longitud, perfil):
        # Calcula las afinidades y prepara la reserva de candidatos.
        # Recibe:
        #     catalogo (CatalogoDeJuegos): el catálogo cargado.
        #     candidatos (list[str]): al menos una clave, sin repetir.
        #     longitud (int): juegos por lista (número entero positivo).
        #     perfil (PerfilDeGustos): gustos aprendidos.
        self.catalogo = catalogo
        todas = {}
        # Se calcula la afinidad de cada candidato y se ordenan de mayor a menor.
        for clave in candidatos:
            todas[clave] = estimar_afinidad(catalogo.juegos[clave], perfil)
        ordenados = sorted(candidatos, key=lambda clave: (-todas[clave], clave))
        self.candidatos = ordenados[:max(TAMANO_DE_RESERVA, longitud)]
        # Si la lista tendrá dos o más juegos, la reserva debe incluir el mejor anuncio,
        # aunque todavía no tenga reseñas, y el mejor juego ya publicado.
        self.longitud = min(longitud, len(self.candidatos))
        self.representantes = {}
        if self.longitud > 1:
            # Se busca el primer publicado y el primer anunciado en orden de afinidad.
            indice = 0
            while len(self.representantes) < 2 and indice < len(ordenados):
                clave = ordenados[indice]
                self.representantes.setdefault(catalogo.juegos[clave].anunciado, clave)
                indice += 1
            for clave in self.representantes.values():
                if clave not in self.candidatos:
                    self.candidatos[-1] = clave
        # Se agregan juegos que representan gustos distintos y se calculan sus afinidades.
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
        # El parecido con cada favorito se calcula una sola vez, porque muchas listas
        # repiten los mismos juegos.
        self.parecidos_a_favoritos = {}
        for titulo, favorito in perfil.favoritos.items():
            self.parecidos_a_favoritos[titulo] = {
                k: parecido_al_favorito(rasgos_para_comparar(catalogo.juegos[k]), favorito)
                for k in self.candidatos
            }
        # Más adelante, ruta_por_gustos arma una lista inicial paso a paso; aquí solo se
        # deja el lugar vacío.
        self.inicial_por_gustos = None

    def ruta_por_gustos(self):
        # Arma una lista inicial juego por juego: en cada paso agrega el candidato que deja
        # la lista con mejor aptitud junto con los ya elegidos. Se calcula una vez y se recuerda.
        # Devuelve:
        #     tuple[str]: la lista, con un publicado y un anunciado si los hay.
        if self.inicial_por_gustos is None:
            ruta = []
            for _ in range(self.longitud):
                opciones = (k for k in self.candidatos if k not in ruta)
                mejor = max(opciones, key=lambda k: self.aptitud(ruta + [k]))
                ruta.append(mejor)
            self.inicial_por_gustos = self.combinar_lanzamientos(ruta)
        return self.inicial_por_gustos

    def combinar_lanzamientos(self, ruta):
        # Si hay juegos publicados y anunciados, y la lista tiene solo de un tipo, el último
        # juego se cambia por el mejor del otro tipo.
        # Recibe:
        #     ruta (list[str]): una lista de claves.
        # Devuelve:
        #     tuple[str]: la lista corregida.
        if len(self.representantes) == 2:
            estado = self.catalogo.juegos[ruta[0]].anunciado
            if all(self.catalogo.juegos[k].anunciado == estado for k in ruta):
                ruta[-1] = self.representantes[not estado]
        return tuple(ruta)

    def parecido(self, a, b):
        # Mide qué tanto se parecen dos juegos y lo recuerda para no repetir la cuenta.
        # Recibe:
        #     a, b (str): claves de la reserva.
        # Devuelve:
        #     tuple: (similitud de Jaccard entre 0 y 1, True si son de la misma saga).
        pareja = (a, b) if a < b else (b, a)
        if pareja not in self.parecidos:
            primero = self.catalogo.juegos[a]
            segundo = self.catalogo.juegos[b]
            union = primero.atributos | segundo.atributos
            # Jaccard: rasgos en común divididos entre todos los rasgos distintos de los dos.
            similitud = 0.0
            if union:
                similitud = len(primero.atributos & segundo.atributos) / len(union)
            misma_saga = primero.saga != "" and primero.saga == segundo.saga
            self.parecidos[pareja] = (similitud, misma_saga)
        return self.parecidos[pareja]

    def medir(self, ruta):
        # Calcula las tres calificaciones de una lista.
        # Recibe:
        #     ruta (tuple[str]): al menos una clave de la reserva, sin repetir.
        # Devuelve:
        #     MedidasDeRuta: afinidad, variedad y continuidad.
        afinidad = sum(self.afinidades[clave] for clave in ruta) / len(ruta)
        senales = [afinidad]
        if len(self.parecidos_a_favoritos) > 1:
            # Por cada favorito se busca el juego de la lista que más se le parece; así se
            # premia que la lista tenga algo para cada favorito.
            cobertura = sum(max(parecidos[k] for k in ruta) for parecidos in self.parecidos_a_favoritos.values())
            senales.append(cobertura / len(self.parecidos_a_favoritos))
        if self.frecuencia_personal and len(ruta) > 1:
            # Si un género aparece en casi toda la lista pero en pocos de tus juegos, la
            # lista pierde puntos. La referencia son tus favoritos y tus «me interesa».
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
            # La variedad mira todas las parejas de juegos; la continuidad, solo los vecinos.
            total_pares = len(ruta) * (len(ruta) - 1) / 2
            variedad = max(0.0, 1 - suma_pares / total_pares)
            continuidad = suma_vecinos / (len(ruta) - 1)
            if len(self.gustos_para_variedad) > 1:
                # La variedad también premia que la lista cubra varios de los géneros elegidos
                # y que cada juego represente una combinación distinta de ellos.
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
        # Califica una lista: es el número que el algoritmo evolutivo trata de hacer lo
        # más grande posible.
        # Recibe:
        #     ruta (tuple[str]): una lista válida.
        # Devuelve:
        #     float: su aptitud, entre 0 y 1.
        return self.medir(ruta).aptitud()

    def mutar(self, padre, dirigida, azar):
        # Crea una lista hija cambiando una sola cosa de la lista padre (mutación).
        # Con probabilidad PROBABILIDAD_DE_INTERCAMBIO cambia de lugar dos juegos (cambia el
        # orden). Si no, cambia un juego por otro que no esté en la lista: uno de los
        # preferidos (los de más afinidad) si la mutación es dirigida, o cualquiera de la
        # reserva si no lo es.
        # Recibe:
        #     padre (tuple[str]): una lista válida.
        #     dirigida (bool): True si el juego nuevo debe salir de los preferidos.
        #     azar (random.Random): generador de números al azar.
        # Devuelve:
        #     tuple[str]: lista válida del mismo tamaño y sin juegos repetidos.
        ruta = list(padre)
        hay_sustitutos = self.longitud < len(self.candidatos)
        # Si no hay juegos de reemplazo, la única mutación posible es cambiar el orden.
        intercambiar = self.longitud > 1 and (not hay_sustitutos or azar.random() < PROBABILIDAD_DE_INTERCAMBIO)
        if intercambiar:
            a, b = azar.sample(range(self.longitud), 2)
            ruta[a], ruta[b] = ruta[b], ruta[a]
        elif hay_sustitutos:
            # Cambio de un juego: se elige uno que no esté ya en la lista.
            opciones = self.preferidos if dirigida else self.candidatos
            if len(opciones) <= max(TAMANO_DE_PREFERIDOS, 2 * self.longitud):
                nuevo = azar.choice([clave for clave in opciones if clave not in padre])
            else:
                # Si hay más del doble de opciones que juegos en la lista, se escoge al azar
                # hasta dar con uno que no esté; cada intento acierta al menos la mitad de
                # las veces, y es más rápido que revisar toda la reserva.
                nuevo = azar.choice(opciones)
                while nuevo in padre:
                    nuevo = azar.choice(opciones)
            posicion = azar.randrange(self.longitud)
            ruta[posicion] = nuevo
            # Si el cambio deja la lista sin su único juego anunciado o publicado, se
            # deshace y el hijo queda igual al padre.
            if len(self.representantes) == 2:
                estado_anterior = self.catalogo.juegos[padre[posicion]].anunciado
                if not any(self.catalogo.juegos[k].anunciado == estado_anterior for k in ruta):
                    ruta = list(padre)
        return tuple(ruta)

    def cruzar(self, padre, madre, azar):
        # Crea una lista hija mezclando dos listas (cruzamiento de un punto con reparación).
        # El hijo copia los primeros juegos del padre, hasta un punto de corte elegido al
        # azar, y se completa con los juegos de la madre que todavía no tiene, en el orden en
        # que aparecen en ella. Así hereda el orden de los dos y nunca repite un juego. Por
        # ejemplo, con el corte en 2, el padre (A, B, C, D) y la madre (C, E, A, F) dan
        # (A, B, C, E): se copian A y B, y de la madre se toman C y E (A ya estaba).
        # Recibe:
        #     padre, madre (tuple[str]): listas válidas del mismo tamaño.
        #     azar (random.Random): generador de números al azar.
        # Devuelve:
        #     tuple[str]: lista válida del mismo tamaño y sin repetidos.
        corte = azar.randint(1, self.longitud - 1) if self.longitud > 1 else 1
        inicio = list(padre[:corte])
        # La madre tiene «longitud» juegos distintos y a lo más «corte» de ellos ya están en
        # el inicio, así que siempre quedan suficientes para completar al hijo.
        resto = [clave for clave in madre if clave not in inicio]
        hijo = inicio + resto[:self.longitud - corte]
        # Igual que en la población inicial, se conserva un juego anunciado y uno publicado.
        return self.combinar_lanzamientos(hijo)

    def poblacion_inicial(self, cantidad, azar):
        # Crea la primera generación de listas.
        # Recibe:
        #     cantidad (int): cuántas listas (número entero positivo).
        #     azar (random.Random): generador de números al azar.
        # Devuelve:
        #     list[tuple[str]]: una lista con los juegos de mayor afinidad, otra armada paso
        #     a paso si hay varios gustos o favoritos, y las demás al azar.
        iniciales = [self.combinar_lanzamientos(self.candidatos[:self.longitud])]
        if cantidad > 1 and (len(self.gustos_para_variedad) > 1 or len(self.parecidos_a_favoritos) > 1):
            iniciales.append(self.ruta_por_gustos())
        for _ in range(cantidad - len(iniciales)):
            iniciales.append(self.combinar_lanzamientos(azar.sample(self.candidatos, self.longitud)))
        return iniciales


def evolucionar_ruta(problema, configuracion, semilla, presupuesto=PRESUPUESTO_DE_BUSQUEDA):
    # Ejecuta el algoritmo evolutivo que arma una lista.
    # Recibe:
    #     problema (ProblemaDeRuta): problema con al menos un candidato.
    #     configuracion (tuple): (poblacion, descendientes, torneo, dirigida, cruzamiento) válida.
    #     semilla (int): fija el azar, para poder repetir el resultado.
    #     presupuesto (int): cuántas listas se pueden calificar; al menos la población.
    # Devuelve:
    #     ResultadoEvolutivo: la mejor lista y las medidas de la ejecución.
    azar = random.Random(semilla)
    if len(problema.candidatos) == 1:
        # Con un solo candidato no hay nada que evolucionar: la lista es ese juego.
        ruta = tuple(problema.candidatos)
        aptitud = problema.aptitud(ruta)
        resultado = ResultadoEvolutivo(ruta, aptitud, [(0, 1, aptitud)], 0, 1, 0.0)
    else:
        algoritmo = AlgoritmoEvolutivo(configuracion, problema.aptitud, problema.mutar, problema.cruzar,
                                       presupuesto, azar)
        resultado = algoritmo.ejecutar(problema.poblacion_inicial(configuracion[0], azar))
    return resultado


# ----------------------------------------------------------------------
# Meta-evolutivo: un algoritmo evolutivo que busca la mejor configuración del que arma
# las listas. Sus individuos no son listas de juegos, sino configuraciones de cinco genes.
# Para calificar una configuración se ejecuta 50 veces el algoritmo de las listas con
# jugadores simulados cuyos gustos verdaderos se conocen.
# ----------------------------------------------------------------------
class EscenarioDeAjuste:
    # Un problema de prueba con un jugador simulado.
    # Atributos:
    #     problema (ProblemaDeRuta): problema armado con lo que el recomendador aprendió
    #         del jugador simulado.
    #     gusto_oculto (dict[str, float]): cuánto le gusta de verdad cada candidato al
    #         jugador; el recomendador no lo ve, solo sirve para medir.
    #     semillas (list[int]): una semilla por cada ejecución repetida.
    #     aptitud_inicial (float): aptitud de la lista «voraz» (los juegos de mayor
    #         afinidad, sin pensar en variedad ni orden), que siempre está en la primera
    #         generación.
    #     aptitud_de_referencia (float): la mejor aptitud conocida, encontrada con
    #         búsquedas diez veces más largas.

    def __init__(self, problema, gusto_oculto, semillas, aptitud_inicial, aptitud_de_referencia):
        # Guarda los datos del escenario (ver los atributos de la clase).
        self.problema = problema
        self.gusto_oculto = gusto_oculto
        self.semillas = semillas
        self.aptitud_inicial = aptitud_inicial
        self.aptitud_de_referencia = aptitud_de_referencia

    def calidad(self, aptitud):
        # Convierte la aptitud de una lista en «qué parte de la mejora posible se logró».
        # Recibe:
        #     aptitud (float): aptitud de la mejor lista de una ejecución.
        # Devuelve:
        #     float: 0 si no mejoró la lista voraz, 1 si llegó a la mejor aptitud conocida;
        #     se limita a valores entre 0 y 1.
        mejora_posible = self.aptitud_de_referencia - self.aptitud_inicial
        fraccion = 1.0
        if mejora_posible > 1e-12:
            fraccion = (aptitud - self.aptitud_inicial) / mejora_posible
        return min(1.0, max(0.0, fraccion))

    def objetivo(self):
        # Devuelve la aptitud que se considera «ya llegó»: la lista voraz más el
        # OBJETIVO_DE_CONVERGENCIA (95 %) de la mejora posible.
        mejora_posible = self.aptitud_de_referencia - self.aptitud_inicial
        return self.aptitud_inicial + OBJETIVO_DE_CONVERGENCIA * mejora_posible


def generar_escenarios(catalogo, disponibles, longitud, cantidad, repeticiones, semilla):
    # Crea jugadores simulados para calificar configuraciones del algoritmo de las listas.
    # Cada jugador simulado prefiere en secreto dos géneros comunes. Su gusto verdadero por
    # un juego es mayor si el juego tiene uno de esos géneros y si tiene buenas reseñas.
    # Igual que una persona real, solo declara uno de sus dos géneros en el cuestionario y
    # valora 14 juegos; el recomendador aprende sus gustos con esa información incompleta.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     disponibles (list[str]): claves recomendables (al menos longitud + 1).
    #     longitud (int): juegos por lista.
    #     cantidad (int): cuántos jugadores simulados.
    #     repeticiones (int): ejecuciones por jugador.
    #     semilla (int): fija el azar, para que los jugadores sean siempre los mismos.
    # Devuelve:
    #     list[EscenarioDeAjuste]: un escenario por jugador.
    origen = random.Random(semilla)
    escenarios = []
    for _ in range(cantidad):
        azar = random.Random(origen.getrandbits(64))
        # Cada jugador ve 514 juegos al azar: valora los primeros 14 y los demás son los candidatos.
        muestra = azar.sample(disponibles, min(514, len(disponibles)))
        total_observados = min(14, max(0, len(muestra) - longitud))
        observados = muestra[:total_observados]
        candidatos = muestra[total_observados:]
        # Gustos secretos: dos géneros que aparecen en al menos 6 juegos de la muestra.
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
        # Lo que sí ve el recomendador: un género declarado y las valoraciones. Cuanto más le
        # guste en secreto un juego, más probable es que el jugador marque «me interesa».
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
        # Límites para calificar: la lista voraz (0) y la mejor de tres búsquedas largas (1).
        inicial = problema.aptitud(problema.combinar_lanzamientos(problema.candidatos[:problema.longitud]))
        referencia = inicial
        for _ in range(3):
            larga = evolucionar_ruta(problema, AJUSTE_INICIAL, azar.getrandbits(64), 10 * PRESUPUESTO_DE_BUSQUEDA)
            referencia = max(referencia, larga.aptitud)
        gusto_oculto = {clave: gustos[clave] for clave in problema.candidatos}
        escenarios.append(EscenarioDeAjuste(problema, gusto_oculto, semillas, inicial, referencia))
    return escenarios


class DesempenoEvolutivo:
    # Calificaciones promedio de una configuración en varias ejecuciones.
    # Atributos:
    #     calidad (float): qué parte de la mejora posible logran sus listas, en promedio,
    #         entre 0 y 1.
    #     convergencia (float): en qué generación llega, en promedio, al
    #         OBJETIVO_DE_CONVERGENCIA; si una ejecución nunca llega, cuenta todas sus
    #         generaciones. Es la medida de eficiencia que pide el enunciado.
    #     rapidez (float): promedio de 1 − (evaluaciones hasta llegar / evaluaciones
    #         totales), entre 0 y 1; vale 0 si no llegó. Se mide en evaluaciones porque,
    #         con el mismo presupuesto, una configuración con menos hijos por generación
    #         hace más generaciones y parecería más lenta sin serlo.
    #     diversidad (float): diversidad genética promedio, entre 0 y 1.
    #     ejecuciones (int): cuántas ejecuciones se promediaron.
    #     interes (float): gusto secreto promedio de los jugadores simulados por las
    #         listas encontradas; solo se informa, no entra en la aptitud.

    def __init__(self, calidad, convergencia, rapidez, diversidad, ejecuciones, interes):
        # Guarda los promedios (ver los atributos de la clase).
        self.calidad = calidad
        self.convergencia = convergencia
        self.rapidez = rapidez
        self.diversidad = diversidad
        self.ejecuciones = ejecuciones
        self.interes = interes

    def aptitud(self):
        # Junta las calificaciones en una sola. Las tres medidas del enunciado están entre
        # 0 y 1. La calidad pesa más; la rapidez premia llegar pronto y la diversidad premia
        # explorar. Se usa la calidad «como fracción de la mejora posible» porque la aptitud
        # directa de las listas casi no cambia entre configuraciones y la diversidad
        # terminaría decidiendo todo.
        # Devuelve:
        #     float: 0.70 calidad + 0.15 rapidez + 0.15 diversidad, entre 0 y 1.
        return 0.70 * self.calidad + 0.15 * self.rapidez + 0.15 * self.diversidad


def resumir_ejecuciones(resultados, calidades, objetivos, intereses):
    # Saca el promedio de las medidas de varias ejecuciones.
    # Recibe:
    #     resultados (list[ResultadoEvolutivo]): al menos una ejecución.
    #     calidades (list[float]): calidad de la mejor lista de cada ejecución.
    #     objetivos (list[float]): aptitud de «ya llegó» de cada ejecución.
    #     intereses (list[float]): gusto secreto por cada lista; puede estar vacía si no
    #         se conoce.
    # Devuelve:
    #     DesempenoEvolutivo: los promedios.
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
    # Califica una configuración del algoritmo de las listas con todas sus ejecuciones.
    # Recibe:
    #     configuracion (tuple): configuración válida.
    #     escenarios (list[EscenarioDeAjuste]): jugadores simulados con sus semillas; en
    #         total, EJECUCIONES_POR_CONFIGURACION ejecuciones.
    # Devuelve:
    #     DesempenoEvolutivo: los promedios. La calidad de cada ejecución es la parte de la
    #     mejora posible que logró (ver EscenarioDeAjuste.calidad).
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
    # La función de aptitud del meta-evolutivo, con memoria.
    # Los jugadores simulados y las semillas no cambian, así que calificar dos veces la
    # misma configuración da lo mismo; la memoria evita repetir ese trabajo.
    # Atributos:
    #     escenarios (list[EscenarioDeAjuste]): los problemas de prueba.
    #     desempenos (dict): configuración → su DesempenoEvolutivo ya medido.
    #     avisar_cada (int): cada cuántas configuraciones nuevas se avisa del avance; 0 no avisa.

    def __init__(self, escenarios, avisar_cada=0):
        # Guarda los escenarios y empieza con la memoria vacía.
        # Recibe:
        #     escenarios, avisar_cada: ver los atributos de la clase.
        self.escenarios = escenarios
        self.desempenos = {}
        self.avisar_cada = avisar_cada

    def desempeno(self, configuracion):
        # Califica una configuración; si ya estaba en la memoria, no repite el trabajo.
        # Recibe:
        #     configuracion (tuple): configuración válida.
        # Devuelve:
        #     DesempenoEvolutivo: sus calificaciones promedio.
        if configuracion not in self.desempenos:
            self.desempenos[configuracion] = medir_configuracion(configuracion, self.escenarios)
            if self.avisar_cada > 0 and len(self.desempenos) % self.avisar_cada == 0:
                print(f"  {len(self.desempenos)} configuraciones medidas…", flush=True)
        return self.desempenos[configuracion]

    def aptitud(self, configuracion):
        # Es la función de aptitud que usa el meta-evolutivo.
        # Recibe:
        #     configuracion (tuple): configuración válida.
        # Devuelve:
        #     float: su aptitud (ver DesempenoEvolutivo.aptitud).
        return self.desempeno(configuracion).aptitud()


def configuraciones_posibles(presupuesto=PRESUPUESTO_DE_BUSQUEDA):
    # Hace la lista de todas las configuraciones que el meta-evolutivo puede probar.
    # Recibe:
    #     presupuesto (int): evaluaciones con las que se ejecutarán.
    # Devuelve:
    #     list[tuple]: todas las combinaciones válidas de VALORES_DE_AJUSTE.
    # product arma todas las combinaciones, igual que cinco ciclos for, uno dentro de otro.
    return [configuracion for configuracion in product(*VALORES_DE_AJUSTE)
            if configuracion_valida(configuracion, presupuesto)]


def vecinas_de_configuracion(padre, dirigida):
    # Hace la lista de configuraciones que se obtienen cambiando un solo gen.
    # Recibe:
    #     padre (tuple): una configuración válida.
    #     dirigida (bool): True solo acepta el valor anterior o el siguiente del gen en su
    #         lista de VALORES_DE_AJUSTE (un cambio pequeño); False acepta cualquier otro valor.
    # Devuelve:
    #     list[tuple]: las vecinas válidas; si no hay vecinas cercanas, devuelve todas.
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
    # Mutación del meta-evolutivo: cambia un gen de la configuración.
    # Recibe:
    #     padre (tuple): una configuración válida.
    #     dirigida (bool): True si el cambio debe ser a un valor vecino.
    #     azar (random.Random): generador de números al azar.
    # Devuelve:
    #     tuple: hija válida que difiere del padre en un gen.
    return azar.choice(vecinas_de_configuracion(padre, dirigida))


def cruzar_configuracion(padre, madre, azar):
    # Cruzamiento del meta-evolutivo (cruzamiento uniforme): cada gen se hereda del padre o
    # de la madre, como si se lanzara una moneda.
    # Por ejemplo, (30, 18, 3, 0.45, 0.0) y (12, 6, 5, 0.90, 0.50) pueden dar
    # (12, 18, 3, 0.90, 0.50). Esa hija no sirve, porque tendría más hijos por generación
    # que población; en ese caso hereda del padre la pareja (poblacion, descendientes),
    # que sí es compatible.
    # Recibe:
    #     padre, madre (tuple): configuraciones válidas.
    #     azar (random.Random): generador de números al azar.
    # Devuelve:
    #     tuple: hija válida.
    hija = [azar.choice((gen_del_padre, gen_de_la_madre)) for gen_del_padre, gen_de_la_madre in zip(padre, madre)]
    if not configuracion_valida(tuple(hija)):
        hija[0], hija[1] = padre[0], padre[1]
    return tuple(hija)


def ajustar_parametros(evaluador, configuracion_meta, semilla, presupuesto=PRESUPUESTO_DEL_META):
    # Ejecuta el meta-evolutivo para elegir la configuración del algoritmo de las listas.
    # La primera generación incluye la configuración hecha a mano (AJUSTE_INICIAL); como
    # los mejores siempre sobreviven, el resultado nunca es peor que ella.
    # Recibe:
    #     evaluador (EvaluadorDeConfiguraciones): la función de aptitud con memoria.
    #     configuracion_meta (tuple): la configuración del propio meta-evolutivo; su
    #         población debe caber en el presupuesto.
    #     semilla (int): fija el azar.
    #     presupuesto (int): cuántas configuraciones puede calificar.
    # Devuelve:
    #     ResultadoEvolutivo: la mejor configuración y las medidas de la búsqueda.
    azar = random.Random(semilla)
    posibles = [c for c in configuraciones_posibles() if c != AJUSTE_INICIAL]
    iniciales = [AJUSTE_INICIAL] + azar.sample(posibles, configuracion_meta[0] - 1)
    algoritmo = AlgoritmoEvolutivo(configuracion_meta, evaluador.aptitud, mutar_configuracion,
                                   cruzar_configuracion, presupuesto, azar)
    return algoritmo.ejecutar(iniciales)


def escenarios_tipicos(catalogo, longitud, semilla):
    # Crea los jugadores simulados de siempre: 5 jugadores × 10 ejecuciones = 50 ejecuciones.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     longitud (int): juegos por lista.
    #     semilla (int): semilla base del programa.
    # Devuelve:
    #     list[EscenarioDeAjuste]: escenarios con EJECUCIONES_POR_CONFIGURACION
    #     ejecuciones en total.
    repeticiones = max(1, EJECUCIONES_POR_CONFIGURACION // ESCENARIOS_DE_AJUSTE)
    return generar_escenarios(catalogo, catalogo.claves_recomendables, longitud,
                              ESCENARIOS_DE_AJUSTE, repeticiones, semilla + 1000)


def firma_del_ajuste(catalogo, longitud, semilla):
    # Arma una «firma» con las condiciones de un ajuste, para saber si el ajuste guardado
    # todavía sirve.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     longitud (int): juegos por lista.
    #     semilla (int): semilla base del programa.
    # Devuelve:
    #     str: texto JSON con la versión, el año inicial, la longitud, la semilla y el
    #     tamaño y la fecha de cada catálogo. Si algo cambia, se ajusta de nuevo. Los
    #     anuncios de Steam no entran en la firma: cambian cada semana y son pocos.
    archivos = []
    for ruta in catalogo.fuentes:
        datos = ruta.stat()
        archivos.append([str(ruta.resolve()), datos.st_size, datos.st_mtime_ns])
    return json.dumps([VERSION_DEL_AJUSTE, ANIO_DESDE, longitud, semilla, archivos], ensure_ascii=False)


def parametros_para_recomendar(carpeta, catalogo, longitud, semilla):
    # Consigue la configuración del algoritmo de las listas: la guardada o una nueva.
    # Los jugadores simulados no dependen de quién usa el programa, así que el resultado
    # se guarda en un archivo común de datos_juegos y lo usan todos los perfiles.
    # Recibe:
    #     carpeta (Path): la carpeta datos_juegos.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     longitud (int): juegos por lista.
    #     semilla (int): semilla base del programa.
    # Devuelve:
    #     tuple: (poblacion, descendientes, torneo, dirigida, cruzamiento) válida.
    conexion = sqlite3.connect(carpeta / NOMBRE_DE_LOS_AJUSTES, timeout=10)
    try:
        conexion.execute("CREATE TABLE IF NOT EXISTS configuraciones (clave TEXT PRIMARY KEY, parametros TEXT NOT NULL)")
        parametros = parametros_guardados_o_nuevos(conexion, catalogo, longitud, semilla)
    finally:
        conexion.close()
    return parametros


def parametros_guardados_o_nuevos(conexion, catalogo, longitud, semilla):
    # Busca un ajuste con la firma de hoy; si no hay, ejecuta el meta-evolutivo y lo guarda.
    # Recibe:
    #     conexion (sqlite3.Connection): archivo de ajustes con la tabla configuraciones.
    #     catalogo, longitud, semilla: ver parametros_para_recomendar.
    # Devuelve:
    #     tuple: configuración válida.
    clave = firma_del_ajuste(catalogo, longitud, semilla)
    fila = conexion.execute("SELECT parametros FROM configuraciones WHERE clave=?", (clave,)).fetchone()
    if fila is None:
        print("Ajustando el evolutivo con el meta-evolutivo (solo la primera vez con esta longitud)…", flush=True)
        evaluador = EvaluadorDeConfiguraciones(escenarios_tipicos(catalogo, longitud, semilla), avisar_cada=10)
        parametros = ajustar_parametros(evaluador, CONFIGURACION_DEL_META, semilla + 2000).mejor
        desempeno = evaluador.desempeno(parametros)
        poblacion, descendientes, torneo, dirigida, cruzamiento = parametros
        print(f"Parámetros elegidos: población {poblacion}, {descendientes} descendientes, "
              f"torneo de {torneo}, mutación dirigida {dirigida:.0%}, "
              f"{cruzamiento:.0%} de hijos por cruzamiento. "
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
    # Lee lo que la persona escribe en la consola.
    # Atributos:
    #     cerrada (bool): True si no se debe preguntar nada, porque HACER_PREGUNTAS es
    #         False o porque la entrada se terminó. Entonces cada pregunta devuelve un
    #         texto vacío, que quiere decir «omitir».

    def __init__(self, interactiva=True):
        # Recibe:
        #     interactiva (bool): False apaga todas las preguntas.
        self.cerrada = not interactiva

    def preguntar(self, mensaje):
        # Muestra una pregunta y lee la respuesta.
        # Recibe:
        #     mensaje (str): el texto de la pregunta.
        # Devuelve:
        #     str: la respuesta sin espacios al principio ni al final; texto vacío si la
        #     consola está cerrada.
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
        # Recibe:
        #     mensaje (str): el texto de la pregunta.
        # Devuelve:
        #     bool: True si la respuesta empieza con «s».
        return normalizar(self.preguntar(mensaje)).startswith("s")


def mostrar_opciones(opciones, columnas=4):
    # Muestra una lista numerada en columnas.
    # Recibe:
    #     opciones (list[str]): los textos; se numeran desde 1.
    #     columnas (int): cuántas opciones por renglón (número entero positivo).
    celdas = [f"{i:>3}) {texto:<20}" for i, texto in enumerate(opciones, 1)]
    for inicio in range(0, len(celdas), columnas):
        print("".join(celdas[inicio:inicio + columnas]).rstrip())


def interpretar_lista(texto, opciones):
    # Entiende una respuesta con números o nombres separados por comas.
    # Recibe:
    #     texto (str): por ejemplo «1, 3 12, terror».
    #     opciones (list[str]): las opciones, numeradas desde 1.
    # Devuelve:
    #     tuple: (elegidas, desconocidas). elegidas son las opciones reconocidas, sin
    #     repetir y en el orden escrito; desconocidas son los pedazos que no corresponden a
    #     ninguna opción.
    por_nombre = {normalizar(opcion): opcion for opcion in opciones}
    reconocidas = []
    desconocidas = []
    for parte in texto.split(","):
        palabras = parte.split()
        if palabras and all(p.isdigit() for p in palabras):
            # Un pedazo con solo números puede traer varios separados por espacios, como «3 12».
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
    # Si una opción se escribió dos veces, se queda solo la primera.
    elegidas = []
    for opcion in reconocidas:
        if opcion not in elegidas:
            elegidas.append(opcion)
    return elegidas, desconocidas


def elegir_generos(consola, opciones, mensaje):
    # Pregunta una lista de géneros hasta que la respuesta se entienda.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     opciones (list[str]): los géneros, numerados desde 1.
    #     mensaje (str): la pregunta.
    # Devuelve:
    #     list[str]: los géneros elegidos; lista vacía si la persona pulsa Enter.
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
    # Busca un juego por parte de su título y deja que la persona elija el correcto.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     texto (str): parte del título que escribió la persona.
    # Devuelve:
    #     str o None: la clave elegida; None si no hubo resultados o la persona eligió
    #     «ninguno».
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
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
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
    # Pregunta la plataforma hasta reconocerla o hasta que la persona pulse Enter.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    # Devuelve:
    #     str: el nombre de la plataforma; texto vacío si le da igual.
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
    # Hace el cuestionario de gustos.
    # Pide al menos un género o un juego, para que la primera lista ya sea personal y no
    # solo una lista de los juegos más populares.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    # Devuelve:
    #     Preferencias: las respuestas; respondido es False si la entrada se terminó sin
    #     datos suficientes.
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
    # Resume en una línea los gustos guardados.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     preferencias (Preferencias): respuestas del cuestionario.
    # Devuelve:
    #     str: por ejemplo «géneros que te gustan: Rol, Terror · favoritos: Silent Hill 2 ·
    #     plataforma PS2».
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
    # Consigue los gustos de la persona: los guardados o los de un cuestionario nuevo.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     conexion (sqlite3.Connection): perfil con sus tablas.
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
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
    # Escribe el nombre de un rasgo para explicar por qué se recomienda un juego.
    # Recibe:
    #     juego (FichaDeJuego): la ficha que tiene el rasgo.
    #     atributo (tuple): el rasgo (tipo, valor).
    # Devuelve:
    #     str: por ejemplo «Terror», «atmosférico» o «estudio Konami».
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
            # Una etiqueta que significa un género se muestra con el nombre de ese género.
            nombre = ETIQUETAS_DE_GENERO[valor][-1]
    else:
        nombre = f"{tipo} {valor.title()}"
    return nombre


def mostrar_recomendaciones(problema, resultado, perfil, numero_de_lista):
    # Muestra la lista recomendada con una razón breve para cada juego.
    # Recibe:
    #     problema (ProblemaDeRuta): el problema ya resuelto.
    #     resultado (ResultadoEvolutivo): lo que encontró el algoritmo evolutivo.
    #     perfil (PerfilDeGustos): gustos aprendidos.
    #     numero_de_lista (int): número de la lista en esta sesión (desde 1).
    cantidad = len(resultado.mejor)
    palabra = "juego" if cantidad == 1 else "juegos"
    print(f"\nTus recomendaciones · lista {numero_de_lista} ({cantidad} {palabra})")
    frecuencias = problema.catalogo.frecuencia_de_atributos
    total = len(problema.catalogo.claves_recomendables)

    def relevancia(rasgo):
        # Qué tan buena razón es un rasgo para explicar una recomendación: su peso en tus
        # gustos multiplicado por qué tan raro es en el catálogo. Así no se explica con
        # rasgos que tienen casi todos los juegos, como «un jugador».
        # Recibe:
        #     rasgo (tuple): el rasgo (tipo, valor).
        # Devuelve:
        #     float: la relevancia; cuanto mayor, mejor razón.
        aprendido = perfil.pesos.get(rasgo, 0.0)
        if perfil.con_historial and perfil.generos_declarados:
            aprendido *= PESO_DEL_HISTORIAL
            if rasgo in perfil.generos_declarados:
                aprendido += (1 - PESO_DEL_HISTORIAL) * PESO_PREVIO_GUSTA
        return aprendido * PESO_POR_TIPO[rasgo[0]] * math.log1p(total / (1 + frecuencias[rasgo]))
    anterior = None
    # Para cada juego se muestra su descripción, de qué catálogo salió y sus razones.
    for posicion, clave in enumerate(resultado.mejor, 1):
        ficha = problema.catalogo.juegos[clave]
        fuentes = [nombre for nombre, presente in (("Steam", ficha.en_steam), ("ventas", ficha.con_ventas)) if presente]
        print(f"{posicion}. {problema.catalogo.describir(clave)} · Catálogo: {' y '.join(fuentes)}")
        # Razón principal: el género y el otro rasgo más relevantes del juego.
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
        # Si hay favoritos, se dice cuál se parece más a este juego y qué comparten.
        if perfil.favoritos:
            parecido = problema.parecidos_a_favoritos
            favorito = max(perfil.favoritos, key=lambda k: parecido[k][clave])
            compartidos = rasgos_para_comparar(ficha) & perfil.favoritos[favorito]
            if compartidos:
                rasgo = min(compartidos, key=lambda r: (frecuencias[r], r))
                titulo = problema.catalogo.juegos[favorito].titulo
                print(f"   Comparte «{nombrar_atributo(ficha, rasgo)}» con tu favorito {titulo}.")
        # Si el juego tiene suficientes reseñas, se dice cuántas se tomaron en cuenta.
        if ficha.evidencia_publica >= MINIMO_DE_RESENAS:
            print(f"   Se consideraron {int(ficha.evidencia_publica):,} reseñas del juego.")
        # Razón secundaria: el rasgo menos común que comparte con el juego anterior.
        if anterior is not None:
            comunes = sorted(anterior.atributos & ficha.atributos, key=lambda r: (frecuencias[r], r))
            if comunes:
                print(f"   Comparte «{nombrar_atributo(ficha, comunes[0])}» con el juego anterior.")
        anterior = ficha


def interpretar_valoraciones(texto, cantidad):
    # Entiende una valoración como «1 3 -2».
    # Recibe:
    #     texto (str): números separados por espacios o comas; el signo menos quiere decir
    #         «no me interesa».
    #     cantidad (int): cuántos juegos tiene la lista.
    # Devuelve:
    #     tuple: (valoraciones, errores). valoraciones une cada posición (desde 1) con 1 o
    #     −1; errores son los pedazos que no se entendieron.
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
    # Pide y guarda la valoración de una lista recomendada.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     conexion (sqlite3.Connection): perfil con sus tablas.
    #     ruta (tuple[str]): claves de la lista que se mostró.
    # Devuelve:
    #     bool: True si se guardó al menos una valoración; False si la persona la saltó o
    #     la consola está cerrada.
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
# Recomendación: los pasos que se siguen para mostrar cada lista.
# ----------------------------------------------------------------------
def resolver_referencia(catalogo, texto):
    # Encuentra el juego de referencia de esta ejecución (JUEGO_DE_REFERENCIA).
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     texto (str): título escrito; puede estar vacío.
    # Devuelve:
    #     str o None: la clave del juego; None si no se escribió o no se encontró (en ese
    #     caso muestra títulos parecidos).
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
    # Decide con qué plataforma se filtra esta ejecución.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     opciones (argparse.Namespace): PLATAFORMA_PREFERIDA, si se escribió, tiene prioridad.
    #     preferencias (Preferencias): la plataforma del cuestionario.
    # Devuelve:
    #     str: el nombre de la plataforma; texto vacío para todas.
    # Puede fallar:
    #     ValueError: si PLATAFORMA_PREFERIDA no es una plataforma conocida.
    plataforma = catalogo.resolver_plataforma(opciones.plataforma) or ""
    if not plataforma and preferencias.plataforma:
        plataforma = catalogo.buscar_plataforma(preferencias.plataforma) or ""
        if not plataforma:
            print(f"La plataforma guardada ({preferencias.plataforma}) no está en este catálogo; "
                  "usaré todas.")
    return plataforma


def actualizar_resenas(catalogo, claves, perfil, longitud, conexion):
    # Actualiza con la tienda de Steam las reseñas de los candidatos con más afinidad.
    # La tienda da el número real de reseñas y el porcentaje positivo; se guardan siete días.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     claves (list[str]): los candidatos.
    #     perfil (PerfilDeGustos): gustos aprendidos, para elegir a quién preguntar primero.
    #     longitud (int): juegos por lista; se pregunta por max(12, 2 × longitud) juegos.
    #     conexion (sqlite3.Connection): perfil, donde se guardan las reseñas.
    ahora = int(time.time())
    guardadas = {a: (n, p) for a, n, p in conexion.execute(
        "SELECT appid, total, porcentaje FROM resumen_resenas WHERE fecha >= ?", (ahora - 7 * 86400,))}
    ordenadas = sorted(claves, key=lambda k: (-estimar_afinidad(catalogo.juegos[k], perfil), k))
    pendientes = [catalogo.juegos[k].appid for k in ordenadas if catalogo.juegos[k].appid
                  and catalogo.juegos[k].appid not in guardadas and not catalogo.juegos[k].anunciado]
    # Solo se pregunta por los de más afinidad, para no hacer demasiadas consultas.
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
    # Con las reseñas guardadas se recalcula la nota de cada candidato (mismo suavizado que
    # resena_publica).
    for clave in claves:
        juego = catalogo.juegos[clave]
        if juego.appid in guardadas:
            total, porcentaje = guardadas[juego.appid]
            juego.evidencia_publica = total
            juego.calidad_publica = (total * porcentaje / 100 + 13) / (total + 20)


def candidatos_revisados(catalogo, candidatos, perfil, longitud, conexion):
    # Deja solo los candidatos cuyo contenido ya se comprobó que es apto.
    # Las revisiones se guardan 30 días, así se pueden usar incluso sin internet.
    # «sin_datos» quiere decir que Steam respondió, pero sin avisos de contenido; se vuelve a
    # preguntar después de siete días, por si la ficha del juego se completa.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     candidatos (list[str]): claves que pasaron los filtros.
    #     perfil (PerfilDeGustos): gustos aprendidos, para revisar primero los más afines.
    #     longitud (int): juegos por lista; decide cuántos se revisan.
    #     conexion (sqlite3.Connection): perfil, donde se guardan las revisiones.
    # Devuelve:
    #     list[str]: los candidatos revisados y aptos, de mayor a menor afinidad.
    ahora = int(time.time())
    anteriores = {appid: resultado for appid, resultado, fecha in conexion.execute(
        "SELECT appid, resultado, fecha FROM revision_steam WHERE fecha >= ?", (ahora - 30 * 86400,))
        if resultado != "sin_datos" or fecha >= ahora - 7 * 86400}
    descartados = ("excluir", "sin_datos")
    ordenados = sorted(candidatos, key=lambda k: (-estimar_afinidad(catalogo.juegos[k], perfil), k))
    admitidos = []
    pendientes = set()
    for clave in ordenados:
        juego = catalogo.juegos[clave]
        estado = anteriores.get(juego.appid, "")
        # Un juego que Steam ya marcó como no apto (o sin datos) no entra ni se vuelve a preguntar.
        if estado not in descartados:
            if juego.contenido_revisado or estado == "revisado":
                admitidos.append(clave)
            elif juego.appid:
                pendientes.add(clave)
    # Se revisan primero los mejores de cada tipo (publicados y anunciados), para poder
    # mezclar estrenos y anuncios. Se limita el número de consultas a la tienda; los juegos
    # que no se alcanzan a revisar se quedan fuera.
    por_revisar = []
    for anunciado in (False, True):
        grupo = [k for k in ordenados if catalogo.juegos[k].anunciado == anunciado
                 and (catalogo.juegos[k].appid or catalogo.juegos[k].contenido_revisado)
                 and anteriores.get(catalogo.juegos[k].appid) not in descartados]
        cupo = max(12, 2 * longitud)
        variados = muestra_variada(catalogo, grupo, perfil, max(16, 3 * longitud))
        # Se alternan juegos de alta afinidad y juegos que representan gustos distintos.
        turnos = zip_longest(grupo[:cupo], variados)
        seleccion = dict.fromkeys(k for turno in turnos for k in turno if k is not None)
        por_revisar.extend(islice((k for k in seleccion if k in pendientes), max(16, 3 * longitud)))
    # Se pregunta a Steam por los avisos de contenido, cuatro juegos al mismo tiempo.
    if por_revisar:
        print("Comprobando los avisos de contenido de Steam…", flush=True)
        with ThreadPoolExecutor(max_workers=4) as consultas:
            trabajos = {k: consultas.submit(producto_de_steam, catalogo.juegos[k].appid) for k in por_revisar}
            for clave, trabajo in trabajos.items():
                try:
                    estado = revisar_producto(trabajo.result()) or "sin_datos"
                except (OSError, ValueError, HTTPException, KeyError, TypeError, AttributeError):
                    # Si Steam no responde, el juego queda sin revisar: no se recomienda y no se guarda.
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
    # Aprende los gustos, arma una lista con el algoritmo evolutivo y la muestra.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     preferencias (Preferencias): respuestas del cuestionario.
    #     actividad (dict[str, ActividadDeJuego]): señales personales.
    #     vistos (set[str]): juegos ya mostrados en esta sesión; no se repiten.
    #     plataforma (str): plataforma elegida; vacía acepta todas.
    #     parametros (tuple): configuración del algoritmo evolutivo (cinco genes).
    #     opciones (argparse.Namespace): opciones de la ejecución.
    #     numero_de_lista (int): número de la lista en esta sesión.
    #     conexion (sqlite3.Connection): perfil, donde se guardan reseñas y revisiones.
    # Devuelve:
    #     tuple[str]: claves recomendadas; tupla vacía si no quedan candidatos.
    candidatos = catalogo.candidatos(plataforma, set(actividad) | vistos, preferencias.evitados)
    # Paso 1: se aprenden los gustos. Paso 2: solo quedan los juegos con contenido revisado.
    perfil = aprender_perfil(catalogo, actividad, preferencias, catalogo.claves_recomendables, opciones.semilla)
    candidatos = candidatos_revisados(catalogo, candidatos, perfil, opciones.longitud, conexion)
    # Si una consola casi no tiene estrenos, se buscan sus juegos anteriores.
    if not candidatos and plataforma and plataforma not in ("PC", "Mac"):
        print(f"No hay estrenos verificables con tus filtros en {plataforma}. Buscando en su catálogo histórico…")
        historicos = catalogo.candidatos(plataforma, set(actividad) | vistos, preferencias.evitados, historicos=True)
        candidatos = candidatos_revisados(catalogo, historicos, perfil, opciones.longitud, conexion)
    ruta = ()
    if not candidatos:
        print("No quedan juegos con compatibilidad y contenido comprobados que cumplan tus filtros.")
    else:
        # Paso 3: se actualizan las reseñas, se arma la lista y se muestra.
        actualizar_resenas(catalogo, candidatos, perfil, opciones.longitud, conexion)
        problema = ProblemaDeRuta(catalogo, candidatos, opciones.longitud, perfil)
        resultado = evolucionar_ruta(problema, parametros, opciones.semilla + numero_de_lista)
        mostrar_recomendaciones(problema, resultado, perfil, numero_de_lista)
        ruta = resultado.mejor
    return ruta


def archivo_del_jugador(consola, opciones):
    # Pregunta el apodo y devuelve el archivo del perfil de esa persona.
    # Sin preguntas (HACER_PREGUNTAS = False) o con --perfil se usa el archivo indicado.
    # Recibe:
    #     consola (Consola): lee las respuestas de la persona.
    #     opciones (argparse.Namespace): opciones de la ejecución.
    # Devuelve:
    #     Path: el archivo del perfil.
    # Si no se pregunta el apodo, o la persona pulsa Enter, se usa el perfil de siempre.
    archivo = opciones.perfil
    if opciones.elegir_jugador:
        apodo = consola.preguntar("¿Quién juega? Escribe tu apodo (Enter para el perfil de siempre): ").strip()
        if apodo:
            # El apodo nunca se usa tal cual como nombre de archivo: se convierte en un código
            # (SHA-256) que siempre es el mismo para el mismo apodo y acepta acentos, espacios
            # y símbolos.
            nombre = " ".join(unicodedata.normalize("NFKC", apodo).casefold().split())
            clave = hashlib.sha256(nombre.encode("utf-8")).hexdigest()
            carpeta = opciones.carpeta / "perfiles"
            carpeta.mkdir(exist_ok=True)
            print(f"Perfil de {apodo}.")
            archivo = carpeta / (clave + ".sqlite3")
    return archivo


def recomendar(catalogo, opciones):
    # Sesión completa de recomendación.
    # Lee o pregunta los gustos, consigue la configuración del algoritmo evolutivo y
    # muestra listas mientras la persona las valore y pida otra.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     opciones (argparse.Namespace): opciones de la ejecución.
    consola = Consola(opciones.interactivo)
    conexion = sqlite3.connect(archivo_del_jugador(consola, opciones), timeout=10)
    # try/finally hace que el archivo del perfil se cierre aunque ocurra un error.
    try:
        crear_tablas(conexion)
        preferencias = preparar_preferencias(consola, conexion, catalogo, opciones.cambiar_gustos)
        plataforma_valida = True
        # Las versiones anteriores aceptaban Linux como plataforma; hoy se pide elegir otra.
        # Si no se puede preguntar, no se recomienda hasta que se elija una.
        if not opciones.plataforma and clave_de_plataforma(preferencias.plataforma) == "linux":
            print("Tu perfil guardaba Linux. Elige tu plataforma actual.")
            if consola.cerrada:
                print("Indícala en PLATAFORMA_PREFERIDA o ejecuta el cuestionario.")
                plataforma_valida = False
            else:
                preferencias.plataforma = elegir_plataforma(consola, catalogo)
                guardar_preferencias(conexion, preferencias)
        if plataforma_valida:
            sesion_de_listas(catalogo, opciones, consola, conexion, preferencias)
    finally:
        conexion.close()


def sesion_de_listas(catalogo, opciones, consola, conexion, preferencias):
    # Muestra listas mientras la persona las valore y pida otra.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
    #     opciones (argparse.Namespace): opciones de la ejecución.
    #     consola (Consola): lee las respuestas de la persona.
    #     conexion (sqlite3.Connection): perfil con sus tablas.
    #     preferencias (Preferencias): respuestas del cuestionario.
    # Se juntan el juego de referencia, la plataforma y las señales personales.
    referencia = resolver_referencia(catalogo, opciones.titulo)
    plataforma = plataforma_de_la_ejecucion(catalogo, opciones, preferencias)
    actividad = actividad_personal(conexion, catalogo, preferencias)
    if referencia:
        obtener_actividad(actividad, referencia).favorito = True
    if not hay_informacion_personal(preferencias, actividad):
        # Sin gustos no se recomienda: la lista sería solo de los juegos más populares.
        print("Todavía no conozco tus gustos. Ejecuta el programa con preguntas (HACER_PREGUNTAS = True) "
              "o indica un juego de referencia.")
    else:
        parametros = (parametros_para_recomendar(opciones.carpeta / NOMBRE_DE_LAS_COPIAS, catalogo,
                                                 opciones.longitud, opciones.semilla)
                      if catalogo.claves_recomendables else AJUSTE_INICIAL)
        numero_de_lista = 1
        vistos = set()
        otra_lista = True
        # Cada vuelta es una lista nueva; los gustos se recalculan con lo que se valoró.
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


# ----------------------------------------------------------------------
# Experimentos del reporte.
# ----------------------------------------------------------------------
def formato_de_configuracion(configuracion):
    # Escribe una configuración como texto corto, por ejemplo «(30, 18, 3, 0.45, 0.25)».
    # Recibe:
    #     configuracion (tuple): los cinco genes.
    # Devuelve:
    #     str: el texto.
    poblacion, descendientes, torneo, dirigida, cruzamiento = configuracion
    return f"({poblacion}, {descendientes}, {torneo}, {dirigida:.2f}, {cruzamiento:.2f})"


def imprimir_tabla(filas, desempenos, con_interes=True):
    # Muestra una tabla de configuraciones con sus calificaciones.
    # Recibe:
    #     filas (list[tuple]): (nombre del renglón, configuración).
    #     desempenos (dict): configuración → DesempenoEvolutivo.
    #     con_interes (bool): si se muestra la columna del gusto secreto de los jugadores.
    encabezado = (f"  {'Configuración':<36}{'(pob, desc, torneo, dirig, cruz)':<34}{'Calidad':>9}"
                  f"{'Conv. (gen)':>13}{'Rapidez':>9}{'Diversidad':>12}{'Aptitud':>9}")
    if con_interes:
        encabezado += f"{'Interés':>9}"
    print(encabezado)
    for nombre, configuracion in filas:
        d = desempenos[configuracion]
        renglon = (f"  {nombre:<36}{formato_de_configuracion(configuracion):<34}{d.calidad:>9.4f}"
                   f"{d.convergencia:>13.2f}{d.rapidez:>9.4f}{d.diversidad:>12.4f}{d.aptitud():>9.4f}")
        if con_interes:
            renglon += f"{d.interes:>9.4f}"
        print(renglon)


def repetir_meta(evaluador, configuracion_meta, repeticiones, semilla, peor, optima):
    # Ejecuta varias veces el meta-evolutivo con la misma configuración.
    # Recibe:
    #     evaluador (EvaluadorDeConfiguraciones): la aptitud con memoria; en los
    #         experimentos ya tiene calificadas todas las configuraciones.
    #     configuracion_meta (tuple): la configuración del meta-evolutivo.
    #     repeticiones (int): cuántas ejecuciones (número entero positivo).
    #     semilla (int): semilla base; cada ejecución usa semilla + i.
    #     peor, optima (float): aptitud de la peor y de la mejor configuración posibles;
    #         sirven para calificar qué tan cerca de la mejor llegó el meta-evolutivo.
    # Devuelve:
    #     tuple: (DesempenoEvolutivo del meta-evolutivo, la mejor configuración que
    #     encontró cada ejecución). La calidad de cada ejecución es
    #     (aptitud encontrada − peor) / (óptima − peor).
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
    # 1. Paisaje completo: califica con 50 ejecuciones todas las configuraciones posibles
    #    del algoritmo de las listas y compara la mejor con la hecha a mano. También muestra
    #    la mejor configuración para cada porcentaje de cruzamiento.
    # 2. Meta-evolutivo: lo ejecuta 50 veces con CONFIGURACION_DEL_META y cuenta cuántas
    #    veces encuentra la mejor configuración.
    # 3. La pregunta del enunciado: prueba cada configuración como configuración del
    #    meta-evolutivo (50 ejecuciones cada una) y compara la mejor para el meta-evolutivo
    #    con la mejor para el algoritmo de las listas.
    # Recibe:
    #     catalogo (CatalogoDeJuegos): el catálogo cargado.
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
    # ¿Conviene el cruzamiento? Se compara la mejor configuración de cada porcentaje de cruzamiento.
    print("\n  Mejor configuración para cada porcentaje de hijos por cruzamiento:")
    filas_de_cruzamiento = []
    for cruzamiento in VALORES_DE_AJUSTE[4]:
        # ordenadas va de mejor a peor, así que la primera con ese valor es la mejor.
        mejor_con_ese_valor = next(c for c in ordenadas if c[4] == cruzamiento)
        filas_de_cruzamiento.append((f"Cruzamiento {cruzamiento:.0%} (lugar {ordenadas.index(mejor_con_ese_valor) + 1})",
                                     mejor_con_ese_valor))
    imprimir_tabla(filas_de_cruzamiento, desempenos)
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
# Opciones y punto de entrada del programa.
# ----------------------------------------------------------------------
def leer_opciones(argumentos=None):
    # Junta las opciones de esta ejecución: las constantes de la sección «Opciones de
    # ejecución» y, si el programa se abre desde una terminal, sus argumentos.
    # Recibe:
    #     argumentos (list[str] o None): argumentos; None usa los de la terminal (en Spyder
    #         no hay ninguno).
    # Devuelve:
    #     argparse.Namespace: titulo (str), plataforma (str), longitud (int de 1 a
    #     LONGITUD_MAXIMA), carpeta (Path que existe), perfil (Path), cambiar_gustos,
    #     interactivo, elegir_jugador y experimentos (bool) y semilla (int).
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
    # Si no se escribió nada en la terminal, se usan las constantes de arriba.
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
    # Recibe:
    #     argumentos (list[str] o None): argumentos de la terminal.
    opciones = leer_opciones(argumentos)
    # Cada etapa dice cuánto tardó, para saber cuál hace lenta la preparación.
    print("Preparando los catálogos de videojuegos…", flush=True)
    inicio = time.time()
    copias = localizar_catalogos(opciones.carpeta)
    print(f"  Catálogos de Kaggle listos en {time.time() - inicio:.0f} s.", flush=True)
    inicio = time.time()
    anuncios = anuncios_de_steam(opciones.carpeta)
    consolas = consolas_de_wikidata(opciones.carpeta)
    print(f"  Anuncios de Steam y consolas de Wikidata listos en {time.time() - inicio:.0f} s.", flush=True)
    inicio = time.time()
    catalogo = CatalogoDeJuegos(list(copias.values()), anuncios, consolas, opciones.carpeta / NOMBRE_DE_LAS_COPIAS)
    print(f"  Catálogo unificado y etiquetas de Steam listos en {time.time() - inicio:.0f} s.", flush=True)
    # El resumen por fuente sirve para comprobar que se usaron los dos catálogos.
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
    # Con MODO_EXPERIMENTOS se ejecutan los experimentos; si no, se recomienda.
    if opciones.experimentos and not catalogo.claves_recomendables:
        print(f"Esta copia no contiene juegos recomendables desde {ANIO_DESDE}. Puedes actualizar el CSV de Steam.")
    elif opciones.experimentos:
        ejecutar_experimentos(catalogo, opciones)
    else:
        recomendar(catalogo, opciones)


# Esto se ejecuta al pulsar F5. Si algo falla con los archivos o con internet, se muestra un
# mensaje claro en lugar de un error largo; Ctrl+C detiene el programa sin perder el perfil.
if __name__ == "__main__":
    try:
        principal()
    except ERRORES_DE_EJECUCION as error:
        print(f"No se pudo completar la ejecución. {error}")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida. Tus gustos y valoraciones guardados se conservan.")
