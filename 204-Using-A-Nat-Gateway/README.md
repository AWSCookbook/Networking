# Using a NAT Gateway for Outbound Internet Access from Private Subnets
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “204-Using-A-Nat-Gateway/cdk-AWS-Cookbook-204” directory and follow the subsequent steps: 

```
cd 204-Using-A-Nat-Gateway/cdk-AWS-Cookbook-204/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```
### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`


## Clean up 
### Delete the NAT gateway that you created (this may take up to 1 minute to delete):

`aws ec2 delete-nat-gateway --nat-gateway-id $NAT_GATEWAY_ID`

### Wait until the NAT gateway has reached the “deleted” state:
```
aws ec2 describe-nat-gateways --nat-gateway-id $NAT_GATEWAY_ID \
    --output text --query NatGateways[0].State
```

### Release the Elastic IP address that you created:

`aws ec2 release-address --allocation-id $ALLOCATION_ID`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:
```
unset ALLOCATION_ID
unset NAT_GATEWAY_ID
```
### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
