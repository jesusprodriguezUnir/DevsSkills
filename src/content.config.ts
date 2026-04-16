import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const skillsCollection = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/skills" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['Antigravity', 'Claude', 'VS Code', 'Opencode', '.NET Core', 'General']),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = {
  'skills': skillsCollection,
};
