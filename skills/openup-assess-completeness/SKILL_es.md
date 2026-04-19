---
name: openup-assess-completeness
description: Evaluación de preparación ligera antes de completar la tarea o transición de fase
arguments:
  - name: scope
    description: Assessment scope (task, iteration, phase)
    required: false
  - name: strict
    description: "Fail on any missing items (true/false, default: false)"
    required: false
---

# Evaluar la integridad

Evaluación de preparación ligera para verificar que todo el trabajo requerido esté completo antes de marcar una tarea como realizada, completar una iteración o realizar fases de transición.

## Proceso

### 1. Determinar el alcance de la evaluación

Basado en `$ARGUMENTS[scope]` (por defecto "tarea"):

| Alcance | Enfoque | Cheques típicos |
|-------|-------|----------------|
| tarea | Finalización de una sola tarea | Código, pruebas, documentos, confirmación |
| iteración | Finalización de iteración | Todas las tareas, métricas y objetivos cumplidos |
| fase | Transición de fase | Criterios de fase, artefactos |

### 2. Realizar comprobaciones específicas del ámbito

**Alcance de la tarea:**
- No hay cambios no confirmados (o los cambios son intencionales): `git status --porcelain`
- Los archivos modificados coinciden con el alcance de la tarea.
- Existen pruebas para código nuevo y aprobación.
- La cobertura de la prueba es aceptable.
- El código es autodocumentado; documentos de diseño actualizados si corresponde
- La tarea existe en la hoja de ruta con un estado preciso.

**Alcance de la iteración** (todas las comprobaciones de tareas más):
- Todas las tareas de iteración completadas; sin tareas incompletas de alta prioridad
- Tareas bloqueadas documentadas.
- Se cumplieron los objetivos de iteración; comparación planificada versus real; velocidad capturada
- Estado del proyecto y hoja de ruta actualizados; lista de riesgos actualizada
- Pasan todas las pruebas; sin errores críticos; revisión del código completa

**Alcance de la fase** (todas las comprobaciones de iteración más):
- Criterios de salida de fase cumplidos:
  - Inicio: Visión, partes interesadas, lista de riesgos inicial
  - Elaboración: Línea base de arquitectura, 80% casos de uso detallados.
  - Construcción: Característica completa, cobertura de prueba adecuada
  - Transición: implementación lista, documentación de usuario completa
- Los artefactos de fase requeridos existen, se revisan y están controlados por versión.
- Se obtuvo la aceptación de las partes interesadas; próxima fase prevista; riesgos identificados

### 3. Generar informe de preparación

Genere un informe estructurado con: alcance, fecha, modo estricto, estado general de PASO/FALLO, verificaciones realizadas con resultados, elementos faltantes, recomendaciones y próximos pasos.

### 4. Manejar el modo estricto

Si `$ARGUMENTS[strict] == ​​"true"`: cualquier elemento faltante resulta en FAIL. De lo contrario: proporcione advertencias sobre elementos faltantes; puede pasar con recomendaciones.

## Producción

Devoluciones: alcance de la evaluación, estado general de aprobación/reprobación, verificaciones realizadas con resultados, elementos faltantes, recomendaciones, próximos pasos.

## Ver también

- [openup-complete-task](../complete-task/SKILL.md) - Completa la tarea después de aprobar la evaluación
- [openup-retrospective](../retrospective/SKILL.md) - Crear retrospectiva después de la iteración
- [openup-phase-review](../phase-review/SKILL.md) - Proceso de revisión de fase formal
