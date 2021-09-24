#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_208.cdk_aws_cookbook_208_stack import CdkAwsCookbook208Stack


app = cdk.App()
CdkAwsCookbook208Stack(app, "cdk-aws-cookbook-208")

app.synth()
