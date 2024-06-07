# Online Rental Management System

## Overview

The Online Rental Management System is a web application designed to facilitate the rental of items. It allows users to list items for rent, request items for rent, manage rental requests, and update item statuses. The project is built using Django, MongoDB, and integrates AdminLTE for a responsive and user-friendly interface.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **Profile Management**: Users can view and edit their profiles.
- **Item Management**: Users can add, edit, and delete items they own.
- **Rental Requests**: Users can request items for rent and manage their requests.
- **Search Functionality**: Users can search for available items.
- **Status Updates**: Owners can update the status of their items (e.g., rented, available).
- **Responsive Design**: The interface is designed using AdminLTE for a responsive and modern look.

## Models

### Item

- **name**: Name of the item.
- **picture**: Image of the item.
- **rental_price**: Price for renting the item.
- **description**: Description of the item.
- **keywords**: Keywords associated with the item.
- **owner**: Owner of the item (User).
- **status**: Status of the item (e.g., available, rented).

### RentalRequest

- **item**: The item being requested.
- **requester**: The user requesting the item.
- **status**: Status of the rental request (e.g., requested, rented, returned).
- **requested_at**: Timestamp when the request was made.
- **is_completed**: Boolean indicating if the rental request is completed.

### Profile

- **user**: User associated with the profile.
- **first_name**: First name of the user.
- **last_name**: Last name of the user.
- **phone_number**: Phone number of the user.

## Views

- **Home**: Displays available items for rent.
- **Profile**: Displays user profile and rental requests.
- **Manage Items**: Allows users to manage their items.
- **Add Item**: Form to add a new item.
- **Search Items**: Displays search results for items.

## URLs

- **/register/**: User registration.
- **/login/**: User login.
- **/logout/**: User logout.
- **/profile/**: User profile.
- **/manage-items/**: Manage user items.
- **/add-item/**: Add a new item.
- **/search/**: Search items.
- **/update-item-status/<pk>/<status>/**: Update item status.
- **/cancel-request/<pk>/**: Cancel a rental request.
- **/confirm-return/<pk>/**: Confirm return of a rented item.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/MohdAleeRehman/Online-Rental-Management-System.git
    cd Online-Rental-Management-System
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

6. Access the application at `http://127.0.0.1:8000/`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.
