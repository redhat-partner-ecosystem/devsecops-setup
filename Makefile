VERSION = 1.0.0
BUILD_NAMESPACE = devsecops-setup

.PHONY: namespace
namespace:
	oc new-project ${BUILD_NAMESPACE}

.PHONY: install
install: install_tasks install_pipelines
	oc policy add-role-to-user system:image-builder \
		system:serviceaccount:${BUILD_NAMESPACE}:builder \
		--namespace=openshift
	oc apply -f image-builder/builder.yaml
	oc apply -f pipelines/config/pipelines.yaml
	oc apply -f pipelines/config/rolebindings.yaml

.PHONY: install_pipelines
install_pipelines:
	oc apply -n ${BUILD_NAMESPACE} -f pipelines/build/
	oc apply -n ${BUILD_NAMESPACE} -f pipelines/rollout/

.PHONY: install_tasks
install_tasks:
	oc apply -f pipelines/clustertasks/

.PHONY: cleanup
cleanup:
	oc delete build --all -n ${BUILD_NAMESPACE}
	oc delete pipelineruns,taskruns --all -n ${BUILD_NAMESPACE}
	oc delete pod --field-selector=status.phase==Succeeded -n ${BUILD_NAMESPACE}
