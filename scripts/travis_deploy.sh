#!/bin/bash

if [ -z "$CI" ]; then
    echo "Will only continue on CI"
    exit
fi

set -x
sudo brew install golang

export GOPATH=$HOME/go # don't forget to change your path correctly!
export GOROOT=/usr/local/opt/go/libexec
mkdir -p $GOPATH $GOPATH/src $GOPATH/pkg $GOPATH/bin
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

go get github.com/tcnksm/ghr
ghr --help

if ["$TRAVIS_BRANCH" -eq "master"]; then
    echo "Deploy..."
    echo $TRAVIS_REPO_SLUG
    ghr -t ${GITHUB_TOKEN} -u ${CIRCLE_PROJECT_USERNAME} -r ${CIRCLE_PROJECT_REPONAME} -c ${CIRCLE_SHA1} ${VERSION} ./dist/pdc-$(VERSION)-darwin.tar.gz
fi
