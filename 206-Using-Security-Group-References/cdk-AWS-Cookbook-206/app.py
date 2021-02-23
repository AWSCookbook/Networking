#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_206.cdk_aws_cookbook_206_stack import CdkAwsCookbook206Stack


app = core.App()
CdkAwsCookbook206Stack(app, "cdk-aws-cookbook-206")

app.synth()
