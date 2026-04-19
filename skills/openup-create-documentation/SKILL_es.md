---
name: openup-create-documentation
description: Genera documentación legible para humanos a partir de código y artefactos
arguments:
  - name: doc_type
    description: Tipo de documentación (guia-usuario, referencia-api, solucion-problemas, tutorial)
    required: true
  - name: feature
    description: Funcionalidad o componente a documentar
    required: true
  - name: output_path
    description: Ruta de salida para la documentación (opcional, por defecto docs/user-guides/)
    required: false
---

# Crear Documentación

Genera documentación legible para humanos a partir de casos de uso, código y artefactos.

##Proceso

### 1. Determinar tipo de documentación

Según `$ARGUMENTS[doc_type]`:

| tipo_doc | Plantilla | Propósito |
|----------|-----------|-----------|
| guia-usuario | plantilla-guía-usuario.md | Documentación para el usuario final |
| referencia-api | plantilla-referencia-api.md | Documentación de la API |
| solucion-problemas | (generada) | Problemas comunes y soluciones |
| tutorial | (generada) | Aprendizaje paso a paso |

### 2. Material Recopilar Fuente

Lea las fuentes relevantes para la funcionalidad: casos de uso (`docs/use-cases/`), casos de prueba (`docs/test-cases/`), documentos de diseño (`docs/design/`) y código fuente (`src/`). Adaptar las fuentes según el tipo de documentación.

### 3. Generar Documentación

Consultar los archivos específicos por tipo para el proceso detallado de generación:
- [guía-usuario.md](./guía-usuario.md)
- [api-referencia.md](./api-referencia.md)
- [solución de problemas.md](./solución de problemas.md)
- [tutorial.md](./tutorial.md)

### 4. Validar y Revisar

- Verificar que todos los ejemplos son correctos
- Probar los ejemplos de código si aplica
- Comprobar las referencias cruzadas
- Asegurar la claridad para el público objetivo.

### 5. Crear Archivo de Documentación

- Ruta por defecto: `docs/user-guides/<funcionalidad>-<tipo_doc>.md`
- Ruta personalizada: Usar `$ARGUMENTS[output_path]` si se proporciona
- Enlazar documentación relacionada

## Ejemplo de uso

```
/openup-create-documentation doc_type: guia-usuario feature: autenticacion-usuarios
/openup-create-documentation doc_type: referencia-api feature: api-pagos output_path: docs/api/
```

## Errores Comunes

| Error | causa | Solución |
|-------|-------|----------|
| Caso de uso no encontrado | La funcionalidad carece de casos de uso | Crear primero los casos de uso |
| Código no encontrado | La funcionalidad no está implementada | Verificar el nombre y estado de la funcionalidad |
| Plantilla no disponible | La plantilla no está disponible | Usar estructura genérica |

## Referencias

- Plantilla de Guía de Usuario: `docs-eng-process/templates/user-guide-template.md`
- Plantilla de Referencia de API: `docs-eng-process/templates/api-reference-template.md`

## Ver También

- [openup-create-use-case](../create-use-case/SKILL.md) - Crear primero los casos de uso
- [openup-detail-use-case](../detail-use-case/SKILL.md) - Detallar casos de uso para mejor documentación
