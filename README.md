	•	Student Name: Hadia Qaiser
	•	Student ID: 20069602
	•	Programme: MSc Information Systems
	•	Lecturer Name: Paul Laird
	•	Module Title: Programming for Information Systems
	•	Assignment Title: CA2 
	•	Project Title:  Medoracare - Product Authenticity and Shade Finder System.
	•	Google Doc link: https://docs.google.com/document/d/1oOD6VhoLN43uevyR00IGfuGkrU4cxDFAR3OW6NCP1kg/edit?usp=sharing

📒 Description:
This project is for a small Pakistani local company "Medora of London". The company sells widely across Pakistan but lacks an online system to help customers verify originality or choose the correct shade. The indivituality of this project is based on this gap, this system combine simple design with real use idea, showing how users can check product real or fake and find perfect shade in one small system.

💄 Web App Name: MedoraCare
A full-stack web application built using Flask, SQLite, HTML, CSS, and JavaScript, and deployed on AWS EC2. The project simulates a cosmetics platform with shade finder, product authenticity check, wishlist, and reviews.

🚀 Features
	•	Shade finder
	•	Product Authenticity (batch) check
	•	Wishlist management
	•	Product reviews

🛠 Language/Tool used
Frontend
	•	HTML5
	•	CSS3
	•	JavaScript (Fetch API)

Backend
	•	Python 3
	•	Flask (REST APIs)
	•	SQLAlchemy (ORM)

Database
	•	SQLite (development)

Tools & Cloud
	•	VS Code
	•	GitHub
	•	AWS EC2 (Linux)
	•	SSH (key-based access)

📁 Project Structure
MEDORACARE_PROJECT/
│
├── backend/                     # Flask backend
│   ├── app.py                   # Main Flask application (API routes)
│   ├── db.py                    # Database connection & configuration
│   ├── models.py                # SQLAlchemy database models
│   ├── seed.py                  # Script to insert sample data
│   └── medora.db                # SQLite database file
│
├── frontend/                    # Frontend files
│   ├── app.js                   # JavaScript logic (API calls)
│   ├── config.json              # Backend API configuration
│   ├── index.html               # Main UI page
│   └── style.css                # Styling for the UI
│
├── tests/                       # Unit and integration tests
│   ├── test_ping.py             # API health check test
│   ├── test_models_product.py   # Product model tests
│   ├── test_models_batch.py     # Batch/authenticity tests
│   ├── test_models_shade.py     # Shade model tests
│   ├── test_models_review.py    # Review model tests
│   └── test_models_wishlist.py  # Wishlist model tests
│
├── venv/                        # Python virtual environment (All files inside were craeted by default)
├── __init__.py                  # Project initializer
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignored files for Git (Such as all venv files)
└── README.md                    # Project documentation

⚙️ Local Setup
•	python3 -m venv venv
•	source venv/bin/activate
•	pip install flask sqlalchemy
•	python3 -m backend.app

☁️ AWS Deployment
•	Created AWS EC2 Linux instance
•	Enabled SSH (security group)
•	Connected using SSH key
•	Installed Python, SQLite & dependencies
•	Ran Flask app on EC2
•	Frontend is served via Flask from EC2 and backend APIs with SQLite are also hosted and executed on same EC2 machine.

🖱️ Commands used to run this App
•	cd Downloads (Open Terminal, Change directory to Downloads)
•	ssh -i ~/Downloads/medoracare-ec2-key.pem ec2-user@34.247.14.89 (SSH into EC2 Instance using key and Elastic IP)
•	source ~/venv/bin/activate (Activate Virtual Environment)
•	cd ~/Programming_CA (Changing directory to Project Folder)
•	python3 -m backend.app (Starting my backend)
•	Running on http://34.247.14.89:5000 (Open this link)



## Reference: I have used Chrome and AI to enhance the wording of my README file.