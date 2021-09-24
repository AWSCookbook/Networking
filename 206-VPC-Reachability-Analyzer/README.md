# Using VPC Reachability Analyzer to Verify and Troubleshoot Network Paths
## Preparation
### This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the  “206-VPC-Reachability-Analyzer/cdk-AWS-Cookbook-206/” directory and follow the subsequent steps: 

```
cd 206-VPC-Reachability-Analyzer/cdk-AWS-Cookbook-206/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`



## Clean up 
### Delete the analyses:

```
aws ec2 delete-network-insights-analysis \
--network-insights-analysis-id $ANALYSIS_ID_1

aws ec2 delete-network-insights-analysis \
--network-insights-analysis-id $ANALYSIS_ID_2
```

### Delete the path:

```
aws ec2 delete-network-insights-path \
--network-insights-path-id $INSIGHTS_PATH_ID
```

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:

```
unset INSIGHTS_PATH_ID
unset ANALYSIS_ID_1
unset ANALYSIS_ID_2
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
