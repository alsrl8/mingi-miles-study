---
id: topic-go-type-ownership-001
created: 2026-07-31
status: active
tags: [go, design, package-boundaries, agent-run-observer]
source: direct-experience
visibility: public
---

# Type ownership at a Go package boundary

## The decision

When a downstream package consumes a type from an upstream package, there are
two options: reuse the upstream type in the downstream API, or define a
downstream type with the same information and convert between them.

The deciding question is not "are these fields the same today?" but:

> Does the downstream type have a reason to change that the upstream type does
> not share?

If no such reason exists, a duplicate is not a boundary. It is one shape
written twice.

## What each option actually costs

Reuse (`[]llm.Event` inside the analysis result):

- the upstream shape becomes part of the downstream published contract, so an
  upstream field rename or JSON tag change is a downstream contract change;
- no conversion code, no drift, no per-field maintenance.

Duplicate (`[]analyze.Event`):

- the downstream contract is stable against upstream churn, but only because a
  conversion function absorbs the difference, and that function must be written
  and tested;
- when the upstream type gains a field, the duplicate silently omits it. The
  compiler reports nothing, because the two types were never required to match.

The second cost is the one that surprises people. A copied struct does not
decouple two packages. It moves the coupling out of the type system and into a
conversion function that no longer has a compiler checking it.

## Worked example

In `projects/agent-run-observer`, `analyze.Event` and `analyze.EventError` are
field-for-field copies of `llm.Event` and `llm.EventError`, JSON tags included.
Applying the question above:

- Does the analysis event have a reason to change independently? Not today. It
  currently carries exactly the source event.
- What does the copy buy? Nothing yet: `GetAiResponse` does not populate
  `Events` at all, so the duplicate has zero behavior behind it.
- What does the copy cost? A conversion loop that must be written, plus the
  silent-omission risk described above.

The copy earns its existence at the moment the analysis output genuinely
diverges, for example:

- it drops `Arguments`, because raw tool arguments may carry data that must not
  reach a rendered page;
- it adds a derived field such as "this call repeats an earlier one", which the
  source log has no basis to contain.

At that point the shapes differ, the conversion function is doing real work,
and the boundary is honest.

## Common misconception

"Defining my own type decouples my package." It does not, by itself. Decoupling
exists only when the two shapes actually differ and the conversion between them
is explicit and tested. Before that, a duplicate is a maintenance obligation
disguised as an architecture decision.

## Applying it

Start by reusing the upstream type. Introduce a downstream type on the first
concrete requirement that makes the shapes differ, and write the conversion
with a test at the same time. This ordering keeps every boundary traceable to
the requirement that created it.
