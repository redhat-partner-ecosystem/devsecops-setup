"""
Create a security scan report for a image stream.

Usage:

secscan.py <namespace> <image_stream> <tag> <git_repo>

"""

import os
import sys
from dotenv import load_dotenv
from github import Github

from quay import get_repo_tags, get_manifest_security
from gh import get_create_label, create_issue

if __name__ == '__main__':

    # for local dev/test
    load_dotenv()

    # get the QUAY/GITHUB endpoint and auth token from ENV
    QUAY_ENDPOINT = os.getenv('QUAY_ENDPOINT', '')
    QUAY_TOKEN = os.getenv('QUAY_TOKEN', '')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

    # get the rest of the parameters from ARGV
    NAMESPACE = sys.argv[1]
    IMAGE_STREAM = sys.argv[2]
    TAG = sys.argv[3]
    GIT_REPO = sys.argv[4]

    # find all the available tags
    tags = get_repo_tags(QUAY_ENDPOINT, QUAY_TOKEN, NAMESPACE, IMAGE_STREAM)

    if tags == {}:
        print(f"  --> Aborting. Can't find repo {NAMESPACE}/{IMAGE_STREAM}")
        sys.exit(0)  # this is not good

    # look for a specific TAG
    manifest_ref = ''
    for tag in tags['tags']:
        if tag['name'] == TAG:
            manifest_ref = tag['manifest_digest']
            break

    if manifest_ref == '':
        print(f"  --> Aborting. Can't find tag {TAG} in {NAMESPACE}/{IMAGE_STREAM}")
        sys.exit(0)  # this is not good

    # get the security scan results
    scan = get_manifest_security(
        QUAY_ENDPOINT, QUAY_TOKEN, NAMESPACE, IMAGE_STREAM, manifest_ref)

    if scan == {}:
        print(f"  --> Aborting. No security scan results for {NAMESPACE}/{IMAGE_STREAM}")
        sys.exit(0)  # this is not good

    # only continue if the image was actually scanned
    if not scan['status'] == 'scanned':
        print(f"  --> Aborting. No security scan results for {NAMESPACE}/{IMAGE_STREAM}")
        sys.exit(0)

    # get all the features, i.e. installed packages
    features = scan['data']['Layer']['Features']
    if len(features) == 0:
        sys.exit(0)  # abort, but no error

    # get access to GitHub
    g = Github(GITHUB_TOKEN)
    # find the repo
    repo = g.get_repo(GIT_REPO)
    # create a generic secscan label if it doesn't already exist
    secscan_label = get_create_label(
        repo, "security scan", "Vulnerabilities detected by Quay Security Scanner", "ff0000")

    pkg = 0
    vul = 0

    # find all packages with a vulnerability and create an GitHub issue for each
    for feature in features:
        pkg = pkg + 1
        if len(feature['Vulnerabilities']) > 0:
            for v in feature['Vulnerabilities']:
                vul = vul + 1

                title = f"{feature['Name']}: {v['Name']} - {v['Severity']}"
                create_issue(repo, title, v['Description'], labels=[
                             secscan_label])
                             
                print(f"Created issue: {title}")

    print(f"Image stream {NAMESPACE}/{IMAGE_STREAM}:{TAG}: scanned {pkg} packages, found {vul} vulnerabilities.")