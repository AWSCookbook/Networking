#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_203.cdk_aws_cookbook_203_stack import CdkAwsCookbook203Stack


app = core.App()
CdkAwsCookbook203Stack(app, "cdk-aws-cookbook-203")

app.synth()
