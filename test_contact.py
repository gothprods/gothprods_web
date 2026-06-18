from app import app
with app.test_client() as client:
    response = client.post('/submit_contact', data={
        'name': 'Test',
        'email': 'test@test.com',
        'message': 'Hello'
    })
    print("Status:", response.status_code)
    print("Response:", response.text)
