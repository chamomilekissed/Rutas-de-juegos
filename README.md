[README.md](https://github.com/user-attachments/files/35108204/README.md)
# Recomendador evolutivo de videojuegos

Si vuelves varias veces a *Silent Hill 2*, ¿qué otro juego podría interesarte? Este programa aprende de tus partidas y recomienda **hasta cinco videojuegos en orden**, sin preguntarte tus gustos. En la consola verás por qué eligió cada título y qué comparte con el anterior.

## Prueba la demostración

Necesitas **Python 3.10 o posterior**. El archivo `proyecto2.py` incluye los dos catálogos y utiliza la biblioteca estándar de Python. Puedes ejecutarlo sin conexión.

- **En Spyder**, abre `proyecto2.py`, busca `MODO = "recomendar"`, cámbialo por `MODO = "demo"` y pulsa **F5**.
- **En la terminal**, abre la carpeta donde guardaste el archivo y ejecuta este comando.

```bash
python proyecto2.py --modo demo
```

La demo imprime dos rutas. Con la configuración inicial, la primera empieza por *ATRI -My Dear Moments-*. Luego simula seis sesiones de *Resident Evil 2*, cuatro de *Silent Hill 2* y una de *Rocket League*. Ahora la primera sugerencia es *The Evil Within 2*. Debajo del título puedes leer qué rasgos aprendió a favorecer el programa, entre ellos el terror psicológico.

## Cómo pasa de tus partidas a una ruta

1. **Reúne los candidatos.** Combina los catálogos de ventas y de Steam. Cada juego tiene una ficha con los datos disponibles, como plataforma y género. Si eliges una plataforma, filtra por ella. Aparta los juegos en los que detectó actividad, aunque solo haya registrado una sesión.
2. **Estima la afinidad.** La afinidad indica cuánto podría interesarte un título. Al principio usa reseñas y popularidad. Dos o más sesiones de un juego, o al menos 90 minutos registrados en Steam, cuentan como señal de interés. Una **regresión logística** compara los rasgos de estos juegos con los de juegos de uso breve y una muestra del catálogo. Así aprende, por ejemplo, cuánto peso dar al terror cuando puntúa un juego nuevo.
3. **Prueba rutas por mutación.** Cada lista de juegos es un *individuo*. El conjunto de listas es la *población*. El algoritmo conserva algunas de las mejores y elige un solo padre para crear cada variante. Puede sustituir un título, pasando de `[A, B, C]` a `[A, D, C]`, o intercambiar dos puestos para probar `[B, A, C]`. La **mutación** es su único operador de variación.

Cada ruta recibe una nota de 0 a 1 llamada **aptitud**. El **60 %** corresponde a la afinidad media con tu perfil, el **20 %** a la variedad de la lista y el **20 %** al parecido entre juegos consecutivos. Por eso cambiar el orden puede mejorar una ruta aunque contenga los mismos títulos. Un segundo algoritmo evolutivo muta un parámetro a la vez para ajustar el primero, por ejemplo, cuántas rutas compara en cada generación.

## Usarlo con tus propias partidas

En Spyder, vuelve a `MODO = "recomendar"`. En la terminal, ejecuta `python proyecto2.py`. Al arrancar, intenta leer la actividad local de Steam. Guarda los totales en un archivo llamado `perfil_jugador.sqlite3`. La primera recomendación también tarda en ajustar el algoritmo. Las siguientes pueden reutilizar esos ajustes.

También puedes crear un archivo de texto llamado `historial_juego.csv` en la misma carpeta. Guárdalo en UTF-8 y usa punto y coma para separar el título del total de sesiones.

```csv
titulo;sesiones
Resident Evil 2;6
Silent Hill 2;4
Rocket League;1
```

Si vuelves a jugar *Silent Hill 2*, cambia el 4 por un 5. Son **totales acumulados**. Este comando prueba el CSV en un perfil nuevo y limita la ruta a juegos de PC.

```bash
python proyecto2.py --sin-steam --perfil prueba.sqlite3 --plataforma PC
```

Puedes consultar las plataformas disponibles con `python proyecto2.py --modo catalogo`.

## Por dónde empezar a leer el código

Abre `proyecto2.py` en tu editor y busca estos nombres en orden. El bloque largo llamado `DATOS_INCLUIDOS` contiene los catálogos comprimidos.

| Busca | Qué observar |
| --- | --- |
| `def principal(` | Carga el catálogo, aplica la plataforma y abre el modo que elegiste. |
| `def recomendar(` | Lee la actividad, deja fuera los juegos conocidos y pide una ruta. |
| `def aprender_perfil(` | Convierte partidas en pesos. La función `estimar_afinidad` usa esos pesos para puntuar cada juego. |
| `def mutar(self, padre)` | Sustituye o mueve títulos. El método `medir` de la clase `Problema` calcula qué puntuación recibe la lista. |

## Errores comprobados y mejoras posibles

| Qué sucede hoy | Qué lo causa | Cómo se podría mejorar |
| --- | --- | --- |
| *Prey* de 2006 y *Prey* de 2017 comparten una sola ficha. Jugar uno puede excluir ambos. | El catálogo los agrupa por el título y conserva el año más antiguo. | Identificar las ediciones por su ID y comprobar año y estudio antes de unir fichas. |
| Si registras 60 sesiones por error y corriges el CSV a 6, el perfil sigue usando 60. | Al importar, el programa conserva el máximo registrado para evitar contar dos veces las mismas partidas. | Añadir una opción de corrección. Hoy puedes probar el CSV corregido con un perfil nuevo mediante `--perfil`. |
| Un título mal escrito puede quedar fuera del perfil sin aviso. | El importador solo incorpora los nombres que reconoce en el catálogo. | Mostrar qué filas se omitieron y sugerir coincidencias para que puedas corregirlas. |

También hay un límite al interpretar los gustos. Puedes terminar un juego corto en una sesión y disfrutarlo mucho. Comparar tu tiempo de juego con la duración habitual del título ayudaría a interpretar esa señal.

## Cómo comprobar los resultados

Ejecuta `python proyecto2.py --modo experimento`. Tras ajustar los parámetros con seis escenarios simulados, compara cuatro métodos en **50 escenarios nuevos**. Los métodos son popularidad, afinidad individual, evolución con parámetros fijos y evolución con parámetros ajustados. En `resultados_experimento.csv` quedan 200 filas. Un cero en `violaciones` indica que la ruta tiene la longitud esperada y contiene solo juegos permitidos y sin repetir.

El interés que se mide en ese experimento es simulado. Una mejora sería probar las rutas con jugadores y observar qué recomendaciones deciden jugar por segunda vez.

## Datos incluidos

El catálogo combina `Video_Games_Sales_as_at_22_Dec_2016.csv` con la versión 59 del catálogo de Steam de FronkonGames. Al agrupar por título, esta edición reúne **158 706 fichas**. [Steam Games Dataset en Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/versions/59)
