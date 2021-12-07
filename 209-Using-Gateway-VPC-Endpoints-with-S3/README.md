# Controlling Network Access to S3 from your VPC using VPC Endpoints
## Preparation
### This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of the Chapter 2 repo cd to the “209-Using-Gateway-VPC-Endpoints-with-S3/cdk-AWS-Cookbook-209” directory and follow the subsequent steps: 

```shell
cd 209-Using-Gateway-VPC-Endpoints-with-S3/cdk-AWS-Cookbook-209/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

```
python helper.py
```

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-209” directory):

`cd ..`



## Clean up 

### Delete the VPC Endpoint:

`aws ec2 delete-vpc-endpoints --vpc-endpoint-ids $END_POINT_ID`

### Go to the cdk-AWS-Cookbook-209 directory:

`cd cdk-AWS-Cookbook-209/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset your manually created environment variables:

`unset END_POINT_ID`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
