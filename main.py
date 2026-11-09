from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

FEATURE_NAMES = [
    "experience_level_label",
    "role_family",
    "employment_type",
    "company_size",
]

EXPERIENCE_LEVEL_CODES = {
    "Entry-level": 0,
    "Executive-level": 1,
    "Mid-level": 2,
    "Senior-level": 3,
}
ROLE_FAMILY_CODES = {
    "AI Architect": 0,
    "AI Engineer": 1,
    "Analytics Manager": 2,
    "Computer Vision": 3,
    "Data Analyst": 4,
    "Data Engineer": 5,
    "Data Scientist": 6,
    "ML Engineer": 7,
    "NLP": 8,
    "Other / Unclassified": 9,
    "Research Scientist": 10,
}
EMPLOYMENT_TYPE_CODES = {"CT": 0, "FL": 1, "FT": 2, "PT": 3}
COMPANY_SIZE_CODES = {"L": 0, "M": 1, "S": 2}

MODEL_PATH = Path(__file__).resolve().with_name("xgboost_best_model.pkl")
STATIC_PATH = Path(__file__).resolve().with_name("static")

app = FastAPI(
    title="AI Job Salary Prediction API",
    description="Predict salary in USD using the trained AI job salary model.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

model = joblib.load(MODEL_PATH)
model_features = getattr(model, "feature_names_in_", None)
if model_features is None or list(model_features) != FEATURE_NAMES:
    raise RuntimeError(
        f"Model at {MODEL_PATH} must have features in this order: {FEATURE_NAMES}"
    )


class SalaryPredictionRequest(BaseModel):
    experience_level_label: Literal[
        "Entry-level", "Executive-level", "Mid-level", "Senior-level"
    ]
    role_family: Literal[
        "AI Architect",
        "AI Engineer",
        "Analytics Manager",
        "Computer Vision",
        "Data Analyst",
        "Data Engineer",
        "Data Scientist",
        "ML Engineer",
        "NLP",
        "Other / Unclassified",
        "Research Scientist",
    ]
    employment_type: Literal["CT", "FL", "FT", "PT"]
    company_size: Literal["L", "M", "S"]


class SalaryPredictionResponse(BaseModel):
    predicted_salary_usd: float


@app.get("/")
def root() -> FileResponse:
    return FileResponse(STATIC_PATH / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/predict",
    response_model=SalaryPredictionResponse,
)
def predict_salary(
    request: SalaryPredictionRequest,
) -> SalaryPredictionResponse:
    features = pd.DataFrame(
        [
            {
                "experience_level_label": EXPERIENCE_LEVEL_CODES[
                    request.experience_level_label
                ],
                "role_family": ROLE_FAMILY_CODES[request.role_family],
                "employment_type": EMPLOYMENT_TYPE_CODES[request.employment_type],
                "company_size": COMPANY_SIZE_CODES[request.company_size],
            }
        ],
        columns=FEATURE_NAMES,
    )
    predicted_salary = float(model.predict(features)[0])
    return SalaryPredictionResponse(predicted_salary_usd=predicted_salary)
