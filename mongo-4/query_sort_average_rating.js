db.reviews.aggregate([
  { $group: { _id: "$product_id", avg_rating: { $avg: "$rating" } } }, // Stage 1: Group
  { $sort: { avg_rating: -1 } } // Stage 2: Sort
])
