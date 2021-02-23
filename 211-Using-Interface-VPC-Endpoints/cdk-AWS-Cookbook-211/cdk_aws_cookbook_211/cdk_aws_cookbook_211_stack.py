from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core,
)


class CdkAwsCookbook211Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
            name="ISOLATED",
            subnet_type=ec2.SubnetType.ISOLATED,
            cidr_mask=24
        )

        # create VPC
        vpc1 = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC1-211',
            cidr='10.10.0.0/23',
            subnet_configuration=[isolated_subnets]
        )

        vpc1.add_interface_endpoint(
            'VPC1SSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc1.add_interface_endpoint(
            'VPC1EC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc1.add_interface_endpoint(
            'VPC1SSMMessagedInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc2 = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC2-211',
            cidr='10.10.0.0/23',
            subnet_configuration=[isolated_subnets]
        )

        VPC2SSMInterfaceEndpoint = vpc2.add_interface_endpoint(
            'VPC2SSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc2.add_interface_endpoint(
            'VPC2EC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc2.add_interface_endpoint(
            'VPC2SSMMessagedInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
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
            'VPC2Id',
            value=vpc2.vpc_id
        )

        core.CfnOutput(
            self,
            'Instance1ID',
            value=instance1.instance_id
        )

        core.CfnOutput(
            self,
            'Instance2ID',
            value=instance2.instance_id
        )

        vpc1_isoalted_subnets = vpc1.select_subnets(subnet_type=ec2.SubnetType.ISOLATED)

        core.CfnOutput(
            self,
            'VPC1Subnets',
            value=', '.join(map(str, vpc1_isoalted_subnets.subnet_ids))
        )
        core.CfnOutput(
            self,
            'VPC2InterfaceEndpointSG',
            value=VPC2SSMInterfaceEndpoint.security_group_id
        )

        vpc2_isolated_subnets_list = vpc2.select_subnets(subnet_type=ec2.SubnetType.ISOLATED)

        core.CfnOutput(
            self,
            'VPC2Subnet1ID',
            value=vpc2_isolated_subnets_list.subnets[0].subnet_id
        )
