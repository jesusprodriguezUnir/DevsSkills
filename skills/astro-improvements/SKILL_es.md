# Mejoras en Astro

Skill para auditar una aplicación Astro, detectar antipatrones en cuatro dimensiones y producir un informe priorizado con recetas concretas de refactorización con ejemplos Antes/Después.

## Cuándo Usar

- Antes de un lanzamiento a producción para detectar regresiones
- Cuando salten alertas de presupuesto de rendimiento (LCP, CLS, tamaño de bundle)
- Al incorporarse a una codebase Astro desconocida
- Tras migrar de SSG a SSR (o viceversa)
- Sospecha de over-hydration o JavaScript innecesario en el cliente
- Auditoría rutinaria de accesibilidad o SEO

## Dimensiones

| Dimensión | Peso | Foco |
|-----------|------|------|
| ⚡ **Performance & Islands** | 30% | Directivas `client:*`, coste de hidratación, `<Image>`, prefetch, tamaño de bundle |
| 🏗️ **Architecture & Structure** | 25% | Layouts, content collections, routing, SSR vs SSG, `astro.config.mjs` |
| 🔍 **SEO, Accesibilidad y Meta** | 25% | HTML semántico, ARIA, sitemap, robots, Open Graph, atributo `lang`, headings |
| 🛠️ **DX, TypeScript y Calidad** | 20% | `tsconfig`, tipos de env, interfaces `Props`, linting, `astro check` en CI |

## Proceso

### Paso 1: Inventario

Leer en este orden:
- `astro.config.mjs` — modo de salida (SSG/SSR/hybrid), integraciones, adaptadores
- `package.json` — versión de Astro, integraciones de framework, herramientas de bundle
- Árbol de `src/` — layouts, páginas, componentes, content, middleware
- `public/` — assets estáticos que no pasan por el pipeline de Astro

Verificar:
```
✅ El modo de salida es explícito e intencionado
✅ Solo están listadas las integraciones necesarias
⚠️ Mezcla de .astro y componentes de framework (React/Vue) sin límite claro
❌ No se encuentra astro.config.mjs → no es posible continuar con fiabilidad
```

### Paso 2: Mapear hallazgos a dimensiones

Por cada archivo o patrón detectado, asignarlo a una de las cuatro dimensiones e indicar la ruta relevante (`src/components/Card.astro:12`).

### Paso 3: Puntuar severidad

| Severidad | Criterio |
|-----------|----------|
| 🔴 **Crítico** | Bloquea la indexación SEO, rompe la accesibilidad para tecnologías asistivas, o envía más de 100 KB de JS innecesario a cada visitante |
| 🟡 **Mayor** | Degrada Core Web Vitals, genera arquitectura confusa o causa fricción de DX en cada funcionalidad |
| 🟢 **Menor** | Problema de pulido — mejora medible pero sin impacto inmediato |

### Paso 4: Proponer refactorizaciones

Para cada hallazgo 🔴 Crítico y 🟡 Mayor, proporcionar un fragmento Antes/Después. Para los hallazgos 🟢 Menores basta una corrección de una línea.

### Paso 5: Emitir informe

Usar la [Plantilla de Informe](#plantilla-de-informe) al final de esta skill.

---

## Catálogo de Mejoras

### ⚡ Performance & Islands

#### `client:load` usado en contenido estático — 🔴 Crítico

Cada `client:load` envía el bundle completo del framework al navegador antes de que la página sea interactiva. Reservarlo para componentes que realmente necesiten APIs del navegador al cargar.

```astro
<!-- ❌ Antes — envía el bundle de React aunque Card sea HTML puro -->
<Card client:load title="Hola" />

<!-- ✅ Después — sin directiva: se renderiza a HTML estático en build time -->
<Card title="Hola" />

<!-- ✅ Después — interactivo solo cuando entra en el viewport -->
<Counter client:visible initialCount={0} />
```

**Corrección:** Auditar cada directiva `client:*`. Usar `client:visible` para interactividad bajo el pliegue, `client:idle` para widgets de baja prioridad, y ninguna directiva para componentes completamente estáticos.

---

#### `<img>` sin `<Image>` — 🟡 Mayor

El componente `<Image>` de Astro genera `srcset` responsive, convierte a WebP/AVIF y añade ancho/alto para evitar layout shift. Las etiquetas `<img>` normales omiten todo esto.

```astro
<!-- ❌ Antes -->
<img src="/hero.jpg" alt="Hero" />

<!-- ✅ Después -->
---
import { Image } from 'astro:assets';
import heroImg from '../assets/hero.jpg';
---
<Image src={heroImg} alt="Hero" width={1200} height={600} />
```

**Corrección:** Reemplazar `<img src="...">` por `<Image>` en todas las imágenes locales y remotas. Configurar `image.remotePatterns` en `astro.config.mjs` para fuentes externas.

---

#### Sin estrategia de prefetch — 🟢 Menor

Astro soporta prefetching automático de enlaces con una sola línea de configuración. Sin él, las navegaciones se sienten más lentas de lo necesario en sitios multipágina.

```js
// ❌ Antes — astro.config.mjs sin configuración de prefetch
export default defineConfig({ ... });

// ✅ Después — prefetch al pasar el cursor, opt-out por enlace con data-astro-prefetch="false"
export default defineConfig({
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' }
});
```

**Corrección:** Añadir configuración de `prefetch` a `astro.config.mjs`. Usar `prefetchAll: true` solo en sitios pequeños con pocas páginas.

---

### 🏗️ Architecture & Structure

#### Lógica en el front matter en lugar de Content Collections — 🔴 Crítico

Incrustar arrays de datos o lógica de fetch directamente en el front matter de páginas `.astro` elimina la seguridad de tipos y hace el contenido no consultable.

```astro
<!-- ❌ Antes — datos hardcodeados en el front matter de la página -->
---
const posts = [
  { title: 'Post 1', date: '2024-01-01', slug: 'post-1' },
  { title: 'Post 2', date: '2024-02-01', slug: 'post-2' },
];
---

<!-- ✅ Después — definir una colección con schema -->
```

```ts
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

export const collections = {
  blog: defineCollection({
    schema: z.object({ title: z.string(), date: z.coerce.date() }),
  }),
};
```

```astro
<!-- src/pages/blog/index.astro -->
---
import { getCollection } from 'astro:content';
const posts = await getCollection('blog');
---
```

**Corrección:** Mover los datos repetidos a `src/content/{coleccion}/` con un schema Zod en `src/content/config.ts`. Usar `getCollection()` para consultar con inferencia completa de TypeScript.

---

#### Layouts duplicados — 🟡 Mayor

El boilerplate de `<html>`, `<head>` y `<body>` copiado entre páginas hace que los cambios globales (cabeceras CSP, fuentes, analytics) sean propensos a errores.

```astro
<!-- ❌ Antes — el mismo <head> repetido en cada página -->
<html lang="es">
  <head><title>...</title><link rel="stylesheet" .../></head>
  <body>...</body>
</html>

<!-- ✅ Después — un único componente Layout -->
---
import Layout from '../layouts/Layout.astro';
---
<Layout title="Inicio">
  <main>...</main>
</Layout>
```

**Corrección:** Extraer un `src/layouts/Layout.astro` que sea propietario de `<html>`, `<head>` y los estilos globales. Pasar `title` y `description` como props.

---

#### Integraciones sin uso en `astro.config.mjs` — 🟢 Menor

Cada integración registrada se ejecuta en build time. Las integraciones sobrantes de experimentos aumentan el tiempo de build y pueden introducir transformaciones inesperadas.

```js
// ❌ Antes — @astrojs/react listado pero sin archivos .jsx/.tsx
import react from '@astrojs/react';
export default defineConfig({ integrations: [react()] });

// ✅ Después — solo las integraciones realmente en uso
export default defineConfig({ integrations: [sitemap()] });
```

**Corrección:** Cruzar las `integrations` con `src/` — si ningún archivo de componentes usa un framework, eliminar su integración y su paquete.

---

### 🔍 SEO, Accesibilidad y Meta

#### Falta el atributo `lang` en `<html>` — 🔴 Crítico

Los lectores de pantalla y los motores de búsqueda necesitan `lang` para interpretar el contenido correctamente. Su ausencia es un fallo WCAG 2.1 Nivel A.

```astro
<!-- ❌ Antes -->
<html>

<!-- ✅ Después -->
<html lang="es">
```

**Corrección:** Añadir `lang` al `<html>` raíz en cada layout. Aceptarlo como prop (`lang = 'es'`) en sitios multilingüe.

---

#### Falta Open Graph y meta description — 🟡 Mayor

Las páginas sin `og:title`, `og:description` y `description` aparecen como URLs desnudas cuando se comparten en redes sociales y posicionan peor en búsquedas.

```astro
<!-- ❌ Antes — Layout.astro head solo con <title> -->
<head>
  <title>{title}</title>
</head>

<!-- ✅ Después -->
<head>
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:type" content="website" />
  <meta property="og:image" content={new URL(ogImage, Astro.url)} />
</head>
```

**Corrección:** Añadir un componente `<SEO>` o extender las props del Layout para aceptar `description` e `ogImage`. Hacer `description` obligatorio vía TypeScript.

---

#### Niveles de heading saltados — 🟡 Mayor

Saltar de `<h1>` a `<h3>` rompe el esquema del documento que usan los lectores de pantalla y degrada la estructura de headings para SEO.

```astro
<!-- ❌ Antes -->
<h1>Blog</h1>
<h3>Últimas entradas</h3>  <!-- falta h2 -->

<!-- ✅ Después -->
<h1>Blog</h1>
<h2>Últimas entradas</h2>
<h3>{post.title}</h3>
```

**Corrección:** Aplicar un solo `<h1>` por página y niveles secuenciales. Usar el panel de Accesibilidad de DevTools o axe para auditar el árbol de headings.

---

### 🛠️ DX, TypeScript y Calidad

#### `strict: false` en `tsconfig.json` — 🔴 Crítico

Deshabilitar el modo estricto oculta errores de `null`/`undefined`, tipos `any` implícitos y parámetros de función sin verificar — fuentes habituales de errores en runtime en componentes Astro.

```jsonc
// ❌ Antes
{ "extends": "astro/tsconfigs/base", "compilerOptions": { "strict": false } }

// ✅ Después — usar el preset más estricto que incluye Astro
{ "extends": "astro/tsconfigs/strictest" }
```

**Corrección:** Reemplazar por `astro/tsconfigs/strictest` (o como mínimo `astro/tsconfigs/strict`). Corregir los errores de tipo resultantes antes de activarlo — no suprimir con `// @ts-ignore`.

---

#### `import.meta.env` sin declaraciones de tipos — 🟡 Mayor

Acceder a variables de entorno personalizadas sin un `env.d.ts` hace que TypeScript las trate como `any`, ocultando errores tipográficos en los nombres de variable.

```ts
// ❌ Antes — sin env.d.ts, el IDE no tiene autocompletado
const key = import.meta.env.PUBLIC_API_KEY; // tipo: any

// ✅ Después — src/env.d.ts
/// <reference types="astro/client" />
interface ImportMetaEnv {
  readonly PUBLIC_API_KEY: string;
  readonly SECRET_DB_URL: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

**Corrección:** Crear `src/env.d.ts` con declaraciones tipadas para cada variable de entorno. Añadir una verificación en CI que falle si las variables de `.env.example` no están en `env.d.ts`.

---

#### Componentes sin interfaz `Props` — 🟢 Menor

Las props sin tipos impiden el autocompletado del IDE y permiten que los consumidores pasen valores incorrectos sin advertencia.

```astro
<!-- ❌ Antes — sin tipos de props -->
---
const { title, count } = Astro.props;
---

<!-- ✅ Después -->
---
interface Props {
  title: string;
  count?: number;
}
const { title, count = 0 } = Astro.props;
---
```

**Corrección:** Añadir un bloque `interface Props` a cada componente `.astro` que acepte props. Usar `astro check` (ver más abajo) para detectar violaciones.

---

## Plantilla de Informe

````markdown
# Mejoras en Astro — {nombre del proyecto}

## 📊 Puntuación Global: {X}/100

| Dimensión | Puntuación | Estado |
|-----------|-----------|--------|
| ⚡ Performance & Islands | {X}/30 | {✅ ⚠️ ❌} |
| 🏗️ Architecture & Structure | {X}/25 | {✅ ⚠️ ❌} |
| 🔍 SEO, Accesibilidad y Meta | {X}/25 | {✅ ⚠️ ❌} |
| 🛠️ DX, TypeScript y Calidad | {X}/20 | {✅ ⚠️ ❌} |

## Veredicto

{🟢 LISTO PARA PRODUCCIÓN | 🟡 LISTO CON CORRECCIONES MENORES | 🔴 REQUIERE TRABAJO ANTES DE PRODUCCIÓN}

## Hallazgos

| # | Severidad | Dimensión | Ubicación | Esfuerzo |
|---|-----------|-----------|-----------|---------|
| 1 | 🔴 Crítico | Performance | `src/components/Hero.astro:8` | S |
| 2 | 🟡 Mayor | Architecture | `src/pages/blog/index.astro:3–18` | M |

## Hallazgos Detallados

### Hallazgo 1 — {título}
**Archivo:** `src/...`  
**Por qué importa:** ...  
**Antes:**
```astro
...
```
**Después:**
```astro
...
```

## Plan de Acción — Top 5

1. [ ] {Corrección de mayor impacto — enlace al hallazgo}
2. [ ] ...
3. [ ] ...
4. [ ] ...
5. [ ] ...

## Checklist

- [ ] Sin `client:load` en componentes puramente estáticos
- [ ] Todas las etiquetas `<img>` reemplazadas por `<Image>`
- [ ] Las integraciones de `astro.config.mjs` coinciden con el uso real
- [ ] Cada layout tiene `lang` en `<html>`
- [ ] `og:title`, `og:description` y `description` presentes en todas las páginas
- [ ] Sin niveles de heading saltados
- [ ] `tsconfig.json` extiende `astro/tsconfigs/strictest`
- [ ] `src/env.d.ts` tipifica todas las variables de `import.meta.env`
- [ ] Todos los componentes tienen una interfaz `Props`
- [ ] `astro check` se ejecuta en CI sin errores
````

## Heurísticas y Quick Wins

- Si `client:load` está en un componente sin event handlers ni llamadas a APIs del navegador → eliminar la directiva por completo.
- Si el output de `astro.config.mjs` es `'server'` pero cada página carece de datos dinámicos → cambiar a `'static'` y eliminar el adaptador.
- Si `@astrojs/sitemap` no está presente y el sitio es SSG → añadirlo; los motores de búsqueda no descubrirán automáticamente todas las páginas.
- Si una página tiene dos o más etiquetas `<h1>` → refactorizar para que solo el título de página use `<h1>`.
- Si `astro check` no está en el pipeline de CI → añadirlo antes del paso de build; detecta errores de tipo que TypeScript solo no detecta en archivos `.astro`.
