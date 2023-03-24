# devsecops-config

This is a generic implementation of a GitOps workflow for secure, revision and audit-proof application delivery on Red Hat OpenShift.

It uses several technologies such as:

* Red Hat OpenShift GitOps (a.k.a Argo CD)
* Red Hat OpenShift Pipelines (a.k.a. Tekton)
* Red Hat OpenShift Dev Spaces
* Red Hat Quay and the Red Hat Quay Bridge Operator (optional)
* Red Hat Quay Container Security Operator (optional)
* Gitea ([https://github.com/go-gitea/gitea](https://github.com/go-gitea/gitea))

## Preparation

The following section explains how to install and configure the operators and how to to deploy the build- and rollout pipelines.

### Operators

See [operator/README.md](operators/README.md) for a step-by-step guid how to install and configure the operators.

### Deploy the Pipelines

There are two generic Tekton pipelines to support secure builds and auditable rollouts of container images:
