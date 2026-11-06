db.students.aggregate([
  {$match: { department: "CSE" } },
  { $group: { _id: "$department", averageMarks: { $avg: "$marks" } } } ])
