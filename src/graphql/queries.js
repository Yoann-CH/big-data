/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getRestaurantsByLocation = /* GraphQL */ `
  query GetRestaurantsByLocation($location: String!) {
    getRestaurantsByLocation(location: $location) {
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
export const getReviewsByRestaurant = /* GraphQL */ `
  query GetReviewsByRestaurant($restaurant_id: ID!) {
    getReviewsByRestaurant(restaurant_id: $restaurant_id) {
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
export const getRestaurant = /* GraphQL */ `
  query GetRestaurant($id: ID!) {
    getRestaurant(id: $id) {
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
export const listRestaurants = /* GraphQL */ `
  query ListRestaurants(
    $filter: ModelRestaurantFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listRestaurants(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
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
      nextToken
    }
  }
`;
export const getReview = /* GraphQL */ `
  query GetReview($id: ID!) {
    getReview(id: $id) {
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
export const listReviews = /* GraphQL */ `
  query ListReviews(
    $id: ID
    $filter: ModelReviewFilterInput
    $limit: Int
    $nextToken: String
    $sortDirection: ModelSortDirection
  ) {
    listReviews(
      id: $id
      filter: $filter
      limit: $limit
      nextToken: $nextToken
      sortDirection: $sortDirection
    ) {
      items {
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
      nextToken
    }
  }
`;
export const reviewsByRestaurant_id = /* GraphQL */ `
  query ReviewsByRestaurant_id(
    $restaurant_id: ID!
    $sortDirection: ModelSortDirection
    $filter: ModelReviewFilterInput
    $limit: Int
    $nextToken: String
  ) {
    reviewsByRestaurant_id(
      restaurant_id: $restaurant_id
      sortDirection: $sortDirection
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
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
      nextToken
    }
  }
`;
