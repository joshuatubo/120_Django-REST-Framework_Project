# Secure Message Exchange System

This project consists of two Django REST Framework applications that communicate securely through encrypted messages.

## Setup Instructions

1. Create two virtual environments:

```bash
python -m venv sender_env
python -m venv receiver_env
```

2. Activate the virtual environments:

```bash
# For sender app
sender_env\Scripts\activate
# For receiver app
receiver_env\Scripts\activate
```

3. Install dependencies in both environments:

```bash
pip install -r requirements.txt
```

4. Run migrations for both applications:

```bash
python manage.py migrate
```

5. Create superuser for both applications:

```bash
python manage.py createsuperuser
```

6. Run the applications (use different terminals):

```bash
# Sender app (port 8000)
python manage.py runserver

# Receiver app (port 8001)
python manage.py runserver 8001
```

## Features

- Secure user authentication
- Encrypted message transmission
- Custom middleware for security
- User-friendly dashboard
- Message history tracking

 
## Pictures of our Project
message_sender
![message_sender1](https://github.com/user-attachments/assets/4a005572-e5d1-42ab-a505-0f16c36a327f)
![message_sender2](https://github.com/user-attachments/assets/66dac603-23c0-4a58-86dd-2b48a916167b)
![message_sender3](https://github.com/user-attachments/assets/e2cf5d2e-d388-4e16-99b7-41e4ba90734d)
![message_sender4](https://github.com/user-attachments/assets/6844d43d-f3ed-427a-a217-6226fd3c5623)
![message_sender5](https://github.com/user-attachments/assets/24f133af-2ce7-4974-9569-af1e834a219b)

message_sender Code
![ms_code1](https://github.com/user-attachments/assets/986ed920-0d02-4c7f-95e9-6d12766180af)
![ms_code2](https://github.com/user-attachments/assets/7e16cd63-99d3-4f64-b645-909e27d0b436)
![ms_code3](https://github.com/user-attachments/assets/44715d31-064a-44ad-a713-39fd82c88413)



message_receiver
![message_receicer1](https://github.com/user-attachments/assets/db939e15-e334-475c-9c13-c049d15c48c0)
![message_receiver2](https://github.com/user-attachments/assets/8efd37d9-e4bc-441a-bb8d-4198eb1ed9fe)
![message_receiver3](https://github.com/user-attachments/assets/0fa0da4c-5f34-40f6-af3c-7b08e7f8e055)

message_receiver Code
![mr_code1](https://github.com/user-attachments/assets/bd045f5e-2a02-4ffd-a509-2613254c18bc)
![mr_code2](https://github.com/user-attachments/assets/1aeef5c5-372f-4b96-8043-fb51d09abb75)
![mr_code3](https://github.com/user-attachments/assets/d5ec6bae-18a4-4e21-b0c1-b2923910d0b7)




