# bookstore project
This is a very simple bookstore website built with Django.The website displays products. Users can add and remove products to/from their cart while also specifying the quantity of each item

## Setting Up and Running Your Django Project

### Step 1: Prerequisites
Make sure you have Python and Django installed on your system.

Run:pip install django

### Step 2: Create a New Django Project

Open your terminal or command prompt.

Run: django-admin startproject bookstore

### Step 3: Navigate to Your Project Directory

Change directory to your project folder.

Run: cd bookstore

## Step 4: Create a New Django App

Create a new Django app inside your project.

Run: python manage.py startapp store

### Step 5: Apply Migrations 

Apply database migrations.

Run: python manage.py migrate

## Step 6: Create a Superuser

Create a superuser (admin) for the Django admin panel.

Run: python manage.py createsuperuser

## Step 7: Run the Development Server

Start the development server.

Run: python manage.py runserver

### Step 8: Access Your Django Project

Visit http://127.0.0.1:8000/ in your browser to see your Django project in action.

### Step 9: Access Django Admin Panel

Access the Django admin panel at http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

### Step 10: Additional Steps
Customize your Django project by defining models, views, and templates. Configure URL patterns, handle forms, and set up your database models.


### Update Setting
In setting.py 
EMAIL_HOST_USER = 'Use your Gmail '
EMAIL_HOST_PASSWORD = 'Use you generated password'







