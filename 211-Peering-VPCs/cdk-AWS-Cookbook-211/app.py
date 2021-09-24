#!/usr/bin/env python3
import aws_cdk as cdk

from cdk_aws_cookbook_211.cdk_aws_cookbook_211_stack import CdkAwsCookbook211Stack


app = cdk.App()
CdkAwsCookbook211Stack(app, "cdk-aws-cookbook-211")

app.synth()
