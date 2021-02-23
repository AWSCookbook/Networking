#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_207.cdk_aws_cookbook_207_stack import CdkAwsCookbook207Stack


app = core.App()
CdkAwsCookbook207Stack(app, "cdk-aws-cookbook-207")

app.synth()
