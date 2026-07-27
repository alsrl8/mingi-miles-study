# Web UI Reference

## Contents

1. Purpose and boundary
2. Start from the template
3. Content architecture
4. Progress contract
5. Cross-device Supabase extension
6. GitHub Pages preparation
7. Validation

## Purpose and boundary

Build the UI around the next learning action, not around a document browser.
The dashboard should show the current track, verified learning state, next task,
review due date, and one clear resume action. A lesson should preserve this
order:

```text
explanation -> worked example -> guided task -> independent task
-> closed-resource assessment -> corrective route -> delayed review
```

The bundled example is a static Astro application. Its browser-local progress
adapter exists only to demonstrate the interaction model during development.
It does not synchronize devices, authenticate a learner, prove assessment
quality, or update `maps/progress.md`.

## Start from the template

Copy `assets/web-ui-template/` into a Web application directory, then run:

```bash
npm install
npm run dev
npm run build
```

The template uses the current Astro content collection pattern:
`src/content.config.ts`, `defineCollection()`, and the `glob()` loader. Its
standalone fixtures are presentation projections of the richer repository
contracts. They keep lessons, assignments, and assessments in separate
collections joined by stable IDs.
When integrating the template into this repository, replace the fixtures
through a build-time content adapter rather than maintaining a second
hand-authored curriculum.

The adapter validates canonical definitions first, then projects display fields
such as titles, prompts, steps, and learner-visible criteria. It must retain
canonical-only fields—including allowed resources, complete rubrics, answer
keys, corrective routes, reassessment variants, and review schedules—for
grading and progress workflows even when a page does not render them. The Web
schema is intentionally not an authoring contract.

The important template files are:

| Path | Responsibility |
| --- | --- |
| `src/content.config.ts` | Validates lesson, assignment, and assessment fixtures |
| `src/content/lessons/` | Standalone lesson fixture with stable references |
| `src/content/assignments/` | Guided and independent assignment fixtures |
| `src/content/assessments/` | Assessment and corrective-route fixture |
| `src/data/checkpoint.json` | Explicit active lesson and evidence-free starting state |
| `src/pages/index.astro` | Next-action dashboard |
| `src/pages/lessons/[id].astro` | Complete learning loop |
| `src/lib/progress.ts` | Adapter contract and development-only local implementation |
| `src/lib/active-progress.ts` | Single binding to replace with an authenticated adapter |
| `src/styles/global.css` | Responsive visual system |

Keep durable concept content in the repository. Do not turn UI component files
into a second curriculum source of truth.

## Content architecture

Use three boundaries:

1. Git stores public curriculum, lessons, assignments, assessments, and rubrics.
2. A progress store records learner-specific attempts, evidence, and due dates.
3. `maps/progress.md` is an agent-readable checkpoint generated from verified
   evidence at a meaningful stopping point.

Render content statically where possible. Add client JavaScript only for
learner interactions such as progress toggles, answer drafting, sign-in, and
attempt submission. Keep assessment answers hidden until the learner has
produced a response.

Do not equate a completed checkbox with mastery. A checkbox is navigation state.
Mastery state changes require the evidence defined in `learning-model.md`.

## Progress contract

Keep navigation state and mastery evidence separate. The development adapter
implements only navigation state:

```ts
interface NavigationProgressAdapter {
  read(lessonId: string): ProgressResult;
  setStage(
    lessonId: string,
    stage: LessonStage,
    complete: boolean,
  ): ProgressResult;
  reset(lessonId: string): ProgressResult;
}
```

An authenticated evidence adapter adds asynchronous attempt and review
operations:

```ts
interface EvidenceProgressAdapter {
  saveAttempt(input: AttemptInput): Promise<Attempt>;
  getDueReviews(): Promise<ReviewDue[]>;
}
```

Store criterion-level evidence rather than only one score. A useful minimum
record contains:

- authenticated learner ID;
- lesson and assessment IDs;
- attempt number and timestamps;
- submitted answer or artifact reference;
- result for explain, apply, diagnose, and transfer;
- hints used;
- grading confidence and uncertainty;
- corrective route;
- next review due date.

The local adapter stores a versioned map keyed by lesson ID under one
`localStorage` key. It keeps only stage checkboxes and timestamps. It does not
persist draft answers because a public/shared browser is not an appropriate
durable evidence store. When storage is blocked, it keeps in-memory state for
the current tab and displays a warning.

## Cross-device Supabase extension

Use Supabase Auth to identify the learner and Postgres with Row Level Security
to isolate progress. GitHub OAuth is a suitable sign-in option for this
repository. Configure the OAuth application and callback in the Supabase and
GitHub dashboards; do not commit OAuth secrets.

Only expose the project URL and publishable key to browser code. Never place a
service-role key in Astro `PUBLIC_` variables, built assets, repository files,
or GitHub Pages configuration. The template ignores `.env` and `.env.*` while
allowing a reviewed `.env.example`.

A minimal table and authorization policy are:

```sql
create table public.learning_attempts (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  lesson_id text not null,
  assessment_id text not null,
  attempt_number integer not null check (attempt_number > 0),
  evidence jsonb not null,
  mastery_state text not null check (
    mastery_state in (
      'learning', 'practiced', 'provisional', 'review_due', 'retained'
    )
  ),
  corrective_route text,
  review_due_at timestamptz,
  created_at timestamptz not null default now(),
  unique (user_id, assessment_id, attempt_number)
);

alter table public.learning_attempts enable row level security;

create policy "Learners read their own attempts"
on public.learning_attempts
for select
to authenticated
using ((select auth.uid()) = user_id);

create policy "Learners create their own attempts"
on public.learning_attempts
for insert
to authenticated
with check ((select auth.uid()) = user_id);

create policy "Learners update their own attempts"
on public.learning_attempts
for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);
```

Add a delete policy only if the product explicitly supports deletion. Enable
RLS on every table exposed through the Data API. Test with two separate
non-admin accounts and confirm that neither can read or mutate the other's
rows.

Implement the remote adapter only after Auth works:

1. Install `@supabase/supabase-js`.
2. Create the browser client from `PUBLIC_SUPABASE_URL` and
   `PUBLIC_SUPABASE_PUBLISHABLE_KEY`.
3. Call `signInWithOAuth({ provider: 'github' })`.
4. Wait for an authenticated session before reading or writing progress.
5. Insert rows with `user_id` equal to the authenticated user ID.
6. Let RLS authorize every request; never rely on a hidden UI control.
7. Implement `NavigationProgressAdapter` and switch the one binding in
   `src/lib/active-progress.ts`; do not spread backend selection through
   components.
8. Derive the concise Git checkpoint through a reviewed server or agent
   workflow. Browser events must not directly overwrite the source-of-truth
   checkpoint.

Official references:

- [Astro content collections](https://docs.astro.build/en/guides/content-collections/)
- [Astro GitHub Pages deployment](https://docs.astro.build/en/guides/deploy/github/)
- [Supabase GitHub login](https://supabase.com/docs/guides/auth/social-login/auth-github)
- [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)

## GitHub Pages preparation

GitHub Pages can host the static build through Astro's official GitHub Action.
When the repository owner chooses to enable deployment:

1. Set `site` to the final Pages origin in `astro.config.mjs`.
2. Set `ASTRO_BASE=/mingi-miles-study` or a matching `base` value when deploying
   under a repository subpath. The template builds internal URLs through
   `src/lib/urls.ts`.
3. Add a workflow using the current `withastro/action` version from Astro's
   deployment guide.
4. Commit `package-lock.json` so the Action detects npm.
5. Configure GitHub Pages to use GitHub Actions.
6. Add the production origin to Supabase Auth's allowed redirect URLs before
   enabling GitHub login.

These are owner-controlled production changes. The bundled template does not
include a deployment workflow, live origin, Supabase project, credentials, or
Pages activation.

## Validation

Run the checks from the copied template directory:

```bash
npm ci
npm run check
npm run build
ASTRO_BASE=/mingi-miles-study npm run build
```

Then inspect the generated site at mobile and desktop widths. Confirm:

- dashboard and lesson routes build;
- every lesson has all learning-loop stages;
- content schema rejects incomplete entries;
- assessment criteria stay hidden until an answer is submitted;
- local progress is explicitly labeled browser-only;
- no secret, service-role value, private learning data, placeholder, or
  production URL is present;
- keyboard focus, form labels, semantic headings, and reduced-motion behavior
  remain usable.
