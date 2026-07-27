import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// These schemas validate presentation projections for the standalone example.
// Canonical repository definitions remain richer; see references/web-ui.md for
// the required build-time transformation boundary.
const assignments = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/assignments' }),
  schema: z.object({
    id: z.string(),
    lessonId: z.string(),
    mode: z.enum(['guided', 'faded', 'independent', 'transfer']),
    title: z.string(),
    prompt: z.string(),
    steps: z.array(z.string()).optional(),
    hint: z.string().optional(),
    success: z.string(),
    constraints: z.array(z.string()),
    artifact: z.string(),
    answerPlaceholder: z.string().optional(),
  }),
});

const assessments = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/assessments' }),
  schema: z.object({
    id: z.string(),
    lessonId: z.string(),
    resourcePolicy: z.string(),
    questions: z.array(
      z.object({
        id: z.string(),
        prompt: z.string(),
        criterion: z.string(),
      }),
    ),
    passingEvidence: z.string(),
    correction: z.array(
      z.object({
        cause: z.string(),
        signal: z.string(),
        action: z.string(),
      }),
    ),
  }),
});

const lessons = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/lessons' }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    eyebrow: z.string(),
    summary: z.string(),
    estimatedMinutes: z.number().int().positive(),
    track: z.string(),
    order: z.number().int().positive(),
    prerequisite: z.string(),
    objective: z.string(),
    explanation: z.array(
      z.object({
        title: z.string(),
        body: z.string(),
      }),
    ),
    mentalModel: z.object({
      title: z.string(),
      steps: z.array(
        z.object({
          label: z.string(),
          name: z.string(),
          description: z.string(),
          transition: z.string().optional(),
        }),
      ),
    }),
    misconception: z.object({
      title: z.string(),
      body: z.string(),
    }),
    recallCheck: z.object({
      prompt: z.string(),
      answer: z.string(),
    }),
    workedExample: z.object({
      title: z.string(),
      scenario: z.string(),
      steps: z.array(
        z.object({
          action: z.string(),
          reasoning: z.string(),
        }),
      ),
      conclusion: z.string(),
    }),
    completionLabels: z.object({
      explanation: z.string(),
      workedExample: z.string(),
      guidedTask: z.string(),
      independentTask: z.string(),
      assessment: z.string(),
    }),
    guidedAssignmentId: z.string(),
    independentAssignmentId: z.string(),
    assessmentId: z.string(),
  }),
});

export const collections = { assignments, assessments, lessons };
