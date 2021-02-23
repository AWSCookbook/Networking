#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_210.cdk_aws_cookbook_210_stack import CdkAwsCookbook210Stack


app = core.App()
CdkAwsCookbook210Stack(app, "cdk-aws-cookbook-210")

app.synth()
