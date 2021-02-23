#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_204.cdk_aws_cookbook_204_stack import CdkAwsCookbook204Stack


app = core.App()
CdkAwsCookbook204Stack(app, "cdk-aws-cookbook-204")

app.synth()
