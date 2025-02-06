import json
import boto3
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect
from decimal import Decimal
import uuid
from datetime import datetime
import traceback
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import io
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
import pandas as pd

# Initialisation de NLTK avec toutes les ressources nécessaires
def initialize_nltk():
    """Initialise les ressources NLTK nécessaires"""
    try:
        # Liste simplifiée des ressources essentielles
        resources = [
            'punkt',
            'stopwords',
            'averaged_perceptron_tagger',
            'words'
        ]
        
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                print(f"Téléchargement de {resource}...")
                nltk.download(resource, quiet=True)
                
    except Exception as e:
        print(f"Erreur lors de l'initialisation NLTK: {str(e)}")
        raise

# Appeler l'initialisation au démarrage
initialize_nltk()

# Chargement des stop words français
stop_words = set(stopwords.words('french'))
# Ajout de stop words spécifiques aux restaurants
custom_stop_words = {
    'restaurant', 'plat', 'menu', 'service', 'fois', 'très', 'bien',
    'bon', 'bonne', 'fait', 'plus', 'moins', 'tout', 'tous', 'toute',
    'toutes', 'vraiment', 'peu', 'assez', 'trop', 'très'
}
stop_words.update(custom_stop_words)

dynamodb = boto3.resource('dynamodb')
review_table = dynamodb.Table('Review-pr6ldw4tmzejjoqjxwtlfg2iem-dev')

s3 = boto3.client('s3')
BUCKET_NAME = 'restaurant-graphs-dev'  # Créez ce bucket dans S3

def detect_language(text):
    """Détecte la langue du texte (fr ou en)"""
    try:
        return detect(text)
    except:
        return 'en'  # par défaut en anglais si la détection échoue

def analyze_sentiment(text, language):
    """Analyse améliorée du sentiment d'un texte avec prise en compte de contextes multiples"""
    try:
        # Dictionnaire des mots critiques et leur impact
        critical_words = {
            'fr': {
                # Problèmes d'hygiène graves
                'souris': -0.9, 'rat': -0.9, 'cafard': -0.9, 'insecte': -0.8, 
                'moisissure': -0.8, 'crasse': -0.8,
                # Problèmes de santé
                'intoxication': -0.9, 'malade': -0.8, 'vomir': -0.9, 'diarrhée': -0.9,
                'nausée': -0.8, 'empoisonnement': -0.9,
                # Hygiène générale
                'sale': -0.7, 'insalubre': -0.8, 'hygiène': -0.7, 'malsain': -0.7,
                'cru': -0.6, 'pourri': -0.8,
                # Service
                'impoli': -0.6, 'désagréable': -0.6, 'arnaque': -0.7, 'vol': -0.7,
                # Nourriture
                'immangeable': -0.8, 'infecte': -0.8, 'dégoûtant': -0.8
            },
            'en': {
                # Serious hygiene issues
                'mouse': -0.9, 'mice': -0.9, 'rat': -0.9, 'roach': -0.9, 'cockroach': -0.9,
                'bug': -0.8, 'mold': -0.8, 'filth': -0.8,
                # Health issues
                'sick': -0.8, 'vomit': -0.9, 'diarrhea': -0.9, 'food poisoning': -0.9,
                'nausea': -0.8, 'stomach': -0.7,
                # General hygiene
                'dirty': -0.7, 'unsanitary': -0.8, 'hygiene': -0.7, 'unsafe': -0.7,
                'raw': -0.6, 'rotten': -0.8,
                # Service
                'rude': -0.6, 'awful': -0.7, 'scam': -0.7, 'theft': -0.7,
                # Food quality
                'inedible': -0.8, 'disgusting': -0.8, 'terrible': -0.7
            }
        }

        # Modificateurs qui peuvent inverser ou atténuer le sentiment
        negation_words = {
            'fr': {'pas', 'plus', 'jamais', 'aucun', 'sans', 'non'},
            'en': {'not', 'never', 'no', 'none', 'without', "didn't", "wasn't", "isn't", "aren't"}
        }

        # Mots positifs qui peuvent être inversés
        positive_words = {
            'fr': {'bon': 0.6, 'excellent': 0.8, 'délicieux': 0.7, 'parfait': 0.8, 
                  'super': 0.7, 'génial': 0.7},
            'en': {'good': 0.6, 'great': 0.7, 'excellent': 0.8, 'delicious': 0.7, 
                  'perfect': 0.8, 'amazing': 0.7}
        }

        # Analyse de base avec TextBlob
        if language == 'fr':
            blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
            base_score = blob.sentiment[0]
        else:
            blob = TextBlob(text)
            base_score = blob.sentiment.polarity

        words = text.lower().split()
        critical_score = 0
        critical_words_found = 0
        negation_count = 0
        positive_score = 0
        
        # Analyse du contexte et des négations
        for i, word in enumerate(words):
            # Vérification des mots critiques
            if word in critical_words.get(language, {}):
                critical_score += critical_words[language][word]
                critical_words_found += 1
            
            # Vérification des mots positifs
            if word in positive_words.get(language, {}):
                # Vérifie si le mot positif est précédé d'une négation
                if i > 0 and words[i-1] in negation_words.get(language, {}):
                    positive_score -= positive_words[language][word]
                else:
                    positive_score += positive_words[language][word]
            
            # Compte les négations
            if word in negation_words.get(language, {}):
                negation_count += 1

        # Calcul du score final
        if critical_words_found > 0:
            # Les problèmes critiques ont plus de poids
            critical_weight = 0.7
            base_weight = 0.2
            positive_weight = 0.1
            
            final_score = (
                (critical_score * critical_weight) +
                (base_score * base_weight) +
                (positive_score * positive_weight)
            ) / (1 + critical_words_found * 0.3)
        else:
            # Sans problèmes critiques, équilibrer entre base et positif
            base_weight = 0.6
            positive_weight = 0.4
            
            final_score = (
                (base_score * base_weight) +
                (positive_score * positive_weight)
            )

        # Ajustement en fonction des négations
        if negation_count > 0:
            final_score *= (1 - (negation_count * 0.2))

        return round(max(-1.0, min(1.0, final_score)), 2)
    except Exception as e:
        print(f"Erreur lors de l'analyse du sentiment: {str(e)}")
        return 0.0

def extract_keywords(text, language):
    """Extrait les mots-clés avec leur fréquence"""
    tokens = nltk.word_tokenize(text.lower())
    
    if language == 'fr':
        stop_words = set(stopwords.words('french'))
        stop_words.update(custom_stop_words)
    else:
        stop_words = set(stopwords.words('english'))
        stop_words.update({
            'restaurant', 'food', 'place', 'time', 'service',
            'good', 'great', 'nice', 'better', 'best',
            'really', 'very', 'much', 'many', 'lot'
        })

    words = [
        word for word in tokens
        if word.isalnum() and
        len(word) > 3 and
        word not in stop_words
    ]
    
    word_counts = Counter(words)
    return [{'word': word, 'frequency': count} for word, count in word_counts.most_common(20)]

def merge_similar_words(word_counts):
    """Fusionne les mots similaires et additionne leurs fréquences"""
    merged = {}
    processed = set()
    
    word_items = [(item['word'], item['frequency']) for item in word_counts]
    
    for i, (word1, freq1) in enumerate(word_items):
        if word1 in processed:
            continue
            
        total_freq = freq1
        base_word = word1
        processed.add(word1)
        
        # Cherche les mots similaires
        for word2, freq2 in word_items[i+1:]:
            if word2 not in processed:
                similarity = SequenceMatcher(None, word1, word2).ratio()
                if similarity > 0.8:  # Seuil de similarité
                    total_freq += freq2
                    processed.add(word2)
        
        merged[base_word] = total_freq
    
    return [{'word': word, 'frequency': freq} for word, freq in merged.items()]

def create_word_cloud_graph(word_cloud_data, restaurant_id):
    """Crée un nuage de mots"""
    try:
        # Création du dictionnaire pour wordcloud
        word_dict = {item['word']: item['frequency'] for item in word_cloud_data}
        
        # Configuration de la wordcloud
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            max_words=50,
            relative_scaling=0.5,
            min_font_size=10,
            max_font_size=120,
            colormap='viridis'
        ).generate_from_frequencies(word_dict)
        
        # Création du graphique
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nuage de mots des avis', pad=20)
        
        # Sauvegarde en mémoire
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight', dpi=300)
        img_data.seek(0)
        
        # Upload vers S3
        s3_key = f'wordcloud/{restaurant_id}.png'
        s3.upload_fileobj(img_data, BUCKET_NAME, s3_key)
        
        plt.close()
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        
    except Exception as e:
        print(f"Erreur lors de la création du nuage de mots: {str(e)}")
        return None

def create_sentiment_distribution_graph(reviews, restaurant_id):
    """Crée un graphique de la distribution des sentiments"""
    try:
        plt.figure(figsize=(12, 6))
        
        # Extraction des scores de sentiment
        sentiment_scores = [float(review.get('sentiment_score', 0)) for review in reviews]
        
        # Définition des intervalles et labels
        bins = [-1.0, -0.6, -0.2, 0.2, 0.6, 1.0]
        labels = ['Très négatif', 'Négatif', 'Neutre', 'Positif', 'Très positif']
        
        # Conversion des scores en catégories
        categories = pd.cut(sentiment_scores, 
                          bins=bins, 
                          labels=labels, 
                          include_lowest=True)
        
        # Création du graphique avec Seaborn
        sns.set_style("whitegrid")
        ax = sns.countplot(x=categories, palette='RdYlGn')
        
        # Personnalisation du graphique
        plt.title('Distribution des sentiments dans les avis', pad=20)
        plt.xlabel('Sentiment')
        plt.ylabel('Nombre d\'avis')
        
        # Rotation des labels pour une meilleure lisibilité
        plt.xticks(rotation=45)
        
        # Ajout des valeurs sur chaque barre
        for i in ax.containers:
            ax.bar_label(i)
        
        # Ajustement automatique de la mise en page
        plt.tight_layout()
        
        # Sauvegarde en mémoire
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight', dpi=300)
        img_data.seek(0)
        
        # Upload vers S3
        s3_key = f'sentiment/{restaurant_id}.png'
        s3.upload_fileobj(img_data, BUCKET_NAME, s3_key)
        
        plt.close()
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        
    except Exception as e:
        print(f"Erreur lors de la création du graphique de sentiment: {str(e)}")
        return None

def analyze_reviews(reviews, restaurant_id):
    """Analyse un ensemble d'avis"""
    all_keywords = []
    
    # Mise à jour de la table Restaurant
    restaurant_table = dynamodb.Table('Restaurant-pr6ldw4tmzejjoqjxwtlfg2iem-dev')
    
    for review in reviews:
        try:
            detected_lang = detect_language(review['text'])
            sentiment_score = analyze_sentiment(review['text'], detected_lang)
            keywords = extract_keywords(review['text'], detected_lang)
            
            all_keywords.extend(keywords)
            
            # Mise à jour de l'avis
            review_table.update_item(
                Key={'id': review['id']},
                UpdateExpression='SET sentiment_score = :s, detected_lang = :l, word_cloud = :wc',
                ExpressionAttributeValues={
                    ':s': Decimal(str(sentiment_score)),
                    ':l': detected_lang,
                    ':wc': keywords
                }
            )
            
        except Exception as e:
            print(f"Erreur lors du traitement de l'avis {review.get('id')}: {str(e)}")
            continue
    
    # Fusion des mots-clés similaires
    merged_keywords = merge_similar_words(all_keywords)
    
    # Création des graphiques
    wordcloud_url = create_word_cloud_graph(merged_keywords, restaurant_id)
    sentiment_url = create_sentiment_distribution_graph(reviews, restaurant_id)
    
    # Mise à jour du restaurant
    try:
        restaurant_table.update_item(
            Key={'id': restaurant_id},
            UpdateExpression='SET word_cloud = :wc, last_updated = :lu, wordcloud_graph = :wg, sentiment_graph = :sg',
            ExpressionAttributeValues={
                ':wc': merged_keywords,
                ':lu': datetime.now().isoformat(),
                ':wg': wordcloud_url,
                ':sg': sentiment_url
            }
        )
    except Exception as e:
        print(f"Erreur lors de la mise à jour du restaurant {restaurant_id}: {str(e)}")

def get_all_restaurants():
    """Récupère tous les restaurants depuis DynamoDB"""
    restaurant_table = dynamodb.Table('Restaurant-pr6ldw4tmzejjoqjxwtlfg2iem-dev')
    
    restaurants = []
    last_evaluated_key = None
    
    while True:
        if last_evaluated_key:
            response = restaurant_table.scan(ExclusiveStartKey=last_evaluated_key)
        else:
            response = restaurant_table.scan()
            
        restaurants.extend(response.get('Items', []))
        
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break
            
    return restaurants

def decimal_to_float(obj):
    """Convertit les objets Decimal en float pour la sérialisation JSON"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(x) for x in obj]
    return obj

def analyze_all_restaurants(max_restaurants=100):
    """Analyse tous les restaurants et leurs avis"""
    restaurants = get_all_restaurants()
    print(f"Nombre total de restaurants trouvés : {len(restaurants)}")
    
    for restaurant in restaurants[:max_restaurants]:
        restaurant_id = restaurant['id']
        print(f"Analyse du restaurant : {restaurant['name']} (ID: {restaurant_id})")
        
        # Récupérer les avis du restaurant
        response = review_table.query(
            IndexName='byRestaurant',
            KeyConditionExpression='restaurant_id = :rid',
            ExpressionAttributeValues={
                ':rid': restaurant_id
            }
        )
        
        reviews = response.get('Items', [])
        if not reviews:
            print(f"Aucun avis trouvé pour le restaurant {restaurant_id}")
            continue
            
        # Analyser les avis du restaurant
        analyze_reviews(reviews, restaurant_id)
        
        print(f"Analyse terminée pour le restaurant {restaurant_id}")

def handler(event, context):
    try:
        operation = event.get('operation', 'single')
        
        if operation == 'analyze_all':
            max_restaurants = event.get('max_restaurants', 100)
            analyze_all_restaurants(max_restaurants)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Analyse globale terminée'
                }, ensure_ascii=False)
            }
        else:
            # Code existant pour l'analyse d'un seul restaurant
            restaurant_id = event.get('restaurant_id')
            if not restaurant_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'restaurant_id est requis pour l\'analyse individuelle'
                    }, ensure_ascii=False)
                }
            
            # Récupération des avis depuis DynamoDB
            response = review_table.query(
                IndexName='byRestaurant',
                KeyConditionExpression='restaurant_id = :rid',
                ExpressionAttributeValues={
                    ':rid': restaurant_id
                }
            )
            
            reviews = response.get('Items', [])
            if not reviews:
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'message': 'Aucun avis trouvé pour ce restaurant'
                    }, ensure_ascii=False)
                }
            
            # Analyse des avis
            analyze_reviews(reviews, restaurant_id)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Analyse terminée'
                }, ensure_ascii=False)
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }, ensure_ascii=False)
        }