######################################################################################

# https://hub.docker.com/_/postgres/tags
FROM postgres:16.3-bookworm@sha256:d0f363f8366fbc3f52d172c6e76bc27151c3d643b870e1062b4e8bfe65baf609

######################################################################################

ARG USER_ID
ARG GROUP_ID
ARG USER_NAME

SHELL ["/bin/bash", "-e", "-u", "-o", "pipefail", "-c"]

######################################################################################

USER root:root

######################################################################################

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait /usr/local/bin/wait
ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64 /usr/local/bin/dumb-init

RUN { \
        echo '2241be671073520e028b2f12df1e9ef0419014cffb5670b7a80b2080804be17d */usr/local/bin/wait'; \
        echo 'e874b55f3279ca41415d290c512a7ba9d08f98041b28ae7c2acb19a545f1c4df */usr/local/bin/dumb-init'; \
    } >> '/usr/local/bin/sha256'; \
    sha256sum -cw --strict < /usr/local/bin/sha256; \
    rm -rf /usr/local/bin/sha256;

RUN chmod +x /usr/local/bin/wait; \
    chmod +x /usr/local/bin/dumb-init; \
    /usr/local/bin/dumb-init --version; \
    /usr/local/bin/wait --version;

######################################################################################

RUN groupadd -g "${GROUP_ID}" -o "${USER_NAME}"
RUN useradd -m -u "${USER_ID}" -g "${GROUP_ID}" -o -s /bin/bash "${USER_NAME}"

######################################################################################

USER "${USER_ID}":"${GROUP_ID}"

######################################################################################

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]

ENV WAIT_COMMAND='/usr/local/bin/docker-entrypoint.sh postgres'

CMD ["/usr/local/bin/wait"]

######################################################################################
