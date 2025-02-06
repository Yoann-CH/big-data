import json
import boto3
from decimal import Decimal
from datetime import datetime
from handlers.yelp_scraper import scrape_search_results, scrape_reviews
from botocore.exceptions import ClientError
from urllib.parse import unquote

dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')

def handler(event, context):
    try:
        restaurant_table = dynamodb.Table('Restaurant-pr6ldw4tmzejjoqjxwtlfg2iem-dev')
        review_table = dynamodb.Table('Review-pr6ldw4tmzejjoqjxwtlfg2iem-dev')
        
        operation = event.get('operation', 'restaurants')
        location = event.get('location', 'Paris')
        max_restaurants = event.get('max_restaurants', 10)
        max_reviews = event.get('max_reviews_per_restaurant', 10)
        
        if operation == 'restaurants_and_reviews':
            search_url = f'https://www.yelp.fr/search?find_desc=Restaurants&find_loc={location}&sortby=review_count'
            restaurants = scrape_search_results(search_url, max_pages=1)
            total_reviews = 0
            
            for resto in restaurants[:max_restaurants]:
                restaurant_id = unquote(resto['url'].split('/')[-1].split('?')[0])
                
                # Sauvegarder le restaurant
                restaurant_item = {
                    'id': restaurant_id,
                    'name': resto['name'],
                    'url': resto['url'],
                    'rating': Decimal(str(resto['rating'])),
                    'reviews_count': resto['reviews_count'],
                    'location': resto['location'],
                    'last_updated': resto['last_updated']
                }
                
                restaurant_table.put_item(Item=restaurant_item)
                print(f"Restaurant ajouté : {resto['name']}")
                
                # Scraper et sauvegarder les avis pour ce restaurant
                reviews = scrape_reviews(resto['url'], max_reviews=max_reviews)
                
                for review in reviews:
                    # Nettoyer et normaliser l'ID de l'avis
                    clean_user_name = review['user_name'].replace(' ', '_')
                    clean_date = review['date'].replace(' ', '_')
                    review_id = f"{restaurant_id}_{clean_user_name}_{clean_date}"
                    
                    review_item = {
                        'id': review_id,
                        'restaurant_id': restaurant_id,
                        'user_name': review['user_name'],
                        'user_location': review['user_location'],
                        'date': review['date'],
                        'text': review['text'],
                        'rating': Decimal(str(review['rating'])),
                        'reactions': review['reactions'],
                        'review_type': review['review_type'],
                        'page_number': review['page_number'],
                        'scraped_at': review['scraped_at']
                    }
                    
                    review_table.put_item(Item=review_item)
                
                total_reviews += len(reviews)
                print(f"Ajout de {len(reviews)} avis pour {resto['name']}")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Scraping des restaurants et avis réussi',
                    'restaurants_count': len(restaurants),
                    'total_reviews': total_reviews
                }, ensure_ascii=False)
            }
            
        else:
            raise Exception("Opération non valide")
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }, ensure_ascii=False)
        }