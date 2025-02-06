# API REST

### récupérer les restaurants : 

```http request
https://cqsxbesjv1.execute-api.eu-west-3.amazonaws.com/dev/restaurants
```


### récupérer un restaurant : 

```http request
https://cqsxbesjv1.execute-api.eu-west-3.amazonaws.com/dev/restaurant/{restaurant_id}
```


dans la réponse, on a :

sentiment_graph (url) pour télécharger le graphique des sentiments
wordcloud_graph (url) pour télécharger le graphique des mots clés


### récupérer les reviews d'un restaurant : 

```http request
https://cqsxbesjv1.execute-api.eu-west-3.amazonaws.com/dev/restaurant/{restaurant_id}/reviews
```

