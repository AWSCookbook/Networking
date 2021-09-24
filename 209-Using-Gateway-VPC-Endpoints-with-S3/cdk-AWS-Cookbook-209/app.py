#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_209.cdk_aws_cookbook_209_stack import CdkAwsCookbook209Stack


app = cdk.App()
CdkAwsCookbook209Stack(app, "cdk-aws-cookbook-209")

app.synth()
