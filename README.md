# Insurance Premium Predictor API

FastAPI service that predicts an insurance premium category from user health/lifestyle inputs, using a trained scikit-learn model with Pydantic-validated requests.

## Docker Image

```bash
docker pull aarav01go/insurance-premium-api
```

## Run

```bash
docker run -p 8000:8000 aarav01go/insurance-premium-api
```

App will be live at `http://localhost:8000`.

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/predict` | POST | Returns predicted premium category with confidence and class probabilities |

## Sample Request

> Adjust fields to match your actual request schema in `schema/`.

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 65,
    "income_lpa": 10,
    "smoker": false,
    "city": "Delhi",
    "occupation": "private_job"
  }'
```

## Sample Response

```json
{
  "predicted_category": "medium",
  "confidence": 0.87,
  "class_probability": {
    "low": 0.05,
    "medium": 0.87,
    "high": 0.08
  }
}
```

## Tech Stack

- FastAPI + Uvicorn
- Pydantic (request validation)
- scikit-learn (model)
- Docker

## Build Locally

```bash
docker build -t aarav01go/insurance-premium-api .
```

## Notes

- Model file (`model.pkl`) is loaded from the `model/` directory at startup.
- Model version is currently tracked manually (`MODEL_Version` in `predict.py`).
