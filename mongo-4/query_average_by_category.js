db.reviews.aggregate([
  { $group: { _id: "$category", avg_rating: { $avg: "$rating" } } }
])
