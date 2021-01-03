import os
import json
import base64
import boto3  

from todos import decimalencoder 
   
dynamodb = boto3.resource('dynamodb')
#Create client for comprehend service
comprehend = boto3.client('comprehend') 
#Create client for translate service
translator = boto3.client('translate') 
def translate(event, context):   
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # Entry from table
    text = result['Item']['text'] 
    
    #detect dominant language
    comprehend_response = comprehend.detect_dominant_language( Text=text) 
    language = comprehend_response['Languages'][0]['LanguageCode'];
    
    #translate from dominant language to target language
    translated = translator.translate_text(Text=text, SourceLanguageCode=language, TargetLanguageCode=event['pathParameters']['language'])
    result['Item']['text'] = translated.get('TranslatedText')
    
    
    
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }
    return response