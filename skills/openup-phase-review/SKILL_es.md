---
name: openup-phase-review
description: Verifique los criterios de finalización de la fase y prepárese para la revisión de la fase
arguments:
  - name: phase
    description: The phase to review (inception, elaboration, construction, transition)
    required: false
---

# Revisión de fase

Esta habilidad verifica los criterios de finalización de la fase y prepara la documentación para una reunión de revisión de la fase.

## Cuándo utilizar

Utilice esta habilidad cuando:
- Se acerca el final de una fase y es necesario comprobar su finalización.
- Preparación de la reunión de revisión de fase con las partes interesadas.
- Evaluar la preparación para pasar a la siguiente fase.
- Generación de documentación resumen de fase.
- Necesidad de demostrar los logros de la fase.

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- Recién comenzando una fase (usa la habilidad de fase en su lugar)
- Necesidad de completar tareas de iteración (use `/openup-complete-task`)
- Buscando planificación de iteración (use `/openup-create-iteration-plan`)
- La fase claramente no está completa (continuar trabajando primero)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [ ] Se verifican todos los criterios de finalización de fase.
- [ ] Los elementos faltantes están claramente identificados
- [ ] Se genera el resumen de revisión de fase
- [] Se proporcionan recomendaciones para la siguiente fase.
- [] El usuario sabe qué decisiones son necesarias

## Proceso

### 1. Leer el estado actual del proyecto

Lea `docs/project-status.md` para determinar:
- Fase actual (o use `$ARGUMENTS[phase]` si se proporciona)
- Estado de iteración
- Lista de verificación de criterios de finalización de fase

### 2. Verificar los criterios de finalización de la fase

Para la fase actual, verifique que se cumplan todos los criterios de finalización:

**Inicio: Hito de los objetivos del ciclo de vida**:
- [ ] Documento de visión aprobado por las partes interesadas
- [ ] Casos de uso clave identificados (20-30% detallados)
- [ ] Riesgos importantes documentados con estrategias de mitigación
- [ ] Plan inicial del proyecto con estimaciones de costos/cronograma
- [ ] Caso de negocio demuestra viabilidad
- [ ] Acuerdo de las partes interesadas para proceder

**Elaboración - Hito de la Arquitectura del Ciclo de Vida**:
- [] Cuaderno de arquitectura completado
- [ ] Casos de uso críticos detallados (80%)
- [ ] Riesgos técnicos identificados y mitigados
- [ ] Prototipo(s) decisiones arquitectónicas clave validadas
- [ ] Plan de proyecto refinado con estimaciones precisas
- [ ] Acuerdo de partes interesadas sobre arquitectura

**Construcción - Hito de capacidad operativa**:
- [] El producto es lo suficientemente estable para realizar pruebas beta.
- [] Resultados de la prueba alfa documentados
- [] Problemas críticos resueltos
- [ ] La documentación del usuario es adecuada
- [] Acuerdo de las partes interesadas para implementar a los usuarios beta

**Transición: hito del lanzamiento del producto**:
- [ ] El producto está listo para su lanzamiento.
- [] Todas las pruebas de aceptación pasan
- [] Documentación de implementación completa
- [ ] Materiales de apoyo listos
- [ ] Se obtuvo la aprobación de las partes interesadas

### 3. Generar resumen de revisión de fase

Cree un resumen de revisión de fase que incluya:
- Logros de fase
- Productos de trabajo completados.
- Riesgos y problemas
- Lecciones aprendidas
- Recomendaciones para la siguiente fase.

### 4. Crear presentación de revisión

Genere un esquema de presentación de revisión:
- Resumen ejecutivo
- Objetivos de fase vs. resultados
- Demostraciones (si corresponde)
- Cuestiones abiertas y decisiones necesarias.

### 5. Notificar al usuario

Informar al usuario que:
- Los materiales de revisión de la fase están listos.
- Cualquier criterio de finalización que aún no se haya cumplido.
- Decisiones necesarias de las partes interesadas

## Producción

Devoluciones:
- Estado de la lista de verificación de criterios de finalización de fase
- Lista de productos de trabajo completados.
- Resumen de revisión
- Recomendaciones

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Estado del proyecto no encontrado | docs/project-status.md no existe | Inicialice el proyecto con la habilidad de fase primero |
| Fase no reconocida | Nombre de fase no válido proporcionado | Uso fase válida: inicio, elaboración, construcción, transición |
| Criterios no cumplidos | Fase incompleta | Continuar con excepciones de trabajo o documentos |

## Referencias

- Hitos de fase: `docs-eng-process/openup-knowledge-base/practice-management/risk_value_lifecycle/guidances/concepts/phase-milestones.md`
- Flujo de trabajo del agente: `docs-eng-process/agent-workflow.md`

## Ver también

- [openup-inception](../../openup-phases/inception/SKILL.md) - Detalles de la fase inicial
- [openup-elaboration](../../openup-phases/elaboration/SKILL.md) - Detalles de la fase de elaboración
- [openup-construction](../../openup-phases/construction/SKILL.md) - Detalles de la fase de construcción
- [openup-transition](../../openup-phases/transition/SKILL.md) - Detalles de la fase de transición
