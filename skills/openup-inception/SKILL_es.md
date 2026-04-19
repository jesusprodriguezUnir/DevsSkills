---
name: openup-inception
description: Inicializar y gestionar las actividades de la fase inicial: definir el alcance, la visión y la viabilidad.
arguments:
  - name: activity
    description: Specific activity to perform (initiate, check-status, next-steps)
    required: false
---

# Fase de inicio

Esta habilidad lo guía a través de la fase inicial de OpenUP: define el alcance, la visión y la viabilidad.

## Cuándo utilizar

Utilice esta habilidad cuando:
- Inicio de un nuevo proyecto y necesidad de definir alcance y visión.
- Necesidad de identificar las partes interesadas clave y los riesgos.
- Preparación para pasar de la idea al caso de negocio validado.
- Comprobar si la fase de inicio está completa
- Obtener orientación sobre los próximos pasos en Inception

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- Actualmente en fase de Elaboración, Construcción o Transición (use la habilidad de fase adecuada)
- Necesidad de crear artefactos específicos como documentos de visión o casos de uso (usar habilidades de artefactos)
- Ya tengo una visión clara y una base de arquitectura (pasar a Elaboración)
- Buscando planificación de iteración (use `/openup-create-iteration-plan`)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [ ] El estado de la fase se comprende claramente (iniciada, en curso o completa)
- [ ] Se identifican o crean artefactos clave (visión, lista de riesgos, hoja de ruta)
- [ ] Los próximos pasos están claramente definidos
- [ ] Las partes interesadas y los riesgos están documentados.

## Descripción general del inicio

**Objetivo**: comprender qué construir e identificar los riesgos clave
**Duración**: normalmente de 2 a 4 semanas
**Hito clave**: Objetivos del ciclo de vida

## Objetivos de la fase

1. Definir la visión del proyecto.
2. Comprender el problema a resolver
3. Identificar las partes interesadas clave
4. Definir el alcance inicial
5. Identificar los principales riesgos
6. Demostrar viabilidad con un caso de negocio

## Criterios de finalización

- [ ] Documento de visión aprobado por las partes interesadas
- [ ] Casos de uso clave identificados (20-30% detallados)
- [ ] Riesgos importantes documentados con estrategias de mitigación
- [ ] Plan inicial del proyecto con estimaciones de costos/cronograma
- [ ] Caso de negocio demuestra viabilidad
- [ ] Acuerdo de las partes interesadas para proceder

## Proceso

### 1. Leer el estado del proyecto

Lea `docs/project-status.md` para:
- Confirmar que la fase es "inicio".
- Verificar los objetivos de iteración.
- Revisar elementos de trabajo activos.

### 2. Basado en la actividad

**`iniciar`**: Iniciar la fase inicial
- Actualice `docs/project-status.md` para configurar `fase: inicio`
- Crear `docs/vision.md` inicial a partir de la plantilla
- Crear `docs/risk-list.md` inicial a partir de la plantilla
- Crear `docs/roadmap.md` con el trabajo pendiente inicial

**`check-status`**: Revisar el progreso
- Verifique todos los criterios de finalización anteriores
- Enumerar lo que se hizo y lo que queda
- Identificar bloqueadores

**`próximos pasos`**: obtener recomendaciones
- Sugerir próximas tareas según el estado actual
- Priorizar por dependencias y valor.

## Productos de trabajo clave

- **Visión** (`docs/vision.md`) - Visión y alcance del proyecto
- **Casos de uso** (`docs/use-cases/*.md`) - Casos de uso clave
- **Lista de riesgos** (`docs/risk-list.md`) - Riesgos identificados
- **Plan de proyecto** (`docs/project-plan.md`) - Plan inicial
- **Glosario** (`docs/glossary.md`) - Terminología del proyecto

## Equipo recomendado

Para el trabajo de la fase inicial, cree un equipo con:
- **analista** - Requisitos y visión del líder
- **director-de-proyecto** - Planificar y coordinar
- Agregar **arquitecto** para evaluación de viabilidad técnica

## Referencias

- Fase inicial: `docs-eng-process/openup-knowledge-base/practice-management/risk_value_lifecycle/guidances/concepts/phase-inception.md`
- Rol de analista: `docs-eng-process/openup-knowledge-base/core/role/roles/analyst-6.md`
- Plantilla de visión: `docs-eng-process/templates/vision.md`

## Ver también

- [openup-create-vision](../../openup-artifacts/create-vision/SKILL.md) - Generar documento de visión
- [openup-shared-vision](../../openup-artifacts/shared-vision/SKILL.md) - Crear una visión técnica compartida
- [openup-create-risk-list](../../openup-artifacts/create-risk-list/SKILL.md) - Crear evaluación de riesgos
- [openup-elaboration](../elaboration/SKILL.md) - Siguiente fase después del inicio
- [openup-start-iteration](../../openup-workflow/start-iteration/SKILL.md) - Comenzar la planificación de la iteración
