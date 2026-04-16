---
name: dotnet-wiki-generator
description: Genera documentación wiki estructurada a partir de código fuente .NET Core. Extrae XML docs, analiza arquitectura, y produce páginas Markdown para GitHub Wiki o Confluence. Úsala para documentar APIs, dominios y decisiones de arquitectura.
license: Private
compatibility: Requiere .NET 8+ SDK. Soporta salida Markdown y HTML.
---

# .NET Core — Generador de Wiki

Skill para generar documentación wiki profesional y estructurada a partir de proyectos .NET Core.

## Capacidades

1. **Extracción automática** de XML documentation comments
2. **Análisis de arquitectura** — capas, dependencias, patrones usados
3. **Generación de diagramas** — dependencias entre proyectos, flujos de datos
4. **Índice navegable** — tabla de contenidos jerárquica
5. **API Reference** — documentación de endpoints, DTOs y contratos

## Estructura de Wiki Generada

```
wiki/
├── Home.md                      # Página principal con visión general
├── getting-started.md           # Guía de inicio rápido
├── architecture/
│   ├── overview.md              # Diagrama y descripción de capas
│   ├── decisions.md             # ADRs (Architecture Decision Records)
│   └── dependencies.md          # Mapa de dependencias entre proyectos
├── domain/
│   ├── entities.md              # Entidades del dominio
│   ├── value-objects.md         # Value Objects
│   └── events.md                # Eventos de dominio
├── api/
│   ├── endpoints.md             # Lista de endpoints REST
│   ├── authentication.md        # Flujo de autenticación
│   └── error-codes.md           # Códigos de error y respuestas
├── database/
│   ├── schema.md                # Esquema de base de datos
│   └── migrations.md            # Historial de migraciones
└── development/
    ├── setup.md                 # Configuración del entorno
    ├── conventions.md           # Convenciones de código
    └── testing.md               # Guía de testing
```

## Proceso de Generación

### Paso 1: Escanear la Solución

```bash
# Obtener estructura del proyecto
dotnet sln list
```

Analizar:
- Proyectos en la solución y sus relaciones
- NuGet packages usados (para inferir stack)
- Archivos de configuración (`appsettings.json`, `Program.cs`)
- Migraciones de Entity Framework

### Paso 2: Extraer Documentación del Código

Buscar y extraer:

```csharp
/// <summary>
/// Servicio principal para gestión de usuarios.
/// </summary>
/// <remarks>
/// Implementa el patrón Repository + Unit of Work.
/// Las operaciones de escritura son transaccionales.
/// </remarks>
public class UserService : IUserService
```

### Paso 3: Generar Home.md

```markdown
# {NombreProyecto}

> {Descripción extraída del .csproj o README}

## Stack Tecnológico

| Categoría | Tecnología |
|-----------|-----------|
| Framework | .NET 8 |
| ORM | Entity Framework Core 8 |
| Auth | JWT + Identity |
| Cache | Redis |
| Mensajería | MediatR |

## Arquitectura

{Diagrama Mermaid generado automáticamente}

## Proyectos

| Proyecto | Tipo | Descripción |
|----------|------|-------------|
| src/Domain | Class Library | Entidades, interfaces, eventos |
| src/Application | Class Library | Casos de uso, DTOs, validaciones |
| src/Infrastructure | Class Library | EF Core, servicios externos |
| src/API | Web API | Controllers, middleware, config |

## Enlaces Rápidos

- [Guía de Inicio](getting-started.md)
- [Arquitectura](architecture/overview.md)
- [API Reference](api/endpoints.md)
- [Base de Datos](database/schema.md)
```

### Paso 4: Generar Documentación de API

Para cada Controller, generar:

```markdown
## POST /api/users

Crea un nuevo usuario en el sistema.

### Request

```json
{
  "name": "string (requerido, 2-100 chars)",
  "email": "string (requerido, formato email)",
  "role": "string (admin | user | viewer)"
}
``` 

### Responses

| Código | Descripción | Body |
|--------|-------------|------|
| 201 | Usuario creado | `UserDto` |
| 400 | Validación fallida | `ProblemDetails` |
| 409 | Email duplicado | `ProblemDetails` |

### Ejemplo

```bash
curl -X POST https://api.example.com/api/users \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan", "email": "juan@example.com", "role": "user"}'
```
```

### Paso 5: Generar Architecture Decision Records (ADRs)

```markdown
## ADR-001: Usar MediatR para CQRS

**Estado**: Aceptado  
**Fecha**: 2024-01-15

### Contexto
Necesitamos separar las operaciones de lectura y escritura para mejorar la escalabilidad.

### Decisión
Usar MediatR como mediador para implementar CQRS ligero sin event sourcing.

### Consecuencias
- ✅ Handlers desacoplados y testables
- ✅ Pipeline behaviors para cross-cutting concerns
- ⚠️ Indirección adicional puede dificultar debugging
```

## Formato de Salida

### Para GitHub Wiki
- Archivos `.md` en directorio `wiki/`
- Enlaces relativos entre páginas
- Sidebar (`_Sidebar.md`) con navegación

### Para Confluence
- Formato Confluence Wiki markup
- Macros de código y tablas nativas
- Jerarquía de páginas padre-hijo

## Checklist de Documentación Completa

- [ ] Home con visión general del proyecto
- [ ] Diagrama de arquitectura actualizado
- [ ] Cada endpoint documentado con request/response
- [ ] Entidades del dominio con relaciones
- [ ] Guía de setup para nuevos desarrolladores
- [ ] ADRs para decisiones técnicas importantes
- [ ] Convenciones de código documentadas
- [ ] Esquema de base de datos actualizado

## Mantenimiento

### Automatización con CI/CD

```yaml
# Regenerar wiki en cada merge a main
- name: Generate Wiki
  run: |
    dotnet tool run docfx build docs/docfx.json
    # O ejecutar el script de generación personalizado
```

### Señales de Wiki Obsoleta

- Endpoints documentados que ya no existen
- Diagramas que no reflejan los proyectos actuales
- Configuraciones que ya no aplican
- Versiones de paquetes desactualizadas
