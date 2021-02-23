from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core
)


class CdkAwsCookbook208Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
                name="Isolated",
                subnet_type=ec2.SubnetType.ISOLATED,
                cidr_mask=24)

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
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc.add_interface_endpoint(
            'VPCEC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.ISOLATED
            ),
        )

        vpc.add_interface_endpoint(
            'VPCSSMMessagesInterfaceEndpoint',
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

        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            allow_all_outbound=False,
            role=iam_role,
            vpc=vpc,
        )

        ssm_endpoint.connections.allow_from(
            instance.connections, ec2.Port.tcp(443), "Ingress"
        )

        ssmmessages_endpoint.connections.allow_from(
            instance.connections, ec2.Port.tcp(443), "Ingress"
        )

        ec2messages_endpoint.connections.allow_from(
            instance.connections, ec2.Port.tcp(443), "Ingress"
        )

        instance.connections.allow_to(
            ssm_endpoint.connections, ec2.Port.tcp(443), "Egress"
        )

        instance.connections.allow_to(
            ssmmessages_endpoint.connections, ec2.Port.tcp(443), "Egress"
        )

        instance.connections.allow_to(
            ec2messages_endpoint.connections, ec2.Port.tcp(443), "Egress"
        )

        # -------- End EC2 Helper ---------
        # outputs

        core.CfnOutput(
            self,
            'InstanceID',
            value=instance.instance_id
        )
        # -------- End EC2 Helper ---------

        # outputs

        isolated_subnet_list = vpc.select_subnets(subnet_type=ec2.SubnetType.ISOLATED)

        core.CfnOutput(
            self,
            'Sub1RouteTableID',
            value=isolated_subnet_list.subnets[0].route_table.route_table_id
        )

        core.CfnOutput(
            self,
            'InstanceId',
            value=instance.instance_id
        )

        core.CfnOutput(
            self,
            'InstanceSG',
            value=instance.connections.security_groups[0].security_group_id
        )
