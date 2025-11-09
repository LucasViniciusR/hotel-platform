# hotel-platform
This is a small open-source project I’m building to learn and share how a real-world hotel management backend could work.
It covers the basics like handling rooms, guests, and reservations, plus things like authentication, email notifications, and scheduled background tasks.

The idea is to keep it simple but structured. something that could be expanded later with a React frontend or extra modules.

# Feedback & Contributions

I'm always open to feedback and ideas. Feel free to reach out and suggest changes.
If you’d like to improve something, suggest a feature, or just leave a comment, you can open an issue or a pull request!

## Features

* **User authentication with roles**: Admin, Staff, Customer
* **CRUD operations**: Rooms, Guests, Reservations
* **Email notifications**: Reservation confirmations using Celery
* **Scheduled tasks**: Automatic cleanup of expired reservations with Celery Beat
* **Dockerized setup**: Easy local development and testing

---

## Getting Started

### Prerequisites

* [Docker & Docker Compose](https://docs.docker.com/get-docker/)
* Python 3.11+ (optional if you want to run without Docker)

### Quick Start (Docker)

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/hotel-platform.git
   cd hotel-platform
   ```

2. Copy the example file and fill in the required values:

   ```
   cp .env.example .env
   ```

3. Start the stack:

   ```bash
   docker-compose up --build
   ```

4. Access the API:

   ```
   http://localhost:8000/api/
   ```

---

## Future Plans

* Add a React frontend for full-stack demo
* Improve email templates and notifications
* Add more roles and permissions
