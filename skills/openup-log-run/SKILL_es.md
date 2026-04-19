---
name: openup-log-run
description: Cree registros de trazabilidad (rebajas + JSONL) para la ejecución actual del agente
arguments:
  - name: run_id
    description: Unique identifier for this run (optional, auto-generates if not provided)
    required: false
---

# Ejecución de registro

Cree registros de trazabilidad para la ejecución actual del agente. **Llame solo DESPUÉS de que se hayan confirmado todos los cambios** (los registros requieren SHA de confirmación real).

## Requisitos previos

- `git status --porcelain` regresa vacío (todos los cambios confirmados)
- Los SHA de confirmación están disponibles como referencia

## Proceso

### 1. Generar ID de ejecución

Si no se proporciona `$ARGUMENTS[run_id]`, genere: `AAAA-MM-DDTHH:MM:SSZ-agent-branch`

### 2. Recopilar metadatos de ejecución

- Rama: `git rama --show-current`
- Tronco: detectar a través de `origin/HEAD`, respaldo `main`/`master`
- Marcas de tiempo de inicio/finalización
- Fase de `docs/project-status.md`
- Confirma: `git log --oneline <since>...HEAD`

### 3. Crear registro de rebajas

Cree `docs/agent-logs/YYYY/MM/DD/<timestamp>-<agent>-<branch>.md` con:
- Ejecutar metadatos (rama, troncal, marcas de tiempo)
- Roles asumidos y cambios.
- Tareas realizadas (una por límite de tarea de rol principal)
- Confirmar SHA creados durante la ejecución
- Uso del rol de consultoría
- Decisiones/supuestos clave + enlaces a documentos
- Instrucciones/indicaciones iniciales (textualmente)

### 4. Agregar entrada JSONL

Agregue a `docs/agent-logs/agent-runs.jsonl`:

```json
{"run_id":"<id>","agent":"claude","branch":"<branch>","trunk":"<trunk>","start":"<ts>","end":"<ts>","phase":"<phase>","iteration_goals":["..."],"prompt_hash":"sha256:...","md_log_path":"<path>","tasks":[{"role":"<role>","objective":"<obj>","start":"<ts>","end":"<ts>","commits":["<sha>"],"docs_updated":["<path>"],"consulting_roles":["<role>"]}],"decisions":["<path>"],"notes":"<summary>"}
```

### 5. Verificar

- El registro de rebajas existe y es legible.
- La entrada JSONL es JSON válida.
- Confirmar que los SHA a los que se hace referencia realmente existen
- Todos los campos obligatorios están completos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Cambios no confirmados | Archivos no confirmados | `git add -A && git commit` primero |
| JSONL no válido | Error de formato JSON | Verifique la sintaxis antes de agregar |
| Confirmaciones faltantes | No hay confirmaciones para ejecutar | Verificar que la ejecución esté completa |
| Directorio no encontrado | docs/agent-logs/faltan | Primero cree la estructura del directorio |

## Referencias

- SOP de registro de trazabilidad: `docs-eng-process/agent-workflow.md`

## Ver también

- [openup-complete-task](../complete-task/SKILL.md) - Llama esta habilidad automáticamente
- [openup-start-iteration](../start-iteration/SKILL.md) - Registra el inicio de la iteración
