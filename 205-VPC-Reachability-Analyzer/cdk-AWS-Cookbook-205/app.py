#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_205.cdk_aws_cookbook_205_stack import CdkAwsCookbook205Stack


app = core.App()
CdkAwsCookbook205Stack(app, "cdk-aws-cookbook-205")

app.synth()
