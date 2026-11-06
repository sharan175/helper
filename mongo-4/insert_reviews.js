db.reviews.insertMany (  [
  { customer_name: "Alice", product_id: "P101", category: "Electronics", rating: 4, comment: "Good quality, fast delivery.", review_date: ISODate("2025-09-01") },
  { customer_name: "Bob",   product_id: "P101", category: "Electronics", rating: 5, comment: "Excellent product!", review_date: ISODate("2025-09-02") },
  { customer_name: "Charlie", product_id: "P102", category: "Books", rating: 3, comment: "Decent read but slow shipping.", review_date: ISODate("2025-09-03") },
  { customer_name: "David", product_id: "P103", category: "Clothing", rating: 2, comment: "Poor quality material.", review_date: ISODate("2025-09-04") },
  { customer_name: "Emma", product_id: "P102", category: "Books", rating: 4, comment: "Enjoyed the book!", review_date: ISODate("2025-09-05") }
]);
