#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_205.cdk_aws_cookbook_205_stack import CdkAwsCookbook205Stack


app = cdk.App()
CdkAwsCookbook205Stack(app, "cdk-aws-cookbook-205")

app.synth()
