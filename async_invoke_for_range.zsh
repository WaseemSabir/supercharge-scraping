#!/bin/zsh

# Simple script that invokes the lambda function async for a given range.
# Sample Usage:
# Above line invokes the function from 101 page to 10000
#           ./async_invoke_for_range.zsh 101 10000
start=$1
end=$2
total=$(($end - $start + 1))
progress=0

for i in $(seq $start $end); do
  aws lambda invoke --function-name scraper --invocation-type Event --cli-binary-format raw-in-base64-out --payload "{ \"page\": $i }" /dev/stdout >/dev/null

  # Update progress bar
  ((progress = (i - $start) * 100 / $total))
  printf "\r[%-100s] %d%%" $(printf "%-100s" "#" | tr ' ' '#') $progress
done

printf "\n"
