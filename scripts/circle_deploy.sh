#!/usr/bin/env bash

set -x
set -eo pipefail

if [ -z "$CI" ]; then
    echo "Will only continue on CI"
    exit
fi

if [[ "$CIRCLE_BRANCH" != "master" ]]; then
    echo "Will only continue for master builds"
    exit
fi

export VERSION=$(./dist/pdc/pdc --version)
wget https://dl.google.com/go/go1.12.3.linux-amd64.tar.gz

sudo tar -C /usr/local -xzf go1.12.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$HOME/go/bin

go get github.com/tcnksm/ghr

echo "Starting deployment of pseudo@$VERSION"

ghr -t ${GITHUB_TOKEN} -u ${CIRCLE_PROJECT_USERNAME} -r ${CIRCLE_PROJECT_REPONAME} -c ${CIRCLE_SHA1} -n v${VERSION} -b $(cat LATEST_RELEASE.md) ${VERSION} ./dist/pdc-${VERSION}-linux.tar.gz

# build package and upload to pypi index
# echo "[distutils]" >> ~/.pypirc
# echo "index-servers = pypi" >> ~/.pypirc
# echo "[pypi]" >> ~/.pypirc
# echo "username=$PYPI_USERNAME" >> ~/.pypirc
# echo "password=$PYPI_PASSWORD" >> ~/.pypirc

# python setup.py sdist bdist_wheel
# pipenv run twine upload dist/*