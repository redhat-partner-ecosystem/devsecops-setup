#FROM ubi8/ubi:8.6
#FROM registry.access.redhat.com/ubi8/python-39-minimal
FROM registry.access.redhat.com/ubi8/s2i-core:1-339

USER root

ENV PYTHON_VERSION=3.9 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    TEKTON_VERSION=0.25.0

RUN INSTALL_PKGS="git \
  unzip \
  wget \
  which \
  nss_wrapper \
  python39 python39-devel python39-setuptools python39-pip" && \
  yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
  rpm -V $INSTALL_PKGS && \
  yum -y clean all --enablerepo='*'

# Upgrade Pip
RUN python3.9 -m pip install --upgrade pip

# Create a Python virtual environment for use by any application
RUN python3.9 -m venv ${APP_ROOT} && \
  chown -R 1001:0 ${APP_ROOT} && \
  fix-permissions ${APP_ROOT} -P && \
  rpm-file-permissions

# Install the GitHub CLI 'gh'
RUN dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
  dnf -y install gh

# Install Kubectl CLI 'kubectl'
# see https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
RUN curl -o /usr/local/bin/kubectl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
  chmod +x /usr/local/bin/kubectl

# Install the Tekton CLI 'tkn'
# see https://tekton.dev/docs/cli/
RUN curl -LO "https://github.com/tektoncd/cli/releases/download/v0.25.0/tkn_${TEKTON_VERSION}_Linux_x86_64.tar.gz" && \
  tar xvzf tkn_${TEKTON_VERSION}_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn && \
  chmod +x /usr/local/bin/tkn && \
  rm tkn_${TEKTON_VERSION}_Linux_x86_64.tar.gz

# Install the Argo CD CLI 'argocd'
# see https://argo-cd.readthedocs.io/en/stable/cli_installation/
RUN curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64 && \
  chmod +x /usr/local/bin/argocd

# Add custom scripts / code
COPY ./scripts ${APP_ROOT}/src

# Install python dependencies
RUN pip install -r ${APP_ROOT}/src/requirements.txt

USER 1001