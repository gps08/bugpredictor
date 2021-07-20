from models import TrainIn, FeedbackIn, Features
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle

from utils import load_data, get_features
from consts import Constants

model = None
feature_cols = Constants.features_list

def init():
    train_req = TrainIn(
        model_name='mlp',
        metrics=['accuracy', 'precision', 'recall', 'f1_score'],
        extra_params={'solver': 'adam', 'max_iter': 600},
        feature_cols=feature_cols
    )
    print(f'Model loaded with following metrics', train(train_req))

def normalize(x):
    return MinMaxScaler(feature_range=(0, 1)).fit_transform(x)

def save_model():
    if not model:
        return
    with open(Constants.model_filename, 'wb') as f:
        pickle.dump(model, f)

def train(train_req: TrainIn):
    x, y = load_data(train_req.feature_cols)
    x = normalize(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    globals()['model'] = Constants.models_map[train_req.model_name](**train_req.extra_params)
    globals()['feature_cols'] = train_req.feature_cols
    y_pred = model.fit(x_train, y_train).predict(x_test)
    save_model()
    metrics = {}
    for name in train_req.metrics:
        if name in Constants.metrics_map:
            val = Constants.metrics_map[name](y_test, y_pred)
            metrics[name] = round(100 * val, ndigits=2)
        else:
            metrics[name] = 'Not recognised'
    return metrics

def predict(features: list[Features]):
    if not model:
        return None
    x_test = normalize([f.as_list(feature_cols) for f in features])
    return [True if i == 1 else False for i in model.predict(x_test)]

def retrain(feedbacks: list[FeedbackIn]):
    if not model:
        return None
    x = [get_features(f.code).as_list(feature_cols) for f in feedbacks]
    y = [1.0 if f.is_buggy else 0.0 for f in feedbacks]
    model.fit(x, y)
    save_model()
