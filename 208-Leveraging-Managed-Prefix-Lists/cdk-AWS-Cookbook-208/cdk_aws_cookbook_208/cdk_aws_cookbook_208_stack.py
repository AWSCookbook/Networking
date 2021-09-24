from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
)

class CdkAwsCookbook208Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        public_subnets = ec2.SubnetConfiguration(
                name="Public",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24)

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            cidr='10.10.0.0/23',
            subnet_configuration=[public_subnets]
        )

        # -------- Begin EC2 Helper ---------
        ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        user_data = ec2.UserData.for_linux()
        user_data.add_commands('sudo yum -y update',
                               'sudo yum install -y httpd',
                               'sudo systemctl start httpd')

        iam_role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        instance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            user_data=user_data,
            allow_all_outbound=True,
            role=iam_role,
            vpc=vpc,
        )

        #user_data_2_commands = ec2.UserData.for_linux()
        #user_data_2_commands.add_commands("#!/bin/sh")
        #user_data_2_commands.add_commands("yum install httpd -y")
        #user_data_2_commands.add_commands("service httpd start")
        #user_data_2_commands.add_commands("echo \"<html><h1>AWSCookbook App 2 running on $(hostname -f)</h1></html>\" > /var/www/html/index.html")

        instance2 = ec2.Instance(
            self,
            "Instance2",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            user_data=user_data,
            allow_all_outbound=True,
            role=iam_role,
            vpc=vpc,
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
            'InstanceIp1',
            value=instance1.instance_public_ip
        )

        CfnOutput(
            self,
            'InstanceIp2',
            value=instance2.instance_public_ip
        )
