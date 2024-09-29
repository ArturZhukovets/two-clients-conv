######################################################################################

# https://hub.docker.com/r/dpage/pgadmin4/tags
FROM dpage/pgadmin4:8.9@sha256:9d75116cc9cfbf33a0927a9928c99a46356b658bb7bfc2345ff921e5f7725e3f

######################################################################################

ARG USER_ID
ARG GROUP_ID
ARG USER_NAME

SHELL ["/bin/sh", "-e", "-u", "-o", "pipefail", "-c"]

######################################################################################

USER root:root

######################################################################################

RUN apk add --no-cache wget

# install dumb-init
RUN DUMB_INIT_VERSION='1.2.5'; \
    wget -q --quiet -O '/usr/local/bin/dumb-init' "https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_x86_64"; \
    echo 'e874b55f3279ca41415d290c512a7ba9d08f98041b28ae7c2acb19a545f1c4df */usr/local/bin/dumb-init' > '/usr/local/bin/sha256'; \
    sha256sum -cw < '/usr/local/bin/sha256'; \
    chmod +x '/usr/local/bin/dumb-init'; \
    /usr/local/bin/dumb-init --version

# install wait
RUN WAIT_VERSION='2.12.1'; \
    wget -q --quiet -O '/usr/local/bin/wait' "https://github.com/ufoscout/docker-compose-wait/releases/download/${WAIT_VERSION}/wait"; \
    echo '2241be671073520e028b2f12df1e9ef0419014cffb5670b7a80b2080804be17d */usr/local/bin/wait' > '/usr/local/bin/sha256'; \
    sha256sum -cw < '/usr/local/bin/sha256'; \
    chmod +x '/usr/local/bin/wait'; \
    /usr/local/bin/wait --version

######################################################################################

RUN groupadd -g "${GROUP_ID}" -o "${USER_NAME}"
RUN useradd -m -u "${USER_ID}" -g "${GROUP_ID}" -o -s /bin/bash "${USER_NAME}"

RUN mkdir -p /var/log/pgadmin
RUN chown -R "${USER_ID}":"${GROUP_ID}" /var/log/pgadmin

RUN mkdir -p /var/lib/pgadmin
RUN chown -R "${USER_ID}":"${GROUP_ID}" /var/lib/pgadmin

RUN chown -R "${USER_ID}":"${GROUP_ID}" /pgadmin4

######################################################################################

USER "${USER_ID}":"${GROUP_ID}"

######################################################################################

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]

ENV WAIT_COMMAND='/entrypoint.sh'

CMD ["/usr/local/bin/wait"]

######################################################################################
