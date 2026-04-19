---
name: openup-create-use-case
description: Crea una especificación de caso de uso a partir de la plantilla
arguments:
  - name: use_case_name
    description: Nombre del caso de uso
    required: true
  - name: primary_actor
    description: El actor principal de este caso de uso
    required: true
  - name: description
    description: Descripción breve de lo que logra el caso de uso
    required: true
---

# Crear Caso de Uso

Esta habilidad crea una especificación de caso de uso a partir de la plantilla OpenUP.

## Cuándo usar

Usa esta habilidad cuando:
- Necesites documentar interacciones del usuario con el sistema
- Estés en la fase de Inicio o Elaboración definiendo requisitos
- Captura requisitos funcionales desde la perspectiva del usuario
- Necesites especifican precondiciones, flujos y postcondiciones
- Crees escenarios de prueba a partir de requisitos.

## Cuándo NO Usar

NO usa esta habilidad cuando:
- Necesites requisitos no funcionales (usa el cuaderno de arquitectura)
- Busques especificaciones técnicas (usa documentos de diseño)
- Documentes comportamiento interno del sistema (usa diseño técnico)
- El caso de uso ya existe (actualiza el archivo existente)

## Criterios de Éxito

Tras usar esta habilidad, verifica:
- [ ] El archivo de caso de uso existe en `docs/use-cases/`
- [ ] El nombre del caso de uso y el actor principal están definidos
- [ ] El flujo básico está documentado
- [ ] Los flujos alternativos están identificados
- [ ] Las pre/postcondiciones están especificadas

##Proceso

### 1. Crear Directorio de Casos de Uso

Asegúrese de que el directorio `docs/use-cases/` exista.

### 2. Generar Nombre de Archivo

Crear el nombre de archivo a partir del nombre del caso de uso: `docs/use-cases/<nombre-caso-uso>.md`

### 3. Copiar plantilla

Copiar `docs-eng-process/templates/use-case-specification.md` al nuevo archivo.

### 4. Completar el Caso de Uso

Actualizar la especificación del caso de uso con:
- **Nombre del caso de uso**: `$ARGUMENTS[use_case_name]`
- **Actor principal**: `$ARGUMENTS[actor_primario]`
- **Descripción**: `$ARGUMENTS[descripción]`
- **Precondiciones**: Qué debe ser cierto antes de comenzar
- **Flujo básico**: Interacción principal paso a paso
- **Flujos alternativos**: Caminos alternativos y casos límite
- **Postcondiciones**: Qué es cierto tras la finalización

### 5. Validar Completitud

Asegurar que el caso de uso incluye:
- Nombre y descripción claros
- Actores identificados
- Flujo básico de eventos
- Flujos de clave alternativa
- Pre/postcondiciones

##Salida

Devuelve:
- Ruta al archivo de caso de uso creado
- ID del caso de uso (para seguimiento)
- Secciones completadas

## Errores Comunes

| Error | causa | Solución |
|-------|-------|----------|
| Plantilla no encontrada | Ruta de plantilla incorrecta | Verificar que existe `docs-eng-process/templates/use-case-specification.md` |
| Nombre de archivo inválido | El nombre del caso de uso tiene caracteres no válidos | Sanear el nombre de archivo, reemplazar espacios con guiones |
| Actores ausentes | Actores no identificados | Identificar actores primarios y secundarios desde la visión/requisitos |

## Referencias

- Plantilla de Caso de Uso: `docs-eng-process/templates/use-case-specification.md`
- Producto de Trabajo de Caso de Uso: `docs-eng-process/openup-knowledge-base/core/common/workproducts/use_case.md`

## Ver También

- [openup-create-vision](../create-vision/SKILL.md) - Definir primero la visión del proyecto
- [openup-detail-use-case](../detail-use-case/SKILL.md) - Transformar caso de uso de alto nivel en escenarios detallados
- [openup-create-test-plan](../create-test-plan/SKILL.md) - Generar pruebas desde los casos de uso
- [openup-elaboration](../../openup-phases/elaboration/SKILL.md) - Detalle de casos de uso en la fase de Elaboración
