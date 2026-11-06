db.reviews.aggregate([  { $group: { _id: "$product_id", total_reviews: { $sum: 1 } } } ])
