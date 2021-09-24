#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_210.cdk_aws_cookbook_210_stack import CdkAwsCookbook210Stack


app = cdk.App()
CdkAwsCookbook210Stack(app, "cdk-aws-cookbook-210")

app.synth()
