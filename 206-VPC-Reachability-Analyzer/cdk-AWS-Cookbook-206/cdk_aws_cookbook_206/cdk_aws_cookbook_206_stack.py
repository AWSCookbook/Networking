from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
)


class CdkAwsCookbook206Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
            name="Isolated",
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            cidr_mask=24
        )

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            cidr='10.10.0.0/23',
            subnet_configuration=[isolated_subnets]
        )

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

        vpc.add_gateway_endpoint(
            's3GateWayEndPoint',
            service=ec2.GatewayVpcEndpointAwsService('s3'),
            subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)],
        )

        iam_role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        instance1_sg = ec2.SecurityGroup(
            self,
            'instance1_sg',
            vpc=vpc
        )

        instance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc,
            security_group=instance1_sg,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[vpc.isolated_subnets[0]]
            )
        )

        instance2_sg = ec2.SecurityGroup(
            self,
            'instance2_sg',
            vpc=vpc
        )

        instance2 = ec2.Instance(
            self,
            "Instance2",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc,
            security_group=instance2_sg,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[vpc.isolated_subnets[1]]
            )
        )

        # outputs

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
            'InstanceSgId1',
            value=instance1_sg.security_group_id
        )

        CfnOutput(
            self,
            'InstanceSgId2',
            value=instance2_sg.security_group_id
        )
