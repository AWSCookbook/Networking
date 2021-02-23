from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    core,
)


class CdkAwsCookbook207Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            cidr='10.10.0.0/21',
        )

        fargate_service_security_group = ec2.SecurityGroup(
            self,
            'fargate_service_security_group',
            description='Security Group for the Fargate Service',
            allow_all_outbound=True,
            vpc=vpc
        )

        # create ECS Cluster
        ecs_cluster = ecs.Cluster(
            self,
            'AWS-Cookbook-EcsCluster',
            cluster_name='awscookbook207',
            vpc=vpc
        )

        FargateTask = ecs.FargateTaskDefinition(
            self,
            'FargateTask',
            cpu=256,
            memory_limit_mib=512,
        )

        ContainerDef = ecs.ContainerDefinition(
            self,
            'ContainerDef',
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            task_definition=FargateTask,
        )

        ContainerDef.add_port_mappings(
            ecs.PortMapping(
                container_port=80
            )
        )

        ecs.FargateService(
            self,
            'awscookbook207Service',
            cluster=ecs_cluster,
            task_definition=FargateTask,
            assign_public_ip=False,
            desired_count=2,
            enable_ecs_managed_tags=False,
            # health_check_grace_period=core.Duration.seconds(60),
            max_healthy_percent=100,
            min_healthy_percent=0,
            platform_version=ecs.FargatePlatformVersion('LATEST'),
            security_group=fargate_service_security_group,
            service_name='awscookbook207Service',
            vpc_subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType('PRIVATE')
            )
        )

        # outputs

        core.CfnOutput(
            self,
            'VPCId',
            value=vpc.vpc_id
        )

        core.CfnOutput(
            self,
            'ECSClusterName',
            value=ecs_cluster.cluster_name
        )

        public_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        core.CfnOutput(
            self,
            'VPCPublicSubnets',
            value=', '.join(map(str, public_subnets.subnet_ids))
        )

        core.CfnOutput(
            self,
            'AppSgId',
            value=fargate_service_security_group.security_group_id
        )
