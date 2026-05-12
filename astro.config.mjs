// @ts-check
import { defineConfig } from 'astro/config';

const isVercel = process.env.VERCEL === '1';

// https://astro.build/config
export default defineConfig({
  site: isVercel
    ? 'https://devs-skills.vercel.app'
    : 'https://jesusprodriguezUnir.github.io',
  base: isVercel ? '/' : '/DevsSkills',
});
