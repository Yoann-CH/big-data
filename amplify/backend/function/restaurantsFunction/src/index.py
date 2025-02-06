import json
import boto3
from boto3.dynamodb.conditions import Key
import logging
import os
import traceback

# Configuration du logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        logger.info("Début de l'exécution de la fonction")
        
        # Initialisation DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Restaurant-pr6ldw4tmzejjoqjxwtlfg2iem-dev')
        
        logger.info("Scan de la table DynamoDB")
        response = table.scan()
        items = response.get('Items', [])
        
        logger.info(f"Nombre d'éléments trouvés : {len(items)}")
        
        # Supprimer les champs word_cloud et word_cloud_graph
        cleaned_items = []
        for item in items:
            cleaned_item = {k: v for k, v in item.items() if k not in ['word_cloud', 'wordcloud_graph', 'sentiment_graph']}
            cleaned_items.append(cleaned_item)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps(cleaned_items, default=str)
        }
        
    except Exception as e:
        logger.error(f"ERREUR: {str(e)}")
        logger.error(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Erreur interne du serveur',
                'stackTrace': traceback.format_exc()
            })
        }