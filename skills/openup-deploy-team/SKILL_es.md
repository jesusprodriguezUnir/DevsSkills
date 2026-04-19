---
name: openup-deploy-team
description: Implementar un equipo de agentes OpenUP para trabajar en la iteración actual
arguments:
  - name: team_type
    description: Type of team to create (feature, investigation, construction, elaboration, inception, transition, planning, full)
    required: false
  - name: roles
    description: Specific roles to include (analyst, architect, developer, tester, project-manager). Comma-separated.
    required: false
---

# Implementar equipo

Esta habilidad implementa un equipo de agentes de OpenUP para trabajar en la iteración actual. Lee el contexto de la iteración y crea el equipo apropiado con las asignaciones de roles adecuadas.

## Cuándo utilizar

Utilice esta habilidad **después** de que `/openup-start-iteration` se haya completado:
- Se inicializa la iteración.
- Se crea la sucursal
- Se actualiza el estado del proyecto.
- La hoja de ruta tiene la tarea.

Luego usa esta habilidad para desplegar el equipo.

## Cuándo NO usarlo

NO uses esta habilidad:
- Antes de que se haya llamado a `/openup-start-iteration`
- Sin conocer el objetivo de la iteración.
- Para trabajos que no sean OpenUP

## Proceso

### 1. Leer el contexto de iteración actual

Lea `docs/project-status.md` para obtener:
- Fase actual
- Número de iteración actual
- Objetivo de iteración actual
- Tarea actual (si está configurada)

### 2. Determinar la composición del equipo

Según el objetivo de la iteración y el tipo_equipo:
- **característica**: analista, arquitecto, desarrollador, probador
- **investigación**: arquitecto, desarrollador, probador
- **construcción**: desarrollador, probador (+ arquitecto, analista según sea necesario)
- **elaboración**: arquitecto, desarrollador, tester (+ analista según sea necesario)
- **inception**: analista, director de proyecto (+ arquitecto según sea necesario)
- **transición**: tester, director de proyecto, desarrollador (+ analista según sea necesario)
- **planificación**: director de proyecto, analista (+ arquitecto, desarrollador según sea necesario)
- **completo**: todos los roles

O utilice roles personalizados de `$ARGUMENTS[roles]`

### 3. Crea el equipo

Genere compañeros de equipo utilizando la herramienta Tarea con los tipos de subagente adecuados.

### 4. Informar al equipo

Enviar mensaje inicial a todos los compañeros de equipo con:
- Objetivo de iteración
- Fase actual
- Contexto de la tarea
- Flujo de trabajo esperado
- Instrucciones de coordinación

### 5. Configurar la coordinación

Asegúrese de que el líder del equipo sepa:
- Monitorear el progreso
- Asignar tareas a los roles apropiados.
- Utilice `/openup-complete-task` cuando haya terminado el trabajo.

## Producción

Devoluciones:
- Composición del equipo
- Asignaciones de miembros del equipo.
- Contexto de iteración actual
- Flujo de trabajo esperado

## Ejemplo de uso

```
/openup-deploy-team team_type: feature
```

O con roles específicos:
```
/roles del equipo openup-deploy: analista,desarrollador,probador
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| No se encontró ninguna iteración | docs/project-status.md no existe o no hay iteración activa | Ejecute /openup-start-iteration primero |
| Tipo de equipo desconocido | parámetro team_type no reconocido | Utilice uno de: característica, investigación, construcción, elaboración, inicio, transición, planificación, completo |
| No se puede generar equipo | Equipos de agentes no habilitados | Establecer CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 |

## Ver también

- [openup-start-iteration](../openup-start-iteration/SKILL.md) - Inicialice la iteración primero
- [openup-complete-task](../openup-complete-task/SKILL.md) - Completa el trabajo cuando termines
- [Configuraciones de equipo](../../teams/) - Archivos de definición de equipo
