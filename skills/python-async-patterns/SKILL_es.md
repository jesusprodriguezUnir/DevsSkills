---
name: python-async-patterns
description: Guías exhaustivas de programación asíncrona en Python con Asyncio, operaciones I/O y protección frente al bloqueo del Event Loop.
category: Python
license: Private
---

# Patrones Asíncronos en Python

## Cuándo usar esta habilidad

Sigue estas directrices cuando:
- Entables la creación de endpoints robustos de alta demanda (p. ej. en FastAPI).
- Orquestes múltiples llamadas HTTP en paralelo o Scrapers Web.
- Interactúes con bases de datos adaptadas a I/O (asyncpg, acore).
- Necesites enlazar entornos estrictamente síncronos y costosos delegándolos a hilos.

## Multitarea Cooperativa en el Event Loop

`asyncio` introduce la multitarea cooperativa en Python. En lugar de ceder el poder al Sistema Operativo, tu propio código asume la responsabilidad de liberar paso al Event Loop mediante la palabra reservada `await`.

Regla Sagrada: **Jamás bloquees un proceso continuo y pesado carente del modificador await dentro de un bloque `async def`. Esta negligencia congela todo tu ecosistema concurrente.**

```python
import asyncio
import time

# TERRIBLE Y LETAL - Pausa todas las peticiones activas de tus usuarios.
async def mal_patron():
    time.sleep(5)  

# EXCELENTE - Permite a otros usuarios interactuar mientras se aguarda.
async def buen_patron():
    await asyncio.sleep(5)
```

## Disparando la Concurrencia

Si pretendes cargar tres páginas web que no dependen una de la otra, lanzalas a la vez y agrúpalas mediante `asyncio.gather`.

```python
import asyncio

async def consultar_usuario(id: int):
    # Simulacro red/DB
    await asyncio.sleep(1)
    return f"Usuario {id}"

async def principal():
    # Toma 1 solo segundo. Lanza y extrae los tres valores simultáneamente.
    resultados = await asyncio.gather(
        consultar_usuario(1),
        consultar_usuario(2),
        consultar_usuario(3)
    )
    print(resultados)
```

## Puentes al Infierno (Código Síncrono a Asíncrono)

Para encriptaciones costosas o librerías del pasado sin capa asíncrona (ej. el módulo `requests`), despácha la tara hacia el contenedor de Hilos propio (`threadpool`) evadiendo interrumpir el Event Loop principal de `asyncio`.

```python
import asyncio
import requests # Librería Síncrona

def bloquear_la_red():
    respuesta = requests.get('https://example.com')
    return respuesta.status_code

async def principal():
    # Offload al ThreadPool subyacente de Python
    loop = asyncio.get_running_loop()
    estado = await loop.run_in_executor(None, bloquear_la_red)
    print(estado)
```

## Control estricto
A largo plazo, considera abstraer en favor de librearías como `anyio` u operar usando TaskGroups (`asyncio.TaskGroup`) para controlar y detener flujos huérfanos que provocan fugas de memoria incontrolables.
