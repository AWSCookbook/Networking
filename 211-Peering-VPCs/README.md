# Peering Two VPCs Together for Inter-VPC Network Communication
## Preparation

### This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the  “211-Peering-VPCs/cdk-AWS-Cookbook-211” directory and follow the subsequent steps: 
```
cd 211-Peering-VPCs/cdk-AWS-Cookbook-211/
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

## Clean up 
### Delete the security group rule 
```
aws ec2 revoke-security-group-ingress \
--protocol icmp --port -1 \
--source-group $INSTANCE_SG_1 \
--group-id $INSTANCE_SG_2
```

### Delete the Peering connection
```
aws ec2 delete-vpc-peering-connection \
--vpc-peering-connection-id $VPC_PEERING_CONNECTION_ID
```

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:
```
python helper.py --unset
```

### Unset your manually created environment variables
```
unset VPC_PEERING_CONNECTION_ID
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:
```
cdk destroy && deactivate && rm -r .venv/ && cd ../..
```
