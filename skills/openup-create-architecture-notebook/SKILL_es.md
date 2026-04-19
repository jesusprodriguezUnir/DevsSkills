---
name: openup-create-architecture-notebook
description: Genera o actualiza la documentación de arquitectura a partir de la plantilla.
arguments:
  - name: system_name
    description: Nombre del sistema
    required: true
  - name: architectural_concerns
    description: Preocupaciones arquitectónicas clave a abordar
    required: false
---

# Crear Cuaderno de Arquitectura

Esta habilidad genera o actualiza un cuaderno de arquitectura a partir de la plantilla OpenUP.

## Cuándo usar

Usa esta habilidad cuando:
- Comienza la fase de Elaboración y necesitas documentar la arquitectura.
- Tomes decisiones arquitectónicas significativas
- Necesites documentar el diseño y las restricciones del sistema.
- Establezcas la línea base de arquitectura.
- Revisa o actualiza la arquitectura existente.

## Cuándo NO Usar

NO usa esta habilidad cuando:
- Estés en la fase de Inicio antes de definir la arquitectura (usa `/openup-create-vision`)
- Necesites diseño detallado de componentes (usa documentos de diseño)
- Busques detalles de implementación (usa documentación del código)
- El cuaderno de arquitectura existe y solo necesita cambios menores (edítalo directamente)

## Criterios de Éxito

Tras usar esta habilidad, verifica:
- [ ] El cuaderno de arquitectura existe en `docs/architecture-notebook.md`
- [ ] El nombre y contexto del sistema están definidos
- [ ] Las decisiones arquitectónicas clave están documentadas
- [ ] Las restricciones arquitectónicas están listadas
- [ ] Los atributos de calidad están especificados

##Proceso

### 1. Comprobar Arquitectura Existente

Comprobar si existe `docs/architecture-notebook.md`:
- Si existe, actualízalo
- Si no existe, crear desde la plantilla

### 2. Leer Contexto del Proyecto

Lea `docs/project-status.md` y `docs/vision.md` para comprender:
- Requisitos del sistema
- Restricciones
- Preocupaciones de los interesados

### 3. Copiar plantilla (si es nuevo)

Si se crea nuevo, copie `docs-eng-process/templates/architecture-notebook.md` a `docs/architecture-notebook.md`

### 4. Completar el Cuaderno de Arquitectura

Actualizar con:
- **Nombre del sistema**: `$ARGUMENTS[nombre_sistema]`
- **Preocupaciones arquitectónicas**: De `$ARGUMENTS[architectural_concerns]` o derivadas de los requisitos
- **Visión general de la arquitectura**: Arquitectura del sistema a alto nivel
- **Decisiones arquitectónicas clave**: Justificación de las decisiones principales
- **Restricciones**: Restricciones técnicas y de negocio
- **Atributos de calidad**: Requisitos de rendimiento, seguridad y escalabilidad
- **Descomposición en subsistemas**: Componentes principales del sistema

### 5. Validar Completitud

Asegurar que el cuaderno de arquitectura incluya:
- Visión general y contexto del sistema.
- Decisiones arquitectónicas clave con justificación
- Restricciones arquitectónicas
- Requisitos de atributos de calidad
- Descomposición en subsistemas/componentes

##Salida

Devuelve:
- Ruta al cuaderno de arquitectura.
- Lista de secciones completadas
- Decisiones arquitectónicas documentadas

## Errores Comunes

| Error | causa | Solución |
|-------|-------|----------|
| Plantilla no encontrada | Ruta de plantilla incorrecta | Verificar que existe `docs-eng-process/templates/architecture-notebook.md` |
| Contexto insuficiente | Visión/requisitos no definidos | Crear primero el documento de visión |
| Sobrescribir existente | El cuaderno de arquitectura ya existe | Actualizar el archivo existente en lugar de crear uno nuevo |

## Referencias

- Plantilla de Cuaderno de Arquitectura: `docs-eng-process/templates/architecture-notebook.md`
- Producto de Trabajo de Arquitectura: `docs-eng-process/openup-knowledge-base/practice-technical/evolutionary_arch/base/workproducts/architecture-notebook-6.md`
- Rol de Arquitecto: `docs-eng-process/openup-knowledge-base/core/role/roles/architect-6.md`

## Ver También

- [openup-elaboration](../../openup-phases/elaboration/SKILL.md) - Guía de la fase de Elaboración
- [openup-create-vision](../create-vision/SKILL.md) - Definir visión antes de la arquitectura
- [openup-create-risk-list](../create-risk-list/SKILL.md) - Documentar riesgos técnicos
