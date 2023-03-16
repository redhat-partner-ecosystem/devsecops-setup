# Installation

## Install the GitOps operators

Subscribe to the operators:

```shell
oc apply -f operators/openshift-gitops-operator.yaml
oc apply -f operators/openshift-pipeline-operator.yaml
```

Verify that the default GitOps instance is up-and-running:

```shell
oc get pods -n openshift-gitops
```

## Install the Dev Spaces

Subscribe to the operator:

```shell
oc apply -f operators/devworkspace-operator.yaml
oc apply -f operators/devworkspace-instance
```

That's all ...


## Usefull commands

```shell
# list installed operators
oc get csv

# list available operators
oc get packagemanifests -n openshift-marketplace

```
