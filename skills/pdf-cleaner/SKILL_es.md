---
name: pdf-cleaner
description: Skill para procesar cuadernillos en PDF, eliminando marcas de agua o texto de "Rubio", agregando una marca registrada personalizada y organizando los resultados por carpetas. Útil para limpieza de materiales históricos y rebranding.
license: Private
compatibility: Requiere Node.js 18+, pdf-lib y fs-extra.
---

# Limpiador de PDF

Esta habilidad permite realizar un procesamiento por lotes de archivos PDF dentro de la solución para adecuarlos a la nueva marca "Caligrafía Mágica".

## Capacidades

1. **Detección de PDFs**: Escanea `public/recursos` y `public/pdfs`.
2. **Limpieza de Marca**: Cubre áreas de texto relacionadas con "Rubio".
3. **Marcas de agua**: Agregue "Caligrafía Mágica ®" en cada página.
4. **Organización**: Clasifica cada salida en `public/processed/[nombre-original]/`.

## Guiones

- `scripts/process-pdfs.ts`: El motor principal de procesamiento.

##Manual de uso

```bash
# Para ejecutar desde la raíz
npx ts-node .agent/skills/pdf-cleaner/scripts/process-pdfs.ts
```

## Configuración

- **Texto de Marca**: Editar `process-pdfs.ts` para cambiar el texto decorativo.
- **Áreas de Redacción**: Por defecto, se aplican máscaras en la parte superior e inferior de las páginas si se detecta texto específico o se configura como patrón fijo.
