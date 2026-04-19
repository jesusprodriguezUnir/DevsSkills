---
name: python-performance-optimization
description: Domina el perfilado y la optimización en Python (cProfile, memory_profiler, optimización de CPU y estructuras de datos eficientes).
category: Python
license: Private
---

# Optimización de Rendimiento en Python

## Cuándo usar esta habilidad

Recurre a esta habilidad cuando necesites:
- Identificar y resolver cuellos de botella de CPU o memoria en proyectos Python.
- Mejorar la velocidad de ejecución de pipelines de datos o scripts recurrentes.
- Seleccionar las estructuras de datos más eficientes para bucles críticos.
- Usar perfiladores para identificar las líneas exactas que causan ralentizaciones.

## Herramientas Esenciales de Perfilado (Profiling)

### Perfilado de CPU

Evita siempre adivinar el origen de la ineficiencia. `cProfile` viene con Python y aporta métricas claras en C:

```bash
python -m cProfile -s cumtime mi_script.py
```

Para una inspección línea por línea, instala `line_profiler` y marca las funciones objetivo con `@profile`:

```bash
kernprof -l -v mi_script.py
```

### Perfilado de Memoria

Si sufres problemas de asignación de memoria o fugas, utiliza `memory_profiler`:

```python
from memory_profiler import profile

@profile
def funcion_intensiva_en_memoria():
    # Cálculos grandes
    pass
```

## Antipatrones y Mejores Prácticas

### 1. El Global Interpreter Lock (GIL) no siempre es el enemigo
- **Tareas de Red o Disco (I/O Bound)**: Utiliza `asyncio` o `threading`. El hilo en Python suelta el GIL mientras espera I/O.
- **Tareas Matemáticas (CPU Bound)**: Utiliza el módulo `multiprocessing` para operar en núcleos de CPU paralelos evadiendo el GIL.

### 2. Estructuras de Datos Eficientes
- Nunca modifiques o extraigas objetos por el comienzo de una lista (`list.pop(0)`). Utiliza `collections.deque` si prevees actuar como cola FIFO con un coste O(1).
- Evita verificar pertenencia contra listas (`if x in list:`). Realiza estos test unitarios O(1) convirtiendo tu contenedor a objeto `set`.

### 3. Vectorización en lugar de bucles for
La ejecución de un `for` en el intérprete de Python es significativamente lenta al arrastrar "overhead" en cada iteración.
```python
# Lento
[x * 2 for x in data]

# Altamente Eficiente (usando C detrás con numpy)
data_array * 2
```

## Concatenación de Cadenas (Strings)

Evita las uniones con el operador `+` en bucles, pues Python reconstruye en memoria una cadena tras otra.
```python
# Menos Optimo
resultado = ""
for caracter in data:
    resultado += caracter

# Óptimo (O(N))
resultado = "".join(data)
```
