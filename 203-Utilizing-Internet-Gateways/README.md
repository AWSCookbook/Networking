# Connecting Your VPC to the Internet Using an Internet Gateway

## Preparation Steps
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

In the root of this Chapter’s repo cd to the “203-Utilizing-Internet-Gateways/cdk-AWS-Cookbook-203” directory:
```
cd 203-Utilizing-Internet-Gateways/cdk-AWS-Cookbook-203/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip 
pip install -r requirements.txt
cdk deploy
```

Wait for the cdk deploy command to complete. 

We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`



## Clean up 
Disassociate the Elastic IP address from the EC2 Instance:
```
aws ec2 disassociate-address --association-id \
$(aws ec2 describe-addresses \
--allocation-ids $ALLOCATION_ID \
--output text --query Addresses[0].AssociationId)
```

Deallocate the Elastic IP address that you created:

`aws ec2 release-address --allocation-id $ALLOCATION_ID`

Detach the IGW:
```
aws ec2 detach-internet-gateway \
--internet-gateway-id $INET_GATEWAY_ID --vpc-id $VPC_ID
```

Delete the IGW:
```
aws ec2 delete-internet-gateway \
--internet-gateway-id $INET_GATEWAY_ID
```

To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

Unset the environment variable that you created manually:
```
unset INET_GATEWAY_ID
unset ALLOCATION_ID
```

Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

