---
name: openup-elaboration
description: Inicializar y gestionar las actividades de la fase de elaboración: establecer una línea base de arquitectura
arguments:
  - name: activity
    description: Specific activity to perform (initiate, check-status, next-steps)
    required: false
---

# Fase de Elaboración

Esta habilidad lo guía a través de la fase de elaboración de OpenUP: establecer la línea base de la arquitectura.

## Cuándo utilizar

Utilice esta habilidad cuando:
- El inicio está completo y es necesario establecer una base de arquitectura
- Necesidad de diseñar y validar la arquitectura del sistema.
- Resolver elementos técnicos de alto riesgo.
- Implementación de prototipos arquitectónicos.
- Comprobar si la fase de elaboración está completa.
- Obtener orientación sobre los próximos pasos en la elaboración.

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- Aún definiendo la visión y el alcance del proyecto (use `/openup-inception`)
- La arquitectura es estable y está lista para una construcción incremental (pasar a Construcción)
- Necesidad de crear artefactos específicos (usar habilidades de artefactos)
- Buscando planificación de iteración (use `/openup-create-iteration-plan`)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [ ] El estado de la fase se comprende claramente (iniciada, en curso o completa)
- [] Se crea o actualiza el cuaderno de arquitectura.
- [ ] Los riesgos técnicos son identificados y mitigados
- [] Se detallan los casos de uso críticos.
- [ ] Los próximos pasos están claramente definidos

## Descripción general de la elaboración

**Objetivo**: Diseñar e implementar la arquitectura, resolver elementos de alto riesgo.
**Duración**: normalmente de 4 a 8 semanas
**Hito clave**: Arquitectura del ciclo de vida

## Objetivos de la fase

1. Diseñar y validar la arquitectura.
2. Detallar los casos de uso críticos
3. Implementar y probar la línea base arquitectónica.
4. Refinar el plan del proyecto con estimaciones precisas.
5. Mitigar los riesgos de alta prioridad

## Criterios de finalización

- [] Cuaderno de arquitectura completado
- [ ] Casos de uso críticos detallados (80%)
- [ ] Riesgos técnicos identificados y mitigados
- [ ] Prototipo(s) decisiones arquitectónicas clave validadas
- [ ] Plan de proyecto refinado con estimaciones precisas
- [ ] Acuerdo de partes interesadas sobre arquitectura

## Proceso

### 1. Leer el estado del proyecto

Lea `docs/project-status.md` para:
- Confirmar que la fase es `elaboración`
- Verificar los objetivos de iteración.
- Revisar elementos de trabajo activos.

### 2. Basado en la actividad

**`iniciar`**: Iniciar fase de elaboración
- Actualizar `docs/project-status.md` para configurar `fase: elaboración`
- Crear `docs/architecture-notebook.md` a partir de la plantilla
- Revisar y perfeccionar `docs/risk-list.md` para riesgos técnicos
- Actualización `docs/roadmap.md` con tareas de elaboración

**`check-status`**: Revisar el progreso
- Verifique todos los criterios de finalización anteriores
- Enumerar lo que se hizo y lo que queda
- Identificar bloqueadores

**`próximos pasos`**: obtener recomendaciones
- Sugerir próximas tareas según el estado actual
- Priorizar por riesgo técnico y dependencias.

## Productos de trabajo clave

- **Cuaderno de Arquitectura** (`docs/architecture-notebook.md`) - Documentación de arquitectura
- **Diseño** (`docs/design/*.md`) - Documentos de diseño detallados
- **Casos de uso** (`docs/use-cases/*.md`) - Casos de uso detallados
- **Pruebas de desarrollador** - Implementaciones de prueba
- **Plan de proyecto actualizado** (`docs/project-plan.md`)

## Equipo recomendado

Para el trabajo de la fase de Elaboración, cree un equipo con:
- **arquitecto** - Diseño arquitectónico líder
- **desarrollador** - Implementar línea base arquitectónica
- **tester** - Validar la arquitectura mediante pruebas
- Agregue **analista** para requisitos detallados

## Referencias

- Fase de elaboración: `docs-eng-process/openup-knowledge-base/practice-management/risk_value_lifecycle/guidances/concepts/phase-elaboration.md`
- Rol de arquitecto: `docs-eng-process/openup-knowledge-base/core/role/roles/architect-6.md`
- Plantilla de cuaderno de arquitectura: `docs-eng-process/templates/architecture-notebook.md`

## Ver también

- [openup-create-architecture-notebook](../../openup-artifacts/create-architecture-notebook/SKILL.md) - Generar documentación de arquitectura
- [openup-shared-vision](../../openup-artifacts/shared-vision/SKILL.md) - Crear una visión técnica compartida
- [openup-create-use-case](../../openup-artifacts/create-use-case/SKILL.md) - Crear casos de uso detallados
- [openup-detail-use-case](../../openup-artifacts/detail-use-case/SKILL.md) - Detallar casos de uso con escenarios
- [openup-inception](../inception/SKILL.md) - Fase anterior
- [openup-construction](../construction/SKILL.md) - Siguiente fase después de la Elaboración
