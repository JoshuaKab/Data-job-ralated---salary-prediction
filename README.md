# AI Job Salary Explorer

An interactive web app and FastAPI wrapper for `xgboost_best_model.pkl`. The
salary estimator predicts `salary_in_usd` from experience level, role family,
employment type, and company size.

## Run locally

```powershell
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open the link https://ai-job-salary-api.onrender.com/

## Deploy on Render

1. Push this folder, including `main.py`, `requirements.txt`,
   `render.yaml`, and `xgboost_best_model.pkl`, to a Git repository.
2. In Render, choose **New +** → **Blueprint** and connect that repository.
3. Render will create the web service from `render.yaml`.

The app is served at `/`; the API also provides `GET /health` and `POST /predict`.
Example request:

```json
{
  "experience_level_label": "Senior-level",
  "role_family": "Data Scientist",
  "employment_type": "FT",
  "company_size": "M"
}
```

The prediction response contains `predicted_salary_usd`. The supported values
for each input are listed in the interactive API documentation at `/docs`.
