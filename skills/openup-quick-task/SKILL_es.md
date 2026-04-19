---
name: openup-quick-task
description: Modo de iteración rápida para cambios pequeños: flujo de trabajo simplificado con una sobrecarga mínima
arguments:
  - name: task
    description: Brief description of the task to complete
    required: true
  - name: task_id
    description: Roadmap task ID (optional, creates task if not provided)
    required: false
  - name: skip_branch
    description: "Skip branch creation (default: false)"
    required: false
  - name: skip_commit
    description: "Skip auto-commit (default: false)"
    required: false
  - name: skip_logging
    description: "Skip traceability logging (default: false)"
    required: false
---

# Tarea rápida: modo de iteración rápida

**Quick Task** es un flujo de trabajo liviano para pequeños cambios e iteraciones rápidas. Combina varios pasos en un solo comando manteniendo las prácticas esenciales de OpenUP.

## Cuándo utilizar

Utilice tarea rápida para:
- Pequeñas correcciones de errores (<50 líneas cambiadas)
- Actualizaciones de documentación.
- Cambios de configuración
- Experimentos rápidos
- Correcciones urgentes

**Objetivo**: completar tareas en un 50% menos de tiempo que el flujo de trabajo estándar.

## Cuándo NO usarlo

NO lo use para:
- Nuevas funciones (use el flujo de trabajo estándar)
- Refactorización importante (use `/openup-start-iteration`)
- Tareas que requieren revisión de arquitectura (usar equipo completo)
- Trabajo de desarrollo de varias horas.

## Proceso

### 1. Carga rápida de contexto

```bash
# Load minimal context only
python3 .claude/scripts/batch-context.py --minimal
```

### 2. Rama rápida (opcional)

Si no omite la ramificación:
```golpecito
# Detectar tronco y crear rama rápida
BRANCH_NAME="quick/$(fecha +%Y%m%d-%H%M%S)-$(echo $tarea | tr ' ' '-' | head -c 20)"
git pago -b $BRANCH_NAME
```

### 3. Ejecutar tarea

Implementar el cambio:
- Leer la descripción de la tarea.
- Hacer los cambios necesarios
- Verificar que la solución funcione.

### 4. Confirmación rápida (opcional)

Si no se salta el compromiso:
```golpecito
git agregar.
git commit -m "rápido: $tarea

Coautor de: Claude Opus 4.6 <noreply@anthropic.com>"
```

### 5. Registro rápido (opcional)

Si no omite el registro:
```golpecito
echo "$(fecha -Isegundos) | tarea rápida | $tarea" >> docs/agent-logs/quick-tasks.log
```

## Producción

Devoluciones:
- Confirmación de tarea completada
- Archivos cambiados (recuento)
- Nombre de la sucursal (si se creó)
- Confirmar hash (si se confirma)

## Comparación: estándar versus rápido

| Paso | Flujo de trabajo estándar | Tarea rápida |
|------|-------------------|------------|
| Leer el estado del proyecto | Documento completo | Sólo mínimo |
| Crear sucursal | Denominación basada en tareas | Basado en marca de tiempo |
| Cumplimiento de los POE | Inicio de ejecución completo | Saltado |
| Documentación | Actualización completa | Mínimo |
| Entrada de registro | JSONL completo | Línea de registro simple |
| **Hora típica** | ~8 minutos | ~4 minutos |

## Ejemplos

### Corrección rápida de errores
```
/tarea openup-quick-task: "Corregir error tipográfico en README.md"
```

### Actualización de documentación
```
/tarea openup-quick-task: "Actualizar documentos API para un nuevo punto final"
```

### Saltar ramificación
```
/tarea openup-quick-task: "Agregar comentario a utils.py" skip_branch: verdadero
```

### Control total
```
/tarea openup-quick-task: "Error de autenticación de corrección urgente" skip_commit: false skip_logging: true
```

## Criterios de éxito

- [] Tarea completada
- [] Cambios verificados
- [] Rama creada (si no se omite)
- [] Comprometido (si no se omite)
- [] Registrado (si no se omite)

## Funciones inteligentes

**Detección automática de oportunidades de omisión:**
- Si ya está en la rama de funciones → omitir la rama
- Si no hay cambios en git → omitir confirmación
- Si se cambia un solo archivo → registro mínimo

**Tarea de categorización automática:**
- Corrección de errores → prefijo `bugfix/`
- Documentos → prefijo `docs/`
- Correcciones urgentes → prefijo `hotfix/`

## Ver también

- [openup-start-iteration](../start-iteration/SKILL.md) - Flujo de trabajo de iteración completo
- [openup-complete-task](../complete-task/SKILL.md) - Finalización de tareas con PR
- [openup-tdd-workflow](../tdd-workflow/SKILL.md) - Ciclo TDD
