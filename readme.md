# AsanKharid E-commerce

This project is a Django-based e-commerce application designed to sell products like vegetables, fruits, juices, and other related items. It also includes a fully functional blog where users can read articles. The admin panel allows the management of products, blog posts, categories, and user orders.

## Prerequisites
Before setting up the project, ensure that the following tools are installed on your machine

- Python 3.11
- Django 5.1 or higher
- Virtualenv (optional but recommended)


## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammd-1819/AsanKharid.git


2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install the required dependencies:**
   ```bash
    pip install -r requirements.txt


4. **Apply the migrations:**
   ```bash
    python manage.py migrate


5. **Create a superuser for the admin panel (optional but recommended):**
   ```bash
    python manage.py createsuperuser
    default is: admin@gmail.com
    password : admin


6. **Run the development server:**
    ```bash
    python manage.py runserver


7. **Access the application:**
    Open your browser and go to http://127.0.0.1:8000/ for the main page


## Features
- User registration and login with email verification.
- Browse products (vegetables, fruits, juices) by category.
- Shopping cart functionality allowing users to add, remove, and manage items.
- Admin panel for managing products, orders, users, and blog posts.
- Product filtering and pagination.
- A blog section with the ability to comment on posts (authenticated users only).
- Pagination for blog posts.


## Blog Features
    The blog allows admins to create posts about topics related to fruits, vegetables, and healthy eating. Users can browse and comment on these posts


## Managing Products
Only admin users can create, edit, and delete products. Each product has various attributes, including:

- Name
- Category (Vegetables, Fruits, Juices, etc.)
- Price
- Stock Status
- Description


## Technologies Used
- Backend: Django
- Database: PostgreSQL
- Authentication: Customized Django built-in authentication system
- Frontend: HTML, CSS, JavaScript (with Bootstrap)


## Authors
Designed and Developed by Mohammad Charipour and Parmis Delfani. For more details, visit:
- https://github.com/mohammd-1819
- https://github.com/p-delfani
