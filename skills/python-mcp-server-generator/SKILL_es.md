---
name: python-mcp-server-generator
description: Mejores prácticas para implementar Servidores del Protocolo MCP (Model Context Protocol) en Python para dotar a los Agentes de herramientas.
category: Python
license: Private
---

# Generador de Servidores MCP en Python

## Cuándo usar esta habilidad

Activa este protocolo cuando:
- Construyas proveedores de Contexto y Herramientas para clientes de IA como Claude Desktop.
- Quieras implementar un subsistema especializado que actúe de 'ojos y manos' para tu Model Language.
- Te comuniques bajo un puente de canal estándar (stdio) o Server-Sent Events (SSE).

## El Standard MCP (Model Context Protocol)

MCP conforma un mecanismo desacoplado para trasladar capacidades desarrolladas en Python directamente a interfaces que la IA entiende y ejecuta.

### Servidor Estándar (FastMCP)

Para evitar el exceso de infraesctructura, despliega `FastMCP`:

```python
from mcp.server.fastmcp import FastMCP

# 1. Inicializar la instancia
mcp = FastMCP("Servidor Metereológico")

# 2. Exponer una función al agente de IA con el decorador @mcp.tool
@mcp.tool()
def obtener_tiempo(ciudad: str) -> str:
    """Busca y devuelve el tiempo metereologico de una ciudad en formato string."""
    return f"El tiempo en {ciudad}: 21C, Soleado"

# 3. Arrancar la pasarela
if __name__ == "__main__":
    mcp.run()
```

## Arquitectura de Interfaz o Pasarela (Bridging)

Separa con claridad la variable privada de la variable del Agente. Para mantener robustez y evitar vulnerabilidades provocadas por alucinaciones de la IA, consolida los argumentos entrantes usando validadores como `pydantic`. `FastMCP` transfiere el esquema Python a JSON Schema automáticamente.

```python
from pydantic import BaseModel, Field

class PeticionAlerta(BaseModel):
    mensaje: str = Field(description="El texto de la alerta")
    urgencia: int = Field(description="Nivel del 1 al 5")

@mcp.tool()
def enviar_alerta(peticion: PeticionAlerta) -> str:
    """Envía un mensaje urgente a la sala de operaciones del equipo."""
    print(f"[{peticion.urgencia}] ALERTA: {peticion.mensaje}")
    return "Alerta transmitida correctamente."
```

## Ejecución Pura

Si usas el entorno moderno con `uv` y tu comunicación subyacente es standard input/output (stdio), tu script es directamente inyectable al bloque de configuración JSON del cliente.

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["run", "ruta/a/mi_server.py"]
    }
  }
}
```
