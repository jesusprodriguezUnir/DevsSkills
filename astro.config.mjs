// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const isVercel = process.env.VERCEL === '1';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  site: isVercel
    ? 'https://devs-skills.vercel.app'
    : 'https://jesusprodriguezUnir.github.io',
  base: isVercel ? '/' : '/DevsSkills',
  integrations: [sitemap()],
  prefetch: { defaultStrategy: 'hover' },
});
