# Redirecting HTTP Traffic to HTTPS with an Application Load Balancer

## Preparation Steps
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

In the root of this Chapter’s repo cd to the “207-Using-Load-Balancers-for-HTTPS-Redirections/cdk-AWS-Cookbook-207” directory:
```
cd 207-Using-Load-Balancers-for-HTTPS-Redirection/cdk-AWS-Cookbook-207/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip 
pip install -r requirements.txt
cdk deploy
```

Wait for the cdk deploy command to complete. 

We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

Move back up a directory to perform the steps for the recipe: 
```
cd ..
```
### For this recipe, you will need to create a modified environment variable from the output:

`VPC_PUBLIC_SUBNETS=$(echo ${VPC_PUBLIC_SUBNETS} | tr -d ',"')`


## Clean up 

### Delete the ALB 
```
aws elbv2 delete-load-balancer \
    --load-balancer-arn $LOAD_BALANCER_ARN
```
### Delete the Certificate from 
```
aws iam delete-server-certificate --server-certificate-name AWSCookbook207
```

### Delete the target group
```
aws elbv2 delete-target-group \
    --target-group-arn $TARGET_GROUP
```

### Revoke the security group ingress rule 
```
aws ec2 revoke-security-group-ingress \
    --protocol tcp --port 80 \
    --source-group $ALB_SG_ID \
    --group-id $APP_SG_ID
```

### Delete the Security Group 
```
aws ec2 delete-security-group --group-id $ALB_SG_ID
```

### Go to the cdk-AWS-Cookbook-207 directory:

```
cd cdk-AWS-Cookbook-207/
```

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:

```
unset TASK_ARN
unset LOAD_BALANCER_ARN
unset TARGET_GROUP
unset ALB_SG_ID
unset CERT_ARN
unset CONTAINER_IP
unset HTTPS_LISTENER_ARN
unset LOAD_BALANCER_DNS
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
