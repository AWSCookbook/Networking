#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_211.cdk_aws_cookbook_211_stack import CdkAwsCookbook211Stack


app = core.App()
CdkAwsCookbook211Stack(app, "cdk-aws-cookbook-211")

app.synth()
