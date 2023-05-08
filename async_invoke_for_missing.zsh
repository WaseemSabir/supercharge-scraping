#!/usr/bin/env zsh

# Simple script that invokes the lambda function for all pages listed in missing.txt file.
num_lines=$(wc -l <missing.txt)
count=0
while read -r line; do
  ((progress = (((count)) * 100) / num_lines))
  printf "\rProgress: %d%%" "$progress"
  aws lambda invoke --function-name scraper --invocation-type Event --cli-binary-format raw-in-base64-out --payload "{ \"page\": $((line)) }" /dev/stdout >/dev/null
  count=$((count + 1))
done <missing.txt

printf "\n"
