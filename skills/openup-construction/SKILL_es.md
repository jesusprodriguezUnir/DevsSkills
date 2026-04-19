---
name: openup-construction
description: Inicializar y gestionar las actividades de la fase de construcción: construir el sistema de forma incremental
arguments:
  - name: activity
    description: Specific activity to perform (initiate, check-status, next-steps)
    required: false
---

# Fase de Construcción

Esta habilidad lo guía a través de la fase de construcción de OpenUP: construir el sistema de manera incremental.

## Cuándo utilizar

Utilice esta habilidad cuando:
- Se completa la elaboración y se establece la línea base de la arquitectura.
- Listo para construir el sistema de forma iterativa.
- Implementación de funciones de forma incremental.
- Preparación para las pruebas beta.
- Comprobar si la fase de construcción está completa.
- Obtener orientación sobre los próximos pasos en la construcción.

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- La arquitectura aún no es estable (use `/openup-elaboration`)
- El sistema está listo para la implementación (use `/openup-transition`)
- Necesidad de crear artefactos específicos (usar habilidades de artefactos)
- Buscando planificación de iteración (use `/openup-create-iteration-plan`)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [ ] El estado de la fase se comprende claramente (iniciada, en curso o completa)
- [] Se realiza un seguimiento del progreso de la implementación.
- [ ] La cobertura de la prueba es adecuada
- [] Se identifican las tareas de la siguiente iteración.
- [ ] Se evalúa la preparación Beta

## Descripción general de la construcción

**Objetivo**: construir el sistema de forma iterativa hasta que esté listo para su implementación.
**Duración**: normalmente de 8 a 16 semanas (múltiples iteraciones)
**Hito clave**: Capacidad operativa

## Objetivos de la fase

1. Implementar todas las funciones restantes
2. Probar y perfeccionar el sistema de forma iterativa
3. Prepárese para las pruebas beta
4. Documentación de usuario completa
5. Alcanzar niveles de calidad aceptables

## Criterios de finalización

- [] El producto es lo suficientemente estable para realizar pruebas beta.
- [] Resultados de la prueba alfa documentados
- [] Problemas críticos resueltos
- [ ] La documentación del usuario es adecuada
- [] Acuerdo de las partes interesadas para implementar a los usuarios beta

## Proceso

### 1. Leer el estado del proyecto

Lea `docs/project-status.md` para:
- Confirmar que la fase es "construcción".
- Verificar los objetivos de iteración.
- Revisar elementos de trabajo activos.

### 2. Basado en la actividad

**`iniciar`**: Iniciar fase de construcción
- Actualice `docs/project-status.md` para configurar `fase: construcción`
- Revise `docs/architecture-notebook.md` para obtener orientación sobre la implementación.
- Actualización `docs/roadmap.md` con tareas de construcción
- Crear planes de iteración para las próximas iteraciones.

**`check-status`**: Revisar el progreso
- Verifique todos los criterios de finalización anteriores
- Enumerar lo que se hizo y lo que queda
- Identificar bloqueadores

**`próximos pasos`**: obtener recomendaciones
- Sugerir próximas tareas según el estado actual
- Priorizar por valor y dependencias.

## Productos de trabajo clave

- **Implementación** - Código fuente
- **Pruebas unitarias** - Pruebas escritas por desarrolladores
- **Diseño** (`docs/design/*.md`) - Documentos de diseño detallados
- **Casos de prueba** (`docs/test-cases/*.md`) - Documentación de prueba
- **Documentación de usuario** - Guías y manuales de usuario

## Equipo recomendado

Para el trabajo de la fase de Construcción, cree un equipo con:
- **desarrollador** - Implementación líder
- **tester** - Pruebas y validación continuas
- Agregue **arquitecto** para obtener orientación técnica.
- Agregue **analista** para aclarar los requisitos.

## Enfoque de iteración

Cada iteración de construcción debe:
1. Seleccione funciones de la hoja de ruta
2. Implementar con pruebas
3. Revisar y validar
4. Actualizar la documentación
5. Prepárese para la próxima iteración

## Referencias

- Fase de construcción: `docs-eng-process/openup-knowledge-base/practice-management/risk_value_lifecycle/guidances/concepts/phase-construction.md`
- Rol de desarrollador: `docs-eng-process/openup-knowledge-base/core/role/roles/developer-11.md`
- Rol del probador: `docs-eng-process/openup-knowledge-base/core/role/roles/tester-5.md`

## Ver también

- [openup-complete-task](../../openup-workflow/complete-task/SKILL.md) - Marcar tareas completadas
- [openup-create-test-plan](../../openup-artifacts/create-test-plan/SKILL.md) - Generar casos de prueba
- [openup-elaboration](../elaboration/SKILL.md) - Fase previa
- [openup-transition](../transition/SKILL.md) - Siguiente fase después de la construcción
