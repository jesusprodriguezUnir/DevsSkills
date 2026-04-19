---
name: openup-request-input
description: Crear un documento de solicitud de entrada para la comunicación asincrónica con las partes interesadas
arguments:
  - name: title
    description: Descriptive title for the request
    required: true
  - name: questions
    description: JSON array of questions (type, question_text, options for multiple-choice)
    required: true
  - name: context
    description: Additional context about what the agent is doing
    required: true
  - name: related_task
    description: Optional roadmap task ID (e.g., T-001)
    required: false
---

# Solicitar entrada

Cree un documento de solicitud de entrada para la comunicación asincrónica con las partes interesadas.

## Proceso

### 1. Generar nombre de archivo

Formato: `docs/input-requests/AAAA-MM-DD-<short-topic>.md` (tema derivado de `$ARGUMENTS[title]`).

### 2. Rellenar el frontmatter

```yaml
---
title: "$ARGUMENTS[title]"
created: "<current-timestamp-ISO8601>"
created_by: "agent-name"
status: pending
run_id: "<current-run-id>"
related_task: "$ARGUMENTS[related_task]"  # optional
---
```

### 3. Escribir sección de contexto

Utilice `$ARGUMENTS[context]` para explicar la tarea/fase actual, qué información se necesita y por qué.

### 4. Agregar preguntas

Para cada pregunta en `$ARGUMENTS[questions]`, utilice el formato apropiado:

**elección múltiple**: `### Q[N]: [Título]` con `**Tipo**: opción múltiple`, opciones de casilla de verificación (`- [ ] \`opción\` - Descripción`) y `**Respuesta**:` marcador de posición.

**text**: `### Q[N]: [Título]` con `**Tipo**: texto`, `**Ejemplo**:` opcional y marcador de posición `**Respuesta**:`.

**referencia**: `### Q[N]: [Título]` con `**Tipo**: referencia`, `**Acepta**: Ruta o URL` y `**Respuesta**:` marcador de posición.

### 5. Incluir instrucciones

Agregue instrucciones para el encuestado:
1. Complete la sección de Respuestas para cada pregunta.
2. Actualizar el estado de "pendiente" a "respondido"
3. Guarde el archivo
4. Dígale al agente que continúe

### 6. Notificar al usuario

Informar al usuario de la ubicación del documento y cómo proceder.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Formato de preguntas no válido | Matriz JSON mal formada | Verificar matriz JSON válida |
| Falta contexto | Contexto no proporcionado | Proporcionar argumento de contexto |
| Directorio no encontrado | documentos/solicitudes de entrada/faltantes | Crear directorio primero |

## Referencias

- SOP de entrada asincrónica: `docs-eng-process/agent-workflow.md`
- Plantilla de solicitud de entrada: `docs-eng-process/templates/input-request.md`

## Ver también

- [openup-start-iteration](../start-iteration/SKILL.md) - Procesar solicitudes respondidas al iniciar la iteración
- [openup-complete-task](../complete-task/SKILL.md) - Verifique las respuestas antes de completar
