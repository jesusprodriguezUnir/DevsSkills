---
name: skill-creator
description: Guía para crear o actualizar Agent Skills utilizando la especificación estandarizada SKILL.md, que incluye reglas de nomenclatura, campos frontales opcionales, validación, empaquetado y mejores prácticas para estructurar scripts, referencias y activos.
license: Apache-2.0
---

# Creador de habilidades

Esta habilidad proporciona un flujo de trabajo práctico y alineado con las especificaciones para crear y mantener habilidades de agente.

## Especificación (formato requerido)

### Estructura del directorio

Una habilidad es un directorio que contiene como mínimo un archivo `SKILL.md`:

```
skill-name/
└── SKILL.md
```

Directorios opcionales: `scripts/`, `references/` y `assets/`.

### SKILL.md frontmatter (obligatorio)

```
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Campos opcionales:

```
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
compatibility: Requires git, python3, and internet access
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

| Campo | Requerido | Restricciones |
| --------------- | -------- | ----------- |
| `nombre` | Sí | 1-64 caracteres; letras minúsculas, números, guiones; sin guiones iniciales, finales o consecutivos; debe coincidir con el directorio principal |
| `descripción` | Sí | 1-1024 caracteres; debe describir qué hace la habilidad y cuándo usarla |
| `licencia` | No | Nombre corto de la licencia o referencia al archivo de licencia incluido |
| `compatibilidad` | No | 1-500 caracteres; requisitos ambientales si es necesario |
| `metadatos` | No | Mapeo arbitrario de clave/valor |
| `herramientas-permitidas` | No | Lista delimitada por espacios de herramientas preaprobadas (experimental) |

#### reglas del campo `nombre`

- Debe tener entre 1 y 64 caracteres
- Solo letras minúsculas, dígitos y guiones (`a-z`, `0-9`, `-`)
- No debe comenzar ni terminar con `-`
- No debe contener `--`
- Debe coincidir con el nombre del directorio de habilidades.

Válido:

```
name: pdf-processing
name: data-analysis
name: code-review
```

Inválido:

```
name: PDF-Processing
name: -pdf
name: pdf--processing
```

#### reglas del campo `descripción`

- Debe tener entre 1 y 1024 caracteres
- Debe incluir tanto lo que hace la habilidad como cuándo usarla.
- Incluir palabras clave que ayuden a los agentes a enrutar tareas relevantes.

Bien:

```
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDFs, forms, or document extraction.
```

Pobre:

```
description: Helps with PDFs.
```

## Principios básicos

### Sea conciso

La ventana de contexto se comparte entre los mensajes del sistema, la conversación, los metadatos de habilidades y la entrada de tareas. Suponga que el agente es capaz y solo incluya información no obvia y de alto valor.

### Establecer grados de libertad apropiados

- **Alta libertad**: heurística y orientación para la toma de decisiones
- **Libertad media**: pseudocódigo o scripts con parámetros
- **Baja libertad**: guiones deterministas y secuencias estrictas

Utilice restricciones más estrictas cuando las tareas sean frágiles, propensas a errores o requieran una alta coherencia.

## Anatomía de una habilidad

Una habilidad incluye un `SKILL.md` requerido más recursos incluidos opcionales:

```
skill-name/
├── SKILL.md
├── scripts/        # Executable helpers
├── references/     # Docs loaded on demand
└── assets/         # Templates, images, data
```

### guiones/

Úselo para código repetible u operaciones frágiles que se benefician de la ejecución determinista.

### referencias/

Úselo para documentos grandes o detallados que deben cargarse solo según demanda (esquemas, documentos API, políticas).

### activos/

Úselo para recursos estáticos que se copian o reutilizan en resultados (plantillas, imágenes, fuentes, texto estándar).

### Qué no incluir

Evite documentos adicionales que no ayuden directamente a un agente a completar las tareas (README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.).

## Divulgación progresiva

1. **Metadatos** (nombre + descripción) siempre se carga
2. **SKILL.md body** se carga cuando se activa la habilidad
3. **Recursos** se cargan solo cuando sea necesario

Mantenga `SKILL.md` por debajo de 500 líneas. Mueva referencias profundas a `references/` y vincúlelas desde SKILL.md.

### Patrones

**Patrón 1: Guía de alto nivel con referencias**

```
# PDF Processing

## Inicio rápido

Extraer texto con pdfplomber:
[ejemplo de código]

## Funciones avanzadas

- Llenado de formularios: Ver referencias/FORMS.md
- Referencia de API: ver referencias/REFERENCE.md
- Ejemplos: Ver referencias/EJEMPLOS.md
```

**Patrón 2: organización de dominio específico**

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

**Patrón 3: Detalles condicionales**

```
# DOCX Processing

## Creando documentos

Utilice docx-js para documentos nuevos. Ver referencias/DOCX-JS.md.

## Editar documentos

Para ediciones simples, modifique el XML directamente.

Para cambios rastreados: referencias/REDLINING.md
Para obtener detalles sobre OOXML: referencias/OOXML.md
```

Pautas:

- Mantenga las referencias a un nivel de profundidad desde `SKILL.md`
- Agregar una tabla de contenido para archivos de referencia de más de ~100 líneas

## Proceso de creación de habilidades

1. Comprender la habilidad con ejemplos concretos
2. Planificar contenidos reutilizables (guiones, referencias, activos)
3. Inicializar una nueva habilidad
4. Edite SKILL.md y los recursos incluidos
5. Validar y empaquetar
6. Iterar según el uso real

### Paso 1: entender con ejemplos

Reúna las solicitudes de los usuarios representativos y aclare los casos extremos. Evite demasiadas preguntas por mensaje; Comience con las incógnitas de mayor impacto.

### Paso 2: Planificar contenidos reutilizables

Para cada ejemplo, identifique qué se debe programar, documentar o crear una plantilla. Convierta la lógica repetida en scripts o activos reutilizables.

### Paso 3: inicializa la habilidad

Utilice el script inicializador (de este directorio de habilidades):

```
./scripts/init_skill.py <skill-name> --path <output-directory>
```

El script crea una nueva carpeta de habilidades con una plantilla `SKILL.md` más directorios de ejemplo `scripts/`, `references/` y `assets/`. Elimine los ejemplos no utilizados.

### Paso 4: Editar la habilidad

Escriba instrucciones concisas y orientadas a la acción. Utilice lenguaje imperativo. Asegúrese de que el frontmatter coincida con la especificación y el nombre del directorio.

Consultar referencias si necesitas patrones:

- `referencias/flujos de trabajo.md`
- `referencias/patrones-de-salida.md`

### Paso 5: Validar

Validador preferido (biblioteca de referencia de especificaciones):

```
skills-ref validate ./my-skill
```

Validador local rápido (incluido con esta habilidad):

```
./scripts/quick_validate.py ./my-skill
```

### Paso 6: Paquete

```
./scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

El empaquetador valida primero y luego crea `<skill-name>.skill` (formato zip).

### Paso 7: Iterar

Ejecute la habilidad en tareas reales, observe fallas o fricciones y actualice SKILL.md o los recursos en consecuencia.

## Referencias de archivos

Utilice rutas relativas desde la raíz de la habilidad:

```
See references/REFERENCE.md for details.
Run scripts/extract.py for extraction.
```

Evite cadenas de referencia profundamente anidadas.
