---
name: python-testing-patterns
description: Estrategias integrales de pruebas en Python usando Pytest, fixtures, mocking y metodologías TDD.
category: Python
license: Private
---

# Patrones de Testing en Python

## Cuándo usar esta habilidad

Aplica este conjunto de reglas cuando:
- Entables la creación de una test-suite (batería de pruebas) blindada y robusta en Python.
- Necesites aislar servicios caóticos (APIs, Bases de datos, S3) mediante `unittest.mock`.
- Administres ciclos de inyección de datos reutilizables empleando Fixtures de Pytest.
- Implementes la filosofía Test-Driven Development (TDD) asumiendo una calidad determinista superior.

## Fixtures de Pytest

`pytest` brilla de manera excepcional frente a la librería genérica `unittest` al proveer `fixtures` inyectables que reemplazan la herencia tediosa de clase.

```python
import pytest

@pytest.fixture
def base_de_datos():
    # Arrange / Setup (Preparación)
    conexion = DataBase.connect(":memory:")
    yield conexion
    # Teardown (Destrucción / Limpieza)
    conexion.disconnect()

def test_creacion_de_usuario(base_de_datos):
    user = User(name="Alicia")
    base_de_datos.save(user)
    assert base_de_datos.count() == 1
```

## Mockeado de Dependencias Externas (Mocks & Patches)

Todo requerimiento que salte a la red externa debe falsearse simulando las respuestas (Mocks). Esto asegura pruebas veloces e impenetrables al clima externo.

```python
from unittest.mock import patch

def test_extraccion_datos_externos():
    with patch("miapp.servicios.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1, "name": "Falso"}
        
        resultado = miapp.servicios.extraer_usuario()
        assert resultado["name"] == "Falso"
        mock_get.assert_called_once()
```

## Metodología Test-Driven Development (TDD)

1. **Rojo (Red)**: Escribe una única aserción que materialice tu objetivo y comprueba cómo falla.
2. **Verde (Green)**: Modifica tu código escribiendo la porción estricta de lógica orientada a solventar el fallo. Deténte ahí.
3. **Refactorización (Refactor)**: Reordena, limpia lógica repetida, reduce la indentación de tu código sin miedo y manteniendo el sistema Verde.

## Patrones Avanzados

### Testeo Parametrizado

Utiliza el decorador `@pytest.mark.parametrize` para evitar la proliferación y clonación injusta de códigos por el simple hecho de probar diferentes strings o valores atípicos.

```python
@pytest.mark.parametrize("entrada, esperado", [
    ("", False),
    ("correcto@email.com", True),
    ("email_mal.com", False),
])
def test_validacion_email(entrada, esperado):
    assert es_email_valido(entrada) is esperado
```
