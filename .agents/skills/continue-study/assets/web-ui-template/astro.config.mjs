import { defineConfig } from 'astro/config';

const base = process.env.ASTRO_BASE;

export default defineConfig({
  output: 'static',
  ...(base ? { base } : {}),
});
