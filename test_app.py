from fastapi.testclient import TestClient
from main import app

# test to check the correct functioning of the /ping route
def test_ping():
    with TestClient(app) as client:
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.json() == {'ping': 'pong'}

# test to check if reconfigure route is working as expected
def test_reconfigure():
    payload = {
        'model_name': 'knn',
        'metrics': ['accuracy', 'f1_score'],
        'feature_cols': ['cyclomatic_complexity', 'essential_complexity'],
        'extra_params': {},
    }
    with TestClient(app) as client:
        response = client.post('/reconfigure', json=payload)
        assert response.status_code == 200
        assert 'accuracy' in response.json()['metrics']
        assert 'f1_score' in response.json()['metrics']

# test to check if feedback loop route is working as expected
def test_feedback():
    payload = [{'code': 'some_random_string', 'is_buggy': True}]
    with TestClient(app) as client:
        response = client.post('/feedback', json=payload)
        print(response.text)
        assert response.status_code == 200

# test to check if is_buggy loop route is working as expected
def test_is_buggy():
    payload = {
        'snippets': ['some_random_string']
    }
    with TestClient(app) as client:
        response = client.post('/is_buggy', json=payload)
        assert response.status_code == 200
        assert 'results' in response.json()

# test to check if check_repo loop route is working as expected
def test_check_repo():
    with TestClient(app) as client:
        payload = {
            'repo_url': 'https://github.com/gps08/mlops-iris'
        }
        response = client.post('/check_repo', params=payload)
        assert response.status_code == 200
        assert 'files checked' in response.json()
        assert 'potential buggy files' in response.json()
