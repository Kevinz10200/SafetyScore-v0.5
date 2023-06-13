
import boto3
import os
import json
import processData

access_key = 'AKIATBN6TMNQHELSPP4N'
secret_key = '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'
region_name = 'us-west-1'

# Create the DynamoDB client with the provided access keys and region
dynamodb = boto3.client('dynamodb',
                        region_name=region_name,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)
# AWS DynamoDB details
table_name = 'SafetyScore'
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)

# Upload each row of data to DynamoDB table
# json_data = '{"Date": "12-13-1989", "Person": "TAYTAY", "Score": -13}'

violationsTuple = processData.getViolations() # date:count

# json_data = {"Date": str(violationsTuple[0]), "Person": str(violationsTuple[1]), "Score": int(violationsTuple[2])}

data = {
    "Date": violationsTuple[0],
    "Person": violationsTuple[1],
    "Score": -violationsTuple[2]
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data)

print(repr(json_data))

table.put_item(Item=data)


