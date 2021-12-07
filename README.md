# Chapter 2
## Set and export your default region:

`export AWS_REGION=us-east-1`

## Set your AWS ACCOUNT ID:

`AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)`

## Validate AWS Cli Setup and access:

`aws ec2 describe-instances`
