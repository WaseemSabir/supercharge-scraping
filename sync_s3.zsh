#!/bin/zsh

# Calls simple AWS Cli command to sync S3 Bucket to local storage.
# Add your Bucket's name in place of bucket-name.
aws s3 sync s3://bucket-name .
