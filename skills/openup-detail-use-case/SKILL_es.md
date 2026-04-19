---
name: openup-detail-use-case
description: Transforme un caso de uso de alto nivel en escenarios detallados con casos de prueba
arguments:
  - name: use_case_name
    description: Name of the use case to detail (file name without .md)
    required: true
  - name: generate_tests
    description: "Generate test cases from scenarios (true/false, default: true)"
    required: false
---

# Caso de uso detallado

Esta habilidad transforma una especificación de caso de uso de alto nivel en escenarios detallados con criterios de aceptación de Gherkin y casos de prueba.

## Cuándo utilizar

Utilice esta habilidad cuando:
- Existe un caso de uso de alto nivel pero carece de escenarios detallados.
- Necesidad de documentar caminos felices, flujos alternativos y casos de error.
- Listo para crear criterios de aceptación de Gherkin para la automatización.
- Preparación para generar casos de prueba a partir de casos de uso.
- En fase de Elaboración al detallar requisitos

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- El caso de uso no existe (use `/openup-create-use-case` primero)
- El caso de uso ya está completamente detallado con escenarios.
- Sólo necesitas crear un nuevo caso de uso desde cero.
- Trabajar en requisitos no funcionales (usar cuaderno de arquitectura)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [] El caso de uso se actualiza con escenarios detallados.
- [] La ruta feliz, las rutas alternativas y las rutas de error están documentadas
- [] Los criterios de aceptación de Gherkin están escritos para cada escenario.
- [] Se generan casos de prueba (si generate_tests=true)
- [ ] Todos los actores están identificados (primarios y secundarios)
- [ ] Las condiciones previas y posteriores son claras

## Resumen del proceso

1. Leer el caso de uso existente
2. Identificar escenarios (camino feliz, alternativas, errores)
3. Documente cada escenario con flujos paso a paso.
4. Generar criterios de aceptación de Gherkin
5. Cree casos de prueba (si se solicita)
6. Actualice el archivo de caso de uso.

## Pasos detallados

### 1. Leer el caso de uso existente

Lea el archivo de caso de uso de `docs/use-cases/$ARGUMENTS[use_case_name].md`:
- Extraer el nombre del caso de uso, el ID y la descripción.
- Identificar el actor principal.
- Revisar el flujo básico existente.
- Tenga en cuenta cualquier flujo alternativo ya documentado.

### 2. Identificar escenarios

Divida el caso de uso en distintos escenarios:

**Camino feliz (escenario principal):**
- El principal escenario de éxito donde todo sale como se esperaba.
- El usuario sigue el flujo de trabajo más común.

**Rutas alternativas:**
- Diferentes formas de lograr el mismo objetivo.
- Pasos opcionales o lógica de ramificación.
- Opciones y variaciones del usuario.

**Rutas de error:**
- Entradas o acciones no válidas
- Fallos del sistema
- Casos extremos y condiciones de contorno.

### 3. Escenarios de documentos

Para cada escenario, documente:

| Elemento | Descripción |
|---------|-------------|
| Nombre del escenario | Nombre claro y descriptivo |
| Descripción | Qué hace que este escenario sea único |
| Pasos | Interacción paso a paso (Actor → Sistema) |
| Condiciones previas | Lo que debe ser cierto ante este escenario |
| Poscondiciones | ¿Qué es cierto después de este escenario?

### 4. Generar criterios de aceptación de pepinillo

Para cada escenario, escriba los criterios de formato de Gherkin:

```gherkin
Given <precondition>
And <additional preconditions>
When <actor takes action>
And <additional actions>
Then <expected outcome>
And <additional outcomes>
```

**Ejemplo:**

```gherkin
Given the user is logged in
And the user has items in their cart
When the user clicks "Checkout"
Then the user is redirected to the payment page
And the order total is displayed
```

### 5. Crear casos de prueba (opcional)

Si `$ARGUMENTS[generate_tests] == "verdadero"`:

Cree archivos de casos de prueba para cada escenario en `docs/test-cases/`:
- Formato del nombre de archivo: `<nombre-caso-de-uso>-<escenario>-test.md`
- Utilice la plantilla de caso de prueba como guía.
- Incluir pasos del escenario, datos de prueba y resultados esperados.

### 6. Actualizar el archivo de caso de uso

Actualice el archivo de caso de uso existente con:
- Agregar sección de escenarios detallados
- Incluir criterios de aceptación de Gherkin.
- Enlace a archivos de casos de prueba
- Asegurar que todos los actores estén documentados.
- Verificar que las condiciones previas y posteriores estén completas

## Producción

Devuelve un resumen de:
- Archivo de caso de uso actualizado
- Número de escenarios documentados
- Casos de prueba creados (si corresponde)
- Secciones agregadas al caso de uso.

## Ejemplo de uso

```
/openup-detail-use-case use_case_name: user-login generate_tests: true
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Caso de uso no encontrado | El archivo no existe en docs/use-cases/ | Verifique el nombre del caso de uso o cree un caso de uso primero |
| Sin flujo básico | El caso de uso está incompleto | Complete el flujo básico antes de detallar |
| Escenarios duplicados | Mismo escenario documentado varias veces | Consolidar escenarios similares |
| Actores desaparecidos | Actores no identificados | Identificar actores primarios y secundarios del contexto |

## Referencias

- Plantilla de caso de uso: `docs-eng-process/templates/use-case-specification.md`
- Plantilla de escenarios de casos de uso: `docs-eng-process/templates/use-case-scenarios.md`
- Plantilla de caso de prueba: `docs-eng-process/templates/test-case.md`
- Sintaxis del pepinillo: https://cucumber.io/docs/gherkin/reference/

## Ver también

- [openup-create-use-case](../create-use-case/SKILL.md) - Crea un nuevo caso de uso
- [openup-create-test-plan](../create-test-plan/SKILL.md) - Generar plan de prueba a partir de casos de uso
- [openup-elaboration](../../openup-phases/elaboration/SKILL.md) - Actividades de la fase de elaboración
