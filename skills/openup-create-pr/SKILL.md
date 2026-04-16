---
name: openup-create-pr
description: Crea un pull request con descripción estructurada vinculada al contexto de la tarea en la hoja de ruta
arguments:
  - name: task_id
    description: El ID de la tarea de la hoja de ruta (ej. T-001). Se detecta automáticamente del nombre de la rama si no se proporciona.
    required: false
  - name: branch
    description: La rama desde la que crear la PR. Usa la rama actual si no se proporciona.
    required: false
  - name: title
    description: Título personalizado de la PR. Se genera automáticamente de la tarea si no se proporciona.
    required: false
  - name: base
    description: Rama base donde fusionar (ej. main, develop). Se detecta automáticamente si no se proporciona.
    required: false
---

# Crear Pull Request

Crea una PR con una descripción estructurada vinculada al contexto de la tarea en la hoja de ruta.

## Proceso

### 1. Detectar Estado Actual

1. Usar `$ARGUMENTS[branch]` o `git rev-parse --abbrev-ref HEAD`.
2. Comprobar commits sin fusionar: `git log <tronco>..HEAD --oneline`. Salir si no hay ninguno.
3. Detectar plataforma: `command -v gh` (GitHub) o `command -v glab` (GitLab).
4. Verificar remoto: `git remote get-url origin`.

### 2. Preparar Commits

1. **Protección de tronco**: Si estás en el tronco (main/master/detectado), crear y cambiar a una rama de funcionalidad (`git checkout -b feature/...` o `fix/...`).
2. **Comprobar cambios sin confirmar**: `git status --porcelain`. Si está limpio, saltar al paso 3.
3. **Organizar commits atómicos**: Agrupar cambios en unidades lógicas. Confirmar en orden de dependencia (deps/config → tipos/interfaces → lógica central → funcionalidades dependientes). Seguir el formato de `docs-eng-process/conventions.md`.
4. **Aplicar estrategia de tests**: Empaquetar tests con los commits de funcionalidad. Para correcciones de errores, confirmar primero el test que falla, luego la corrección.
5. **Lint antes de confirmar**: Ejecutar linter/formateador antes de cada commit. Omitir si no hay ninguno configurado.
6. Reglas completas: `commit-procedure.md` en `complete-task/`.

### 3. Extraer Contexto de la Tarea

1. Obtener task_id de `$ARGUMENTS[task_id]` o extraer del nombre de la rama (regex `([Tt]-?\d+)`).
2. Leer `docs/roadmap.md`, buscar la sección de la tarea, extraer descripción/prioridad/estado.
3. Generar título: `[<task_id>] <descripción>` o usar `$ARGUMENTS[title]`.

### 4. Detectar Rama Tronco

Usar `$ARGUMENTS[base]` si se proporciona; de lo contrario, seguir la detección de tronco en `docs-eng-process/agent-workflow.md` (Procedimiento de Ramas). Registrar el tronco detectado en el log de ejecución.

### 5. Generar Descripción de la PR

Usar la plantilla de `docs-eng-process/templates/pr-description.md` y completar:
- Resumen, Contexto de Tarea (id, descripción, prioridad), Cambios Realizados (git diff/log)
- Pruebas Realizadas, Lista de Verificación de Revisión, Incidencias Relacionadas, Cambios Incompatibles, Notas

### 6. Subir Rama y Crear PR

```bash
git push -u origin <rama>
# GitHub:
gh pr create --base <base> --title "<título>" --body "<descripción>" --label "tarea:<task_id>"
# GitLab:
glab mr create --base <base> --title "<título>" --description "<descripción>" --label "tarea:<task_id>"
```

### 7. Actualizar Documentación (Opcional)

- `docs/roadmap.md`: Añadir URL de la PR a la entrada de la tarea
- `docs/project-status.md`: Anotar la PR en Elementos de Trabajo Activos

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Sin commits pendientes | La rama está al día con el tronco | Informar al usuario de que no se necesita PR |
| Remoto no configurado | El remoto de Git no está configurado | `git remote add origin <url>` |
| CLI no instalado | gh/glab no disponible | `brew install gh` o `brew install glab` |
| task_id no encontrado | El nombre de la rama no tiene ID de tarea | Continuar sin contexto de tarea o proporcionar manualmente |
| Hoja de ruta no encontrada | docs/roadmap.md no existe | Continuar sin contexto de tarea, informar al usuario |
| PR ya existe | La rama ya tiene una PR abierta | Informar al usuario de la URL de la PR existente |
| En rama tronco | Trabajando directamente en main/master | Crear automáticamente una rama de funcionalidad antes de confirmar |

## Referencias

- Procedimiento de Ramas: `docs-eng-process/agent-workflow.md`
- Plantilla de Descripción de PR: `docs-eng-process/templates/pr-description.md`
- Hoja de Ruta: `docs/roadmap.md`

## Ver También

- [openup-complete-task](../complete-task/SKILL.md) - Completar tarea y crear PR
- [openup-start-iteration](../start-iteration/SKILL.md) - Iniciar iteración con creación de rama
