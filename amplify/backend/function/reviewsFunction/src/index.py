import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import urllib.parse

dynamodb = boto3.resource('dynamodb')
review_table = dynamodb.Table('Review-pr6ldw4tmzejjoqjxwtlfg2iem-dev')

def decimal_default(obj):
    """Convertit les objets Decimal en float pour la sérialisation JSON"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    try:
        # Récupérer l'ID du restaurant depuis les paramètres de chemin
        restaurant_id = event['pathParameters']['id']
        restaurant_id = urllib.parse.unquote(restaurant_id)
        
        # Récupérer les avis du restaurant
        response = review_table.query(
            IndexName='byRestaurant',
            KeyConditionExpression=Key('restaurant_id').eq(restaurant_id)
        )
        reviews = response.get('Items', [])
        
        # Supprimer les champs word_cloud des avis
        cleaned_reviews = []
        for review in reviews:
            cleaned_review = {k: v for k, v in review.items() if k not in ['word_cloud']}
            cleaned_reviews.append(cleaned_review)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(cleaned_reviews, default=decimal_default)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'error': str(e)})
        }