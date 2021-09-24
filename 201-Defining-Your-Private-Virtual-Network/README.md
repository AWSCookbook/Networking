# Defining Your Private Virtual Network

## Preparation Steps
None


## Clean up 
### Delete the VPC you created:

`aws ec2 delete-vpc --vpc-id $VPC_ID`

### Unset the environment variable that you created manually:

`unset VPC_ID`
