---
name: openup-plan-feature
description: Genere un plan de iteración y una entrada de hoja de ruta para una idea de característica
arguments:
  - name: topic
    description: The feature idea or requirements to plan (e.g., "Add PDF export for chat conversations")
    required: true
  - name: task_id
    description: Override auto-detected task ID (e.g., C3-004). Auto-detected from roadmap if not provided.
    required: false
  - name: priority
    description: Task priority — critical, high, or medium (default medium)
    required: false
  - name: validate
    description: Spawn analyst + architect team to review the plan before finalizing (default false)
    required: false
  - name: create_pr
    description: Create branch, commit, push, and open a PR (default true)
    required: false
---

# Característica del plan

Esta habilidad automatiza todo el flujo de trabajo de "planificar una característica": explora la base de código, genera un plan de iteración detallado, agrega una entrada de hoja de ruta y, opcionalmente, crea un PR, todo a partir de una única idea de característica.

## Cuándo utilizar

Utilice esta habilidad cuando:
- Tiene una idea para una nueva característica y necesita un plan de implementación detallado.
- Quiere agregar una característica a la hoja de ruta con un documento de plan.
- Debes explorar el código base para comprender qué tocará una característica antes de codificar.
- Planificación de una tarea de iteración a partir de una descripción de alto nivel.

## Cuándo NO usarlo

NO uses esta habilidad cuando:
- La función ya tiene un plan de iteración (edítelo directamente)
- Necesitas comenzar a implementar (usa `/openup-start-iteration`)
- La tarea es una solución rápida o una corrección de errores (use `/openup-quick-task`)
- Solo necesita actualizar la hoja de ruta sin un plan (edite `docs/roadmap.md` directamente)

## Criterios de éxito

Después de usar esta habilidad, verifique:
- [] El archivo del plan de iteración existe en `docs/iteration-plans/{task_id}-{slug}.md`
- [] El plan incluye el estado actual con extractos de código reales del código base
- [] El plan incluye el diseño propuesto con ejemplos de código concretos
- [ ] El plan incluye criterios de aceptación, dependencias y archivos clave
- [] La entrada de la hoja de ruta existe en `docs/roadmap.md` con el formato correcto
- [] Se crea PR (si `create_pr` es verdadero)

## Resumen del proceso

1. Leer el contexto del proyecto (estado, hoja de ruta, arquitectura)
2. Detectar automáticamente el ID de la tarea en la hoja de ruta
3. Explore la base de código para obtener código relevante
4. Generar documento de plan de iteración.
5. Actualizar la hoja de ruta con una nueva entrada.
6. Opcionalmente validar con el equipo de analista + arquitecto.
7. Opcionalmente, cree sucursales, confirmaciones, envíos y relaciones públicas.
8. Resumen actual

## Pasos detallados

### 1. Leer el contexto del proyecto

Lea estos archivos para comprender el estado actual del proyecto:
- `docs/project-status.md` — fase actual, iteración, tareas completadas
- `docs/roadmap.md` — tareas existentes, prioridades, dependencias, formato
- `docs/architecture-notebook.md` — decisiones y limitaciones arquitectónicas

Registro:
- Fase actual (por ejemplo, "construcción")
- Número de iteración actual
- Convenciones de nomenclatura para ID de tareas en la fase actual

### 2. ID de tarea de detección automática

Si se proporciona `$ARGUMENTS[task_id]`, úselo directamente.

De lo contrario, realice la detección automática escaneando `docs/roadmap.md`:
1. Identifique el prefijo de fase actual en `docs/project-status.md` (por ejemplo, `C` para Construcción, `E` para Elaboración, `T` para Inicio)
2. Encuentre todos los ID de tareas que coincidan con el patrón `{prefijo}{iteración}-{secuencia}` (por ejemplo, `C3-001`, `C3-002`, `C3-003`)
3. Extraiga el número de secuencia más alto en la iteración actual.
4. Incremente en 1 para obtener el siguiente ID (por ejemplo, si el más alto es "C3-003", el siguiente es "C3-004")
5. Si no existen tareas para la iteración actual, comience en `001`

**Importante**: Escanee también la sección "Funciones futuras/acumuladas" en busca de ID `T-0XX` para evitar colisiones.

### 3. Explorar la base de código

Este es un paso crítico. El plan de iteración debe hacer referencia a archivos y códigos reales, no a descripciones abstractas.

Según el tema de la función ("$ARGUMENTS[topic]`), explore:
1. **Modelos**: Grep/Glob para modelos ActiveRecord relevantes, sus asociaciones, validaciones y alcances.
2. **Controladores**: busque controladores que manejen funciones relacionadas
3. **Servicios**: busque objetos de servicio en `app/services/` relacionados con la característica
4. **Vistas**: busque vistas y parciales relevantes
5. **Rutas**: consulte `config/routes.rb` para ver definiciones de rutas relacionadas
6. **Esquema** — Lea `db/schema.rb` para ver las definiciones de tablas relevantes
7. **Configuraciones regionales**: verifique `config/locales/en.yml` y `config/locales/es.yml` para ver las claves i18n existentes en el área
8. **Pruebas**: busque archivos de prueba existentes para el código afectado
9. **Config** — Verifique `config/app_settings.yml` u otros archivos de configuración si son relevantes

Extraiga fragmentos de código reales (con rutas de archivo y números de línea) para la sección "Estado actual" del plan.

### 4. Generar plan de iteración

Escriba el plan de iteración en `docs/iteration-plans/{task_id_lower}-{slug}.md` donde:
- `{task_id_lower}` es el ID de la tarea en minúscula (por ejemplo, `c3-004`)
- `{slug}` es un slug corto de kebab derivado del tema principal (por ejemplo, `pdf-export`)

Utilice esta estructura (que coincida con el formato establecido del proyecto):

```markdown
# {Task ID}: {Title}

**Fase**: {fase}
**Estado**: pendiente
**Objetivo**: {objetivo de una línea}
**Prioridad**: {prioridad}

---

## Contexto

{Por qué se necesita esta función. Antecedentes y motivación.}

---

## Estado actual

{Para cada área relevante, muestre el código actual real con rutas de archivo y números de línea.
Incluya definiciones de modelos, acciones del controlador, métodos de servicio, extractos de vista, rutas y esquemas.}

### {Área 1} (`ruta/al/archivo.rb`)

```ruby
# Current implementation
```

### {Área 2} (`ruta/al/archivo.rb`)

```ruby
# Current implementation
```

---

## Diseño propuesto

{Para cada cambio, muestre el código propuesto con un antes/después claro o un código nuevo.
Agrupar por unidades lógicas de trabajo (por ejemplo, Migración, Modelo, Servicio, Controlador, Vistas, i18n).}

### {Cambio 1}: {Descripción}

**Archivo**: `ruta/al/archivo.rb`

```ruby
# Proposed implementation
```

### {Cambio 2}: {Descripción}

**Nuevo archivo**: `ruta/al/nuevo_archivo.rb`

```ruby
# Proposed implementation
```

---

## i18n

Nuevas claves para `config/locales/en.yml`:

```yaml
en:
  # new keys
```

Nuevas claves para `config/locales/es.yml`:

```yaml
es:
  # new keys
```

---

## Criterios de aceptación

- [ ] {Criterio 1}
- [ ] {Criterio 2}
-[ ]...

---

## Estrategia de prueba

- {Categoría de prueba 1}: {qué probar}
- {Categoría de prueba 2}: {qué probar}

---

## Dependencias

- {ID de tarea} ({descripción} — {estado})

---

## Archivos clave

| Archivo | Cambiar |
|------|--------|
| `ruta/al/archivo` | {Descripción del cambio} |

---

## Fuera de alcance

- {Artículo 1}
- {Artículo 2}

---

## Preguntas abiertas

1. {Pregunta 1}
2. {Pregunta 2}
```

### 5. Actualizar la hoja de ruta

Inserte una nueva entrada en `docs/roadmap.md` en la sección de fase correcta.

Coincide exactamente con el formato existente:

```markdown
---

## {ID de tarea}: {Título}
**Estado**: pendiente
**Prioridad**: {prioridad}
**Descripción**: {descripción de 1 a 3 oraciones de la función}
- {Entregable clave 1}
- {Entregable clave 2}
-...

**Dependencias**: {ID de tarea separados por comas}

**Ver**: `docs/iteration-plans/{filename}.md`
```

**Reglas de colocación**:
- Insertar debajo del título de fase correcto (por ejemplo, "## Fase de construcción")
- Colocar después de la última entrada en esa sección de fase (antes del encabezado de la siguiente fase o del separador "---")
- Las tareas pendientes deberían aparecer después de las tareas completadas en la misma fase.

### 6. Validar con el equipo (opcional)

Sólo si `$ARGUMENTS[validar]` es `"verdadero"`:

1. **Cree un equipo** usando TeamCreate con el nombre `plan-review-{task_id}`
2. **Crear tareas de revisión**:
   - Tarea para analista: "Revisar la integridad de los requisitos para {task_id}"
   - Tarea para arquitecto: "Revisar la viabilidad técnica de {task_id}"
3. **Regenerar compañeros de equipo**:
   - Analista (tipo_subagente: `propósito general`, nombre_equipo, instrucciones de `.claude/teammates/analyst.md`):
     - Leer el plan de iteración generado.
     - Revisión de: requisitos completos, criterios de aceptación faltantes, alcance poco claro, impacto en las partes interesadas
     - Enviar los resultados por mensaje
   - Arquitecto (tipo_subagente: `propósito general`, nombre_equipo, instrucciones de `.claude/teammates/architect.md`):
     - Leer el plan de iteración generado y `docs/architecture-notebook.md`
     - Revisión de: viabilidad técnica, alineación arquitectónica, problemas de rendimiento, implicaciones de seguridad, riesgos de dependencia
     - Enviar los resultados por mensaje
4. **Espere a que se completen ambas revisiones**
5. **Incorporar comentarios**: actualice el plan de iteración con sugerencias válidas.
6. **Cerrar equipo**: envía solicitudes de cierre a ambos compañeros de equipo y luego elimina el equipo.

### 7. Crear sucursal y PR (opcional)

Sólo si `$ARGUMENTS[create_pr]` no es `"falso"` (el valor predeterminado es verdadero):

1. **Crear rama**: `docs/{task_id_lower}-{slug}` (usa el prefijo `docs/` ya que es solo documentación)
   ```golpecito
   git checkout -b docs/{task_id_lower}-{slug}
   ```

2. **Preparación y compromiso**:
   ```golpecito
   git add docs/iteration-plans/{nombre de archivo}.md docs/roadmap.md
   git commit -m "docs: agregar plan de iteración y entrada de hoja de ruta para {task_id}"
   ```

3. **Empujar rama**:
   ```golpecito
   git push -u documentos de origen/{task_id_lower}-{slug}
   ```

4. **Crear relaciones públicas**:
   ```golpecito
   gh pr crear \
     --title "docs: {ID de tarea} — {Título}" \
     --cuerpo "$(gato <<'EOF'
   ## Resumen

- Agregar plan de iteración para {ID de tarea}: {Título}
   - Agregar entrada de hoja de ruta en la fase {Fase}

## Archivos

- `docs/iteration-plans/{filename}.md` — plan de implementación detallado
   - `docs/roadmap.md` — nueva entrada de hoja de ruta

## Notas de revisión

Este es un PR de planificación (solo documentación). Revise el plan de iteración para:
   - Integridad del diseño propuesto.
   - Precisión del análisis del estado actual.
   - Viabilidad de los criterios de aceptación.

🤖 Generado con [Código Claude](https://claude.com/claude-code)
   EOF
   )"
   ```

### 8. Resumen actual

Envíe un resumen al usuario:

```
## Feature Plan Created

- **ID de tarea**: {task_id}
- **Título**: {título}
- **Prioridad**: {prioridad}
- **Plan de iteración**: `docs/iteration-plans/{filename}.md`
- **Hoja de ruta**: `docs/roadmap.md` actualizado
- **Sucursal**: `docs/{task_id_lower}-{slug}` (si se creó)
- **PR**: {URL PR} (si se crea)
- **Validado**: {sí/no}

### Próximos pasos
- Revisar el plan de iteración.
- Cuando esté listo para implementar: `/openup-start-iteration task_id: {task_id}`
```

## Producción

Devuelve un resumen de:
- ID de tarea (detectada automáticamente o proporcionada)
- Ruta del archivo del plan de iteración
- Ubicación de entrada de la hoja de ruta
- Nombre de la sucursal (si se creó)
- URL de relaciones públicas (si se creó)
- Resultados de la validación (si están validados)

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Colisión de ID de tarea | La identificación detectada automáticamente ya existe | Proporcione el argumento `task_id` explícito |
| Error de análisis de la hoja de ruta | Formato de hoja de ruta inesperado | Verifique que `docs/roadmap.md` siga el formato estándar |
| No se encontró ningún código relevante | La característica es completamente nueva | El plan tendrá un "estado actual" mínimo; se centrará en el "diseño propuesto" |
| Falló la generación del equipo | Equipos de agentes no habilitados | Establezca `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` para validación |
| La creación de relaciones públicas falló | No hay control remoto o gh no instalado | Utilice `create_pr: false` y cree PR manualmente |

## Referencias

- Planes de iteración: `docs/iteration-plans/`
- Hoja de ruta: `docs/roadmap.md`
- Estado del proyecto: `docs/project-status.md`
- Cuaderno de Arquitectura: `docs/architecture-notebook.md`

## Ver también

- [openup-start-iteration](../openup-start-iteration/SKILL.md) — Comience a implementar una tarea planificada
- [openup-create-iteration-plan](../openup-create-iteration-plan/SKILL.md) — Planificación de iteración genérica (nivel de fase)
- [openup-complete-task](../openup-complete-task/SKILL.md) — Marcar la tarea como completada después de la implementación
- [openup-create-pr](../openup-create-pr/SKILL.md) — Crea relaciones públicas con el contexto de la hoja de ruta
