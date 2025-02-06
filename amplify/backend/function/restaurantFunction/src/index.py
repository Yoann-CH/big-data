import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import urllib.parse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
restaurant_table = dynamodb.Table('Restaurant-pr6ldw4tmzejjoqjxwtlfg2iem-dev')

def decimal_default(obj):
    """Convertit les objets Decimal en float pour la sérialisation JSON"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    try:
        # Récupérer et décoder l'ID du restaurant
        restaurant_id = event['pathParameters']['id']
        restaurant_id = urllib.parse.unquote(restaurant_id)
        
        logger.info(f"Recherche du restaurant avec l'ID: {restaurant_id}")
        
        # Récupérer le restaurant
        response = restaurant_table.get_item(Key={'id': restaurant_id})
        restaurant = response.get('Item')
        
        if not restaurant:
            logger.error(f"Restaurant non trouvé pour l'ID: {restaurant_id}")
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,GET'
                },
                'body': json.dumps({'error': 'Restaurant non trouvé'})
            }
        
        # Nettoyer les données du restaurant
        cleaned_restaurant = {k: v for k, v in restaurant.items() if k not in ['word_cloud']}
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(cleaned_restaurant, default=decimal_default)
        }
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({'error': str(e)})
        }