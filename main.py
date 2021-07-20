import uvicorn
from fastapi import FastAPI
from typing import List
import shutil

from models import QueryIn, FeedbackIn, TrainIn
from ml import train, predict, retrain, init
from utils import get_features, load_repo, get_repo_name
from consts import Constants

app = FastAPI(title=Constants.app_name, docs_url="/")
app.add_event_handler("startup", init)

# Route to ensure that the API is up and running
@app.get("/ping")
def ping():
    return {"ping": "pong"}

# Route to train the ML model using certain parameters.
# Payload: TrainIn containing the model name and parameters for success
# Response: Dict with detailed response message and value for success metric (200)
@app.post("/reconfigure", status_code=200, summary='Configure/Change the current ML model')
def reconfigure(train_req: TrainIn):
    metrics = Constants.metrics_map.keys()
    unrecognised_feature = [f for f in train_req.feature_cols if f not in Constants.features_list]
    unrecognised_model = train_req.model_name if train_req.model_name not in Constants.models_map.keys() else ''
    unrecognised_metrics = [m for m in train_req.metrics if m not in metrics]
    if unrecognised_feature or unrecognised_model or unrecognised_metrics:
        result = {'detail': 'Invalid Input'}
        if unrecognised_feature:
            result['unrecognised_feature'] = unrecognised_feature
        if unrecognised_model:
            result['unrecognised_model'] = unrecognised_model
        if unrecognised_metrics:
            result['unrecognised_metrics'] = unrecognised_metrics
        return result
    metrics = train(train_req)
    return {
        "detail": "Model Trained Successfully!",
        "metrics": metrics
    }

# Route to do the prediction for files in a github repo using the chosen ML model
# Payload: QueryIn - list of snippets of code to check
# Response: Result if the provided code snippets are buggy or not (200)
@app.post("/is_buggy", status_code=200, summary='Check if a code snippet is buggy')
def is_buggy(query: QueryIn):
    features = [get_features(i) for i in query.snippets]
    return {"results": predict(features)}

# Route to do the prediction for files in a github repo using the chosen ML model
# Payload: url for the github repo to check ex. https://github.com/gps08/mlops-iris.git
# Response: List of files with potential bugs (200)
@app.post("/check_repo", status_code=200, summary='Check if files in a github repo are buggy')
def check_repo(repo_url):
    file_paths = load_repo(repo_url)
    features = [get_features(open(f).read()) for f in file_paths]
    predictions = predict(features)
    buggy_files = [file_paths[i] for i in range(len(predictions)) if predictions[i]]
    shutil.rmtree(get_repo_name(repo_url))
    return {
        "files checked": file_paths,
        "potential buggy files": buggy_files
    }

# Route to further train the model based on user input in form of feedback loop
# Payload: FeedbackIn containing the parameters and flag to tell if code is buggy or not
# Response: Dict with detail confirming success (200)
@app.post("/feedback", status_code=200, summary='Provide some sample snippets for feedback to the model')
def feedback_loop(data: List[FeedbackIn]):
    retrain(data)
    return {"detail": "Feedback loop successful!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
