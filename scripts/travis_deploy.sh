#!/bin/bash

if [ -z "$CI" ]; then
    echo "Will only continue on CI"
    exit
fi

set -x

export GOPATH=$HOME/go # don't forget to change your path correctly!
export GOROOT=/usr/local/opt/go/libexec
mkdir -p $GOPATH $GOPATH/src $GOPATH/pkg $GOPATH/bin
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

go get github.com/tcnksm/ghr

if [ "$TRAVIS_BRANCH" -eq "master" ]; then
    echo "Starting deployment of pseudo@$VERSION"
    ghr -t ${GITHUB_TOKEN} -u pniedzwiedzinski -r pseudo -c ${TRAVIS_COMMIT} ${VERSION} ./dist/pdc-$(VERSION)-darwin.tar.gz
fi
