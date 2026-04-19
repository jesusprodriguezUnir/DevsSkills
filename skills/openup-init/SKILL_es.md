---
name: openup-init
description: Configuración de proyectos con un solo comando para OpenUP: asistente de inicialización interactivo
arguments:
  - name: project_name
    description: The project name (optional, will prompt if not provided)
    required: false
  - name: project_type
    description: "Type of project: web, api, library, mobile (optional, will prompt if not provided)"
    required: false
  - name: skip_teams
    description: "Skip agent team setup (default: false)"
    required: false
---

# OpenUP Init - Configuración interactiva del proyecto

Esta habilidad proporciona una **inicialización con un solo comando** para proyectos OpenUP, reemplazando el complejo proceso de configuración de varios pasos con un flujo de conversación interactivo.

## Cuándo utilizar

Utilice esta habilidad cuando:
- Iniciar un nuevo proyecto OpenUP
- Configurar OpenUP en un repositorio existente
- Necesita una inicialización rápida del proyecto sin pasos manuales

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- El proyecto ya está inicializado (en su lugar, utilice habilidades de fase)
- Necesidad de personalizar componentes individuales (se recomienda configuración manual)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [] Se crea la estructura del proyecto.
- [ ] Se generan los documentos iniciales
- [] Los equipos de agentes están configurados (si están habilitados)
- [] Git se inicializa (si es necesario)

## Proceso

### 1. Reúna información del proyecto

Si no se proporciona mediante argumentos, solicite interactivamente:

**Nombre del proyecto**: ¿Cómo le gustaría llamar a este proyecto?

**Tipo de proyecto**: ¿Qué tipo de proyecto es este?
- `web` - Aplicación web (frontend/backend)
- `api` - Servicio API REST/GraphQL
- `biblioteca` - Biblioteca/paquete de código reutilizable
- `móvil` - Aplicación móvil
- `cli` - Herramienta de línea de comandos
- `otro` - Especificar

**Fase Inicial**: ¿En qué fase debemos empezar?
- `inception`: define el alcance y la visión (predeterminado para nuevos proyectos)
- `elaboración` - Planificación de arquitectura (para proyectos con visión)
- `construcción` - Desarrollo activo
- `transición` - Preparación para el despliegue

### 2. Crear estructura de proyecto

Cree los siguientes directorios:
```
documentos/
├── solicitudes de entrada/# Documentos de entrada de las partes interesadas
├── casos de uso/ # especificaciones de casos de uso
└── agent-logs/ # Registros de actividad del agente
```

### 3. Generar Documentos Iniciales

#### Estado del proyecto (`docs/project-status.md`)
```rebaja
# Estado del proyecto

**Proyecto**: [PROJECT_NAME]
**Fase**: [INITIAL_PHASE]
**Iteración**: 0
**Objetivo de iteración**: inicialización del proyecto
**Estado**: inicializado
**Tarea actual**: Ninguna
**Iniciado**: [FECHA]
**Última actualización**: [FECHA]
**Actualizado por**: openup-init
```

#### Hoja de ruta (`docs/roadmap.md`)
```rebaja
# Hoja de ruta del proyecto

## T-001: Inicializar la estructura del proyecto OpenUP
**Estado**: completado
**Prioridad**: alta
**Descripción**: Configuración inicial del proyecto y estructura de documentación.

## T-002: [Marcador de posición de siguiente tarea]
**Estado**: pendiente
**Prioridad**: media
**Descripción**: [Por definir]
```

### 4. Configurar equipos de agentes (si no se omite)

**Compruebe si los equipos de agentes están habilitados:**
```golpecito
# Verificar variable de entorno
si [ -z "$CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS" ]; entonces
  echo "Equipos de agentes no habilitados. Habilítelo con:"
  echo "exportar CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"
fi
```

**Crear configuración inicial del equipo:**
- Establecer el tipo de equipo predeterminado según el tipo y la fase del proyecto
- Crear `.claude/settings.json` con los ganchos recomendados

### 5. Inicialice Git (si es necesario)

Compruebe si git está inicializado:
```golpecito
si! git rev-parse --git-dir > /dev/null 2>&1; entonces
  inicio de git
  # Crear compromiso inicial
fi
```

### 6. Crear rama inicial (opcional)

Si comienza con la fase inicial:
- Detectar rama del tronco
- Crear rama: `inception/initialize-project`
- Actualizar el estado del proyecto.

## Producción

Devuelve un resumen de:
- Nombre y tipo de proyecto.
- Fase inicial
- Archivos y directorios creados.
- Próximos pasos

## Valores predeterminados inteligentes

La habilidad utiliza valores predeterminados inteligentes según el tipo de proyecto:

| Tipo de proyecto | Fase predeterminada | Equipo recomendado | Tareas iniciales |
|--------------|---------------|------------------|---------------|
| web | inicio | analista + arquitecto | Requisitos, Arquitectura |
| API | elaboración | arquitecto + promotor | Diseño API, Implementación |
| biblioteca | construcción | desarrollador + probador | Implementación, Pruebas |
| móvil | inicio | analista + arquitecto | Requisitos, Diseño UX |
| cli | construcción | desarrollador | Implementación |

## Plantillas de inicio rápido

### Aplicación web
```golpecito
/openup-init nombre_proyecto: "MyWebApp" tipo_proyecto: web
```

### Servicio API
```golpecito
/openup-init nombre_proyecto: "MiAPI" tipo_proyecto: api
```

### Biblioteca de códigos
```golpecito
/openup-init nombre_proyecto: "MyLib" tipo_proyecto: biblioteca
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Directorio no vacío | Proyecto ya inicializado | Utilice la estructura existente o especifique una nueva ubicación |
| Git no encontrado | Git no instalado | Instale git o use la bandera --no-git |
| Permiso denegado | No se pueden crear directorios | Verificar permisos de directorio |

## Próximos pasos

Después de la inicialización:

1. **Para la fase inicial**: use `/openup-inception actividad: iniciar`
2. **Crear visión**: utilice `/openup-create-vision`
3. **Iniciar la primera iteración**: utilice `/openup-start-iteration`
4. **Equipo de generación**: crea el equipo de agentes apropiado para tu fase

## Ver también

- [openup-inception](../openup-phases/inception/SKILL.md) - Guía de la fase inicial
- [openup-create-vision](../openup-artifacts/create-vision/SKILL.md) - Creación de documentos de visión
- [Configuración de equipos de agentes](../../docs-eng-process/agent-teams-setup.md) - Guía de configuración de equipos

## Ejemplos

### Configuración mínima
```
/inicio-apertura
# Solicita toda la información de forma interactiva
```

### Configuración completa con Teams
```
/openup-init nombre_proyecto: "Comercio electrónico" tipo_proyecto: web
# Crea una estructura de aplicación web con configuración de equipo.
```

### Proyecto existente
```
/openup-init nombre_proyecto: "API existente" tipo_proyecto: api skip_teams: verdadero
# Agrega OpenUP al proyecto existente sin configuración del equipo
```
