#!/bin/bash

setup_git() {
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
}

travis_real_branch() {
    if [ -z "$TRAVIS_PULL_REQUEST" ];then
        # not a travis build
        return 1
    fi
    local branch
    if [ "$TRAVIS_PULL_REQUEST" = "false" ];then
        branch="$TRAVIS_BRANCH"
    else
        branch="$TRAVIS_PULL_REQUEST_BRANCH"
    fi
    if [ -n "$branch" ];then
        echo "$branch"
        return 0
    fi
    return 1
}

git_show_current() {
    local branch
    branch="$(travis_real_branch)"
    ret="$?"
    if [ "$ret" -eq 2 ];then
        return 2 # On pull request, abort
    fi
    # shellcheck disable=SC2181
    if [ "$ret" -ne 0 ];then
        branch="$(git branch --show-current 2>/dev/null)"
        # shellcheck disable=SC2181
        if [ $? -ne 0 ];then
            branch="$(git rev-parse --abbrev-ref HEAD)"
        fi
    fi
    echo "$branch"
    return 0
}

on_branch() {
    local branch
    branch="$(git_show_current)"
    # shellcheck disable=SC2181
    [ $? -ne 0 ] && return 1
    echo "On branch $branch"
    [ "$1" = "$branch" ] && return 0
    return 1
}

check_branches() {
    local branches=(main nightly)

    local cur_branch
    cur_branch="$(git_show_current)"
    # shellcheck disable=SC2181
    [ $? -ne 0 ] && return 1
    for branch in "${branches[@]}";do
        [ "$branch" = "$cur_branch" ] && return 0
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
