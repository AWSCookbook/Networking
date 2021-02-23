#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_212.cdk_aws_cookbook_212_stack import CdkAwsCookbook212Stack


app = core.App()
CdkAwsCookbook212Stack(app, "cdk-aws-cookbook-212")

app.synth()
