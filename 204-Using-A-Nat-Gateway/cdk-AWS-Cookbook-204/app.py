#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_204.cdk_aws_cookbook_204_stack import CdkAwsCookbook204Stack


app = cdk.App()
CdkAwsCookbook204Stack(app, "cdk-aws-cookbook-204")

app.synth()
