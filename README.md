
# Google Meet Clone Backend (Django)

This project is a minimal backend API for a Google Meet clone using Django, Django REST Framework, and Django Channels. It handles authentication, room management, and WebSocket signaling.

---

## 🔧 Tech Stack

- Python 3.12+
- Django 5+
- Django REST Framework
- Django Channels
- Redis (for WebSocket message brokering)

---

## 🚀 Features

- ✅ User Registration & Login (Session Auth)
- ✅ Create & Join Meeting Rooms
- ✅ Track Participants per Room
- ✅ Room Details API
- ✅ WebSocket signaling using Django Channels
- ✅ Per-room signaling groups for isolation

---

## 🗂 API Endpoints

### Auth
| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| POST   | `/register/`   | Register a new user      |
| POST   | `/login/`      | Log in and create session|
| POST   | `/logout/`     | Log out user             |
| GET    | `/auth-test/`  | Test if user is logged in|

### Rooms
| Method | Endpoint              | Description              |
|--------|------------------------|--------------------------|
| POST   | `/create-room/`        | Create a new room        |
| POST   | `/join-room/`          | Join room via code       |
| GET    | `/room/<code>/`        | Get room details         |

### WebSocket
| Protocol | Endpoint                     | Description              |
|----------|-------------------------------|--------------------------|
| WS       | `/ws/room/<room_code>/`       | Connect to room WebSocket|

---

## ⚙️ Setup Instructions

### 1. Clone and Install

```bash
git clone https://github.com/your-username/google-meet-clone-backend.git
cd google-meet-clone-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Redis Server

```bash
redis-server
```

### 3. Run Django Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📄 API Docs

Visit Swagger UI at:  
`http://localhost:8000/api/docs/`  
Visit schema JSON at:  
`http://localhost:8000/api/schema/`

---

## 🧪 Testing With cURL

Example (register):

```bash
curl -X POST http://localhost:8000/register/ \
-H "Content-Type: application/json" \
-d '{"username": "user", "password": "pass"}'
```

---

## 📂 Project Structure (Backend Only)

```
meet/
├── core/
│   ├── models.py         # Room, RoomUser
│   ├── views.py          # REST API views
│   ├── consumers.py      # WebSocket signaling
│   ├── routing.py        # WebSocket routes
│   └── serializers.py    # DRF serializers
├── meet/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
└── manage.py
```

---

## 🔒 Auth Notes

- Uses session-based auth (cookies + CSRF)
- Test using Postman or browser sessions

---

## 🧠 Future Improvements

- JWT-based auth
- Room chat, mute, and host control
- Reconnection handling
- Room expiration

---

## 📝 License

MIT License. Built for learning and demonstration.