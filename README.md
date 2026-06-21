# Django Ticket Management System

## Overview

This is a comprehensive Ticket Management System built using Django. The system allows customers to create support tickets, track their status, and view all their submitted tickets. Engineers can view the ticket queue, accept tickets, and resolve them. The application includes user authentication, role-based access control, and is styled using Bootstrap for a responsive and modern user interface.

## Features

- **User Authentication**: Secure login and registration for customers and engineers.
- **Role-Based Access Control**: Different dashboards and permissions for customers and engineers.
- **Ticket Creation and Management**: Customers can create tickets, and engineers can manage and resolve them.
- **Ticket Queue**: Engineers can view all pending tickets and accept them.
- **Responsive Design**: The application is styled using Bootstrap to ensure it works well on all devices.

## Getting Started

### Prerequisites

- Python 3.x
- Django 3.x
- Bootstrap 5.x

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/Django-Ticket-Management-System.git
    cd Django-Ticket-Management-System
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

- **Customers** can register, log in, create tickets, and view their ticket status.
- **Engineers** can log in, view pending tickets, accept tickets, and mark them as resolved.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [FontAwesome](https://fontawesome.com/)
# client-server
