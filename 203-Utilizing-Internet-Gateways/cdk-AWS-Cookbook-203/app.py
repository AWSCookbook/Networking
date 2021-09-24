#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_203.cdk_aws_cookbook_203_stack import CdkAwsCookbook203Stack


app = cdk.App()
CdkAwsCookbook203Stack(app, "cdk-aws-cookbook-203")

app.synth()
