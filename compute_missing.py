"""
The lambda function stores the scraped data to S3 bucket, such that p_i.json represent data of ith page.
See lambda_scraper.py for detail.

This script syncs the data of S3 Bucket to local storage (in this folder) by using AWS Cli, see sync_s3.zsh.
It then computes which pages are still not scraped (as they would not be present in data) and writes the output
to missing.txt file, so that it can be invoked again.
Beware that these pages might still be in queue.
"""

import os
from subprocess import call

script_name = "sync_s3.zsh"
dir_name_in_s3 = "output/"

# Sync data to local storage
rc = call(f"./{script_name}")

# Compute which pages are still missing.
start, end = 1, 3421
arr = os.listdir(dir_name_in_s3)
file_names = [filename.split('.')[0] for filename in arr]
file_numbers = [int(fn.split('_')[-1]) for fn in file_names]

file_numbers_lookup = {
    num: True
    for num in file_numbers
}

missing = []
for i in range(1, end + 1):
    if not file_numbers_lookup.get(i):
        missing.append(str(i))

# Dump the output to a TXT file
with open('missing.txt', mode='wt', encoding='utf-8') as f:
    f.write('\n'.join(missing))

print(f"‼️Currently missing numbers: {len(missing)}")
print(f"✅Done: {(end - start + 1) - len(missing)}")
