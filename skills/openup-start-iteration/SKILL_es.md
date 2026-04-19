---
name: openup-start-iteration
description: Comience una nueva iteración de OpenUP con el contexto de fase y la selección de tareas adecuados
arguments:
  - name: iteration_number
    description: The iteration number (optional, auto-increments if not provided)
    required: false
  - name: goal
    description: The iteration goal (optional, reads from project-status if not provided)
    required: false
  - name: task_id
    description: The task ID from roadmap to work on (required for task-based branching)
    required: true
  - name: team
    description: Team type to automatically deploy after initialization (feature, investigation, construction, elaboration, inception, transition, planning, full, or none)
    required: false
  - name: deploy_team
    description: "Whether to deploy a team after iteration initialization (true/false, default: false)"
    required: false
---

# Iniciar iteración

Inicialice una nueva iteración de OpenUP: lea el estado del proyecto, cree una rama de tareas y comience a trabajar.

## Criterios de éxito

Una vez completada esta habilidad, TODO lo siguiente debe ser cierto:

- [] El estado del proyecto se actualiza con una nueva iteración.
- [] **COMPROBACIÓN DE BLOQUEO**: `git rev-parse --abbrev-ref HEAD` devuelve un nombre de rama que no es troncal (no `main`, `master` o cualquier tronco que sea). Si devuelve troncal, la habilidad FALLÓ; no continúe.
- [] El objetivo de iteración está definido.
- [ ] Las solicitudes de entrada respondidas se procesan
- [] Se crea la entrada de registro

## Proceso

### 1. Leer el estado del proyecto

Lea `docs/project-status.md` para establecer el contexto:
- Fase actual (inicio | elaboración | construcción | transición)
- Número de iteración actual
- Estado de iteración anterior

### 2. Leer la hoja de ruta e identificar la tarea

Lea `docs/roadmap.md` para:
- Encuentra la tarea especificada por `$ARGUMENTS[task_id]`
- Extraer detalles de la tarea: título, descripción, tipo de tarea (característica, corrección de errores, refactorización, etc.)
- Determinar prioridad y dependencias.
- **Si no se encuentra task_id**: solicite al usuario que especifique qué tarea de la hoja de ruta

### 3. Crear rama de tareas

**Ejecute estos comandos en orden:**

```bash
# 1. Detect trunk
TRUNK=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
[ -z "$TRUNK" ] && TRUNK="main"
git rev-parse --verify "$TRUNK" 2>/dev/null || TRUNK="master"

# 2. Cambie al maletero y obtenga la última versión
git pago "$TRUNK"
git pull origen "$TRUNK" 2>/dev/null || verdadero

# 3. Crear rama (consulte branching.md para conocer los patrones de nombres)
git checkout -b {tipo}/{task_id}-{breve descripción}

# 4. VERIFICAR: esto NO debe devolver el troncal
git rev-parse --abrev-ref CABEZA
```

**Si la sucursal ya existe**, consulta su estado:
- No hay confirmaciones no fusionadas → eliminar y volver a crear desde el tronco
- Tiene confirmaciones no fusionadas → cree PR o fusione primero, luego cree una nueva rama

### 4. Verifique las solicitudes de entrada respondidas

Verifique `docs/input-requests/` para ver si hay archivos con `estado: respondido`. Procese cualquier solicitud respondida antes de continuar.

### 5. Inicializar iteración

Actualice `docs/project-status.md`:
- Incrementar la `iteración` o usar `$ARGUMENTS[iteration_number]` proporcionado
- Establezca `iteration_goal` en `$ARGUMENTS[goal]` proporcionado o derive de la tarea de hoja de ruta
- Establecer "estado" en "en curso"
- Establecer `current_task` al task_id
- Actualizar `iteration_started` a la fecha de hoy

### 6. Inicialización del registro

Cree una entrada en `docs/agent-logs/agent-runs.jsonl` que documente el inicio de la iteración con el contexto de la tarea.

### 7. Implementar equipo (opcional)

Si `$ARGUMENTS[deploy_team]` es `true` o se especifica `$ARGUMENTS[team]`:

1. Determine la composición del equipo según `$ARGUMENTS[team]` o la fase actual:
   - **característica**: analista, arquitecto, desarrollador, probador
   - **investigación**: arquitecto, desarrollador, probador
   - **construcción**: desarrollador, probador
   - **elaboración**: arquitecto, desarrollador, tester
   - **inicio**: analista, director de proyectos
   - **transición**: tester, director de proyecto, desarrollador
   - **planificación**: director de proyecto, analista
   - **completo**: todos los roles

2. Implemente el equipo utilizando la herramienta Tarea, informe a cada compañero de equipo sobre el contexto de la iteración.

## Producción

Devuelve un resumen de:
- Fase actual y número de iteración.
- Tarea en la que se está trabajando (task_id, título)
- Objetivo de iteración
- Nombre de la rama activa (debe ser una rama de tarea no troncal)

## Ver también

- [openup-complete-task](../complete-task/SKILL.md) - Completar tareas de iteración
- [openup-create-iteration-plan](../../openup-artifacts/create-iteration-plan/SKILL.md) - Planificar la iteración antes de comenzar
