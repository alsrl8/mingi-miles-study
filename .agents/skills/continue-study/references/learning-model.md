# Learning Model

## Contents

1. Source-of-truth model
2. Curriculum graph
3. Learning-unit contract
4. Assignment contract
5. Assessment contract
6. Mastery states
7. Corrective loop
8. Review scheduling
9. Progress checkpoint
10. Agent decision rules

## Source-of-truth model

Keep each fact in one canonical layer:

| Layer | Canonical content |
| --- | --- |
| `topics/` | Durable concept explanations |
| `curriculum/` | Tracks, goals, order, and prerequisites |
| `lessons/` | Teachable units referencing concepts |
| `assignments/` | Guided, independent, and transfer work |
| `assessments/` | Questions, rubrics, variants, and corrective routing |
| `inbox/` | Chronological observations and learning logs |
| `reviews/` | Retrieval questions and dated reflection |
| `maps/progress.md` | Current agent-readable checkpoint |
| Progress store | Detailed attempts, scores, due dates, and UI events |

Link to canonical material instead of copying it into another layer.

## Curriculum graph

Model a track as a directed acyclic graph:

- one practical goal;
- foundation concepts;
- explicit prerequisites;
- one or more observable objectives per concept;
- evidence required to advance;
- a final task that transfers learning to a new situation.

Sequence by dependency, not by document creation time. Allow an override only
when Miles explicitly chooses it; record the skipped prerequisite and expected
risk.

Example foundation path for Git synchronization:

```text
working tree
  -> staging and commits
  -> local and remote branches
  -> fetch and rebase
  -> conflict resolution
  -> safe cross-device synchronization
```

## Learning-unit contract

Every lesson contains:

- unique ID and track;
- order and prerequisites;
- observable objectives;
- estimated session size;
- plain-language concept explanation;
- worked example with reasoning;
- common misconception;
- guided task reference;
- independent task reference;
- assessment reference;
- next concept.

Keep a unit bounded. Split it when its objectives cannot be practiced and
assessed together.

## Assignment contract

Assignments progress through four modes:

| Mode | Support | Evidence |
| --- | --- | --- |
| Guided | Steps and relevant hints | Miles follows and explains each decision |
| Faded | Some steps removed | Miles supplies missing decisions |
| Independent | Goal and constraints only | Miles produces a complete solution |
| Transfer | New context | Miles chooses and applies the concept without cues |

Each assignment states:

- objective;
- allowed resources;
- input or scenario;
- expected artifact;
- constraints;
- rubric;
- feedback route after failure.

Hints must reveal less than the full solution and should be recorded when used.

## Assessment contract

Use an assessment to produce evidence, not merely a percentage.

Prefer these evidence types:

- free recall or explanation;
- concrete worked answer;
- code or command sequence;
- diagram or relationship map;
- diagnosis of a flawed example;
- transfer task.

Each assessment defines:

- objectives under test;
- resource policy;
- questions and variants;
- criterion-level rubric;
- passing evidence;
- misconception routes;
- reassessment delay when appropriate.

Multiple-choice questions may diagnose misconceptions, but should not be the
only evidence for application or transfer.

## Mastery states

Use this state progression:

```text
locked
  -> learning
  -> practiced
  -> provisional
  -> review_due
  -> retained
```

| State | Required evidence |
| --- | --- |
| `locked` | An unmet prerequisite exists |
| `learning` | Explanation or worked example has begun |
| `practiced` | Guided or independent work has been submitted |
| `provisional` | Immediate assessment meets the rubric |
| `review_due` | Provisional evidence exists and delayed retrieval is scheduled |
| `retained` | Delayed retrieval or transfer meets the rubric |

Track evidence by dimension:

- explain;
- apply;
- diagnose;
- transfer.

Do not average away a failed critical dimension. State exactly which dimension
still lacks evidence.

## Corrective loop

Route errors by cause:

| Cause | Corrective action |
| --- | --- |
| Missing prerequisite | Return to the smallest missing concept |
| Inaccurate mental model | Contrast the model with a concrete counterexample |
| Procedural error | Trace the decision point and practice a varied procedure |
| Weak retrieval | Use shorter delayed recall before adding complexity |
| Transfer failure | Compare familiar and novel contexts, then retry a new case |
| Ambiguous assessment | Repair the question or rubric before grading again |

After correction, use a different variant. Repeating an identical answer does
not demonstrate transfer.

## Review scheduling

Use delayed retrieval after provisional success. A practical default is:

- first review after one day;
- second review after seven days;
- third review after thirty days.

Treat these intervals as defaults, not universal rules. Shorten the interval
after weak retrieval and lengthen it after strong, low-hint recall. Record the
next due date and the evidence that determined it.

## Progress checkpoint

`maps/progress.md` is the current handoff. It should answer:

1. What is Miles studying?
2. What is the current track and concept?
3. What evidence exists for the current mastery state?
4. Which questions remain unresolved?
5. Where did the session stop?
6. What exact action should begin the next session?
7. Which files support the checkpoint?

Keep chronological history in inbox logs and reviews. Replace stale current
state in the checkpoint rather than accumulating a diary there.

A checkpoint must distinguish:

- verified activity;
- current interpretation;
- planned next action.

## Agent decision rules

- Choose one next concept, not a large syllabus dump.
- Prefer the lowest unmet prerequisite.
- Teach before assigning when no prior evidence exists.
- Fade help as evidence improves.
- Retrieve before revealing notes during assessment and review.
- Use rubric evidence rather than confidence language for mastery.
- Record exact paths and commit evidence before claiming continuity.
- Stop for ambiguous public-safety or grading decisions.
