# Script for those who need to access security groups and set ip frequently due to dynamic local IP.


## Requirements:
 * Python
 
 * Boto3 (AWS SDK)

## Configuration

Having the requirements installed, just configure your account credentials in user / .aws / credentials

[client]

 aws_access_key_id = XXXXXXXXXXXX
 
 aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXX
 
 region = us-east-1

## Execution
And when executing the script, just set the security group or groups and put a description to track the old ip at the time of refresh and the group will not be polluted.

`securities_groups = ["sg-XXXXXXXXXXXXX"]`

` aws = Aws('client')`

`aws.refresh_ip(securities_groups, "description")`