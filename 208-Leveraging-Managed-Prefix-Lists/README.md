# Simplifying Management of CIDRs in Security Groups with Prefix Lists
## Preparation
### This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “208-Leveraging-Managed-Prefix-Lists/cdk-AWS-Cookbook-208” directory and follow the subsequent steps: 

```
cd 208-Leveraging-Managed-Prefix-Lists/cdk-AWS-Cookbook-208
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-208” directory):

`cd ..`

## Clean up 
### Go to the cdk-AWS-Cookbook-208 directory:

`cd cdk-AWS-Cookbook-208/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Delete the Managed Prefix List:

```
aws ec2 delete-managed-prefix-list \
    --prefix-list-id $PREFIX_LIST_ID
```

### Unset your manually created environment variables:

```
unset PREFIX_LIST_ID
unset MY_IP_4
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

## Hint 
### Run this command with the prefix list version you would like to restore in --previous-version:

```
aws ec2 restore-managed-prefix-list-version \
--prefix-list-id $PREFIX_LIST_ID \
--previous-version 1 --current-version 2
```

### Verify that you can no longer access the EC2 instances:

```
curl -m 2 $INSTANCE_IP_1

curl -m 2 $INSTANCE_IP_2

```

