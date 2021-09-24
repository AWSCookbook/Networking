# Granting Dynamic Access by Referencing Security Groups
## Preparation
### This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “205-Using-Security-Group-References/cdk-AWS-Cookbook-205” directory and follow the subsequent steps: 

```
cd 205-Using-Security-Group-References/cdk-AWS-Cookbook-205/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### TWait for the cdk deploy command to complete. 

### TWe created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`



## Clean up 
### Detach the security groups you created from each instance and attach the VPC default security group (so that you can delete the security groups in the next step):

```
aws ec2 modify-instance-attribute --instance-id \
$INSTANCE_ID_1 --groups $DEFAULT_VPC_SECURITY_GROUP

aws ec2 modify-instance-attribute --instance-id \
$INSTANCE_ID_2 --groups $DEFAULT_VPC_SECURITY_GROUP
```

### Delete the security group that you created:

`aws ec2 delete-security-group --group-id $SG_ID`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:

```
unset SG_ID
unset INSTANCE_ID_3
unset INSTANCE_PROFILE
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

## Hint
```
INSTANCE_ID_3=$(aws ec2 run-instances \
--image-id $AMZNLINUXAMI --count 1 \
--instance-type t3.nano --security-group-ids $SG_ID \
--subnet-id $VPC_ISOLATED_SUBNET_1 \
--output text --query Instances[0].InstanceId)
```

### Retrieve the IAM Instance Profile Arn for Instance2 so that you can associate it with your new instance. This will allow the instance to register with SSM:

```
INSTANCE_PROFILE=$(aws ec2 describe-iam-instance-profile-associations \
--filter "Name=instance-id,Values=$INSTANCE_ID_2" \
--output text --query IamInstanceProfileAssociations[0].IamInstanceProfile.Arn)
```

### Associate the IAM Instance Profile with Instance3:

```
aws ec2 associate-iam-instance-profile \
    --instance-id $INSTANCE_ID_3 \
    --iam-instance-profile Arn=$INSTANCE_PROFILE
```

### Reboot the instance to have it register with SSM:

`aws ec2 reboot-instances --instance-ids $INSTANCE_ID_3`

### Once that is complete you can connect to it using SSM Session Manager:

`aws ssm start-session --target $INSTANCE_ID_3`

