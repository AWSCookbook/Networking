#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_208.cdk_aws_cookbook_208_stack import CdkAwsCookbook208Stack


app = core.App()
CdkAwsCookbook208Stack(app, "cdk-aws-cookbook-208")

app.synth()
