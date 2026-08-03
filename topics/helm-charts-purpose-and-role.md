---
id: topic-helm-purpose-and-role-001
created: 2026-08-03
status: active
tags: [helm, kubernetes, packaging, release-management]
source: public-helm-documentation
visibility: public
---

# Helm and the chart format

## Why it exists

The unit of the Kubernetes API is a single object. A running application is not
a single object: it is a Deployment, a Service, a ConfigMap, a Secret, an
Ingress, a ServiceAccount, and often RBAC rules and volume claims.
`kubectl apply -f ./manifests` sends every one of those objects to the cluster,
but it does not give them a name as a group, a version, or a history.

Three gaps follow from that:

1. No unit. Nothing in the cluster records that these objects are one
   application at one version.
2. No parameterization. Dev and prod differ in replica count, image tag,
   hostname, and resource limits. Without a parameter layer the answer is
   copies of the same YAML, and copies drift.
3. No reversible change. Rolling back means locating the previous directory of
   YAML and hoping nothing was applied outside it.

Helm's design reads most clearly as one answer per gap.

## Timeline

Verified against `helm.sh/docs/community/history`:

- 2015: Helm Classic starts at Deis and is shown at the first KubeCon.
- January 2016: Helm Classic merges with Google's Kubernetes Deployment
  Manager and moves under Kubernetes governance. Helm 2.0 follows later that
  year. Deployment Manager's server-side component survives the merge, renamed
  Tiller.
- June 2018: Helm moves from a Kubernetes subproject to a full CNCF project.
- November 2019: Helm 3 removes Tiller and returns Helm to a client-side tool.
- 30 April 2020: Helm graduates in the CNCF.
- 12 November 2025: Helm 4.0.0, the first major release in six years. It adds
  WebAssembly-based plugins, server-side apply, kstatus-based resource
  watching, and reproducible chart archives. Helm 3 receives bug fixes through
  8 July 2026 and security fixes through 11 November 2026.

The Tiller episode is the part worth remembering. A server-side component with
broad cluster write access was the price Helm 2 paid for its features, and
removing it was the headline of the next major version. Verified here: the
removal and the stated rationale of returning to a client tool. Not verified
here: the security criticism usually cited as the underlying reason.

## What Helm is

A package manager for Kubernetes, in the sense that apt or Homebrew is one for
an operating system. Since v3 it is a command-line client plus a Go library
that talks directly to the Kubernetes API server. No Helm component runs inside
the cluster.

Two nouns carry the whole model:

- Chart: the package. A directory or archive holding every resource definition
  an application needs, plus its metadata and default values.
- Release: one installed instance of a chart in a cluster. The same chart can
  be installed many times under different release names, each tracked
  separately.

Helm stores release state in Kubernetes Secrets inside the cluster, so it needs
no separate database. That detail is the one most often missed: the cluster
itself remembers which chart, at which version, with which values, produced the
objects currently running.

## Chart layout

```text
chartname/
  Chart.yaml           required metadata: apiVersion, name, version (SemVer 2)
  values.yaml          default configuration the templates read
  values.schema.json   optional JSON Schema validating those values
  templates/           Go templates rendered into Kubernetes manifests
    NOTES.txt          optional post-install message
  charts/              dependent charts, unpacked
  crds/                CustomResourceDefinitions, installed without templating
  LICENSE  README.md   optional
```

`apiVersion: v2` is the Helm 3 and later format: dependencies are declared
inside `Chart.yaml` and a `type` field separates application charts from
library charts. `apiVersion: v1` kept dependencies in a separate
`requirements.yaml` and is still installable.

## The three jobs

1. Packaging. `Chart.yaml` carries a SemVer 2 version and declares
   dependencies, which resolve into `charts/`. The application becomes one
   versioned, distributable artifact.
2. Templating. `templates/` is rendered against `values.yaml`, overridden per
   install with `-f` or `--set`. One chart covers many environments from one
   source.
3. Release lifecycle. `install`, `upgrade`, `rollback`, and `uninstall` each
   record a revision. `helm rollback` acts on recorded state rather than
   re-applying an older folder.

## Common misconception

"Helm is a YAML template engine." Templating is one job of three, and the most
replaceable one: kustomize, jsonnet, or any generator also produces manifests.
The job that is hard to rebuild is the recorded release history in the cluster.

The test is `helm template`. It renders a chart to stdout and creates no
release. If that command covers the need, Helm is being used as a template
engine and the other two jobs are unused. That is a legitimate choice, but it
should be a choice rather than an accident.

## Recall check

The same application runs in dev and prod, differing only in replica count and
image tag. A colleague proposes keeping two directories of plain YAML and
applying each with `kubectl apply -f`.

Name the two things Helm provides that this approach does not, and name the one
thing the plain approach does equally well. Answer before opening the block
below.

<details>
<summary>Reveal after answering</summary>

Helm adds two things. First, a single parameterized source, so the two
environments cannot silently diverge in anything except the values explicitly
declared as variable. Second, a release record with revisions stored in the
cluster, which is what makes `helm rollback` possible at all.

Applying the objects is done equally well by `kubectl apply`. Helm's install
path ends in the same Kubernetes API calls. Helm does not deploy better than
kubectl; it names, versions, and remembers.

</details>

## Sources

- https://helm.sh/docs/community/history/
- https://helm.sh/docs/topics/architecture/
- https://helm.sh/docs/topics/charts/
- https://helm.sh/blog/helm-4-released/
