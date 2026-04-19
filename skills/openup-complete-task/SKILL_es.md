---
name: openup-complete-task
description: Marcar una tarea como completa, actualizar la hoja de ruta, confirmar cambios y preparar registros de trazabilidad
arguments:
  - name: task_id
    description: The task ID to mark as complete (e.g., T-001)
    required: true
  - name: commit_message
    description: Custom commit message (optional, auto-generates if not provided)
    required: false
  - name: create_pr
    description: "Create a pull request after completing the task (default: true — set to 'false' to skip)"
    required: false
---

# Completar tarea

Finalice una tarea completada: confirme los cambios restantes, actualice documentos, cree registros de trazabilidad y cree un PR.

## Criterios de éxito

Una vez completada esta habilidad, TODO lo siguiente debe ser cierto:

- [] Todos los cambios están confirmados (no quedan cambios no confirmados)
- [] Los mensajes de confirmación siguen el formato canónico: `tipo(alcance): descripción [T-XXX]`
- [] La hoja de ruta se actualiza para marcar la tarea como completada
- [] Se actualiza el estado del proyecto.
- [] Los registros de trazabilidad se crean con SHA de confirmación
- [ ] Se crea PR (a menos que `create_pr` fuera explícitamente `"falso"`)

## Pasos detallados

### 1. Verificar la finalización de la tarea

Antes de marcar una tarea como completa, verifique:
- Todo el trabajo de implementación está realizado.
- Todas las pruebas pasan
- La documentación está actualizada.

### 2. Confirmar los cambios restantes

La mayoría de los cambios ya deberían confirmarse como confirmaciones atómicas durante la implementación (consulte `commit-procedure.md`). Este paso maneja cualquier trabajo sobrante no comprometido.

1. Ejecute `git status --porcelain` para verificar cambios no confirmados
2. Si existen cambios:
   - Preparar archivos relevantes: `git add <files>`
   - Confirmar usando formato canónico: `tipo(alcance): descripción [$ARGUMENTS[task_id]]`
   - Utilice `$ARGUMENTS[commit_message]` si se proporciona
3. Verifique: `git status --porcelain` regresa vacío

### 3. Actualizar la hoja de ruta

Actualizar `docs/roadmap.md`:
- Marcar la tarea `$ARGUMENTS[task_id]` como `completada`
- Agregar fecha de finalización

### 4. Actualizar el estado del proyecto

Actualice `docs/project-status.md`:
- Actualizar la tabla "Elementos de trabajo activos"
- Actualizar los campos `last_updated` y `updated_by`

### 5. Crear registros de trazabilidad

Cree registros de rebajas y JSONL:
- Registro de rebajas: `docs/agent-logs/AAAA/MM/DD/<marca de tiempo>-<agente>-<rama>.md`
- Entrada JSONL: agregar a `docs/agent-logs/agent-runs.jsonl`
- Incluir SHA de confirmación en los registros

### 6. Crear solicitud de extracción

**PR se crea de forma predeterminada.** Omita SÓLO si `$ARGUMENTS[create_pr]` es explícitamente `"falso"`.

1. Empuja la rama:
   ```golpecito
   git push -u origen $(git rev-parse --abbrev-ref HEAD)
   ```

2. Verifique que existan confirmaciones no fusionadas:
   ```golpecito
   git log <trunk>..HEAD --oneline
   ```

3. Invocar la habilidad `/openup-create-pr` con `task_id: $ARGUMENTS[task_id]`

4. Informar el resultado al usuario:
   - Éxito → proporcionar URL de relaciones públicas
   - No hay confirmaciones no fusionadas → informar al usuario que no se necesita PR
   - Fallo → explicar el error y proporcionar pasos manuales

## Producción

Devuelve un resumen de:
- Tarea completada
- Confirmar SHA
- Archivos cambiados
- Ubicaciones de registro
- URL de relaciones públicas

## Ver también

- [openup-create-pr](../create-pr/SKILL.md) - Crear solicitud de extracción por separado
- [openup-log-run](../log-run/SKILL.md) - Detalles del registro de trazabilidad
- [openup-start-iteration](../start-iteration/SKILL.md) - Comienza la siguiente iteración
