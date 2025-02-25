echo "Testing API endpoints..."

# Base URL
BASE_URL="http://localhost:8000/api/v1"

# Test health check
echo "Testing health check endpoint..."
curl -s -X GET "${BASE_URL}/health"

echo "Test debug endpoint..."
curl -s -X GET "${BASE_URL}/health/debug"

# Test grading endpoint
echo "Testing grading endpoint..."
curl -s -X POST "${BASE_URL}/grading/grade/" \
  -H "Content-Type: application/json" \
  -d '{
    "student_answer": "Water is H2O. It consists of hydrogen and oxygen atoms.",
    "reference_answer": "Water is a compound with the chemical formula H2O, consisting of two hydrogen atoms bonded to one oxygen atom.",
    "rubric": {
      "Content": {
        "weight": 60,
        "criteria": "Identifies water as H2O and mentions both hydrogen and oxygen"
      },
      "Accuracy": {
        "weight": 40,
        "criteria": "Correctly describes the molecular structure"
      }
    }
  }'

echo "Testing simple endpoint..."
curl -s -X POST "${BASE_URL/grading/test}"

echo "API tests completed."
