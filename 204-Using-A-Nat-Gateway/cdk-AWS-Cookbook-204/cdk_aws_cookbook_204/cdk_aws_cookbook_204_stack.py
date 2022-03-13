from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
)

class CdkAwsCookbook204Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        public_subnets = ec2.SubnetConfiguration(
                name="Public",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24)

        tier2_subnets = ec2.SubnetConfiguration(
                name="Tier2",
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                cidr_mask=24)

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            max_azs=2,
            cidr='10.10.0.0/22',
            subnet_configuration=[public_subnets, tier2_subnets]
        )

        tier2_subnet_list = vpc.select_subnets(subnet_group_name="Tier2")

        # -------- Begin EC2 Helper ---------
        vpc.add_interface_endpoint(
            'VPCSSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc.add_interface_endpoint(
            'VPCEC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc.add_interface_endpoint(
            'VPCSSMMessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        iam_role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        instance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[tier2_subnet_list.subnets[0]]
            )
        )

        instance2 = ec2.Instance(
            self,
            "Instance2",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[tier2_subnet_list.subnets[0]]
            )
        )

        CfnOutput(
            self,
            'InstanceId1',
            value=instance1.instance_id
        )

        CfnOutput(
            self,
            'InstanceId2',
            value=instance2.instance_id
        )
        # -------- End EC2 Helper ---------

        # outputs

        CfnOutput(
            self,
            'VpcId',
            value=vpc.vpc_id
        )

        public_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        CfnOutput(
            self,
            'VpcPublicSubnet1',
            value=public_subnets.subnets[0].subnet_id
        )

        CfnOutput(
            self,
            'PrivateRtId1',
            value=tier2_subnet_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'PrivateRtId2',
            value=tier2_subnet_list.subnets[1].route_table.route_table_id
        )
