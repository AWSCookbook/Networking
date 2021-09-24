#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_206.cdk_aws_cookbook_206_stack import CdkAwsCookbook206Stack


app = cdk.App()
CdkAwsCookbook206Stack(app, "cdk-aws-cookbook-206")

app.synth()
