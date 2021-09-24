# Create Subnets and Route Tables
## Preparation
### Create a VPC
```
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.10.0.0/23 \
--tag-specifications \
'ResourceType=vpc,Tags=[{Key=Name,Value=AWSCookbook202}]' \
--output text --query Vpc.VpcId)
```



## Clean up 
### Delete your subnets:

`aws ec2 delete-subnet --subnet-id $SUBNET_ID_1`

`aws ec2 delete-subnet --subnet-id $SUBNET_ID_2`

### Delete your route table:

`aws ec2 delete-route-table --route-table-id $ROUTE_TABLE_ID`

### Delete your VPC:
`aws ec2 delete-vpc --vpc-id $VPC_ID`

### Unset your manually created environment variables"
```
unset VPC_ID
unset ROUTE_TABLE_ID
unset SUBNET_ID_1
unset SUBNET_ID_2
```
