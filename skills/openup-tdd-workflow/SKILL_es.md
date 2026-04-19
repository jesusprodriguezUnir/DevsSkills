---
name: openup-tdd-workflow
description: Guía del ciclo Test-Driven Development adaptado para agentes de IA con un enfoque pragmático
arguments:
  - name: phase
    description: TDD phase (red, green, refactor, full)
    required: false
  - name: feature
    description: Feature or component to implement
    required: true
---

# Flujo de trabajo TDD

Guíe el ciclo de refactorización rojo-verde con un enfoque pragmático. TDD es una herramienta, no un mandato: utilícela cuando sea útil.

## Proceso

### 1. Determinar la fase

Basado en `$ARGUMENTS[fase]`:

| Fase | Descripción |
|-------|-------------|
| rojo | Escriba la prueba primero (preferiblemente antes de la implementación) |
| verde | Implementar para pasar la prueba (punto de confirmación) |
| refactorizar | Limpiar código mientras pasan las pruebas (opcional para cambios pequeños) |
| lleno | Ejecute el ciclo completo de refactor rojo-verde |

### 2. Ejecutar proceso específico de fase

Ver documentación específica de la fase:
- [Fase ROJA](./red-phase.md) - Prueba fallida de escritura
- [Fase VERDE](./green-phase.md) - Función de implementación
- [Fase REFACTOR](./refactor-phase.md) - Mejora la calidad del código

### 3. Verificar antes de continuar

Después de cada fase:
- ROJO: Escriba el examen primero cuando sea práctico (no es obligatorio en todos los casos)
- VERDE: Verifique que la prueba pase antes de confirmar (confirmar cuando esté verde)
- REFACTOR: Verifica que las pruebas aún pasen; refactor es opcional para pequeños cambios

### 4. Crear registro TDD

Documente el ciclo TDD en `docs/tdd-logs/<feature>-tdd.md`:
- Nombre de la característica, casos de prueba escritos, notas de implementación, refactorización realizada, lecciones aprendidas

## Criterios de éxito

- [ ] Las pruebas están escritas (preferiblemente antes de la implementación)
- [ ] La implementación hace que las pruebas pasen
- [] El código es razonablemente limpio y funcional.
- [] Las pruebas pasan antes de la confirmación.

## Producción

Devuelve un resumen de:
- Fase TDD completada
- Archivo de prueba creado/actualizado
- Archivo de implementación creado/actualizado
- Resultados de la prueba
- Notas de refactorización

## Ver también

- [openup-create-test-plan](../openup-artifacts/create-test-plan/SKILL.md) - Crear un plan de prueba integral
- [openup-complete-task](../complete-task/SKILL.md) - Completa la tarea después del ciclo TDD
- [openup-detail-use-case](../openup-artifacts/detail-use-case/SKILL.md) - Detallar casos de uso antes de escribir pruebas
