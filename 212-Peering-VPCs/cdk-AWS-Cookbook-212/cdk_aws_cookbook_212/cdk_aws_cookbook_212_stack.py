from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core,
)


class CdkAwsCookbook212Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
            name="isolated_subnets",
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            cidr_mask=24
        )

        # create VPCs
        vpc1 = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC1-212',
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

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

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

        core.CfnOutput(
            self,
            'VPC1Id',
            value=vpc1.vpc_id
        )

        core.CfnOutput(
            self,
            'Instance1Id',
            value=instance1.instance_id
        )

        core.CfnOutput(
            self,
            'Instance2Id',
            value=instance2.instance_id
        )

        core.CfnOutput(
            self,
            'Instance1Ip',
            value=instance1.instance_private_ip
        )

        core.CfnOutput(
            self,
            'Instance2Ip',
            value=instance2.instance_private_ip
        )

        core.CfnOutput(
            self,
            'Instance1SG',
            value=instance1.connections.security_groups[0].security_group_id
        )

        core.CfnOutput(
            self,
            'Instance2SG',
            value=instance2.connections.security_groups[0].security_group_id
        )

        core.CfnOutput(
            self,
            'VPC2Id',
            value=vpc2.vpc_id
        )

        vpc1_subnet_list = vpc1.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        core.CfnOutput(
            self,
            'Vpc1SubnetRtId',
            value=vpc1_subnet_list.subnets[0].route_table.route_table_id
        )

        vpc2_subnet_list = vpc2.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        core.CfnOutput(
            self,
            'Vpc2SubnetRtId',
            value=vpc2_subnet_list.subnets[0].route_table.route_table_id
        )

        core.CfnOutput(
            self,
            'VPC1Cidr',
            value=vpc1.vpc_cidr_block
        )

        core.CfnOutput(
            self,
            'VPC2Cidr',
            value=vpc2.vpc_cidr_block
        )
