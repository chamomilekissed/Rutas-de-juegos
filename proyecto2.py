#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:21:32 2026

@author: nattfernandez
"""

# -*- coding: utf-8 -*-
"""
===============================================================================
 PROYECTO DE PROGRAMACIÓN 2 - INTELIGENCIA ARTIFICIAL
 Recomendador de rutas de videojuegos que combina razonamiento basado en
 casos (RBC) con un algoritmo evolutivo (AE).
 Versión: esqueleto inicial (versión 0.1)
===============================================================================

PREGUNTA DE INVESTIGACIÓN
    ¿Usar recomendaciones anteriores (casos) como punto de partida permite
    encontrar mejores rutas que empezar desde cero?

IDEA GENERAL
    - El CATÁLOGO describe los videojuegos (plataformas, etiquetas, saga...).
    - La MEMORIA DE CASOS guarda experiencias completas:
      problema (preferencias y restricciones) + solución (ruta ordenada) +
      resultado (valoraciones del usuario).
    - El ciclo de RBC es: recuperar, reutilizar, revisar y retener.
      La etapa de reutilización se hace mediante evolución: las rutas
      recuperadas forman parte de la población inicial del AE.

MANUAL DE USUARIO
    1. Abrir este archivo en Spyder. Los archivos de datos
       "catalogo_videojuegos.csv" y "memoria_casos.json" deben estar en la
       misma carpeta que este programa. Si "memoria_casos.json" no existe,
       se crea vacío automáticamente.
    2. Ejecutar con F5. Aparece un menú en la consola:
         1) Pedir una recomendación (modo demostración en vivo).
         2) Generar casos sintéticos con usuarios simulados.
         3) Ejecutar el experimento comparativo de las tres versiones.
         4) Mostrar el catálogo.
         5) Mostrar la memoria de casos.
         6) Salir.
    3. En la opción 1 el programa pide la plataforma, los juegos que le
       gustaron al usuario, los que rechazó, los que ya jugó, las etiquetas
       que valora y la longitud de la ruta. Los juegos se indican con su
       número de identificador (ver opción 4), separados por comas.
       Al final se pide valorar cada juego de 1 a 5; esa experiencia se
       retiene como un caso nuevo.
    4. En la opción 3 se comparan "solo casos", "solo evolución" e
       "híbrido" sobre usuarios simulados, con el mismo presupuesto de
       evaluaciones para las dos versiones evolutivas.

NOTA PARA LA ENTREGA
    El profesor pide un solo archivo con extensión .txt y nombre del equipo
    (por ejemplo, EquipoN.txt) junto con los archivos de datos.
===============================================================================
"""

import csv
import json
import math
import os
import random
import statistics
import time
from dataclasses import dataclass, field

import matplotlib.pyplot as plt


# =============================================================================
# CONSTANTES DE CONFIGURACIÓN
# =============================================================================

# Carpeta donde está este programa. En Spyder, __file__ existe al ejecutar con
# F5; si no existe (por ejemplo, en una consola interactiva) se usa la carpeta
# de trabajo actual.
if "__file__" in globals():
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
else:
    CARPETA_BASE = os.getcwd()

RUTA_CATALOGO = os.path.join(CARPETA_BASE, "catalogo_videojuegos.csv")
RUTA_MEMORIA = os.path.join(CARPETA_BASE, "memoria_casos.json")

# Pesos de la función de aptitud: afinidad, variedad y continuidad.
# Deben sumar 1 para que la aptitud quede en el intervalo [0, 1].
PESO_AFINIDAD = 0.6
PESO_VARIEDAD = 0.2
PESO_CONTINUIDAD = 0.2

# Penalización por cada restricción violada en una ruta.
PENALIZACION_RESTRICCION = 0.5

# Parámetros por omisión del algoritmo evolutivo.
PARAMETROS_AE = {
    "tam_poblacion": 30,           # Individuos por generación.
    "prob_cruza": 0.8,             # Probabilidad de cruzar dos padres.
    "prob_mutacion": 0.3,          # Probabilidad de mutar a un hijo.
    "tam_torneo": 3,               # Participantes en cada torneo.
    "num_elites": 2,               # Mejores que pasan intactos.
    "presupuesto_evaluaciones": 1500,  # Evaluaciones de aptitud permitidas.
}

# Número de casos que se recuperan de la memoria.
CASOS_A_RECUPERAR = 5

# Arquetipos de jugador para generar usuarios simulados. Cada arquetipo es
# un conjunto de pesos ocultos por etiqueta (positivos: le gusta; negativos:
# le disgusta). Los usuarios se generan a partir de un arquetipo más ruido,
# de modo que existan usuarios parecidos entre sí (condición necesaria para
# que el razonamiento basado en casos tenga sentido).
ARQUETIPOS = {
    "terror_narrativo": {"terror": 1.0, "narrativa": 0.8, "rompecabezas": 0.5,
                         "exploracion": 0.4, "multijugador": -0.6},
    "terror_social": {"terror": 1.0, "multijugador": 0.9,
                      "supervivencia": 0.6, "narrativa": -0.3},
    "rompecabezas": {"rompecabezas": 1.0, "exploracion": 0.6,
                     "indie": 0.5, "accion": -0.5},
    "rol_mundo_abierto": {"rpg": 1.0, "mundo_abierto": 0.9,
                          "accion": 0.5, "narrativa": 0.4},
    "estrategia": {"estrategia": 1.0, "ciencia_ficcion": 0.4,
                   "multijugador": 0.4, "accion": -0.4},
    "accion_sigilo": {"sigilo": 1.0, "accion": 0.8, "exploracion": 0.3,
                      "plataformas": -0.3},
}


# =============================================================================
# REPRESENTACIÓN DEL CONOCIMIENTO
# =============================================================================

@dataclass
class Videojuego:
    """
    Describe un videojuego del catálogo.

    Atributos:
        identificador (int): número único del juego en el catálogo.
        titulo (str): nombre del juego.
        saga (str): saga a la que pertenece ("ninguna" si no pertenece).
        anio (int): año de publicación.
        plataformas (set[str]): plataformas donde se puede jugar.
        etiquetas (set[str]): características (géneros, temas, mecánicas).
        duracion_horas (int): duración aproximada de la historia principal.
        dificultad (int): dificultad percibida, de 1 (fácil) a 5 (difícil).
    """
    identificador: int
    titulo: str
    saga: str
    anio: int
    plataformas: set
    etiquetas: set
    duracion_horas: int
    dificultad: int


@dataclass
class Problema:
    """
    Describe la petición de un usuario (la parte "problema" de un caso).

    Atributos:
        plataforma (str): plataforma donde jugará (restricción dura).
        longitud (int): número de juegos que debe tener la ruta (>= 1).
        gustados (list[int]): identificadores de juegos que le gustaron.
        rechazados (list[int]): identificadores de juegos que no le gustaron.
        jugados (list[int]): juegos que ya jugó y no deben recomendarse.
        etiquetas_preferidas (list[str]): características que valora.
    """
    plataforma: str
    longitud: int
    gustados: list = field(default_factory=list)
    rechazados: list = field(default_factory=list)
    jugados: list = field(default_factory=list)
    etiquetas_preferidas: list = field(default_factory=list)

    def excluidos(self):
        """Regresa el conjunto de juegos que nunca deben aparecer en la ruta."""
        return set(self.gustados) | set(self.rechazados) | set(self.jugados)


@dataclass
class Caso:
    """
    Una experiencia completa de recomendación.

    Atributos:
        identificador (int): número único del caso.
        problema (Problema): preferencias y restricciones del usuario.
        solucion (list[int]): ruta ordenada de identificadores de juegos.
        valoraciones (dict[int, int]): calificación de 1 a 5 por juego.
        sintetico (bool): True si el caso proviene de un usuario simulado.
    """
    identificador: int
    problema: Problema
    solucion: list
    valoraciones: dict
    sintetico: bool

    def calidad(self):
        """
        Regresa la calidad del caso en [0, 1] a partir de la valoración
        promedio (1 se transforma en 0 y 5 se transforma en 1).
        """
        resultado = 0.5
        if self.valoraciones:
            promedio = statistics.mean(self.valoraciones.values())
            resultado = (promedio - 1) / 4
        return resultado


# =============================================================================
# CATÁLOGO
# =============================================================================

class Catalogo:
    """
    Conjunto de videojuegos cargado desde un archivo CSV separado por ";".
    Las listas dentro de una columna (plataformas, etiquetas) se separan
    con "|".
    """

    def __init__(self, ruta_archivo):
        """Carga el catálogo. ruta_archivo: ruta del CSV."""
        self.juegos = {}
        with open(ruta_archivo, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")
            for fila in lector:
                juego = Videojuego(
                    identificador=int(fila["identificador"]),
                    titulo=fila["titulo"],
                    saga=fila["saga"],
                    anio=int(fila["anio"]),
                    plataformas=set(fila["plataformas"].split("|")),
                    etiquetas=set(fila["etiquetas"].split("|")),
                    duracion_horas=int(fila["duracion_horas"]),
                    dificultad=int(fila["dificultad"]),
                )
                self.juegos[juego.identificador] = juego
        # Vocabulario de etiquetas, ordenado para que sea reproducible.
        self.etiquetas = sorted({e for j in self.juegos.values()
                                 for e in j.etiquetas})
        self.plataformas = sorted({p for j in self.juegos.values()
                                   for p in j.plataformas})

    def vector(self, identificador):
        """Regresa el vector binario de etiquetas de un juego (dict)."""
        juego = self.juegos[identificador]
        return {e: 1.0 for e in juego.etiquetas}

    def candidatos_validos(self, problema):
        """
        Regresa la lista de juegos que cumplen las restricciones duras del
        problema: estar en la plataforma pedida y no estar excluidos.
        """
        excluidos = problema.excluidos()
        return [i for i, j in self.juegos.items()
                if problema.plataforma in j.plataformas and i not in excluidos]

    def titulo(self, identificador):
        """Regresa el título de un juego a partir de su identificador."""
        return self.juegos[identificador].titulo


# =============================================================================
# MEDIDAS DE SIMILITUD
# =============================================================================

def similitud_coseno(vector_a, vector_b):
    """
    Similitud coseno entre dos vectores dispersos representados como dict.
    Regresa un valor en [-1, 1]; regresa 0 si alguno de los vectores es nulo.
    """
    producto = sum(valor * vector_b.get(clave, 0.0)
                   for clave, valor in vector_a.items())
    norma_a = math.sqrt(sum(v * v for v in vector_a.values()))
    norma_b = math.sqrt(sum(v * v for v in vector_b.values()))
    resultado = 0.0
    if norma_a > 0 and norma_b > 0:
        resultado = producto / (norma_a * norma_b)
    return resultado


def similitud_jaccard(conjunto_a, conjunto_b):
    """
    Índice de Jaccard entre dos conjuntos: |A ∩ B| / |A ∪ B|.
    Regresa 0 si ambos conjuntos están vacíos.
    """
    union = conjunto_a | conjunto_b
    resultado = 0.0
    if union:
        resultado = len(conjunto_a & conjunto_b) / len(union)
    return resultado


def vector_preferencias(problema, catalogo):
    """
    Construye el vector de preferencias declaradas del usuario:
    suma los vectores de los juegos que le gustaron (+1), resta la mitad de
    los que rechazó (-0.5) y suma 1 por cada etiqueta preferida explícita.
    """
    vector = {}
    for identificador in problema.gustados:
        for etiqueta in catalogo.juegos[identificador].etiquetas:
            vector[etiqueta] = vector.get(etiqueta, 0.0) + 1.0
    for identificador in problema.rechazados:
        for etiqueta in catalogo.juegos[identificador].etiquetas:
            vector[etiqueta] = vector.get(etiqueta, 0.0) - 0.5
    for etiqueta in problema.etiquetas_preferidas:
        vector[etiqueta] = vector.get(etiqueta, 0.0) + 1.0
    return vector


def similitud_problemas(problema_a, problema_b, catalogo):
    """
    Similitud entre dos problemas en [0, 1]. Combina:
      - 60 %: coseno entre vectores de preferencias (permite encontrar casos
              útiles aunque los usuarios hayan mencionado títulos distintos),
      - 25 %: Jaccard entre los juegos que les gustaron,
      - 15 %: coincidencia de plataforma.
    Los pesos son una primera propuesta y deben justificarse experimentalmente.
    """
    coseno = similitud_coseno(vector_preferencias(problema_a, catalogo),
                              vector_preferencias(problema_b, catalogo))
    coseno = max(0.0, coseno)
    jaccard = similitud_jaccard(set(problema_a.gustados),
                                set(problema_b.gustados))
    misma_plataforma = 1.0 if problema_a.plataforma == problema_b.plataforma else 0.0
    return 0.60 * coseno + 0.25 * jaccard + 0.15 * misma_plataforma


# =============================================================================
# FUNCIÓN DE APTITUD Y RESTRICCIONES
# =============================================================================

def calcular_afinidad(ruta, preferencias, catalogo):
    """
    Afinidad promedio de la ruta con las preferencias, en [0, 1].
    El coseno en [-1, 1] se transforma linealmente a [0, 1].
    """
    valores = [similitud_coseno(preferencias, catalogo.vector(i)) for i in ruta]
    return (statistics.mean(valores) + 1) / 2


def calcular_variedad(ruta, catalogo):
    """
    Variedad de la ruta en [0, 1]: 1 menos la similitud de Jaccard promedio
    entre todos los pares de juegos, con una penalización adicional por
    cada par de juegos de la misma saga.
    """
    pares = [(a, b) for posicion, a in enumerate(ruta) for b in ruta[posicion + 1:]]
    resultado = 1.0
    if pares:
        parecido = statistics.mean(
            similitud_jaccard(catalogo.juegos[a].etiquetas,
                              catalogo.juegos[b].etiquetas) for a, b in pares)
        misma_saga = statistics.mean(
            1.0 if (catalogo.juegos[a].saga == catalogo.juegos[b].saga
                    and catalogo.juegos[a].saga != "ninguna") else 0.0
            for a, b in pares)
        resultado = max(0.0, 1.0 - parecido - 0.5 * misma_saga)
    return resultado


def calcular_continuidad(ruta, catalogo):
    """
    Continuidad de la ruta en [0, 1]: similitud promedio entre juegos
    consecutivos (transiciones suaves). Es la parte de la aptitud que hace
    que el ORDEN de la ruta importe.
    """
    resultado = 1.0
    if len(ruta) > 1:
        resultado = statistics.mean(
            similitud_jaccard(catalogo.juegos[ruta[k]].etiquetas,
                              catalogo.juegos[ruta[k + 1]].etiquetas)
            for k in range(len(ruta) - 1))
    return resultado


def contar_violaciones(ruta, problema, catalogo):
    """
    Cuenta las restricciones violadas por una ruta:
    longitud incorrecta, juegos repetidos, juegos de otra plataforma y
    juegos excluidos (ya jugados, gustados o rechazados).
    """
    excluidos = problema.excluidos()
    violaciones = abs(len(ruta) - problema.longitud)
    violaciones += len(ruta) - len(set(ruta))
    violaciones += sum(1 for i in ruta
                       if problema.plataforma not in catalogo.juegos[i].plataformas)
    violaciones += sum(1 for i in ruta if i in excluidos)
    return violaciones


def evaluar_ruta(ruta, problema, catalogo, preferencias):
    """
    Función de aptitud. Regresa un número (mayor es mejor):
        aptitud = w_a * afinidad + w_v * variedad + w_c * continuidad
                  - penalización * violaciones
    """
    aptitud = (PESO_AFINIDAD * calcular_afinidad(ruta, preferencias, catalogo)
               + PESO_VARIEDAD * calcular_variedad(ruta, catalogo)
               + PESO_CONTINUIDAD * calcular_continuidad(ruta, catalogo))
    aptitud -= PENALIZACION_RESTRICCION * contar_violaciones(ruta, problema, catalogo)
    return aptitud


def reparar_ruta(ruta, problema, catalogo, preferencias, generador):
    """
    Operador de reparación: elimina juegos inválidos o repetidos y completa
    la ruta hasta la longitud pedida con candidatos válidos, eligiendo al
    azar entre los cinco más afines (así se conserva algo de exploración).
    Si no hay suficientes candidatos, regresa una ruta más corta.
    """
    validos = set(catalogo.candidatos_validos(problema))
    reparada = []
    for identificador in ruta:
        if identificador in validos and identificador not in reparada:
            reparada.append(identificador)
    reparada = reparada[:problema.longitud]
    disponibles = [i for i in validos if i not in reparada]
    disponibles.sort(key=lambda i: similitud_coseno(preferencias, catalogo.vector(i)),
                     reverse=True)
    while len(reparada) < problema.longitud and disponibles:
        elegido = generador.choice(disponibles[:5])
        reparada.append(elegido)
        disponibles.remove(elegido)
    return reparada


# =============================================================================
# MEMORIA DE CASOS (RECUPERAR Y RETENER)
# =============================================================================

class MemoriaCasos:
    """Almacena los casos y los guarda en un archivo JSON."""

    def __init__(self, ruta_archivo=None):
        """
        Crea la memoria. Si ruta_archivo es None, la memoria vive solo en
        RAM (útil para experimentos que no deben modificar el archivo).
        """
        self.ruta_archivo = ruta_archivo
        self.casos = []
        if ruta_archivo is not None and os.path.exists(ruta_archivo):
            self.cargar()

    def cargar(self):
        """Lee los casos desde el archivo JSON."""
        with open(self.ruta_archivo, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.casos = [
            Caso(identificador=d["identificador"],
                 problema=Problema(**d["problema"]),
                 solucion=d["solucion"],
                 valoraciones={int(k): v for k, v in d["valoraciones"].items()},
                 sintetico=d["sintetico"])
            for d in datos]

    def guardar(self):
        """Escribe todos los casos en el archivo JSON (si hay archivo)."""
        if self.ruta_archivo is not None:
            datos = [{"identificador": c.identificador,
                      "problema": vars(c.problema),
                      "solucion": c.solucion,
                      "valoraciones": c.valoraciones,
                      "sintetico": c.sintetico} for c in self.casos]
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)

    def retener(self, problema, solucion, valoraciones, sintetico):
        """Etapa RETENER: agrega un caso nuevo y lo guarda."""
        caso = Caso(identificador=len(self.casos) + 1, problema=problema,
                    solucion=list(solucion), valoraciones=dict(valoraciones),
                    sintetico=sintetico)
        self.casos.append(caso)
        self.guardar()
        return caso

    def recuperar(self, problema, catalogo, k=CASOS_A_RECUPERAR):
        """
        Etapa RECUPERAR: regresa los k casos más útiles como una lista de
        pares (puntuación, caso), ordenada de mayor a menor. La puntuación
        combina la similitud del problema con la calidad del resultado:
            puntuación = similitud * (0.5 + 0.5 * calidad)
        """
        puntuados = [(similitud_problemas(problema, c.problema, catalogo)
                      * (0.5 + 0.5 * c.calidad()), c) for c in self.casos]
        puntuados.sort(key=lambda par: par[0], reverse=True)
        return puntuados[:k]


def adaptar_solucion(caso, problema, catalogo, preferencias, generador):
    """
    Adaptación básica de una solución recuperada (sin evolución):
    quita los juegos que el usuario anterior rechazó (valoración <= 2) y
    repara la ruta para que cumpla las restricciones del problema nuevo.
    """
    sin_rechazos = [i for i in caso.solucion if caso.valoraciones.get(i, 3) > 2]
    return reparar_ruta(sin_rechazos, problema, catalogo, preferencias, generador)


# =============================================================================
# ALGORITMO EVOLUTIVO (REUTILIZAR MEDIANTE EVOLUCIÓN)
# =============================================================================

class AlgoritmoEvolutivo:
    """
    Algoritmo evolutivo que busca la mejor ruta para un problema.
    Cada individuo es una lista ordenada de identificadores de juegos.
    El criterio de paro es el presupuesto de evaluaciones de aptitud, para
    que la comparación entre versiones sea justa.
    """

    def __init__(self, problema, catalogo, parametros, generador):
        """
        problema (Problema), catalogo (Catalogo), parametros (dict con las
        mismas llaves que PARAMETROS_AE), generador (random.Random).
        """
        self.problema = problema
        self.catalogo = catalogo
        self.parametros = parametros
        self.generador = generador
        self.preferencias = vector_preferencias(problema, catalogo)
        self.candidatos = catalogo.candidatos_validos(problema)
        self.evaluaciones = 0

    def evaluar(self, ruta):
        """Evalúa una ruta y cuenta la evaluación contra el presupuesto."""
        self.evaluaciones += 1
        return evaluar_ruta(ruta, self.problema, self.catalogo, self.preferencias)

    def ruta_aleatoria(self):
        """Genera una ruta válida al azar."""
        cantidad = min(self.problema.longitud, len(self.candidatos))
        return self.generador.sample(self.candidatos, cantidad)

    # ----- Operadores de variación -------------------------------------------

    def mutar(self, ruta):
        """
        Aplica una de tres mutaciones, elegida al azar:
          1) sustituir un juego por otro candidato cualquiera,
          2) sustituir un juego por uno de los más afines a las preferencias,
          3) intercambiar dos posiciones (mejora la continuidad).
        Regresa una ruta nueva; no modifica la original.
        """
        nueva = list(ruta)
        disponibles = [i for i in self.candidatos if i not in nueva]
        tipo = self.generador.randint(1, 3)
        if tipo == 3 or not disponibles:
            if len(nueva) > 1:
                a, b = self.generador.sample(range(len(nueva)), 2)
                nueva[a], nueva[b] = nueva[b], nueva[a]
        else:
            posicion = self.generador.randrange(len(nueva))
            if tipo == 2:
                disponibles.sort(key=lambda i: similitud_coseno(
                    self.preferencias, self.catalogo.vector(i)), reverse=True)
                disponibles = disponibles[:5]
            nueva[posicion] = self.generador.choice(disponibles)
        return nueva

    def cruzar(self, padre_a, padre_b):
        """
        Cruza de orden adaptada a rutas: copia un segmento del padre A y
        completa con los juegos del padre B en el orden en que aparecen,
        sin repetir. Si falta algún juego, la reparación lo completa.
        """
        inicio = self.generador.randrange(len(padre_a))
        fin = self.generador.randrange(inicio, len(padre_a)) + 1
        hijo = padre_a[inicio:fin]
        resto = [i for i in padre_b if i not in hijo]
        hijo = hijo + resto[:self.problema.longitud - len(hijo)]
        return reparar_ruta(hijo, self.problema, self.catalogo,
                            self.preferencias, self.generador)

    def seleccionar(self, poblacion, aptitudes):
        """Selección por torneo: regresa el mejor de tam_torneo individuos."""
        participantes = self.generador.sample(range(len(poblacion)),
                                              self.parametros["tam_torneo"])
        ganador = max(participantes, key=lambda i: aptitudes[i])
        return poblacion[ganador]

    # ----- Medidas -----------------------------------------------------------

    @staticmethod
    def diversidad(poblacion):
        """
        Diversidad genética de la población en [0, 1]: distancia de Jaccard
        promedio entre pares de individuos (como conjuntos de juegos).
        """
        pares = [(a, b) for k, a in enumerate(poblacion) for b in poblacion[k + 1:]]
        resultado = 0.0
        if pares:
            resultado = statistics.mean(1 - similitud_jaccard(set(a), set(b))
                                        for a, b in pares)
        return resultado

    # ----- Ciclo principal ---------------------------------------------------

    def ejecutar(self, poblacion_inicial=None):
        """
        Ejecuta la evolución.
        poblacion_inicial: lista de rutas sembradas (por ejemplo, soluciones
        recuperadas); se completa con rutas aleatorias hasta tam_poblacion.
        Regresa un dict con la mejor ruta, su aptitud, el historial de la
        mejor aptitud por generación, la generación de convergencia (última
        en la que mejoró), las evaluaciones usadas y la diversidad promedio.
        """
        tam = self.parametros["tam_poblacion"]
        poblacion = [list(r) for r in (poblacion_inicial or [])][:tam]
        while len(poblacion) < tam:
            poblacion.append(self.ruta_aleatoria())
        aptitudes = [self.evaluar(r) for r in poblacion]

        historial = [max(aptitudes)]
        diversidades = [self.diversidad(poblacion)]
        generacion = 0
        generacion_convergencia = 0
        por_generacion = tam - self.parametros["num_elites"]

        # Se evoluciona mientras alcance el presupuesto para una generación
        # completa.
        while self.evaluaciones + por_generacion <= self.parametros["presupuesto_evaluaciones"]:
            generacion += 1
            orden = sorted(range(tam), key=lambda i: aptitudes[i], reverse=True)
            nueva = [poblacion[i] for i in orden[:self.parametros["num_elites"]]]
            nuevas_aptitudes = [aptitudes[i] for i in orden[:self.parametros["num_elites"]]]
            while len(nueva) < tam:
                padre_a = self.seleccionar(poblacion, aptitudes)
                padre_b = self.seleccionar(poblacion, aptitudes)
                if self.generador.random() < self.parametros["prob_cruza"]:
                    hijo = self.cruzar(padre_a, padre_b)
                else:
                    hijo = list(padre_a)
                if self.generador.random() < self.parametros["prob_mutacion"]:
                    hijo = self.mutar(hijo)
                nueva.append(hijo)
                nuevas_aptitudes.append(self.evaluar(hijo))
            poblacion, aptitudes = nueva, nuevas_aptitudes
            if max(aptitudes) > historial[-1] + 1e-9:
                generacion_convergencia = generacion
            historial.append(max(aptitudes))
            diversidades.append(self.diversidad(poblacion))

        mejor = max(range(tam), key=lambda i: aptitudes[i])
        return {"ruta": poblacion[mejor], "aptitud": aptitudes[mejor],
                "historial": historial,
                "generacion_convergencia": generacion_convergencia,
                "evaluaciones": self.evaluaciones,
                "diversidad": statistics.mean(diversidades)}


# =============================================================================
# LAS TRES VERSIONES DEL RECOMENDADOR
# =============================================================================

def recomendar_solo_casos(problema, catalogo, memoria, generador):
    """
    Versión 1 - Solo casos: recupera, adapta con reglas básicas y regresa la
    mejor ruta adaptada. Si la memoria está vacía, construye una ruta con los
    candidatos más afines (arranque en frío).
    """
    preferencias = vector_preferencias(problema, catalogo)
    recuperados = memoria.recuperar(problema, catalogo)
    rutas = [adaptar_solucion(c, problema, catalogo, preferencias, generador)
             for _, c in recuperados]
    if not rutas:
        rutas = [reparar_ruta([], problema, catalogo, preferencias, generador)]
    aptitudes = [evaluar_ruta(r, problema, catalogo, preferencias) for r in rutas]
    mejor = max(range(len(rutas)), key=lambda i: aptitudes[i])
    return {"ruta": rutas[mejor], "aptitud": aptitudes[mejor],
            "historial": [aptitudes[mejor]], "generacion_convergencia": 0,
            "evaluaciones": len(rutas), "diversidad": 0.0,
            "casos_usados": [c.identificador for _, c in recuperados]}


def recomendar_solo_evolucion(problema, catalogo, parametros, generador):
    """Versión 2 - Solo evolución: población inicial completamente aleatoria."""
    algoritmo = AlgoritmoEvolutivo(problema, catalogo, parametros, generador)
    return algoritmo.ejecutar()


def recomendar_hibrido(problema, catalogo, memoria, parametros, generador,
                       fraccion_sembrada=0.5):
    """
    Versión 3 - Híbrido: las rutas recuperadas y adaptadas, más variantes
    mutadas de ellas, forman hasta fraccion_sembrada de la población inicial;
    el resto es aleatorio para mantener la exploración.
    """
    algoritmo = AlgoritmoEvolutivo(problema, catalogo, parametros, generador)
    recuperados = memoria.recuperar(problema, catalogo)
    semillas = [adaptar_solucion(c, problema, catalogo, algoritmo.preferencias,
                                 generador) for _, c in recuperados]
    limite = int(parametros["tam_poblacion"] * fraccion_sembrada)
    variantes = []
    indice = 0
    while semillas and len(semillas) + len(variantes) < limite:
        variantes.append(algoritmo.mutar(semillas[indice % len(semillas)]))
        indice += 1
    resultado = algoritmo.ejecutar((semillas + variantes)[:limite])
    resultado["casos_usados"] = [c.identificador for _, c in recuperados]
    return resultado


# =============================================================================
# USUARIOS SIMULADOS (ETAPA REVISAR EN LOS EXPERIMENTOS)
# =============================================================================

class UsuarioSimulado:
    """
    Usuario artificial con gustos OCULTOS. El recomendador solo ve el
    problema declarado (algunos juegos que le gustaron, etc.); la valoración
    se calcula con los gustos ocultos. Así se puede medir si una ruta
    "gusta", y no solo si obtiene buena aptitud.
    """

    def __init__(self, catalogo, generador, longitud=5):
        """Crea un usuario a partir de un arquetipo al azar más ruido."""
        self.catalogo = catalogo
        self.arquetipo = generador.choice(sorted(ARQUETIPOS))
        self.pesos = {e: ARQUETIPOS[self.arquetipo].get(e, 0.0)
                      + generador.gauss(0, 0.25) for e in catalogo.etiquetas}
        self.plataforma = generador.choice(["PC", "PC", "PlayStation",
                                            "Xbox", "Switch"])
        self.problema = self.declarar_problema(generador, longitud)

    def utilidad(self, identificador):
        """Utilidad oculta de un juego en [-1, 1] (coseno con los pesos)."""
        return similitud_coseno(self.pesos, self.catalogo.vector(identificador))

    def valorar(self, identificador):
        """Valoración de 1 a 5 de un juego, a partir de su utilidad oculta."""
        return 1 + round(4 * max(0.0, self.utilidad(identificador)))

    def declarar_problema(self, generador, longitud):
        """
        Construye el problema que el usuario "dice": de una muestra de juegos
        de su plataforma declara los 3 mejores como gustados, el peor como
        rechazado, otros 2 como jugados y sus 2 etiquetas favoritas.
        """
        propios = [i for i, j in self.catalogo.juegos.items()
                   if self.plataforma in j.plataformas]
        muestra = generador.sample(propios, min(10, len(propios)))
        muestra.sort(key=self.utilidad, reverse=True)
        favoritas = sorted(self.pesos, key=self.pesos.get, reverse=True)[:2]
        return Problema(plataforma=self.plataforma, longitud=longitud,
                        gustados=muestra[:3], rechazados=muestra[-1:],
                        jugados=muestra[3:5], etiquetas_preferidas=favoritas)


def poblar_memoria_sintetica(memoria, catalogo, cantidad, generador):
    """
    Genera 'cantidad' casos sintéticos: crea usuarios simulados, les
    recomienda una ruta con solo evolución, la valora con sus gustos ocultos
    y la retiene en la memoria con la marca sintetico=True.
    """
    for _ in range(cantidad):
        usuario = UsuarioSimulado(catalogo, generador)
        resultado = recomendar_solo_evolucion(usuario.problema, catalogo,
                                              PARAMETROS_AE, generador)
        valoraciones = {i: usuario.valorar(i) for i in resultado["ruta"]}
        memoria.retener(usuario.problema, resultado["ruta"], valoraciones, True)


# =============================================================================
# EXPERIMENTOS
# =============================================================================

def satisfaccion(ruta, usuario):
    """Valoración promedio (1 a 5) que el usuario simulado da a la ruta."""
    resultado = 1.0
    if ruta:
        resultado = statistics.mean(usuario.valorar(i) for i in ruta)
    return resultado


def experimento_comparativo(catalogo, num_ejecuciones=50, casos_entrenamiento=60,
                            semilla=2026, graficar=True):
    """
    Compara las tres versiones sobre num_ejecuciones usuarios de prueba.
    1) Llena una memoria temporal con casos sintéticos (entrenamiento).
    2) Para cada usuario de prueba ejecuta las tres versiones.
    3) Imprime promedio y desviación estándar de: aptitud, satisfacción
       simulada, generación de convergencia, evaluaciones, diversidad,
       tiempo y violaciones de restricciones.
    Regresa un dict versión -> lista de resultados.
    """
    generador = random.Random(semilla)
    memoria = MemoriaCasos(None)
    print(f"\nGenerando {casos_entrenamiento} casos sintéticos de entrenamiento...")
    poblar_memoria_sintetica(memoria, catalogo, casos_entrenamiento, generador)

    versiones = ["solo_casos", "solo_evolucion", "hibrido"]
    resultados = {v: [] for v in versiones}
    for ejecucion in range(num_ejecuciones):
        usuario = UsuarioSimulado(catalogo, generador)
        for version in versiones:
            # Misma semilla por ejecución para las tres versiones.
            generador_version = random.Random(semilla * 1000 + ejecucion)
            inicio = time.perf_counter()
            if version == "solo_casos":
                r = recomendar_solo_casos(usuario.problema, catalogo, memoria,
                                          generador_version)
            elif version == "solo_evolucion":
                r = recomendar_solo_evolucion(usuario.problema, catalogo,
                                              PARAMETROS_AE, generador_version)
            else:
                r = recomendar_hibrido(usuario.problema, catalogo, memoria,
                                       PARAMETROS_AE, generador_version)
            r["tiempo"] = time.perf_counter() - inicio
            r["satisfaccion"] = satisfaccion(r["ruta"], usuario)
            r["violaciones"] = contar_violaciones(r["ruta"], usuario.problema, catalogo)
            resultados[version].append(r)

    metricas = ["aptitud", "satisfaccion", "generacion_convergencia",
                "evaluaciones", "diversidad", "tiempo", "violaciones"]
    print(f"\nResultados promedio sobre {num_ejecuciones} usuarios de prueba")
    print(f"{'métrica':<25}" + "".join(f"{v:>22}" for v in versiones))
    for metrica in metricas:
        fila = f"{metrica:<25}"
        for version in versiones:
            valores = [r[metrica] for r in resultados[version]]
            desviacion = statistics.stdev(valores) if len(valores) > 1 else 0.0
            fila += f"{statistics.mean(valores):>13.4f} ± {desviacion:<6.3f}"
        print(fila)

    if graficar:
        graficar_convergencia(resultados)
    return resultados


def graficar_convergencia(resultados):
    """Grafica la mejor aptitud promedio por generación de las versiones evolutivas."""
    plt.figure(figsize=(7, 4))
    for version in ["solo_evolucion", "hibrido"]:
        historiales = [r["historial"] for r in resultados[version]]
        largo = min(len(h) for h in historiales)
        promedio = [statistics.mean(h[g] for h in historiales) for g in range(largo)]
        plt.plot(range(largo), promedio, label=version.replace("_", " "))
    plt.xlabel("Generación")
    plt.ylabel("Mejor aptitud promedio")
    plt.title("Convergencia: solo evolución contra híbrido")
    plt.legend()
    plt.tight_layout()
    plt.show()


# =============================================================================
# INTERFAZ DE CONSOLA (DEMOSTRACIÓN EN VIVO)
# =============================================================================

def leer_lista_enteros(mensaje, catalogo):
    """
    Pide una lista de identificadores separados por comas. Ignora los
    valores que no sean números o que no existan en el catálogo.
    """
    texto = input(mensaje).strip()
    resultado = []
    for parte in texto.split(","):
        parte = parte.strip()
        if parte.isdigit() and int(parte) in catalogo.juegos:
            resultado.append(int(parte))
    return resultado


def leer_entero(mensaje, minimo, maximo, por_omision):
    """Pide un entero en [minimo, maximo]; si es inválido usa por_omision."""
    texto = input(mensaje).strip()
    resultado = por_omision
    if texto.isdigit() and minimo <= int(texto) <= maximo:
        resultado = int(texto)
    return resultado


def mostrar_catalogo(catalogo):
    """Imprime el catálogo en forma de tabla."""
    for juego in catalogo.juegos.values():
        print(f"{juego.identificador:>3}  {juego.titulo:<40} "
              f"{', '.join(sorted(juego.etiquetas))}")


def mostrar_memoria(memoria, catalogo):
    """Imprime un resumen de los casos almacenados."""
    print(f"\nCasos almacenados: {len(memoria.casos)}")
    for caso in memoria.casos[-10:]:
        marca = "sintético" if caso.sintetico else "real"
        titulos = ", ".join(catalogo.titulo(i) for i in caso.solucion)
        print(f"  Caso {caso.identificador} ({marca}, calidad "
              f"{caso.calidad():.2f}): {titulos}")


def sesion_recomendacion(catalogo, memoria):
    """
    Ciclo completo de RBC con un usuario humano:
    recuperar -> reutilizar (híbrido) -> revisar (valoraciones) -> retener.
    """
    print("\nPlataformas disponibles: " + ", ".join(catalogo.plataformas))
    plataforma = input("Plataforma: ").strip()
    if plataforma not in catalogo.plataformas:
        print("Plataforma no reconocida; se usará PC.")
        plataforma = "PC"
    problema = Problema(
        plataforma=plataforma,
        longitud=leer_entero("Número de juegos en la ruta (1-8, por omisión 5): ",
                             1, 8, 5),
        gustados=leer_lista_enteros("Identificadores de juegos que te gustaron: ",
                                    catalogo),
        rechazados=leer_lista_enteros("Identificadores de juegos que no te gustaron: ",
                                      catalogo),
        jugados=leer_lista_enteros("Identificadores de otros juegos que ya jugaste: ",
                                   catalogo),
        etiquetas_preferidas=[e.strip() for e in input(
            "Etiquetas que valoras (" + ", ".join(catalogo.etiquetas) + "): "
        ).split(",") if e.strip() in catalogo.etiquetas])

    generador = random.Random()
    resultado = recomendar_hibrido(problema, catalogo, memoria, PARAMETROS_AE,
                                   generador)
    print(f"\nCasos recuperados: {resultado['casos_usados'] or 'ninguno (arranque en frío)'}")
    print(f"Ruta recomendada (aptitud {resultado['aptitud']:.3f}):")
    for posicion, identificador in enumerate(resultado["ruta"], start=1):
        print(f"  {posicion}. {catalogo.titulo(identificador)}")

    # Etapa REVISAR: el usuario valora cada recomendación.
    valoraciones = {}
    for identificador in resultado["ruta"]:
        valoraciones[identificador] = leer_entero(
            f"Valora «{catalogo.titulo(identificador)}» de 1 a 5: ", 1, 5, 3)

    # Etapa RETENER.
    caso = memoria.retener(problema, resultado["ruta"], valoraciones, False)
    print(f"Experiencia guardada como caso {caso.identificador}.")


def menu_principal():
    """Muestra el menú y ejecuta la opción elegida hasta que se elija salir."""
    catalogo = Catalogo(RUTA_CATALOGO)
    memoria = MemoriaCasos(RUTA_MEMORIA)
    salir = False
    while not salir:
        print("\n==== Recomendador de rutas de videojuegos (RBC + AE) ====")
        print("1) Pedir una recomendación")
        print("2) Generar casos sintéticos")
        print("3) Experimento comparativo")
        print("4) Mostrar catálogo")
        print("5) Mostrar memoria de casos")
        print("6) Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            sesion_recomendacion(catalogo, memoria)
        elif opcion == "2":
            cantidad = leer_entero("¿Cuántos casos? (por omisión 20): ", 1, 1000, 20)
            poblar_memoria_sintetica(memoria, catalogo, cantidad, random.Random())
            print(f"Listo. La memoria tiene {len(memoria.casos)} casos.")
        elif opcion == "3":
            ejecuciones = leer_entero("Número de usuarios de prueba (por omisión 50): ",
                                      2, 500, 50)
            experimento_comparativo(catalogo, num_ejecuciones=ejecuciones)
        elif opcion == "4":
            mostrar_catalogo(catalogo)
        elif opcion == "5":
            mostrar_memoria(memoria, catalogo)
        elif opcion == "6":
            salir = True
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu_principal()
