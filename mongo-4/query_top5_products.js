db.reviews.aggregate([
  { $group: { _id: "$product_id", total_reviews: { $sum: 1 } } }, // Stage 1: Group
  { $sort: { total_reviews: -1 } }, // Stage 2: Sort
  { $limit: 5 } // Stage 3: Limit to Top 5
])
