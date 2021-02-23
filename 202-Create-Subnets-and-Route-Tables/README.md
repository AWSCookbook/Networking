Create Subnets and Route Tables
===============================


aws ec2 create-vpc --cidr-block 172.16.0.0/16

aws ec2 create-vpc
--cidr-block <value>
[--amazon-provided-ipv6-cidr-block | --no-amazon-provided-ipv6-cidr-block]
[--ipv6-pool <value>]
[--ipv6-cidr-block <value>]
[--dry-run | --no-dry-run]
[--instance-tenancy <value>]
[--ipv6-cidr-block-network-border-group <value>]
[--tag-specifications <value>]
[--cli-input-json <value>]
[--generate-cli-skeleton <value>]

{
    "Vpc": {
        "CidrBlock": "172.16.0.0/16",
        "DhcpOptionsId": "dopt-981c6ee2",
        "State": "pending",
        "VpcId": "vpc-040f5eccda552bf8e",
        "OwnerId": "664865145641",
        "InstanceTenancy": "default",
        "Ipv6CidrBlockAssociationSet": [],
        "CidrBlockAssociationSet": [
            {
                "AssociationId": "vpc-cidr-assoc-0283bf708b89675c6",
                "CidrBlock": "172.16.0.0/16",
                "CidrBlockState": {
                    "State": "associated"
                }
            }
        ],
        "IsDefault": false
    }
}

Set your VpcID to an environment variable for the next steps:
export VpcID="vpc-040f5eccda552bf8e"

Create subnets, /24 for each (NOTE: 252 addresses, .1 and .2 .3 and .255 are AWS reserved)

.0: Network address.
.1: Reserved by AWS for the VPC router.
.2: Reserved by AWS. The IP address of the DNS server is the base of the VPC network range plus two. For VPCs with multiple CIDR blocks, the IP address of the DNS server is located in the primary CIDR. We also reserve the base of each subnet range plus two for all CIDR blocks in the VPC. For more information, see Amazon DNS server.
.3: Reserved by AWS for future use.
.255: Network broadcast address. We do not support broadcast in a VPC, therefore we reserve this address.
Source: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html


aws ec2 create-subnet
[--tag-specifications <value>]
[--availability-zone <value>]
[--availability-zone-id <value>]
--cidr-block <value>
[--ipv6-cidr-block <value>]
[--outpost-arn <value>]
--vpc-id <value>
[--dry-run | --no-dry-run]
[--cli-input-json <value>]
[--generate-cli-skeleton <value>]

aws ec2 create-subnet --vpc-id $VpcID --cidr-block 172.16.1.0/24 --availability-zone ${AWS_REGION}a
aws ec2 create-subnet --vpc-id $VpcID --cidr-block 172.16.2.0/24 --availability-zone ${AWS_REGION}b
aws ec2 create-subnet --vpc-id $VpcID--cidr-block 172.16.3.0/24 --availability-zone ${AWS_REGION}a
aws ec2 create-subnet --vpc-id $VpcID --cidr-block 172.16.4.0/24 --availability-zone ${AWS_REGION}b
aws ec2 create-subnet --vpc-id $VpcID --cidr-block 172.16.5.0/24 --availability-zone ${AWS_REGION}a
aws ec2 create-subnet --vpc-id $VpcID --cidr-block 172.16.6.0/24 --availability-zone ${AWS_REGION}b

{
    "Subnet": {
        "AvailabilityZone": "us-east-1a",
        "AvailabilityZoneId": "use1-az4",
        "AvailableIpAddressCount": 251,
        "CidrBlock": "172.16.1.0/24",
        "DefaultForAz": false,
        "MapPublicIpOnLaunch": false,
        "State": "available",
        "SubnetId": "subnet-039b579b168762fbf",
        "VpcId": "vpc-040f5eccda552bf8e",
        "OwnerId": "664865145641",
        "AssignIpv6AddressOnCreation": false,
        "Ipv6CidrBlockAssociationSet": [],
        "SubnetArn": "arn:aws:ec2:${AWS_REGION}:664865145641:subnet/subnet-039b579b168762fbf"
    }
}

Create Route Tables

  create-route-table
[--dry-run | --no-dry-run]
--vpc-id <value>
[--tag-specifications <value>]
[--cli-input-json <value>]
[--generate-cli-skeleton <value>]

aws ec2 create-route-table --vpc-id $VpcID
aws ec2 create-route-table --vpc-id $VpcID
aws ec2 create-route-table --vpc-id $VpcID
aws ec2 create-route-table --vpc-id $VpcID

In the output, set the route table IDs to a environment variables:

{
    "RouteTable": {
        ... 
        "RouteTableId": "rtb-c1c8faa6", 
        ...
    }
}

export RT1=
export RT2=
export RT3=
export RT4=

aws ec2 create-route
  create-route
[--destination-cidr-block <value>]
[--destination-ipv6-cidr-block <value>]
[--destination-prefix-list-id <value>]
[--dry-run | --no-dry-run]
[--vpc-endpoint-id <value>]
[--egress-only-internet-gateway-id <value>]
[--gateway-id <value>]
[--instance-id <value>]
[--nat-gateway-id <value>]
[--transit-gateway-id <value>]
[--local-gateway-id <value>]
[--carrier-gateway-id <value>]
[--network-interface-id <value>]
--route-table-id <value>
[--vpc-peering-connection-id <value>]
[--cli-input-json <value>]
[--generate-cli-skeleton <value>]





Cleanup


aws ec2 delete-subnet --subnet-id
aws ec2 delete-subnet --subnet-id
aws ec2 delete-subnet --subnet-id
aws ec2 delete-subnet --subnet-id
aws ec2 delete-subnet --subnet-id
aws ec2 delete-subnet --subnet-id

Delete your route tables:

aws ec2 delete-route-table --route-table-id
aws ec2 delete-route-table --route-table-id
aws ec2 delete-route-table --route-table-id
aws ec2 delete-route-table --route-table-id

Delete your VPC:

aws ec2 delete-vpc --vpc-id


#!/bin/bash
vpc="vpc-xxxxxxxxxxxxx" 
aws ec2 describe-internet-gateways --filters 'Name=attachment.vpc-id,Values='$vpc | grep InternetGatewayId
aws ec2 describe-subnets --filters 'Name=vpc-id,Values='$vpc | grep SubnetId
aws ec2 describe-route-tables --filters 'Name=vpc-id,Values='$vpc | grep RouteTableId
aws ec2 describe-network-acls --filters 'Name=vpc-id,Values='$vpc | grep NetworkAclId
aws ec2 describe-vpc-peering-connections --filters 'Name=requester-vpc-info.vpc-id,Values='$vpc | grep VpcPeeringConnectionId
aws ec2 describe-vpc-endpoints --filters 'Name=vpc-id,Values='$vpc | grep VpcEndpointId
aws ec2 describe-nat-gateways --filter 'Name=vpc-id,Values='$vpc | grep NatGatewayId
aws ec2 describe-security-groups --filters 'Name=vpc-id,Values='$vpc | grep GroupId
aws ec2 describe-instances --filters 'Name=vpc-id,Values='$vpc | grep InstanceId
aws ec2 describe-vpn-connections --filters 'Name=vpc-id,Values='$vpc | grep VpnConnectionId
aws ec2 describe-vpn-gateways --filters 'Name=attachment.vpc-id,Values='$vpc | grep VpnGatewayId
aws ec2 describe-network-interfaces --filters 'Name=vpc-id,Values='$vpc | grep NetworkInterfaceId

# delete route tables
while read -r rt_id ; do
    aws ec2 delete-route-table --route-table-id $rt_id ;
done < <(aws ec2 describe-route-tables --filters 'Name=vpc-id,Values='$vpc_id | \
    jq -r .RouteTables[].RouteTableId)
# delete all vpc subnets
while read -r subnet_id ; do
    aws ec2 delete-subnet --subnet-id "$subnet_id"
done < <(aws ec2 describe-subnets --filters 'Name=vpc-id,Values='$vpc_id | jq -r '.Subnets[].SubnetId')
# delete vpc
# delete the whole vpc
aws ec2 delete-vpc --vpc-id=$vpc_id