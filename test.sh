#!/bin/bash
declare -A list
first=$(aws ecr list-images --repository-name tasksapp | grep 1.0.1 )
echo ${first}
for i in "${first["imageIds"]}"
do
    echo "5"
done

# branch=$1
# echo "${branch}"
# release_number=$(echo ${branch} | cut -d / -f 2)
# echo "${release_number}"
# for 
# last=$(git tag -l --contains "${release_number}" | tail -n1 | cut -d . -f 3)
# middal=$(git tag -l --contains "${release_number}" | tail -n1 | cut -d . -f 2)
# first=$(git tag -l --contains "${release_number}" | tail -n1 | cut -d . -f 1)
# if [[ ${first} ]]
#     then 
#     echo "${first}"
# else
#     first=$(echo "${release_number}" | tail -n1 | cut -d . -f 1)
#     middal=$(echo "${release_number}" | tail -n1 | cut -d . -f 2)
# fi

# if [[ ${last} ]];
# then
# 	last=$((last+1))
# else
# 	last=0
# fi

# tag="${first}"."${middal}"."${last}"
# echo "${tag}"
# echo ${tag} > tag.txt
# cat tag.txt