---
name: openup-retrospective
description: Genere una retrospectiva de iteraciones con comentarios y elementos de acción.
arguments:
  - name: iteration_number
    description: Iteration to review (optional, defaults to current)
    required: false
  - name: include_metrics
    description: "Include git metrics (true/false, default: true)"
    required: false
---

# Retrospectiva

Genere una retrospectiva de iteraciones que capture lo que salió bien, qué mejorar y los elementos de acción.

## Proceso

### 1. Determinar la iteración

Si se proporciona `$ARGUMENTS[iteration_number]`, úselo. De lo contrario, lea `docs/project-status.md` para conocer el número de iteración actual.

### 2. Leer el contexto del proyecto

Lea `docs/project-status.md` para conocer: objetivo de la iteración, fechas, miembros del equipo y estado general.

### 3. Analizar tareas completadas

Lea `docs/roadmap.md` para identificar: tareas planificadas, completadas, no completadas y agregadas durante la iteración. Tenga en cuenta la complejidad, los desafíos y los éxitos de cada uno.

### 4. Recopile comentarios

Revise estas fuentes para detectar patrones y problemas:
- `docs/agent-logs/` - Registros de ejecución del agente
- `docs/risk-list.md` - Riesgos surgidos o mitigados
- `docs/roadmap.md` - Velocidad (completada vs planificada), elementos bloqueados
- Mensajes de confirmación de Git

### 5. Recopilar métricas (si `$ARGUMENTS[include_metrics] == "true"`)

```bash
# Commits in iteration period
git log --oneline --since="$start_date" --until="$end_date" | wc -l

# Líneas cambiadas
git diff --stat tronco...CABEZA

# Colaboradores activos
git shortlog -sn --since="$fecha_inicio" --until="$fecha_final"
```

Métricas de tareas: tareas planificadas, tareas completadas, tasa de finalización (completada/planificada * 100%).

### 6. Crear documento retrospectivo

Cree `docs/iteration-retrospectives/iteration-{n}-retrospective.md` con secciones:
- **Resumen de la iteración**: número, intervalo de fechas, objetivo, participantes
- **Resumen**: evaluación general, logros clave, principales desafíos
- **Lo que salió bien**: éxitos de proceso, técnicos y de colaboración
- **Qué mejorar**: problemas de proceso, desafíos técnicos, brechas
- **Elementos de acción**: acción específica, propietario, fecha de vencimiento, prioridad para cada mejora
- **Métricas** (si se incluyen): estadísticas de finalización de tareas, estadísticas de git
- **Consideraciones para la próxima iteración**: transferencia, cambios, riesgos a monitorear

### 7. Actualizar el estado del proyecto

En `docs/project-status.md`: agregue un enlace a la retrospectiva, observe los elementos de acción en curso, actualice el estado de la iteración.

## Producción

Devoluciones: ruta del documento retrospectivo, recuentos de lo que salió bien/qué mejorar/elementos de acción, calificación general de la iteración, métricas clave (si se incluyen).

## Ver también

- [openup-start-iteration](../start-iteration/SKILL.md) - Iniciar la siguiente iteración
- [openup-complete-task](../complete-task/SKILL.md) - Completar tareas de iteración
- [openup-assess-completeness](../assess-completeness/SKILL.md) - Evaluar la integridad de la iteración antes de la retrospectiva
- [openup-create-iteration-plan](../openup-artifacts/create-iteration-plan/SKILL.md) - Planifica la próxima iteración en función de la retrospectiva
