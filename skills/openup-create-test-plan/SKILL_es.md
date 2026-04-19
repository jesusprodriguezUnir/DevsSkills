---
name: openup-create-test-plan
description: Genera casos de prueba y plan de pruebas a partir de casos de uso y requisitos.
arguments:
  - name: scope
    description: Qué probar (ej. funcionalidad específica, caso de uso)
    required: true
---

# Crear Plan de Pruebas

Esta habilidad genera casos de prueba y documentación de prueba a partir de las plantillas OpenUP.

## Cuándo usar

Usa esta habilidad cuando:
- Necesites crear casos de prueba para funcionalidades o casos de uso.
- Estés en la fase de Elaboración o Construcción planificando pruebas
- Comienza las pruebas de una nueva funcionalidad.
- Necesidades documentales procedimientos de prueba
- Crees scripts de prueba para automatización.

## Cuándo NO Usar

NO usa esta habilidad cuando:
- Quiere ejecutar pruebas (usa el ejecutor de pruebas)
- Necesites depurar fallos en pruebas (usa herramientas de depuración)
- El plan de pruebas existe y solo necesita cambios menores (edítalo directamente)
- Busques informes de pruebas (usa los informes de pruebas)

## Criterios de Éxito

Tras usar esta habilidad, verifica:
- [ ] Los casos de prueba existen en `docs/test-cases/`
- [ ] Los scripts de prueba existen en `docs/test-scripts/`
- [ ] La cobertura incluye camino feliz y límite de casos
- [ ] Los resultados esperados están definidos
- [ ] Los procedimientos de prueba están documentados

##Proceso

### 1. Leer requisitos

Leer la documentación relevante:
- `docs/use-cases/*.md` para casos de uso
- `docs/requirements/*.md` para requisitos
- Cualquier documento de diseño para el `$ARGUMENTS[scope]`

### 2. Crear Directorio de Pruebas

Asegúrese de que los directorios `docs/test-cases/` y `docs/test-scripts/` existan.

### 3. Copiar plantillas

Copiar las plantillas según sea necesario:
- `docs-eng-process/templates/test-case.md` → `docs/test-cases/<nombre>-test-case.md`
- `docs-eng-process/templates/test-script.md` → `docs/test-scripts/<nombre>-test-script.md`

### 4. Completar los Casos de Prueba

Para cada caso de prueba, documental:
- **ID del caso de prueba** y nombre
- **Descripción**: Qué se está probando
- **Precondiciones**: Estado antes de la prueba
- **Pasos de prueba**: Acciones paso a paso
- **Resultados esperados**: Qué debería ocurrir
- **Postcondiciones**: Estado después de la prueba
- **Prioridad**: Nivel de prioridad del test

### 5. Completar los scripts de prueba

Para cada guión de prueba, documental:
- **ID del script de prueba** y nombre
- **Propósito**: Qué valida el guión
- **Configuración**: Cómo preparar la prueba
- **Procedimientos de prueba**: Pasos detallados de ejecución
- **Limpieza**: Cómo limpiar después de la prueba

### 6. Validar Cobertura

Asegurar que la cobertura de pruebas incluya:
- Escenarios de camino feliz
- Casos límite
- Condiciones de error
- Puntos de integración

##Salida

Devuelve:
- Rutas a los casos de prueba y scripts creados.
- Resumen de cobertura de pruebas.
- Huecos identificados

## Errores Comunes

| Error | causa | Solución |
|-------|-------|----------|
| Plantilla no encontrada | Ruta de plantilla incorrecta | Verificar que `docs-eng-process/templates/test-case.md` y `test-script.md` existen |
| Cobertura insuficiente | Pruebas en solitario de camino feliz | Añadir casos límite y condiciones de error |
| Resultados esperados ausentes | Pasos de prueba sin validación | Definir resultados esperados para cada paso |

## Referencias

- Plantilla de Caso de Prueba: `docs-eng-process/templates/test-case.md`
- Plantilla de Script de Prueba: `docs-eng-process/templates/test-script.md`
- Rol de Probador: `docs-eng-process/openup-knowledge-base/core/role/roles/tester-5.md`

## Ver También

- [openup-create-use-case](../create-use-case/SKILL.md) - Generar pruebas desde casos de uso
- [openup-construction](../../openup-phases/construction/SKILL.md) - Pruebas en la fase de Construcción
- [openup-phase-review](../../openup-workflow/phase-review/SKILL.md) - Revisar cobertura de pruebas
