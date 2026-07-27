# Assessments

Assessments collect evidence for mastery decisions. A percentage alone is not
enough: grade every objective against criterion-level evidence and keep failed
critical dimensions visible.

## Definition and attempt separation

The repository stores public assessment definitions:

- objectives and permitted resources;
- questions and alternate variants;
- criterion-level rubrics;
- passing evidence;
- misconception routes;
- reassessment timing.

The progress store keeps per-user attempts, submitted answers, hints, scores,
timestamps, due dates, and UI events. `maps/progress.md` contains only the
concise current checkpoint needed by another agent or device.

## Required contract

Assessment definitions use stable IDs and include:

- `track`, `lesson`, and objectives under test;
- a clear open-book or closed-resource policy;
- constructed-response, artifact, diagnosis, or transfer questions;
- rubric criteria for `explain`, `apply`, `diagnose`, and `transfer` as
  applicable;
- critical criteria that cannot be averaged away;
- passing rules and grading uncertainty handling;
- corrective routes keyed by failure cause;
- at least one reassessment variant.

`templates/assessment.json` is a complete machine-readable example. JSON keeps
the executable contract strict without adding a YAML parser dependency. Keep answer
keys and feedback in the definition, but the Web UI must withhold them until an
answer is submitted.

## Mastery decisions

- A submitted guided or independent task can support `practiced`.
- Passing the immediate assessment can support `provisional`.
- Scheduling delayed retrieval changes it to `review_due`.
- Only delayed retrieval or a transfer task meeting the rubric supports
  `retained`.

If a prompt or rubric is ambiguous, repair the assessment before grading it.
After correction, use a different variant; repeating the same answer does not
show transfer.
