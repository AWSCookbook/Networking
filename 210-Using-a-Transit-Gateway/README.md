# Enabling Transitive Cross-VPC Connections Using Transit Gateway

## Preparation
### This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “210-Using-a-Transit-Gateway/cdk-AWS-Cookbook-210” directory and follow the subsequent steps: 

```
cd 210-Using-a-Transit-Gateway/cdk-AWS-Cookbook-210
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### For this recipe, you will need to create some modified environment variables to use:
```
ATTACHMENT_SUBNETS_VPC_1=$(echo ${ATTACHMENT_SUBNETS_VPC_1} | tr -d ',"')
ATTACHMENT_SUBNETS_VPC_2=$(echo ${ATTACHMENT_SUBNETS_VPC_2} | tr -d ',"')
ATTACHMENT_SUBNETS_VPC_3=$(echo ${ATTACHMENT_SUBNETS_VPC_3} | tr -d ',"')
```

## Clean up 
### Delete the Transit Gateway attachments. These take a moment to delete. 
```
aws ec2 delete-transit-gateway-vpc-attachment \
--transit-gateway-attachment-id $TGW_ATTACH_1

aws ec2 delete-transit-gateway-vpc-attachment \
--transit-gateway-attachment-id $TGW_ATTACH_2

aws ec2 delete-transit-gateway-vpc-attachment \
--transit-gateway-attachment-id $TGW_ATTACH_3
```

### After the Transit Gateway attachments have been deleted, delete the Transit Gateway 
```
aws ec2 delete-transit-gateway --transit-gateway-id $TGW_ID
```

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:
```
python helper.py --unset
```

### Unset your manually created environment variables
```
unset TRAN_GW_RT
unset TGW_ID
unset ATTACHMENT_SUBNETS_VPC_1
unset ATTACHMENT_SUBNETS_VPC_2
unset ATTACHMENT_SUBNETS_VPC_3
unset NAT_GW_ID_1
unset NAT_GW_ID_2
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:
```
cdk destroy && deactivate && rm -r .venv/ && cd ../..
```
