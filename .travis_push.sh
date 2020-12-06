#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

on_branch() {
    local branch="$(git branch --show-current)"
    if [ "$1" = "$branch" ];then
        return 0
    fi
    return 1
}

commit_files() {

  echo "Setting remote origin..."
  git remote set-url origin https://mmfrenkel:${GH_TOKEN}@github.com/mmfrenkel/KERMit.git > /dev/null 2>&1

  git checkout -b travis_results
  git add travis_reports
  git stash
  git pull origin travis_results
  git stash pop
  git add travis_reports
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
  echo "Commited test files..."

  echo "Pushing travis CI results to github..."
  git push --quiet --set-upstream origin travis_results
}

setup_git
if on_branch main;then
    commit_files
fi
