import json
import logging
from botocore.config import Config
import os
import boto3

logger = logging.getLogger("Subcategory Pipeline")
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    logger.info("The input event is %s",event)
    
    try:
        uuid = event["uuid"]
        complaint = event["Complaint"]
        input_data = [{
            "modelInput": {
                "Complaint": complaint
            }
        }]
        logger.info("Payload---------")
        logger.info(input_data)
        payload = json.dumps(input_data)
        ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
        runtime= boto3.client('runtime.sagemaker', config=Config(retries={'max_attempts': 0}))
        response = runtime.invoke_endpoint(EndpointName = ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=payload)
        logger.info(response)
        result = json.loads(response['Body'].read().decode())
        logger.info(result)
        result["uuid"] = uuid
        return result
   
    except Exception as exc:
        logger.info(exc)
        logger.error(f"Exception i.e. {str(exc)} has occured.")
        prediction = {'complaint':complaint ,'uuid':uuid,'subcategory': {'null': 'error'}}
        return prediction
