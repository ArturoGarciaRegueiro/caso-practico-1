import os
import json
import base64

from todos import decimalencoder
import boto3  
   
dynamodb = boto3.resource('dynamodb')
def translate(event, context):   
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    entry = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }
    
    comprehend = boto3.client(service_name='comprehend', region_name='region')
    text = "It is raining today in Seattle"
    
    print('Calling DetectDominantLanguage')
    print(json.dumps(comprehend.detect_dominant_language(Text = text), sort_keys=True, indent=4))
    print("End of DetectDominantLanguage\n")
    
    response = {
        "statusCode": 200,
        "body": "HY"
    }
    return response