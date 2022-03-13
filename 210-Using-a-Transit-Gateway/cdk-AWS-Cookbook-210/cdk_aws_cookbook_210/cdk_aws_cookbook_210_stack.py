from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
)


class CdkAwsCookbook210Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        attachments_subnets = ec2.SubnetConfiguration(
                name="ATTACHMENTS",
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                cidr_mask=28)

        isolated_subnets = ec2.SubnetConfiguration(
                name="ISOLATED",
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                cidr_mask=28)

        public_subnets = ec2.SubnetConfiguration(
                name="PUBLIC",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=28)

        private_subnets = ec2.SubnetConfiguration(
                name="PRIVATE",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                cidr_mask=28)

        # create VPC
        vpc1 = ec2.Vpc(
            self,
            'AWS-Cookbook-210-VPC1',
            cidr='10.10.0.0/26',
            subnet_configuration=[isolated_subnets, attachments_subnets]
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
            'AWS-Cookbook-210-VPC2',
            cidr='10.10.0.128/25',
            subnet_configuration=[public_subnets, private_subnets, isolated_subnets, attachments_subnets]
        )

        vpc2.add_interface_endpoint(
            'VPC2SSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc2.add_interface_endpoint(
            'VPC2EC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )
        vpc2.add_interface_endpoint(
            'VPC2SSMMessagedInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc3 = ec2.Vpc(
            self,
            'AWS-Cookbook-210-VPC3',
            cidr='10.10.0.64/26',
            subnet_configuration=[isolated_subnets, attachments_subnets]
        )

        vpc3.add_interface_endpoint(
            'VPC3SSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc3.add_interface_endpoint(
            'VPC3EC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )
        vpc3.add_interface_endpoint(
            'VPC3SSMMessagedInterfaceEndpoint',
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

        security_group_instance1 = ec2.SecurityGroup(
            self,
            "Instance1SG",
            vpc=vpc1,
            allow_all_outbound=True
        )
        security_group_instance1.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.all_icmp()
        )

        instance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc1,
            security_group=security_group_instance1
        )

        security_group_instance2 = ec2.SecurityGroup(
            self,
            "Instance2SG",
            vpc=vpc2,
            allow_all_outbound=True
        )
        security_group_instance2.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.all_icmp()
        )

        instance2 = ec2.Instance(
            self,
            "Instance2",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc2,
            security_group=security_group_instance2
        )

        security_group_instance3 = ec2.SecurityGroup(
            self,
            "Instance3SG",
            vpc=vpc3,
            allow_all_outbound=True
        )
        security_group_instance3.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.all_icmp()
        )

        instance3 = ec2.Instance(
            self,
            "Instance3",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc3,
            security_group=security_group_instance3
        )

        # outputs

        CfnOutput(
            self,
            'VpcId1',
            value=vpc1.vpc_id
        )

        CfnOutput(
            self,
            'VpcId2',
            value=vpc2.vpc_id
        )

        CfnOutput(
            self,
            'VpcId3',
            value=vpc3.vpc_id
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
            'InstanceId3',
            value=instance3.instance_id
        )

        vpc1_attachment_subnets = vpc1.select_subnets(subnet_group_name="ATTACHMENTS")

        CfnOutput(
            self,
            'AttachmentSubnetsVpc1',
            value=', '.join(map(str, vpc1_attachment_subnets.subnet_ids))
        )

        vpc2_attachment_subnets = vpc2.select_subnets(subnet_group_name="ATTACHMENTS")

        CfnOutput(
            self,
            'AttachmentSubnetsVpc2',
            value=', '.join(map(str, vpc2_attachment_subnets.subnet_ids))
        )

        vpc3_attachment_subnets = vpc3.select_subnets(subnet_group_name="ATTACHMENTS")

        CfnOutput(
            self,
            'AttachmentSubnetsVpc3',
            value=', '.join(map(str, vpc3_attachment_subnets.subnet_ids))
        )

        vpc1_isolated_subnets_list = vpc1.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        CfnOutput(
            self,
            'Vpc1RtId1',
            value=vpc1_isolated_subnets_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'Vpc1RtId2',
            value=vpc1_isolated_subnets_list.subnets[1].route_table.route_table_id
        )

        vpc2_public_subnets_list = vpc2.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        CfnOutput(
            self,
            'Vpc2PublicSubnetId1',
            value=vpc2_public_subnets_list.subnets[0].subnet_id
        )

        CfnOutput(
            self,
            'Vpc2PublicSubnetId2',
            value=vpc2_public_subnets_list.subnets[1].subnet_id
        )

        CfnOutput(
            self,
            'Vpc2PublicRtId1',
            value=vpc2_public_subnets_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'Vpc2PublicRtId2',
            value=vpc2_public_subnets_list.subnets[1].route_table.route_table_id
        )

        vpc2_isolated_subnets_list = vpc2.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)

        CfnOutput(
            self,
            'Vpc2RtId1',
            value=vpc2_isolated_subnets_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'Vpc2RtId2',
            value=vpc2_isolated_subnets_list.subnets[1].route_table.route_table_id
        )

        vpc3_isolated_subnets_list = vpc3.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        CfnOutput(
            self,
            'Vpc3RtId1',
            value=vpc3_isolated_subnets_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'Vpc3RtId2',
            value=vpc3_isolated_subnets_list.subnets[1].route_table.route_table_id
        )

        vpc2_attachment_subnets_list = vpc2.select_subnets(subnet_group_name="ATTACHMENTS")

        CfnOutput(
            self,
            'Vpc2AttachRtId1',
            value=vpc2_attachment_subnets_list.subnets[0].route_table.route_table_id
        )

        CfnOutput(
            self,
            'Vpc2AttachRtId2',
            value=vpc2_attachment_subnets_list.subnets[1].route_table.route_table_id
        )
