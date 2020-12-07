#!/bin/bash

setup_git() {
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
}

git_show_current() {
    if [ -z "$TRAVIS_BRANCH" ];then
        echo "$TRAVIS_BRANCH"
        return 0
    fi

    local branch
    branch="$(git branch --show-current 2>/dev/null)"
    # shellcheck disable=SC2181
    if [ $? -ne 0 ];then
        branch="$(git rev-parse --abbrev-ref HEAD)"
    fi
    echo "$branch"
    return 0
}

on_branch() {
    local branch
    branch="$(git_show_current)"
    echo "On branch $branch"
    [ "$1" = "$branch" ] && return 0
    return 1
}

check_branches() {
    local branches=(main nightly)
    for branch in "${branches[@]}";do
        on_branch "$branch" && return 0
    done
    return 1
}

commit_files() {
    local treports="./travis_reports"

    echo "Setting remote origin..."
    git remote set-url origin "https://mmfrenkel:${GH_TOKEN}@github.com/mmfrenkel/KERMit.git" > /dev/null 2>&1

    git checkout -b travis_results
    [ ! -d "$treports" ] && mkdir "$treports"
    mv tests "$treports"/backend
    mv reports "$treports"/frontend
    git add travis_reports
    git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
    echo "Commited test files..."

    echo "Pushing travis CI results to github..."
    git push --quiet --set-upstream origin travis_results
}

setup_git
if check_branches;then
    commit_files
fi
