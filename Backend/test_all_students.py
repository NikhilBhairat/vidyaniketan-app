import requests
import json

students = [
    ('9876543210', 'Rahul Sharma'),
    ('9876543211', 'Priya Patel'),
    ('9876543212', 'Amit Kumar'),
]

print('Testing all student logins:\n')

for mobile, name in students:
    data = {'mobile_number': mobile, 'password': 'password123'}
    response = requests.post('http://localhost:8000/api/auth/login/', json=data)
    status = '✅' if response.status_code == 200 else '❌'
    user_data = response.json().get('user', {})
    print(f'{status} {name} ({mobile})')
    print(f'   Status: {response.status_code}, Role: {user_data.get("role", "N/A")}')
    print()
