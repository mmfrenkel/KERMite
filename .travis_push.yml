#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git checkout -b travis_results
  git add backend_test_results frontend_test_results
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add origin https://${GH_TOKEN}@github.com/mmfrenkel/KERMit.git > /dev/null 2>&1
  git push --quiet --set-upstream origin travis_results
}

setup_git
commit_website_files
upload_files

