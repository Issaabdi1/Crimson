import concurrent.futures
import requests
from faker import Faker
import re


def get_csrf_token(session, url):
    response = session.get(url)
    csrf_token = re.search('name="csrfmiddlewaretoken" value="(.+?)"', response.text).group(1)
    return csrf_token


def register_user(user_data):
    with requests.Session() as session:
        sign_up_url = 'https://teamcrimson.pythonanywhere.com/sign_up/'
        csrf_token = get_csrf_token(session, sign_up_url)
        register_data = {
            'csrfmiddlewaretoken': csrf_token,
            **user_data
        }
        headers = {
            'Referer': sign_up_url
        }
        response = session.post(sign_up_url, data=register_data, headers=headers)
        if response.status_code == 200:
            print(f"Registered {user_data['username']}")
            return (True, user_data)
        else:
            print(f"Failed to register {user_data['username']}")
            return (False, user_data)


def login_user(user_data):
    with requests.Session() as session:
        log_in_url = 'https://teamcrimson.pythonanywhere.com/log_in/'
        csrf_token = get_csrf_token(session, log_in_url)
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': user_data['username'],
            'password': user_data['password'],
        }
        headers = {
            'Referer': log_in_url
        }
        response = session.post(log_in_url, data=login_data, headers=headers)
        if response.status_code == 200:
            print(f"Logged in {user_data['username']}")
        else:
            print(f"Failed to log in {user_data['username']}")


def generate_user_data():
    faker = Faker()
    return {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'username': f"@{faker.user_name()}",
        'email': faker.email(),
        'password': 'YourSecurePasswordHere123',
    }


def main():
    users_data = [generate_user_data() for _ in range(500)]

    # Register users
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_user = {executor.submit(register_user, user): user for user in users_data}
        for future in concurrent.futures.as_completed(future_to_user):
            user_data = future_to_user[future]
            try:
                success, user = future.result()
                if success:
                    # You can add logic here if you need to do something with successful registrations
                    pass
            except Exception as exc:
                print(f"{user_data['username']} generated an exception: {exc}")

    # Login users
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(login_user, users_data)


if __name__ == "__main__":
    main()
