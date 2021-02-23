from aws_cdk import (
    aws_ec2 as ec2,
    core,
)


class CdkAwsCookbook205Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
            name="Public",
            subnet_type=ec2.SubnetType.ISOLATED,
            cidr_mask=24
        )

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            cidr='10.10.0.0/23',
            subnet_configuration=[isolated_subnets]
        )

        amzn_linux_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        instance1_sg = ec2.SecurityGroup(
            self,
            'instance1_sg',
            vpc=vpc
        )

        instance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=amzn_linux_ami,
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
            machine_image=amzn_linux_ami,
            vpc=vpc,
            security_group=instance2_sg,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[vpc.isolated_subnets[1]]
            )
        )

        # outputs

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
            'Instance1SgId',
            value=instance1_sg.security_group_id
        )

        core.CfnOutput(
            self,
            'Instance2SgId',
            value=instance2_sg.security_group_id
        )
