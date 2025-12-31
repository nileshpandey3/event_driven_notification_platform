#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.dynamodb_stack import DynamoDBStack


app = cdk.App()
DynamoDBStack(app, "PreferencesDynamoDBStack",

    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),)

app.synth()
