---
name: openup-transition
description: Inicializar y gestionar actividades de la fase de transición: implementar para los usuarios
arguments:
  - name: activity
    description: Specific activity to perform (initiate, check-status, next-steps)
    required: false
---

# Fase de transición

Esta habilidad lo guía a través de la fase de transición de OpenUP: implementación para los usuarios.

## Cuándo utilizar

Utilice esta habilidad cuando:
- La construcción está completa y el sistema está listo para su implementación.
- Preparación para el lanzamiento beta o de producción.
- Realización de pruebas finales y aceptación del usuario.
- Formación de usuarios y personal de soporte.
- Comprobar si la fase de transición está completa
- Obtener orientación sobre los próximos pasos en la transición

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- Todavía implementando funciones (use `/openup-construction`)
- El sistema no es lo suficientemente estable para realizar pruebas (continuar construcción)
- Necesidad de crear artefactos específicos (usar habilidades de artefactos)
- Buscando procedimientos de implementación (use la documentación de DevOps/ops)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [ ] El estado de la fase se comprende claramente (iniciada, en curso o completa)
- [ ] Se evalúa la preparación para la implementación
- [ ] Se preparan materiales de apoyo.
- [ ] La aceptación del usuario está documentada.
- [] La decisión de liberación es clara.

## Descripción general de la transición

**Objetivo**: Implementar el sistema para los usuarios y garantizar su satisfacción.
**Duración**: normalmente de 2 a 4 semanas
**Hito clave**: Lanzamiento del producto

## Objetivos de la fase

1. Implementar el sistema para los usuarios.
2. Capacitar a los usuarios y al personal de soporte.
3. Reparar los defectos encontrados durante las pruebas.
4. Documentación de usuario completa
5. Obtener la aceptación del usuario

## Criterios de finalización

- [ ] El producto está listo para su lanzamiento.
- [] Todas las pruebas de aceptación pasan
- [] Documentación de implementación completa
- [ ] Materiales de apoyo listos
- [ ] Se obtuvo la aprobación de las partes interesadas

## Proceso

### 1. Leer el estado del proyecto

Lea `docs/project-status.md` para:
- Confirmar que la fase es "transición"
- Verificar los objetivos de iteración.
- Revisar elementos de trabajo activos.

### 2. Basado en la actividad

**`iniciar`**: Iniciar fase de transición
- Actualice `docs/project-status.md` para configurar `fase: transición`
- Revisar los resultados de las pruebas de construcción.
- Crear lista de verificación de implementación
- Actualizar `docs/roadmap.md` con tareas de transición

**`check-status`**: Revisar el progreso
- Verifique todos los criterios de finalización anteriores
- Enumerar lo que se hizo y lo que queda
- Identificar bloqueadores

**`próximos pasos`**: obtener recomendaciones
- Sugerir próximas tareas según el estado actual
- Priorizar según la preparación para la implementación

## Productos de trabajo clave

- **Documentación de implementación** - Guías de instalación y configuración
- **Documentación de usuario** - Manuales de usuario finales
- **Materiales de soporte** - Guías de solución de problemas, preguntas frecuentes
- **Resultados de las pruebas** - Informes finales de las pruebas
- **Notas de la versión** - Novedades y cambios

## Equipo recomendado

Para el trabajo de la fase de transición, cree un equipo con:
- **tester** - Liderar las pruebas y validación finales
- **desarrollador** - Solucionar problemas de implementación
- **gerente de proyecto** - Coordinar la implementación
- Agregue **analista** para recibir comentarios y aceptación de los usuarios.

## Actividades de implementación

1. **Pruebas finales** - Pruebas completas que incluyen:
   - Pruebas beta con usuarios reales.
   - Pruebas de rendimiento
   - Pruebas de seguridad
   - Pruebas de aceptación del usuario.

2. **Preparación para la implementación** - Prepárese para el lanzamiento:
   - Crear scripts de implementación
   - Preparar el entorno de producción.
   - Planear procedimientos de reversión
   - Capacitar al personal de apoyo.

3. **Preparación del usuario** - Preparar a los usuarios:
   - Crear documentación de usuario.
   - Desarrollar materiales de capacitación.
   - Realizar sesiones de formación.
   - Preparar materiales de comunicación.

4. **Lanzamiento** - Implementación en producción:
   - Ejecutar plan de implementación.
   - Monitorear problemas
   - Proporcionar apoyo
   - Recopilar comentarios

## Referencias

- Fase de transición: `docs-eng-process/openup-knowledge-base/practice-management/risk_value_lifecycle/guidances/concepts/phase-transition.md`
- Rol del probador: `docs-eng-process/openup-knowledge-base/core/role/roles/tester-5.md`
- Rol del Gerente de Proyecto: `docs-eng-process/openup-knowledge-base/core/role/roles/project-manager-4.md`

## Ver también

- [openup-phase-review](../../openup-workflow/phase-review/SKILL.md) - Verificar la finalización de la fase
- [openup-create-test-plan](../../openup-artifacts/create-test-plan/SKILL.md) - Planificación final de la prueba
- [openup-construction](../construction/SKILL.md) - Fase anterior
- [openup-log-run](../../openup-workflow/log-run/SKILL.md) - Implementación de documentos
