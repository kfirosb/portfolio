#!/bin/bash
branch=$1
echo "${branch}"
release_number=$(echo ${branch} | cut -d / -f 2)
echo "${release_number}"
aws ecr list-images --repository-name tasksapp | grep "${release_number}.*"  | cut -d . -f 3 | cut -d \" -f 1|sort -n -o list.sorted
lastrealese=$(($(cat list.sorted | tail -n1)+1))
echo ${lastrealese}
tag="${release_number}"."${lastrealese}"
echo "${tag}"
echo ${tag} > tag.txt
cat tag.txt