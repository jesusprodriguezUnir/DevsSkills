---
name: openup-create-iteration-plan
description: Planifica la iteración basándose en el estado actual y la hoja de ruta
arguments:
  - name: iteration_number
    description: Número de iteración a planificar
    required: false
---

# Crear Plan de Iteración

Esta skill genera un plan de iteración a partir de la plantilla OpenUP.

## Cuándo Usar

Usa esta skill cuando:
- Comiences una nueva iteración y necesites planificar el trabajo
- Estés en la fase de Construcción planificando iteraciones
- Necesites seleccionar tareas de la hoja de ruta para la iteración
- Asignes tareas a miembros del equipo
- Definas criterios de éxito de la iteración

## Cuándo NO Usar

NO uses esta skill cuando:
- Quieras iniciar la iteración (usa `/openup-start-iteration`)
- Necesites crear la hoja de ruta (usa la gestión de proyecto)
- El plan de iteración existe y solo necesita cambios menores (edítalo directamente)
- Estés en la fase de Inicio (usa las actividades de fase en su lugar)

## Criterios de Éxito

Tras usar esta skill, verifica:
- [ ] El archivo del plan de iteración existe
- [ ] El objetivo de la iteración está claramente definido
- [ ] Las tareas están seleccionadas de la hoja de ruta
- [ ] Las asignaciones de tareas están hechas
- [ ] Los criterios de éxito están especificados

## Proceso

### 1. Leer Estado del Proyecto

Leer `docs/project-status.md` para obtener:
- Fase actual
- Iteración actual
- Objetivos de la iteración

### 2. Leer Hoja de Ruta

Leer `docs/roadmap.md` para identificar:
- Tareas pendientes apropiadas para esta iteración
- Prioridades y dependencias de las tareas

### 3. Determinar Número de Iteración

Usar `$ARGUMENTS[iteration_number]` o auto-incrementar desde la iteración actual.

### 4. Copiar Plantilla

Copiar `docs-eng-process/templates/iteration-plan.md` a `docs/phases/<fase>/iteration-<n>-plan.md`

### 5. Completar el Plan de Iteración

Actualizar con:
- **Número de iteración** y fechas
- **Objetivo de la iteración**: Derivado de la hoja de ruta y los objetivos de fase
- **Tareas seleccionadas**: De la hoja de ruta, priorizadas para esta iteración
- **Asignaciones de tareas**: Qué roles se encargarán de cada tarea
- **Criterios de éxito**: Cómo saber si la iteración tuvo éxito
- **Evaluación de riesgos**: Riesgos específicos de la iteración

### 6. Validar Completitud

Asegurar que el plan de iteración incluya:
- Objetivo de iteración claro
- Lista de tareas a completar
- Asignaciones de tareas
- Criterios de éxito
- Cronograma de la iteración

## Salida

Devuelve:
- Ruta al plan de iteración
- Lista de tareas planificadas
- Composición de equipo recomendada

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Plantilla no encontrada | Ruta de plantilla incorrecta | Verificar que `docs-eng-process/templates/iteration-plan.md` existe |
| Sin tareas disponibles | La hoja de ruta está vacía o todas las tareas completadas | Revisar la hoja de ruta y añadir tareas pendientes |
| Número de iteración inválido | Conflictos o huecos en el número de iteración | Verificar la iteración actual desde el estado del proyecto |

## Referencias

- Plantilla de Plan de Iteración: `docs-eng-process/templates/iteration-plan.md`
- Rol de Jefe de Proyecto: `docs-eng-process/openup-knowledge-base/core/role/roles/project-manager-4.md`

## Ver También

- [openup-start-iteration](../../openup-workflow/start-iteration/SKILL.md) - Iniciar nueva iteración
- [openup-complete-task](../../openup-workflow/complete-task/SKILL.md) - Marcar tareas de iteración como completadas
- [openup-construction](../../openup-phases/construction/SKILL.md) - Planificación de iteraciones de Construcción
