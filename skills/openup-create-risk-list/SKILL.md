---
name: openup-create-risk-list
description: Crea o actualiza el documento de evaluación de riesgos a partir de la plantilla
arguments:
  - name: risks
    description: Array JSON de riesgos a añadir (opcional)
    required: false
---

# Crear Lista de Riesgos

Esta skill crea o actualiza un documento de lista de riesgos a partir de la plantilla OpenUP.

## Cuándo Usar

Usa esta skill cuando:
- Comiences un nuevo proyecto y necesites identificar riesgos
- Estés en la fase de Inicio documentando riesgos principales
- Surjan nuevos riesgos durante el proyecto
- Necesites actualizar la probabilidad o impacto de un riesgo
- Planifiques estrategias de mitigación de riesgos

## Cuándo NO Usar

NO uses esta skill cuando:
- La lista de riesgos existe y solo necesita cambios menores (edítala directamente)
- Busques seguimiento de incidencias (usa el gestor de incidencias)
- Los riesgos se hayan materializado y sean ahora incidencias (gestiónalos como incidencias)
- Necesites un análisis de riesgos detallado (usa el proceso de gestión de riesgos)

## Criterios de Éxito

Tras usar esta skill, verifica:
- [ ] La lista de riesgos existe en `docs/risk-list.md`
- [ ] Los riesgos están documentados con descripciones
- [ ] La probabilidad e impacto están evaluados
- [ ] Las estrategias de mitigación están definidas
- [ ] Los responsables de cada riesgo están asignados

## Proceso

### 1. Comprobar Lista de Riesgos Existente

Comprobar si `docs/risk-list.md` existe:
- Si existe, actualizarla
- Si no existe, crear desde la plantilla

### 2. Copiar Plantilla (si es nueva)

Si se crea nueva, copiar `docs-eng-process/templates/risk-list.md` a `docs/risk-list.md`

### 3. Leer Contexto del Proyecto

Leer `docs/project-status.md` y `docs/vision.md` para identificar riesgos potenciales.

### 4. Completar la Lista de Riesgos

Actualizar con:
- **Nombre del proyecto** y contexto
- **Riesgos**: De `$ARGUMENTS[risks]` o identificados del contexto del proyecto
  Para cada riesgo, documentar:
  - Descripción del riesgo
  - Probabilidad (alta/media/baja)
  - Impacto (alto/medio/bajo)
  - Estrategia de mitigación
  - Responsable

### 5. Validar Completitud

Asegurar que la lista de riesgos incluya:
- Descripciones claras de riesgos
- Evaluaciones de probabilidad e impacto
- Estrategias de mitigación
- Responsables de cada riesgo

## Salida

Devuelve:
- Ruta a la lista de riesgos
- Número de riesgos documentados
- Resumen de riesgos de alta prioridad

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Plantilla no encontrada | Ruta de plantilla incorrecta | Verificar que `docs-eng-process/templates/risk-list.md` existe |
| Sin riesgos identificados | Contexto del proyecto insuficiente | Revisar la visión y los requisitos en busca de riesgos potenciales |
| Mitigación ausente | Riesgos documentados sin mitigación | Añadir estrategia de mitigación para cada riesgo |

## Referencias

- Plantilla de Lista de Riesgos: `docs-eng-process/templates/risk-list.md`
- Gestión de Riesgos: `docs-eng-process/openup-knowledge-base/practice-management/risk_val_lifecycle/`
- Rol de Jefe de Proyecto: `docs-eng-process/openup-knowledge-base/core/role/roles/project-manager-4.md`

## Ver También

- [openup-inception](../../openup-phases/inception/SKILL.md) - Identificación de riesgos en la fase de Inicio
- [openup-create-vision](../create-vision/SKILL.md) - La visión revela riesgos potenciales
- [openup-create-architecture-notebook](../create-architecture-notebook/SKILL.md) - Evaluación de riesgos técnicos
