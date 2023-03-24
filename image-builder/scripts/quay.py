import os
import sys
import requests


def get_repo_tags(endpoint, token, namespace, image_stream, organization_prefix='openshift'):
    """
    GET /api/v1/repository/{repository}/tag/

    https://access.redhat.com/documentation/en-us/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#listrepotags.
    """
    headers = {'Authorization': f"Bearer {token}"}

    response = requests.get(
        f"https://{endpoint}/api/v1/repository/{organization_prefix}_{namespace}/{image_stream}/tag", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}


def get_manifest_security(endpoint, token, namespace, image_stream, manifest_ref, organization_prefix='openshift'):
    """
    GET /api/v1/repository/{repository}/manifest/{manifestref}/security

    See https://access.redhat.com/documentation/en-us/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#getrepomanifestsecurity.
    """
    headers = {'Authorization': f"Bearer {token}"}

    response = requests.get(
        f"https://{endpoint}/api/v1/repository/{organization_prefix}_{namespace}/{image_stream}/manifest/{manifest_ref}/security", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}
