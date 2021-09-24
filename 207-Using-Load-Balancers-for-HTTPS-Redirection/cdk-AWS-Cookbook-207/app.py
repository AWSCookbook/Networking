#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_207.cdk_aws_cookbook_207_stack import CdkAwsCookbook207Stack


app = cdk.App()
CdkAwsCookbook207Stack(app, "cdk-aws-cookbook-207")

app.synth()
