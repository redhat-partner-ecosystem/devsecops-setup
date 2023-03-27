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

### Configuration and secrets

Before you can start any pipeline runs, make sure that all configs and secrets are deployed.

Make a copy of the `secrets/*.example.yaml` files and edit their contents to match your environment.

Deploy the pipeline configs and secrets:

```shell
oc apply -f secrets/pipeline_secrets.yaml -n buildspace
oc apply -f secrets/pipeline_configmap.yaml -n buildspace
```


#### Red Hat OpenShift GitOps configuration and secrets

A default instance is installed in the `openshift-gitops` namespace. 

Verify that the default GitOps instance is up-and-running:

```shell
oc get pods -n openshift-gitops
```

The instance has a default user `admin`. A password is created during the inital deployment. In order to retrieve the password, run:

```shell
oc extract secret/openshift-gitops-cluster -n openshift-gitops --to=-
```

**Note:** this password is also used to access the Argo CD web UI.

Get the ArgoCD route:

```shell
oc get route openshift-gitops-server -n openshift-gitops
```