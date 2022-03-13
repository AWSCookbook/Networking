from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
)


class CdkAwsCookbook211Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
            name="isolated_subnets",
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            cidr_mask=24
        )

        # create VPCs
        vpc1 = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC1-211',
            cidr='10.10.0.0/23',
            max_azs=1,
            subnet_configuration=[isolated_subnets]
        )

        vpc1.add_interface_endpoint(
            'VPC1SSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc1.add_interface_endpoint(
            'VPC1EC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )
        vpc1.add_interface_endpoint(
            'VPC1SSMMessagedInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc2 = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC2-209',
            cidr='10.20.0.0/23',
            max_azs=1,
            subnet_configuration=[isolated_subnets]
        )

        ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        iam_role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        instance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc1,
        )

        instance2 = ec2.Instance(
            self,
            "Instance2",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc2,
        )

        # outputs

        CfnOutput(
            self,
            'VpcId1',
            value=vpc1.vpc_id
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

        CfnOutput(
            self,
            'InstanceIp1',
            value=instance1.instance_private_ip
        )

        CfnOutput(
            self,
            'InstanceIp2',
            value=instance2.instance_private_ip
        )

        CfnOutput(
            self,
            'InstanceSg1',
            value=instance1.connections.security_groups[0].security_group_id
        )

        CfnOutput(
            self,
            'InstanceSg2',
            value=instance2.connections.security_groups[0].security_group_id
        )

        CfnOutput(
            self,
            'VpcId2',
            value=vpc2.vpc_id
        )

        vpc1_subnet_list = vpc1.select_subnets(subnet_type=ec2.SubnetType.ISOLATED)

        CfnOutput(
            self,
            'VpcSubnetRtId1',
            value=vpc1_subnet_list.subnets[0].route_table.route_table_id
        )

        vpc2_subnet_list = vpc2.select_subnets(subnet_type=ec2.SubnetType.ISOLATED)

        CfnOutput(
            self,
            'VpcSubnetRtId2',
            value=vpc2_subnet_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'VpcCidr1',
            value=vpc1.vpc_cidr_block
        )

        CfnOutput(
            self,
            'VpcCidr2',
            value=vpc2.vpc_cidr_block
        )
