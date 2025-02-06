/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createRestaurant = /* GraphQL */ `
  mutation CreateRestaurant(
    $input: CreateRestaurantInput!
    $condition: ModelRestaurantConditionInput
  ) {
    createRestaurant(input: $input, condition: $condition) {
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
export const updateRestaurant = /* GraphQL */ `
  mutation UpdateRestaurant(
    $input: UpdateRestaurantInput!
    $condition: ModelRestaurantConditionInput
  ) {
    updateRestaurant(input: $input, condition: $condition) {
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
export const deleteRestaurant = /* GraphQL */ `
  mutation DeleteRestaurant(
    $input: DeleteRestaurantInput!
    $condition: ModelRestaurantConditionInput
  ) {
    deleteRestaurant(input: $input, condition: $condition) {
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
export const createReview = /* GraphQL */ `
  mutation CreateReview(
    $input: CreateReviewInput!
    $condition: ModelReviewConditionInput
  ) {
    createReview(input: $input, condition: $condition) {
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
export const updateReview = /* GraphQL */ `
  mutation UpdateReview(
    $input: UpdateReviewInput!
    $condition: ModelReviewConditionInput
  ) {
    updateReview(input: $input, condition: $condition) {
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
export const deleteReview = /* GraphQL */ `
  mutation DeleteReview(
    $input: DeleteReviewInput!
    $condition: ModelReviewConditionInput
  ) {
    deleteReview(input: $input, condition: $condition) {
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
