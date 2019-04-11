#!/usr/bin/env bash

if [ -z "$CI" ]; then
    echo "Will only continue on CI"
    exit
fi


wget https://dl.google.com/go/go1.12.3.linux-amd64.tar.gz

sudo tar -C /usr/local -xzf go1.12.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go get github.com/tcnksm/ghr
ghr --help
if [[ $CIRCLE_BRANCH != "master" ]]; then
    echo "Will only continue for master builds"
    exit
fi

echo "Starting deployment..."

ghr -t ${GITHUB_TOKEN} -u ${CIRCLE_PROJECT_USERNAME} -r ${CIRCLE_PROJECT_REPONAME} -c ${CIRCLE_SHA1} ${VERSION} ./dist/pdc-${VERSION}-linux.tar.gz

# build package and upload to pypi index
# echo "[distutils]" >> ~/.pypirc
# echo "index-servers = pypi" >> ~/.pypirc
# echo "[pypi]" >> ~/.pypirc
# echo "username=$PYPI_USERNAME" >> ~/.pypirc
# echo "password=$PYPI_PASSWORD" >> ~/.pypirc

# python setup.py sdist bdist_wheel
# pipenv run twine upload dist/*