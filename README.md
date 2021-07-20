#Bug Prediction System
A Machine learning project to predict bug in code files.

Initial training Dataset: http://promise.site.uottawa.ca/SERepository/datasets/cm1.arff

This app can also scan public github repos with Python code for potential Bug.
It uses various code quality parameters defined by Mccabe and Halstead as features.
Uses Multi Layer Perceptron model by default with 90%+ accuracy.

## API Overview
This project has four API as explained below
- /reconfigure: Configure/Change the current ML model
- /is_buggy: Check if a code snippet is buggy
- /check_repo: Check if files in a github repo are buggy
- /feedback: Provide some sample snippets for feedback to the model

## Setup instructions
- Need git to be installed on the system to checkout the git repos
- Run following command to install required pip libraries
```shell
pip install -r requirements.txt
```
- Run the app using following command
```shell
python main.py
```
- Go to http://0.0.0.0:8888/ in any browser


## Usage Examples

### Check a github repo for potential buggy files (/check_repo)

```shell
curl -X 'POST' \
  'http://0.0.0.0:8888/check_repo?repo_url=https%3A%2F%2Fgithub.com%2Fpallets%2Fflask' \
  -H 'accept: application/json' \
  -d ''
```

```json
{
  "files checked": [
    "flask/setup.py",
    "flask/tests/test_basic.py",
    "flask/tests/conftest.py",
    "flask/tests/test_converters.py",
    "flask/tests/test_logging.py",
    "flask/tests/test_signals.py",
    "flask/tests/test_async.py",
    "flask/tests/test_session_interface.py",
    "flask/tests/test_instance_config.py",
    "flask/tests/test_views.py",
    "flask/tests/test_json_tag.py",
    "flask/tests/test_subclassing.py",
    "flask/tests/test_reqctx.py",
    "flask/tests/test_blueprints.py",
    "flask/tests/test_config.py",
    "flask/tests/test_user_error_handler.py",
    "flask/tests/test_helpers.py",
    "flask/tests/test_json.py",
    "flask/tests/test_cli.py",
    "flask/tests/test_templating.py",
    "flask/tests/test_appctx.py",
    "flask/tests/test_regression.py",
    "flask/tests/test_testing.py",
    "flask/tests/test_apps/blueprintapp/__init__.py",
    "flask/tests/test_apps/blueprintapp/apps/__init__.py",
    "flask/tests/test_apps/blueprintapp/apps/frontend/__init__.py",
    "flask/tests/test_apps/blueprintapp/apps/admin/__init__.py",
    "flask/tests/test_apps/helloworld/hello.py",
    "flask/tests/test_apps/helloworld/wsgi.py",
    "flask/tests/test_apps/subdomaintestmodule/__init__.py",
    "flask/tests/test_apps/cliapp/importerrorapp.py",
    "flask/tests/test_apps/cliapp/__init__.py",
    "flask/tests/test_apps/cliapp/factory.py",
    "flask/tests/test_apps/cliapp/multiapp.py",
    "flask/tests/test_apps/cliapp/app.py",
    "flask/tests/test_apps/cliapp/inner1/__init__.py",
    "flask/tests/test_apps/cliapp/inner1/inner2/flask.py",
    "flask/tests/test_apps/cliapp/inner1/inner2/__init__.py",
    "flask/docs/conf.py",
    "flask/examples/tutorial/setup.py",
    "flask/examples/tutorial/tests/conftest.py",
    "flask/examples/tutorial/tests/test_auth.py",
    "flask/examples/tutorial/tests/test_db.py",
    "flask/examples/tutorial/tests/test_factory.py",
    "flask/examples/tutorial/tests/test_blog.py",
    "flask/examples/tutorial/flaskr/auth.py",
    "flask/examples/tutorial/flaskr/db.py",
    "flask/examples/tutorial/flaskr/__init__.py",
    "flask/examples/tutorial/flaskr/blog.py",
    "flask/examples/javascript/setup.py",
    "flask/examples/javascript/js_example/__init__.py",
    "flask/examples/javascript/js_example/views.py",
    "flask/examples/javascript/tests/test_js_example.py",
    "flask/examples/javascript/tests/conftest.py",
    "flask/src/flask/logging.py",
    "flask/src/flask/signals.py",
    "flask/src/flask/sessions.py",
    "flask/src/flask/config.py",
    "flask/src/flask/templating.py",
    "flask/src/flask/globals.py",
    "flask/src/flask/__init__.py",
    "flask/src/flask/blueprints.py",
    "flask/src/flask/cli.py",
    "flask/src/flask/wrappers.py",
    "flask/src/flask/app.py",
    "flask/src/flask/debughelpers.py",
    "flask/src/flask/scaffold.py",
    "flask/src/flask/ctx.py",
    "flask/src/flask/typing.py",
    "flask/src/flask/testing.py",
    "flask/src/flask/helpers.py",
    "flask/src/flask/__main__.py",
    "flask/src/flask/views.py",
    "flask/src/flask/json/__init__.py",
    "flask/src/flask/json/tag.py"
  ],
  "potential buggy files": [
    "flask/tests/test_cli.py",
    "flask/src/flask/sessions.py",
    "flask/src/flask/cli.py",
    "flask/src/flask/app.py",
    "flask/src/flask/scaffold.py",
    "flask/src/flask/ctx.py",
    "flask/src/flask/helpers.py",
    "flask/src/flask/json/tag.py"
  ]
}
```

### Check a python code snippet for potential bugs (/is_buggy)

```shell
curl -X 'POST' \
  'http://0.0.0.0:8888/is_buggy' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "snippets": [
    "def is_buggy(query: QueryIn):\r\n    features = [get_features(i) for i in query.snippets]\r\n    return {\"results\": predict(features)}"
  ]
}'
```

```json
{
  "results": [
    false
  ]
}

```

### Provide feedback to the model (/feedback)
```shell
curl -X 'POST' \
  'http://0.0.0.0:8888/feedback' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "code": "def predict(features: list[Features]):\r\n    if not model:\r\n        return None\r\n    x_test = normalize([f.as_list() for f in features])\r\n    return [True if i == 1 else False for i in model.predict(x_test)]",
    "is_buggy": true
  }
]'
```
```json
{
  "detail": "Feedback loop successful!"
}
```

### Change the backend classification model (/reconfigure)

####Supported Values
- model_name: naive bayes, knn, mlp, decision tree
- metrics: accuracy, confusion_matrix, f1_score, hamming_loss, jaccard_score, precision, recall
- feature_cols: loc, cyclomatic_complexity, essential_complexity, design_complexity, n_operators, volume,
program_length, difficulty, intelligence, effort, halstead, time_estimate, line_count,
comment_lines, blank_lines, code_lines, unique_operators, unique_operands, tot_operators,
tot_operands, branch_count

```shell
curl -X 'POST' \
  'http://0.0.0.0:8888/reconfigure' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_name": "knn",
  "metrics": [
    "accuracy", "f1_score"
  ],
  "feature_cols": [
    "cyclomatic_complexity", "essential_complexity"
  ],
  "extra_params": {}
}'
```
```json
{
  "detail": "Model Trained Successfully!",
  "metrics": {
    "accuracy": 87,
    "f1_score": 13.33
  }
}
```