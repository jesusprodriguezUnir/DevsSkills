---
name: openup-shared-vision
description: Crea una visión técnica compartida para la alineación del equipo.
arguments:
  - name: technical_objectives
    description: Objetivos técnicos clave a abordar (separados por comas)
    required: false
  - name: scope_focus
    description: Área de enfoque para la definición de alcance DENTRO/FUERA
    required: false
---

#Visión Compartida

Esta habilidad crea un documento de visión técnica compartida que asegura la alineación entre los interesados ​​y el equipo de desarrollo sobre objetivos técnicos, alcance y decisiones clave.

## Cuándo usar

Usa esta habilidad cuando:
- El documento de visión existe pero necesita elaboración técnica.
- Necesites definir el alcance DENTRO/FUERA claramente
- Comienza la fase de Elaboración y necesitas alineación técnica.
- Los miembros del equipo tienen diferente comprensión de la dirección técnica.
- Necesidades documentales decisiones técnicas clave y restricciones

## Cuándo NO Usar

NO usa esta habilidad cuando:
- No existe documento de visión (usa `/openup-create-vision` primero)
- Estés en las fases de Construcción tardía o Transición (ya debería existir)
- Solo necesitas detalles de arquitectura (usa `/openup-create-architecture-notebook`)
- La visión ya está bien definida y comprendida

## Criterios de Éxito

Tras usar esta habilidad, verifica:
- [ ] Los objetivos técnicos están claramente documentados
- [ ] El alcance DENTRO/FUERA está bien definido
- [ ] Las suposiciones y restricciones técnicas están listadas
- [ ] Las decisiones técnicas clave tienen justificación
- [ ] Las preguntas abiertas están registradas para elaboración
- [ ] El documento está enlazado desde la visión principal

## Resumen del Proceso

1. Leer el documento de visión existente
2. Extraer el contexto y los objetivos técnicos
3. Definir el alcance DENTRO/FUERA
4. Documental suposiciones y restricciones técnicas
5. Registrador decisiones técnicas clave
6. Identificar preguntas abiertas

## Pasos Detallados

### 1. Leer la Visión Existente

Leer `docs/vision.md` para comprender:
- Planteamiento del problema del proyecto.
- Necesidades de los interesados
- Objetivos de negocio
- Estado actual del proyecto

### 2. Contexto Técnico Extraer

De la visión y el estado del proyecto, identifique:

**Objetivos Técnicos:**
- ¿Qué problemas técnicos necesitan resolverse?
- ¿Cuáles son los atributos de calidad clave (rendimiento, seguridad, escalabilidad)?
- ¿Qué criterios de éxito técnico existen?

**Si se proporciona `$ARGUMENTS[technical_objectives]`:**
- Centrarse en esos objetivos específicos
- Añadir objetivos técnicos relacionados

**Ejemplos:**
- "Lograr tiempos de respuesta inferiores a un segundo"
- "Soportar 10.000 usuarios concurrentes"
- "Garantizar cifrado de datos en reposo y en tránsito"

### 3. Definir Alcance DENTRO/FUERA

Crear límites claros de lo que se incluye y lo que se excluye:

**DENTRO del Alcance:**
¿Qué funcionalidades y capacidades están definitivamente incluidas?
- Usar `$ARGUMENTS[scope_focus]` como punto de partida si se proporciona
- Listar funcionalidades, capacidades y tecnologías específicas
- Ser específico sobre lo que significa "dentro del alcance"

**FUERA del Alcance:**
¿Qué se excluye exclusivamente para gestionar las expectativas?
- Funcionalidades que específicamente NO se van a construir
- Tecnologías que no se utilizarán
- Capacidades que están fuera del alcance de este proyecto

### 4. Documental Suposiciones Técnicas

Suposiciones del registrador sobre el entorno técnico:

| Suposición | Impacto | Validado Por |
|------------|---------|--------------|
| Ejemplo: PostgreSQL disponible | Bajo - afecta capa de datos | Administrador de bases de datos |
| Ejemplo: Usuarios en navegadores modernos | Medio - afecta frontend | Investigación UX |

### 5. Documental Restricciones Técnicas

Registrar restricciones conocidas que limitan las opciones:

| Restricción | Descripción | Mitigación |
|-------------|-------------|------------|
| Ejemplo: Presupuesto para servicios en la nube | Debe usar soluciones rentables | Arquitectura sin servidor |
| Ejemplo: Integración con sistema legado | Debe funcionar con API existentes | Patrón adaptador |

### 6. Decisiones del Registrador Técnicas Clave

Documentar decisiones técnicas significativas con justificación:

**Ejemplos:**
- Elección del lenguaje de programación
- Estilo arquitectónico (microservicios vs monolito)
- Selección de base de datos
- Enfoque de despliegue

Para cada decisión:
- Qué se decidió
- Por qué (justificación)
- Alternativas consideradas
- Compromisos aceptados

### 7. Identificar Preguntas Abiertas

Listar preguntas que necesitan respuesta durante la elaboración:

| Pregunta | Impacto | Fase Objetivo |
|----------|---------|---------------|
| Ejemplo: ¿Cómo gestionar el modo sin conexión? | Alto - afecta la arquitectura | Elaboración |
| Ejemplo: ¿Límites de la API de terceros? | Medio - afecta el diseño | Elaboración |

### 8. Crear Documento de Visión Compartida

Crear `docs/shared-vision.md` usando la plantilla de visión compartida con:
- Tabla de objetivos técnicos
- Secciones de alcance DENTRO/FUERA
- Tablas de suposiciones y restricciones
- Decisiones técnicas clave
- Preguntas abiertas

### 9. Enlázar desde la Visión Principal

Añadir una referencia en `docs/vision.md`:
```rebaja
##Visión Técnica

Consulta la [Visión Compartida](shared-vision.md) para objetivos técnicos detallados, alcance y decisiones.
```

##Salida

Devuelve un resumen de:
- Documento de visión compartido creado en `docs/shared-vision.md`
- Objetivos técnicos documentados
- Alcance DENTRO/FUERA definido
- Decisiones claves registradas
- Preguntas abiertas identificadas

## Ejemplo de uso

```
/openup-shared-vision technical_objectives: "escalabilidad, seguridad" scope_focus: "autenticación de usuarios"
```

## Errores Comunes

| Error | causa | Solución |
|-------|-------|----------|
| Visión no encontrada | docs/vision.md no existe | Crear primero la visión con /openup-create-vision |
| Demasiado vago | Objetivos no suficientemente específicos | Añadir criterios medicinales |
| Falta alcance FUERA | Solo se definió el alcance DENTRO | Definir siempre ambos DENTRO y FUERA |
| Sin justificación | Decisiones sin fundamento | Añadir el porqué y las alternativas consideradas |

## Referencias

- Plantilla de Visión Compartida: `docs-eng-process/templates/shared-vision.md`
- Plantilla de Visión: `docs-eng-process/templates/vision.md`
- Plantilla de Cuaderno de Arquitectura: `docs-eng-process/templates/architecture-notebook.md`

## Ver También

- [openup-create-vision](../create-vision/SKILL.md) - Crear primero la visión del proyecto
- [openup-create-architecture-notebook](../create-architecture-notebook/SKILL.md) - Crear documentación de arquitectura detallada
- [openup-elaboration](../../openup-phases/elaboration/SKILL.md) - Actividades de la fase de Elaboración
