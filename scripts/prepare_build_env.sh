#!/usr/bin/env bash

###############################################################################

set -Eeuo pipefail  # cspell:disable-line

# For debug output uncomment:
# set -Eeuxo pipefail  # cspell:disable-line

###############################################################################

CUR_DIR="${PWD}"

###############################################################################

function exit_handler () {
    # For debug output uncomment:
    # env

    cd "${CUR_DIR}"
}

trap exit_handler ERR
trap exit_handler EXIT

###############################################################################

BASE_DIR="$(dirname "$0")"
BASE_DIR="$(realpath "${BASE_DIR}")"

WORK_DIR="${WORK_DIR:-"$(realpath "${BASE_DIR}/..")"}"

###############################################################################

cd "${BASE_DIR}"

###############################################################################

if grep -sq 'systemd' /proc/1/sched | head -n 1; then
    echo 'WARNING: This script must call only in docker build env!'
    exit 1
else
    echo "Run in docker"
fi

###############################################################################

L7X_BUILD_DEVELOPMENT="${L7X_BUILD_DEVELOPMENT:-}"
echo "L7X_BUILD_DEVELOPMENT: ${L7X_BUILD_DEVELOPMENT}"

###############################################################################

add-apt-repository ppa:deadsnakes/ppa -y
apt -q update

apt list | grep '^python3.11/'
# apt list | grep '^python3-distutils/'

PYTHON_VERSION='3.11.10-1+jammy1'
DEBIAN_FRONTEND='noninteractive' apt -q install -y -o Dpkg::Options::='--force-confnew' --no-install-recommends \
    "python3.11=${PYTHON_VERSION}" \
    "python3.11-dev=${PYTHON_VERSION}" \
    "python3.11-venv=${PYTHON_VERSION}"

PYTHON="/usr/bin/python3.11"

update-alternatives --install /usr/bin/python3 python3 "${PYTHON}" 1

ldconfig

"${PYTHON}" --version

###############################################################################

# cSpell:ignore skel

PYTHON_BUILDER_USER="${PYTHON_BUILDER_USER:-python_builder}"
PYTHON_BUILDER_USER_ID="${PYTHON_BUILDER_USER_ID:-10000}"
groupadd -r -g "${PYTHON_BUILDER_USER_ID}" "${PYTHON_BUILDER_USER}"
useradd -r -m -s /bin/bash -g "${PYTHON_BUILDER_USER}" -u "${PYTHON_BUILDER_USER_ID}" "${PYTHON_BUILDER_USER}"
cp -r /etc/skel/. "/home/${PYTHON_BUILDER_USER}/"

mkdir -p \
    "/home/${PYTHON_BUILDER_USER}/.local/bin" \
    "/home/${PYTHON_BUILDER_USER}/.config/pypoetry" \
    "/home/${PYTHON_BUILDER_USER}/.cache/pypoetry" \
    "/home/${PYTHON_BUILDER_USER}/.cache/pip" \
    "/home/${PYTHON_BUILDER_USER}/.cache/compiled_python"

chown "${PYTHON_BUILDER_USER}:${PYTHON_BUILDER_USER}" \
    "${WORK_DIR}" \
    "/home/${PYTHON_BUILDER_USER}/.local" \
    "/home/${PYTHON_BUILDER_USER}/.local/bin" \
    "/home/${PYTHON_BUILDER_USER}/.config/pypoetry" \
    "/home/${PYTHON_BUILDER_USER}/.cache/pypoetry" \
    "/home/${PYTHON_BUILDER_USER}/.cache/pip" \
    "/home/${PYTHON_BUILDER_USER}/.cache/compiled_python"

ls -la "/home/${PYTHON_BUILDER_USER}/"

PYTHON_VERSION="${PYTHON_VERSION:-3.11}"
RUN_PYTHON="${RUN_PYTHON:-/usr/bin/python${PYTHON_VERSION}}"
${RUN_PYTHON} --version

###############################################################################

# https://github.com/pypa/get-pip/tags
wget -q -P "${WORK_DIR}/pip-installer/" 'https://raw.githubusercontent.com/pypa/get-pip/24.2/public/get-pip.py'

find "${WORK_DIR}/pip-installer/" -type f -exec sha256sum -b {} \;
echo "6fb7b781206356f45ad79efbb19322caa6c2a5ad39092d0d44d0fec94117e118 *${WORK_DIR}/pip-installer/get-pip.py" > "${WORK_DIR}/pip-installer/sha256"
sha256sum -cw --strict < "${WORK_DIR}/pip-installer/sha256"

${RUN_PYTHON} "${WORK_DIR}/pip-installer/get-pip.py" --no-setuptools --no-wheel

rm -rf "${WORK_DIR}/pip-installer"

${RUN_PYTHON} -m pip --version

###############################################################################

# cSpell:ignore rpds_py cachecontrol fastjsonschema
{
    echo 'SecretStorage==3.3.3 --hash=sha256:f356e6628222568e3af06f2eba8df495efa13b3b63081dafd4f7d9a7b7bc9f99'; \
    echo 'build==1.2.1 --hash=sha256:75e10f767a433d9a86e50d83f418e83efc18ede923ee5ff7df93b6cb0306c5d4'; \
    echo 'cachecontrol==0.14.0 --hash=sha256:f5bf3f0620c38db2e5122c0726bdebb0d16869de966ea6a2befe92470b740ea0'; \
    echo 'certifi==2024.8.30 --hash=sha256:922820b53db7a7257ffbda3f597266d435245903d80737e34f8a45ff3e3230d8'; \
    echo 'cffi==1.17.1 --hash=sha256:610faea79c43e44c71e1ec53a554553fa22321b65fae24889706c0a84d4ad86d'; \
    echo 'charset_normalizer==3.3.2 --hash=sha256:753f10e867343b4511128c6ed8c82f7bec3bd026875576dfd88483c5c73b2fd8'; \
    echo 'cleo==2.1.0 --hash=sha256:4a31bd4dd45695a64ee3c4758f583f134267c2bc518d8ae9a29cf237d009b07e'; \
    echo 'crashtest==0.4.1 --hash=sha256:8d23eac5fa660409f57472e3851dab7ac18aba459a8d19cbbba86d3d5aecd2a5'; \
    echo 'cryptography==43.0.1 --hash=sha256:511f4273808ab590912a93ddb4e3914dfd8a388fed883361b02dea3791f292e1'; \
    echo 'distlib==0.3.8 --hash=sha256:034db59a0b96f8ca18035f36290806a9a6e6bd9d1ff91e45a7f172eb17e51784'; \
    echo 'dulwich==0.21.7 --hash=sha256:7bca4b86e96d6ef18c5bc39828ea349efb5be2f9b1f6ac9863f90589bac1084d'; \
    echo 'fastjsonschema==2.20.0 --hash=sha256:5875f0b0fa7a0043a91e93a9b8f793bcbbba9691e7fd83dca95c28ba26d21f0a'; \
    echo 'filelock==3.15.4 --hash=sha256:6ca1fffae96225dab4c6eaf1c4f4f28cd2568d3ec2a44e15a08520504de468e7'; \
    echo 'idna==3.8 --hash=sha256:050b4e5baadcd44d760cedbd2b8e639f2ff89bbc7a5730fcc662954303377aac'; \
    echo 'importlib_metadata==8.4.0 --hash=sha256:66f342cc6ac9818fc6ff340576acd24d65ba0b3efabb2b4ac08b598965a4a2f1'; \
    echo 'installer==0.7.0 --hash=sha256:05d1933f0a5ba7d8d6296bb6d5018e7c94fa473ceb10cf198a92ccea19c27b53'; \
    echo 'jaraco.classes==3.4.0 --hash=sha256:f662826b6bed8cace05e7ff873ce0f9283b5c924470fe664fff1c2f00f581790'; \
    echo 'jeepney==0.8.0 --hash=sha256:c0a454ad016ca575060802ee4d590dd912e35c122fa04e70306de3d076cce755'; \
    echo 'keyring==24.3.1 --hash=sha256:df38a4d7419a6a60fea5cef1e45a948a3e8430dd12ad88b0f423c5c143906218'; \
    echo 'more_itertools==10.4.0 --hash=sha256:0f7d9f83a0a8dcfa8a2694a770590d98a67ea943e3d9f5298309a484758c4e27'; \
    echo 'msgpack==1.0.8 --hash=sha256:83b5c044f3eff2a6534768ccfd50425939e7a8b5cf9a7261c385de1e20dcfc85'; \
    echo 'packaging==24.1 --hash=sha256:5b8f2217dbdbd2f7f384c41c628544e6d52f2d0f53c6d0c3ea61aa5d1d7ff124'; \
    echo 'pexpect==4.9.0 --hash=sha256:7236d1e080e4936be2dc3e326cec0af72acf9212a7e1d060210e70a47e253523'; \
    echo 'pip==24.2 --hash=sha256:2cd581cf58ab7fcfca4ce8efa6dcacd0de5bf8d0a3eb9ec927e07405f4d9e2a2'; \
    echo 'pkginfo==1.11.1 --hash=sha256:bfa76a714fdfc18a045fcd684dbfc3816b603d9d075febef17cb6582bea29573'; \
    echo 'platformdirs==4.2.2 --hash=sha256:2d7a1657e36a80ea911db832a8a6ece5ee53d8de21edd5cc5879af6530b1bfee'; \
    echo 'poetry==1.8.3 --hash=sha256:88191c69b08d06f9db671b793d68f40048e8904c0718404b63dcc2b5aec62d13'; \
    echo 'poetry_core==1.9.0 --hash=sha256:4e0c9c6ad8cf89956f03b308736d84ea6ddb44089d16f2adc94050108ec1f5a1'; \
    echo 'poetry_plugin_export==1.8.0 --hash=sha256:adbe232cfa0cc04991ea3680c865cf748bff27593b9abcb1f35fb50ed7ba2c22'; \
    echo 'ptyprocess==0.7.0 --hash=sha256:4b41f3967fce3af57cc7e94b888626c18bf37a083e3651ca8feeb66d492fef35'; \
    echo 'pycparser==2.22 --hash=sha256:c3702b6d3dd8c7abc1afa565d7e63d53a1d0bd86cdc24edd75470f4de499cfcc'; \
    echo 'pyproject_hooks==1.1.0 --hash=sha256:7ceeefe9aec63a1064c18d939bdc3adf2d8aa1988a510afec15151578b232aa2'; \
    echo 'rapidfuzz==3.9.7 --hash=sha256:965693c2e9efd425b0f059f5be50ef830129f82892fa1858e220e424d9d0160f'; \
    echo 'requests==2.32.3 --hash=sha256:70761cfe03c773ceb22aa2f671b4757976145175cdfca038c02654d061d6dcc6'; \
    echo 'requests_toolbelt==1.0.0 --hash=sha256:cccfdd665f0a24fcf4726e690f65639d272bb0637b9b92dfd91a5568ccf6bd06'; \
    echo 'setuptools==74.1.2 --hash=sha256:5f4c08aa4d3ebcb57a50c33b1b07e94315d7fc7230f7115e47fc99776c8ce308'; \
    echo 'shellingham==1.5.4 --hash=sha256:7ecfff8f2fd72616f7481040475a65b2bf8af90a56c89140852d1120324e8686'; \
    echo 'tomlkit==0.13.2 --hash=sha256:7a974427f6e119197f670fbbbeae7bef749a6c14e793db934baefc1b5f03efde'; \
    echo 'trove_classifiers==2024.7.2 --hash=sha256:ccc57a33717644df4daca018e7ec3ef57a835c48e96a1e71fc07eb7edac67af6'; \
    echo 'urllib3==2.2.2 --hash=sha256:a448b2f64d686155468037e1ace9f2d2199776e17f0a46610480d311f73e3472'; \
    echo 'virtualenv==20.26.3 --hash=sha256:8cc4a31139e796e9a7de2cd5cf2489de1217193116a8fd42328f1bd65f434589'; \
    echo 'wheel==0.44.0 --hash=sha256:2376a90c98cc337d18623527a97c31797bd02bad0033d41547043a1cbfbe448f'; \
    echo 'zipp==3.20.1 --hash=sha256:9960cd8967c8f85a56f920d5d507274e74f9ff813a0ab8889a5b5be2daf44064'; \
} >> "${WORK_DIR}/poetry_requirements.txt"

# cat "${WORK_DIR}/poetry_requirements.txt"

${RUN_PYTHON} -m pip install --require-hashes --force-reinstall -r "${WORK_DIR}/poetry_requirements.txt"
rm -r "${WORK_DIR}/poetry_requirements.txt"

${RUN_PYTHON} -m poetry --version

###############################################################################
