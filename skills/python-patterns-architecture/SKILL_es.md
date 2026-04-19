---
name: python-patterns-architecture
description: Principios de desarrollo avanzado, sugerencias de tipos (type hints), clean architecture y estructura de proyectos mantenibles en Python.
category: Python
license: Private
---

# Arquitectura y Patrones en Python

## Cuándo usar esta habilidad

Activa este protocolo cuando:
- Necesites refactorizar una base de código monolítica en Python hacia una "Clean Architecture".
- Estés definiendo modelos de dominio y requieras validaciones/definiciones estrictas de tipo usando `typing` o `pydantic`.
- Encaras complejidad inyectando dependencias o aplicando Inversión de Control (IoC) en un entorno Python.

## Type Hints (Sugerencias de Tipado)

El desarrollo moderno de Python confía intensamente en Type Hints (tipado) para mejorar la experiencia de desarrollo e implantar seguridad en CI.

```python
from typing import List, Optional, Callable
from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nombre_usuario: str
    email: Optional[str] = None

def obtener_usuarios_activos(usuarios: List[Usuario], esta_activo: Callable[[Usuario], bool]) -> List[Usuario]:
    return [u for u in usuarios if esta_activo(u)]
```

Utiliza siempre verificadores estáticos como `mypy` o `pyright` en modo estricto.

## La Clean Architecture (Arquitectura Limpia) en Python

Separa tu sistema garantizando la regla de dependencia: Las capas internas (entidades) no deben conocer elementos de las exteriores (frameworks o BBDD).

### 1. Dominio / Entidades
Clases puras en Python, sin rastro de código SQLAlchemy, Django o FastAPI.

### 2. Casos de Uso (Reglas de Negocio)
Orquestan el movimiento de la información y la ejecución en el Dominio.

### 3. Adaptadores (Interfaces)
Controladores y repositorios. Traducen información desde/para el exterior.

```python
from abc import ABC, abstractmethod

# La interfaz que debe cumplir cualquier DB
class InterfazRepositorioUsuarios(ABC):
    @abstractmethod
    def obtener_por_id(self, user_id: int) -> Usuario:
        pass

# El caso de uso
class CasoDeUsoBloquearUsuario:
    def __init__(self, repo: InterfazRepositorioUsuarios):
        self.repo = repo

    def ejecutar(self, user_id: int):
        usuario = self.repo.obtener_por_id(user_id)
        # Lógica de dominio aquí
        return usuario
```

### 4. Frameworks & Drivers
Asegura que el Framework web (punto de entrada) sea el encargado de inyectar las piezas finales.

## Gestión de Errores Estandarizada

No provoques fallos abstractos; implementa excepciones de dominio ad-hoc que tus capas HTTP mapeen automáticamente a códigos estándar correctos.
