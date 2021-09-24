import os
import boto3
import argparse


def change_case(str):
    res = [str[0]]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            res.append('_')
            res.append(c)
        elif c in ('123456789'):
            res.append('_')
            res.append(c)
        else:
            res.append(c.upper())

    return ''.join(res)


parser = argparse.ArgumentParser(description="Generate commands to set and unset environment variables")
parser.add_argument('--unset', action='store_true', help="Generate commands to unset environment variables by setting this flag")

args = parser.parse_args()

os.environ['AWS_DEFAULT_REGION'] = os.environ.get('AWS_REGION')

cfn = boto3.client('cloudformation')
stackname = os.path.basename(os.getcwd()).lower()
response = cfn.describe_stacks(StackName=stackname)
unsets = []
sets = []

outputs = response["Stacks"][0]["Outputs"]
print("Copy and paste the commands below into your terminal")
print("")
for output in outputs:
    if ', ' in output["OutputValue"]:
        sets.append(change_case(output["OutputKey"]) + "='" + ', '.join('"{}"'.format(word) for word in output["OutputValue"].split(", ")) + "'")
    else:
        sets.append(change_case(output["OutputKey"]) + "='" + output["OutputValue"] + "'")
    unsets.append("unset " + change_case(output["OutputKey"]))

if (args.unset):
    print('\n'.join(map(str, unsets)))
else:
    print('\n'.join(map(str, sets)))

print("")
