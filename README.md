Mirchi Bites

Mirchi Bites is a vibrant and modern food delivery website built to provide users with a seamless experience in ordering delicious meals online. The project encompasses a robust backend powered by Django, a dynamic frontend built with HTML, CSS, and JavaScript, and integrates with Razorpay for secure payment processing. The website is designed to be responsive, ensuring a delightful experience across various devices.

Table of Contents
Features
Technologies Used
Architecture
Backend
Frontend
Payment Integration
Deployment
Installation
Usage
Contributing
License
Features
User registration and authentication
Browse and search through a wide variety of food items
Add items to the cart and proceed to checkout
Secure payment processing through Razorpay
Order tracking and management
Responsive design for optimal viewing on mobile and desktop devices
Admin dashboard for managing orders and menu items
Technologies Used
Frontend:
HTML5
CSS3 (Bootstrap)
JavaScript (ES6)
Backend:
Django
Django REST Framework
PostgreSQL
Payment Processing:
Razorpay API


Architecture
The application follows a Model-View-Template (MVT) architecture. The backend handles data storage and retrieval, while the frontend presents the data to users and captures their interactions.



    Frontend
                   
   (HTML, CSS, JavaScript)  
               

    Django            
  (Backend API & Logic)     


   PostgreSQL           
   (Database Management)  


 
Backend
The backend of Mirchi Bites is developed using Django, a high-level Python web framework that encourages rapid development and clean, pragmatic design. Key components include:

User Management: Utilizes Django's built-in authentication system for user registration, login, and profile management.
Database Models: Models for users, orders, and menu items are defined to handle the data effectively.
RESTful API: The Django REST Framework is used to create a RESTful API for seamless communication between the frontend and backend.
Frontend
The frontend is crafted with a modern aesthetic, focusing on user experience and responsiveness. It includes:

Responsive Design: Built using Bootstrap for mobile-first responsiveness.
Dynamic Content: JavaScript is used for handling user interactions and making API calls to the backend.
User-Friendly Interface: Clean layout with intuitive navigation, allowing users to easily browse and order food.
Payment Integration
Mirchi Bites integrates with Razorpay to facilitate secure online payments. Key features include:

Razorpay API: Integrated for handling payment processing.
Order Confirmation: Users receive an order confirmation upon successful payment.
Error Handling: Comprehensive error handling to manage payment failures and user notifications.
Deployment
Mirchi Bites is deployed on Render, ensuring high availability and scalability. The deployment process includes:

Setting up a new web service on Render.
Configuring environment variables for database credentials and Razorpay API keys.
Deploying the application through GitHub integration.
Steps to Deploy:
Push your code to GitHub.
Create a new web service on Render and connect it to your repository.
Set up the necessary environment variables in Render.
Launch the service.
Installation
To run Mirchi Bites locally, follow these steps:

Clone the Repository:

bash
Copy code
git clone https://github.com/Subhammm25/mirchibites.git
cd mirchibites
Set Up a Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Configure Database:

Update the DATABASES setting in settings.py with your local PostgreSQL credentials.
Run Migrations:

bash
Copy code
python manage.py migrate
Create a Superuser (Optional):

bash
Copy code
python manage.py createsuperuser
Start the Development Server:

bash
Copy code
python manage.py runserver
Usage
Visit http://127.0.0.1:8000 in your browser to access the website.
Register for an account or log in to browse and order food.
Navigate through the menu, add items to your cart, and proceed to checkout to make a payment through Razorpay.
Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.
