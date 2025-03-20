# django_project

## Requirements & Scope

### Overall Purpose
This project is a full-stack restaurant booking system. Diners can view available times and make reservations, while restaurant owners can manage bookings, view and edit existing reservations, and handle cancellations. The goal is to streamline the reservation process and prevent double bookings.

### Main Users
- **Restaurant Owner**:  
  - Needs to manage table availability and view, edit, or cancel reservations.  
  - Must ensure that no double bookings occur.
- **Diner (Customer)**:  
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
  - Database: Postgres for production (minimal data in local SQLite3 for testing)
- **Deployment**:  
  - The application will be deployed on a cloud platform (e.g., Heroku) with `DEBUG = False`.
- Assume a single restaurant location with a limited number of tables.

### Additional Notes
- This document forms the basis for creating detailed user stories and an agile backlog.
- A database schema diagram will be added later in this README to illustrate the relationships between tables.
- Detailed manual testing procedures (including test steps, expected vs. actual outcomes) and automated testing results will be documented in a dedicated testing section.

## Agile Backlog & User Stories

### Overview
This project follows an Agile development methodology to build a full-stack restaurant booking system. The user stories and technical tasks outlined below form our initial Agile backlog. These stories have been prioritised and estimated to ensure that we focus on delivering the core functionality first while iterating based on testing and user feedback.

### User Stories

#### For Restaurant Owners:
1. **US-1: Manage Reservations**  
   *As a restaurant owner, I want to view all current and upcoming reservations on a dashboard so that I can effectively manage table allocations and prevent double bookings.*  
   **Acceptance Criteria:**  
   - The dashboard displays a list of reservations with details such as date, time, party size and customer contact information.  
   - Reservations can be filtered by date and time.  
   - The system prevents overlapping bookings for the same table.

2. **US-2: Edit or Cancel Reservations**  
   *As a restaurant owner, I want to edit or cancel a reservation directly from the dashboard so that I can correct errors or free up tables if necessary.*  
   **Acceptance Criteria:**  
   - The owner can click on a reservation to view detailed information.  
   - Options to update or delete the reservation are available.  
   - Changes are immediately reflected on the dashboard.

3. **US-3: Secure Management Access**  
   *As a restaurant owner, I want secure login functionality to access the management dashboard so that only authorised users can modify bookings.*  
   **Acceptance Criteria:**  
   - The login page requires valid credentials (username and password).  
   - After a successful login, the owner is redirected to the dashboard.  
   - Secure session management is in place to protect user data.

#### For Diners:
1. **US-4: Make a Reservation**  
   *As a diner, I want to complete a booking form to reserve a table so that I can dine at my preferred time.*  
   **Acceptance Criteria:**  
   - The booking form accepts date, time, party size and contact details.  
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

| **ID** | **User Story / Task**                                           | **Priority** | **Estimated Effort** | **Notes**                                       |
|--------|-----------------------------------------------------------------|--------------|----------------------|-------------------------------------------------|
| US-1   | View all reservations on the dashboard                          | High         | 8 points             | Core dashboard design and data binding          |
| US-2   | Edit or cancel a reservation                                    | High         | 5 points             | CRUD operations integration                     |
| US-3   | Secure login/logout for owners                                  | High         | 5 points             | Authentication implementation                   |
| US-4   | Diner booking form                                                | High         | 8 points             | Form design and input validation                |
| US-5   | Booking confirmation                                              | Medium       | 3 points             | Confirmation message (and email option)         |
| US-6   | Check reservation status using a reference code                   | Medium       | 3 points             | Reference code system                           |
| T-1    | Set up project structure & configure environment (Django)         | High         | 3 points             | Django setup with proper settings               |
| T-2    | Design database schema with a custom model                        | High         | 5 points             | Include unique relationships and constraints    |
| T-3    | Implement front-end form with full CRUD functionality               | High         | 8 points             | Accessible booking form with a delete option    |
| T-4    | Integrate advanced JavaScript for dynamic UI elements              | Medium       | 5 points             | Real-time updates and input validation          |
| T-5    | Write detailed manual testing procedures                           | Medium       | 3 points             | Document testing for all key features           |

### Development Process
- **Iterative Development:**  
  We will initially focus on high-priority items (US-1, US-4, T-1, T-2) and iterate through development cycles, testing and refinement until core functionality is complete.
  
- **Agile Practices:**  
  - Use a public GitHub project board to track progress, update task statuses, and attach notes or screenshots for each user story and technical task.  
  - Commit frequently with descriptive messages to document the development process and changes made.  
  - Regularly review and adjust the backlog as new requirements or issues arise.

---

## Prototype 

Below is a minimal protoype created using Django templates. This prototype demonstrates the basic layout of our “La Italia” Restaurant Booking System:
hello_world/ └── templates/ └── hello_world/ ├── base.html ├── index.html └── booking.html


- **base.html**: Contains the main layout, navbar, footer, and styling (including the gradient “La Italia” heading, off-white background, and Montserrat font).
- **index.html**: The home page for diners to see a welcome message and link to the booking page.
- **booking.html**: A basic booking form where diners can request a reservation (non-functional prototype for now).

The HTML and styling in these pages serve as an initial design. Actual functionality (saving reservations, preventing double bookings) will be added in later development stages.

---

## Usability Testing

We propose the following test scenarios to validate a smooth user experience:

1. **Scenario: Booking Form (Valid Data)**  
   - **Steps:** User opens `/booking`, enters valid info (name, email, date, time, party size), clicks Submit.  
   - **Expected Outcome:** The form processes successfully; a success or confirmation message is displayed.

2. **Scenario: Booking Form (Invalid Data)**  
   - **Steps:** User opens `/booking`, leaves required fields empty (e.g., no email), clicks Submit.  
   - **Expected Outcome:** The form shows error messages or refuses submission until all required fields are provided.

3. **Scenario: Navigation**  
   - **Steps:** From the Home page `/`, user clicks the “Booking” link in the navbar.  
   - **Expected Outcome:** The user sees the booking form without confusion or errors.

These scenarios help us confirm the core layout and user flow. As development progresses, we will refine and add more detailed usability tests.

