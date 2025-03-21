# django_project

A Django-based restaurant booking system that demonstrates a full-stack web application for "la italia", using an MVC framework, role-based access (simplified for demonstration), and comprehensive testing. This README covers the project scope, requirements, user stories, Agile methodology, installation instructions, usability details, testing, and deployment steps.

See Images of the Project: 
![Screenshot 2025-03-21 at 20 50 55](https://github.com/user-attachments/assets/279395eb-e238-449e-ac0a-148a495a86d8)
![Screenshot 2025-03-21 at 20 51 06](https://github.com/user-attachments/assets/fc5761cb-cbf8-469a-bcfb-4e32c9045a58)
![Screenshot 2025-03-21 at 20 51 18](https://github.com/user-attachments/assets/276daa95-cffc-4607-9f57-39b9e5e5f901)
![Screenshot 2025-03-21 at 20 51 38](https://github.com/user-attachments/assets/e9c36055-148d-4513-8f25-9fdec456e27c)


---

## Table of Contents
1. [Requirements & Scope](#requirements--scope)
2. [Agile Backlog & User Stories](#agile-backlog--user-stories)
3. [Prototype](#prototype)
4. [Installation & Setup](#installation--setup)
5. [Project Structure](#project-structure)
6. [Database Schema & Models](#database-schema--models)
7. [Usage & Features](#usage--features)
8. [Usability](#usability)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Security Considerations](#security-considerations)
12. [Future Improvements](#future-improvements)
13. [Credits & License](#credits--license)

---

## Requirements & Scope

### Overall Purpose
This project is a full-stack restaurant booking system. Diners can view available times and make reservations, while restaurant owners can manage bookings, view and edit existing reservations, and handle cancellations. The goal is to streamline the reservation process and prevent double bookings.

### Main Users
- **Restaurant Owner**  
  - Needs to manage table availability and view, edit, or cancel reservations.  
  - Must ensure that no double bookings occur.
- **Diner (Customer)**  
  - Needs a simple, intuitive booking form to reserve a table.  
  - Should receive immediate confirmation of the booking.

### Functional Requirements
1. **Diner Reservations**  
   - Provide a front-end booking form for inputting date, time, party size, and contact details.  
   - Immediately confirm a reservation if a table is available, or notify the user if not.
2. **Owner Management**  
   - Display an interface for owners to view all upcoming reservations.  
   - Include full CRUD functionality (create, read, update, delete) for reservations via the front-end, without needing to access the admin panel.  
   - Prevent double bookings with automated checks.
3. **User Authentication**  
   - Implement secure user registration, login, and logout for restaurant owners.  
   - Optionally, provide a simplified mechanism (or reference code) for diners to check booking status.

### Constraints & Assumptions
- **Tech Stack**:  
  - Back-End: Django (Python)  
  - Front-End: Custom HTML/CSS with Bootstrap and JavaScript  
  - Database: SQLite3 for local development (optionally Postgres for production)
- **Deployment**:  
  - The application will be deployed on a cloud platform (Heroku) with `DEBUG = False`.
- Assume a single restaurant location with a limited number of tables.

### Additional Notes
- This document forms the basis for creating detailed user stories and an agile backlog.
- A database schema diagram may be added later in this README to illustrate the relationships between tables.
- Detailed manual testing procedures (including test steps, expected vs. actual outcomes) and automated testing results will be documented in a dedicated testing section.

---

## Agile Backlog & User Stories

### Overview
This project follows an Agile development methodology to build a full-stack restaurant booking system. The user stories and technical tasks outlined below form our initial Agile backlog. These stories have been prioritized and estimated to ensure that we focus on delivering the core functionality first while iterating based on testing and user feedback.

### User Stories

#### For Restaurant Owners:
1. **US-1: Manage Reservations**  
   *As a restaurant owner, I want to view all current and upcoming reservations on a dashboard so that I can effectively manage table allocations and prevent double bookings.*  
   **Acceptance Criteria:**  
   - The dashboard displays a list of reservations with details such as date, time, party size, and customer contact information.  
   - Reservations can be filtered by date and time.  
   - The system prevents overlapping bookings for the same table.

2. **US-2: Edit or Cancel Reservations**  
   *As a restaurant owner, I want to edit or cancel a reservation directly from the dashboard so that I can correct errors or free up tables if necessary.*  
   **Acceptance Criteria:**  
   - The owner can click on a reservation to view detailed information.  
   - Options to update or delete the reservation are available.  
   - Changes are immediately reflected on the dashboard.

3. **US-3: Secure Management Access**  
   *As a restaurant owner, I want secure login functionality to access the management dashboard so that only authorized users can modify bookings.*  
   **Acceptance Criteria:**  
   - The login page requires valid credentials (username and password).  
   - After a successful login, the owner is redirected to the dashboard.  
   - Secure session management is in place to protect user data.

#### For Diners:
1. **US-4: Make a Reservation**  
   *As a diner, I want to complete a booking form to reserve a table so that I can dine at my preferred time.*  
   **Acceptance Criteria:**  
   - The booking form accepts date, time, party size, and contact details.  
   - The form validates all input fields and provides immediate feedback if there are errors.  
   - A confirmation message is displayed upon successful submission.

2. **US-5: Receive Booking Confirmation**  
   *As a diner, I want to receive immediate confirmation of my booking so that I know my reservation is successful.*  
   **Acceptance Criteria:**  
   - A confirmation message is displayed after the booking is submitted.  
   - Optionally, the system sends an email confirmation.

3. **US-6: Check Reservation Status**  
   *As a diner, I want to check the status of my reservation using a reference code so that I can verify my booking details.*  
   **Acceptance Criteria:**  
   - A unique reference code is provided upon booking.  
   - A status page allows the diner to enter the reference code and view reservation details.

### Agile Backlog
Below is our initial Agile backlog, which includes user stories (US) and technical tasks (T). Each item includes an estimated effort (story points) and priority level based on its importance for meeting our project objectives.

| **ID** | **User Story / Task**                                       | **Priority** | **Estimated Effort** | **Notes**                                      |
|--------|-------------------------------------------------------------|--------------|----------------------|------------------------------------------------|
| US-1   | View all reservations on the dashboard                      | High         | 8 points             | Core dashboard design and data binding         |
| US-2   | Edit or cancel a reservation                                | High         | 5 points             | CRUD operations integration                    |
| US-3   | Secure login/logout for owners                              | High         | 5 points             | Authentication implementation                  |
| US-4   | Diner booking form                                          | High         | 8 points             | Form design and input validation               |
| US-5   | Booking confirmation                                        | Medium       | 3 points             | Confirmation message (and email option)        |
| US-6   | Check reservation status using a reference code             | Medium       | 3 points             | Reference code system                          |
| T-1    | Set up project structure & configure environment (Django)   | High         | 3 points             | Django setup with proper settings              |
| T-2    | Design database schema with a custom model                  | High         | 5 points             | Include unique relationships and constraints   |
| T-3    | Implement front-end form with full CRUD functionality       | High         | 8 points             | Accessible booking form with a delete option   |
| T-4    | Integrate advanced JavaScript for dynamic UI elements       | Medium       | 5 points             | Real-time updates and input validation         |
| T-5    | Write detailed manual testing procedures                    | Medium       | 3 points             | Document testing for all key features          |

### Development Process
- **Iterative Development**  
  We will initially focus on high-priority items (US-1, US-4, T-1, T-2) and iterate through development cycles, testing, and refinement until core functionality is complete.
- **Agile Practices**  
  - Use a public GitHub project board (or similar) to track progress, update task statuses, and attach notes or screenshots for each user story and technical task.  
  - Commit frequently with descriptive messages to document the development process and changes made.  
  - Regularly review and adjust the backlog as new requirements or issues arise.

---

## Prototype

Below is a minimal prototype created using Django templates. This prototype demonstrates the basic layout of our “La Italia” Restaurant Booking System:

    hello_world/
    └── templates/
        └── hello_world/
            ├── base.html
            ├── index.html
            └── booking.html

- **base.html**: Contains the main layout, navbar, footer, and styling (including the gradient “La Italia” heading, off-white background, and Montserrat font).
- **index.html**: The home page for diners to see a welcome message and link to the booking page.
- **booking.html**: A basic booking form where diners can request a reservation.

The HTML and styling in these pages serve as an initial design. Actual functionality (saving reservations, preventing double bookings) is implemented through Django views, forms, and models, which are described later in this README.

---

## Installation & Setup

1. **Clone the Repository**  
git clone https://github.com/KTP8/django_project.git
cd django_project

2. **Create and Activate a Virtual Environment**
python -m venv venv
source venv/bin/activate  # On macOS/Linux
### or
venv\Scripts\activate  # On Windows

3. **Install Dependencies**
pip install -r requirements.txt

4. **Database Migrations**
python manage.py makemigrations
python manage.py migrate

5. **Run Dev Server**
python manage.py runserver

6. **Open Browser and go to http://127.0.0.1:8000/ to view home page**

## Project Structure

A simplified overview of the project layout:

django_project/
├── my_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hello_world/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── templates/
│       └── hello_world/
│           ├── base.html
│           ├── booking.html
│           ├── booking_confirm.html
│           ├── index.html
│           ├── menu.html
│           ├── ...
└── manage.py

- my_project: Contains Django project-level configurations (settings, URLs, WSGI).
- hello_world: The primary Django app for this booking system (models, forms, views, templates).
- templates: HTML templates for pages like index.html, booking.html, etc.
- manage.py: Django’s command-line utility for running tasks like migrations, starting the server, etc.


### Database Schema & Models

This application uses a single model, Reservation, to store booking data. The Reservation model includes:

- name and email for customer identification.
- date and time for the reservation slot.
- party_size to record how many diners.
- seating_type to distinguish between table and counter seats.
- status to track booking states (e.g., AWAITING, CONFIRMED, CANCELLED).
- cancel_token (UUID) to allow customers to cancel their reservation via a unique link.

Additional models can be added if the restaurant expands functionality (e.g., multiple locations, advanced menu data, etc.).

## Usage & Features 
1. **Home Page**
- A welcoming introduction to “La Italia,” with links to the booking form and other pages.

2. **Booking Page**
- A form where diners submit name, email, date, time, and party size.
- The system validates user inputs (e.g., no double bookings, time within opening hours).
- Upon success, the diner receives a confirmation message (and an email if configured).

3. **Reservation Management**
- Restaurant owners can access a password-protected page (/reservations) to view all bookings.
- IMPORTANT: The password is "boss" (all lowercase).
- Owners can view, delete, or modify reservations (CRUD functionality).

4. **Email Notifications**
- When a reservation is created, an email is sent to the diner (if email settings are properly configured).
- The email includes a uniqye cancellation link to let diners cancel if needed.
- For now, emails will only print to terminal instead of being sent. 

## Usability

Below are some scenarios to validate a smooth user experience and overall usability:

### Scenario: Booking Form (Valid Data)
- **Steps:** User opens `/booking`, enters valid info (name, email, date, time, party size), and clicks Submit.  
- **Expected Outcome:** The form processes successfully, and a confirmation message (and optional email) is displayed.

### Scenario: Booking Form (Invalid Data)
- **Steps:** User opens `/booking`, leaves required fields empty or enters invalid data (e.g., party size of 0, time outside operating hours), then clicks Submit.  
- **Expected Outcome:** The form shows error messages or refuses submission until valid data is provided.

### Scenario: Navigation
- **Steps:** From the home page `/`, the user clicks “Booking” in the navbar.  
- **Expected Outcome:** The booking form loads correctly, and the user can navigate back to Home or other pages without confusion.

These tests help confirm the application is user-friendly and responsive to different inputs.

---

## Testing

### Manual Testing

- **Form Validation**  
  Enter invalid data (e.g., empty fields, dates beyond 6 weeks, or times outside 11:00–22:00) to confirm validation messages.

- **Responsiveness**  
  Resized the browser or use dev tools to simulate mobile devices; the layout remained user-friendly.

- **Navigation**  
  Ensure that the “Booking,” “Menu,” and “Reservations” links all work correctly.

### Automated Testing

- **Django Tests**  
  Found in `hello_world/tests.py`.  
  Example tests include checking the home page’s status code and verifying that a reservation can be created without errors.  
  Run with:
  ```bash
  python manage.py test



## Security Considerations

- **Secret Key & Email Password**  
  Must not be committed to version control. Store them in environment variables or a `.env` file.

- **DEBUG Mode**  
  Set `DEBUG = False` for production to prevent sensitive data leaks.

- **Authentication**  
  The owner’s reservation page is protected by a password (or, in a more advanced setup, Django’s built-in auth with staff roles).

- **Validation**  
  Both front-end (JavaScript) and back-end (Django) validations prevent invalid or malicious inputs.

---

## Future Improvements

- **Enhanced Role-Based Access**  
  Replace the single password for the owner with Django’s user authentication and permissions.

- **Multiple Table Logic**  
  Expand the system to handle multiple tables with advanced seat assignment.

- **Extended Tests**  
  Increase test coverage, including JavaScript unit tests for dynamic UI elements.

- **Advanced Analytics**  
  Generate reports on peak booking times, average party size, etc.

- **Email Sending**
  In future iterations emails sent to user with form that matches website aesthetics containing reservation details.


## Deployment

Below are the steps to deploy on Heroku with a Git repository. The Heroku remote URL for this project is:

https://git.heroku.com/la-italia.git

### Create (or Connect to) the Heroku App:
If the app is already created on Heroku, connect via:
heroku git:remote -a la-italia
or
git remote add heroku https://git.heroku.com/la-italia.git

### Set Environment Variables:
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set EMAIL_HOST_USER='your_email@example.com'
heroku config:set EMAIL_HOST_PASSWORD='your_app_specific_password'

### Push to Heroku:
git push heroku main
heroku run python manage.py migrate

### Set DEBUG=False in Production:
Update settings.py or use an environment variable to ensure your app is secure.

### Collect Static Files:
python manage.py collectstatic

### Open the App:
heroku open

Verify the booking process, email confirmations, and management pages work correctly.

---

## Credits & License

- **Django** (https://www.djangoproject.com/)  
- **Bootstrap** (https://getbootstrap.com/)  
- **jQuery** (https://jquery.com/)  


© 2025 La Italia – Restaurant Booking System
