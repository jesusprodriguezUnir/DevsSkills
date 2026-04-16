---
name: openup-create-vision
description: Genera un documento de visión a partir de la plantilla
arguments:
  - name: project_name
    description: Nombre del proyecto
    required: true
  - name: problem_statement
    description: Descripción breve del problema a resolver
    required: true
---

# Crear Documento de Visión

Esta skill genera un documento de visión a partir de la plantilla OpenUP.

## Cuándo Usar

Usa esta skill cuando:
- Comiences un nuevo proyecto y necesites definir la visión
- Estés en la fase de Inicio y necesites documentar el alcance del proyecto
- Los interesados necesiten una comprensión clara de los objetivos del proyecto
- Necesites definir el planteamiento del problema y la solución propuesta
- Crees los artefactos iniciales del proyecto

## Cuándo NO Usar

NO uses esta skill cuando:
- El documento de visión ya existe (actualízalo directamente o usa un proceso de revisión)
- Necesites requisitos detallados (usa las skills de casos de uso en su lugar)
- Busques arquitectura técnica (usa `/openup-create-architecture-notebook`)
- Estés en fases posteriores (Elaboración+) cuando la visión debería estar estable

## Criterios de Éxito

Tras usar esta skill, verifica:
- [ ] El documento de visión existe en `docs/vision.md`
- [ ] El nombre del proyecto y el planteamiento del problema están completados
- [ ] Los interesados están identificados
- [ ] Las funcionalidades clave están listadas
- [ ] Los criterios de éxito están definidos

## Proceso

### 1. Leer Contexto del Proyecto

Leer `docs/project-status.md` para comprender:
- Fase actual
- Interesados
- Contexto del proyecto

### 2. Copiar Plantilla

Copiar `docs-eng-process/templates/vision.md` a `docs/vision.md`

### 3. Completar el Documento de Visión

Actualizar el documento de visión con:
- **Nombre del proyecto**: `$ARGUMENTS[project_name]`
- **Planteamiento del problema**: `$ARGUMENTS[problem_statement]`
- **Posicionamiento**: Qué hace única a esta solución
- **Interesados**: Interesados clave y sus necesidades
- **Funcionalidades clave**: Lista de funcionalidades a alto nivel
- **Restricciones**: Técnicas, de negocio u otras restricciones

### 4. Validar Completitud

Asegurar que el documento de visión incluya:
- Planteamiento del problema claro
- Visión general de la solución propuesta
- Descripciones de los interesados
- Funcionalidades y beneficios clave
- Criterios de éxito

## Salida

Devuelve:
- Ruta al documento de visión creado
- Lista de secciones completadas
- Secciones que requieren completarse manualmente

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Plantilla no encontrada | Ruta de plantilla incorrecta | Verificar que `docs-eng-process/templates/vision.md` existe |
| El archivo ya existe | El documento de visión ya fue creado | Actualizar el archivo existente o confirmar sobrescritura |
| Argumentos ausentes | Argumentos requeridos no proporcionados | Proporcionar project_name y problem_statement |

## Referencias

- Plantilla de Visión: `docs-eng-process/templates/vision.md`
- Producto de Trabajo de Visión: `docs-eng-process/openup-knowledge-base/core/common/workproducts/vision.md`
- Rol de Analista: `docs-eng-process/openup-knowledge-base/core/role/roles/analyst-6.md`

## Ver También

- [openup-inception](../../openup-phases/inception/SKILL.md) - Guía de la fase de Inicio
- [openup-create-use-case](../create-use-case/SKILL.md) - Crear casos de uso detallados
- [openup-create-risk-list](../create-risk-list/SKILL.md) - Documentar riesgos del proyecto
