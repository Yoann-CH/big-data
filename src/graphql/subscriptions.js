/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onCreateRestaurant = /* GraphQL */ `
  subscription OnCreateRestaurant(
    $filter: ModelSubscriptionRestaurantFilterInput
  ) {
    onCreateRestaurant(filter: $filter) {
      id
      name
      description
      url
      rating
      reviews_count
      location
      last_updated
      reviews {
        items {
          id
          restaurant_id
          user_id
          user_name
          user_location
          date
          text
          rating
          reactions
          page_number
          review_type
          scraped_at
          sentiment_score
          detected_lang
          createdAt
          updatedAt
          restaurantReviewsId
        }
        nextToken
      }
      word_cloud {
        word
        frequency
      }
      wordcloud_graph
      sentiment_graph
      createdAt
      updatedAt
    }
  }
`;
export const onUpdateRestaurant = /* GraphQL */ `
  subscription OnUpdateRestaurant(
    $filter: ModelSubscriptionRestaurantFilterInput
  ) {
    onUpdateRestaurant(filter: $filter) {
      id
      name
      description
      url
      rating
      reviews_count
      location
      last_updated
      reviews {
        items {
          id
          restaurant_id
          user_id
          user_name
          user_location
          date
          text
          rating
          reactions
          page_number
          review_type
          scraped_at
          sentiment_score
          detected_lang
          createdAt
          updatedAt
          restaurantReviewsId
        }
        nextToken
      }
      word_cloud {
        word
        frequency
      }
      wordcloud_graph
      sentiment_graph
      createdAt
      updatedAt
    }
  }
`;
export const onDeleteRestaurant = /* GraphQL */ `
  subscription OnDeleteRestaurant(
    $filter: ModelSubscriptionRestaurantFilterInput
  ) {
    onDeleteRestaurant(filter: $filter) {
      id
      name
      description
      url
      rating
      reviews_count
      location
      last_updated
      reviews {
        items {
          id
          restaurant_id
          user_id
          user_name
          user_location
          date
          text
          rating
          reactions
          page_number
          review_type
          scraped_at
          sentiment_score
          detected_lang
          createdAt
          updatedAt
          restaurantReviewsId
        }
        nextToken
      }
      word_cloud {
        word
        frequency
      }
      wordcloud_graph
      sentiment_graph
      createdAt
      updatedAt
    }
  }
`;
export const onCreateReview = /* GraphQL */ `
  subscription OnCreateReview($filter: ModelSubscriptionReviewFilterInput) {
    onCreateReview(filter: $filter) {
      id
      restaurant_id
      restaurant {
        id
        name
        description
        url
        rating
        reviews_count
        location
        last_updated
        reviews {
          nextToken
        }
        word_cloud {
          word
          frequency
        }
        wordcloud_graph
        sentiment_graph
        createdAt
        updatedAt
      }
      user_id
      user_name
      user_location
      date
      text
      rating
      reactions
      page_number
      review_type
      scraped_at
      sentiment_score
      detected_lang
      word_cloud {
        word
        frequency
      }
      createdAt
      updatedAt
      restaurantReviewsId
    }
  }
`;
export const onUpdateReview = /* GraphQL */ `
  subscription OnUpdateReview($filter: ModelSubscriptionReviewFilterInput) {
    onUpdateReview(filter: $filter) {
      id
      restaurant_id
      restaurant {
        id
        name
        description
        url
        rating
        reviews_count
        location
        last_updated
        reviews {
          nextToken
        }
        word_cloud {
          word
          frequency
        }
        wordcloud_graph
        sentiment_graph
        createdAt
        updatedAt
      }
      user_id
      user_name
      user_location
      date
      text
      rating
      reactions
      page_number
      review_type
      scraped_at
      sentiment_score
      detected_lang
      word_cloud {
        word
        frequency
      }
      createdAt
      updatedAt
      restaurantReviewsId
    }
  }
`;
export const onDeleteReview = /* GraphQL */ `
  subscription OnDeleteReview($filter: ModelSubscriptionReviewFilterInput) {
    onDeleteReview(filter: $filter) {
      id
      restaurant_id
      restaurant {
        id
        name
        description
        url
        rating
        reviews_count
        location
        last_updated
        reviews {
          nextToken
        }
        word_cloud {
          word
          frequency
        }
        wordcloud_graph
        sentiment_graph
        createdAt
        updatedAt
      }
      user_id
      user_name
      user_location
      date
      text
      rating
      reactions
      page_number
      review_type
      scraped_at
      sentiment_score
      detected_lang
      word_cloud {
        word
        frequency
      }
      createdAt
      updatedAt
      restaurantReviewsId
    }
  }
`;
