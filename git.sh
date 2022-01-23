#!/bin/sh
set -eux
cd ../jasima
user=$1
repo=$2
token=$3
git commit -m "Updating repo"
git push https://$token@github.com/$user/$repo.git
