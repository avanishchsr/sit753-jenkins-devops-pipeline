from app.main import app


def test_health_endpoint_returns_healthy_status():
    client = app.test_client()
    response = client.get('/health')
    data = response.get_json()
    assert response.status_code == 200
    assert data['status'] == 'healthy'


def test_jobs_endpoint_returns_three_job_cards():
    client = app.test_client()
    response = client.get('/api/jobs')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]['title'] == 'Retail Assistant'


def test_groups_endpoint_contains_student_communities():
    client = app.test_client()
    response = client.get('/api/groups')
    data = response.get_json()
    group_names = [group['name'] for group in data]
    assert response.status_code == 200
    assert 'Indian Students Melbourne' in group_names
    assert 'Deakin Tech Community' in group_names
