#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_209.cdk_aws_cookbook_209_stack import CdkAwsCookbook209Stack


app = core.App()
CdkAwsCookbook209Stack(app, "cdk-aws-cookbook-209")

app.synth()
