FROM --platform=$BUILDPLATFORM ubuntu:22.04


LABEL maintainer="@k33g_org"

ARG TARGETOS
ARG TARGETARCH

ARG GO_VERSION=${GO_VERSION}

ARG USER_NAME=${USER_NAME}

ARG DEBIAN_FRONTEND=noninteractive

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_COLLATE=C
ENV LC_CTYPE=en_US.UTF-8

# ------------------------------------
# Install Tools
# ------------------------------------
RUN <<EOF
apt-get update 
apt-get install -y curl wget jq git build-essential xz-utils bat software-properties-common sudo sshpass unzip
ln -s /usr/bin/batcat /usr/bin/bat

apt-get clean autoclean
apt-get autoremove --yes
rm -rf /var/lib/{apt,dpkg,cache,log}/
EOF

# ------------------------------------
# Install Go
# ------------------------------------
RUN <<EOF

wget https://golang.org/dl/go${GO_VERSION}.linux-${TARGETARCH}.tar.gz
tar -xvf go${GO_VERSION}.linux-${TARGETARCH}.tar.gz
mv go /usr/local
rm go${GO_VERSION}.linux-${TARGETARCH}.tar.gz
EOF

# ------------------------------------
# Set Environment Variables for Go
# ------------------------------------
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/home/${USER_NAME}/go"
ENV GOROOT="/usr/local/go"

RUN <<EOF
go version
go install -v golang.org/x/tools/gopls@latest
go install -v github.com/ramya-rao-a/go-outline@latest
go install -v github.com/stamblerre/gocode@v1.0.0
go install -v github.com/mgechev/revive@v1.3.2
EOF


# ------------------------------------
# Install Docker
# ------------------------------------
RUN <<EOF
# Add Docker's official GPG key:
apt-get update
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
EOF


# ------------------------------------
# Install Python
# ------------------------------------
RUN <<EOF
apt-get update
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9 python3.9-distutils python3.9-dev python3.9-venv
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9
# Create symlinks
ln -sf /usr/bin/python3.9 /usr/bin/python3
ln -sf /usr/bin/python3.9 /usr/bin/python
ln -sf /usr/local/bin/pip3.9 /usr/local/bin/pip3
ln -sf /usr/local/bin/pip3.9 /usr/local/bin/pip
EOF


# ------------------------------------
# Create a new user
# ------------------------------------
# Create new regular user `${USER_NAME}` and disable password and gecos for later
# --gecos explained well here: https://askubuntu.com/a/1195288/635348
RUN adduser --disabled-password --gecos '' ${USER_NAME}

#  Add new user `${USER_NAME}` to sudo group
RUN adduser ${USER_NAME} sudo

# Ensure sudo group users are not asked for a password when using 
# sudo command by ammending sudoers file
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN <<EOF
groupadd docker
usermod -aG docker ${USER_NAME}
newgrp docker
EOF

#  Add new user `${USER_NAME}` to docker group
RUN adduser ${USER_NAME} docker


# Set the working directory
WORKDIR /home/${USER_NAME}

# Set the user as the owner of the working directory
RUN chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}

# Switch to the regular user
USER ${USER_NAME}

# Avoid the message about sudo
RUN touch ~/.sudo_as_admin_successful

# ------------------------------------
# Install OhMyBash
# ------------------------------------
RUN <<EOF
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
EOF


RUN <<EOF
SNIPPETS_VERSION="0.0.1"
SNIPPETS_OS="${TARGETOS}"
SNIPPETS_ARCH="${TARGETARCH}"
wget https://github.com/bots-garden/snippets/releases/download/v${SNIPPETS_VERSION}/snippets-v${SNIPPETS_VERSION}-${SNIPPETS_OS}-${SNIPPETS_ARCH}
cp snippets-v${SNIPPETS_VERSION}-${SNIPPETS_OS}-${SNIPPETS_ARCH} snippets
chmod +x snippets
rm snippets-v${SNIPPETS_VERSION}-${SNIPPETS_OS}-${SNIPPETS_ARCH}
sudo cp ./snippets /usr/bin
rm snippets
# check the version
snippets version
EOF