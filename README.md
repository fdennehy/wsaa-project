# WSAA Project Repository #

**by Finbar Dennehy**

This repository represents my project submission for the 'Web Services and Applications' (WSAA) module, part of the HDip in Science in Data Analytics at ATU. 

This project is a lightweight web-based dashboard for managing Accounts and Contacts, built with:

- **Flask** for the backend
- **MySQL** as the database
- **HTML, Ajax, JavaScript, jQuery, Chart.js, and Bootstrap** on the frontend

Key functionality includes:
- CRUD operations on Accounts and Contacts
- Reading in data from an external source [Random User Generator](https://randomuser.me/) 
- Real-time visualization of average contact health scores by account.

The project is hosted and can be accessed on [Python Anywhere](https://fdennehy.pythonanywhere.com/)

---

## Features

Manage Accounts:  
- Create, Read, Update, Delete  
- Real-time validation  
- Dummy Account generator (not exposed on the front end)

Manage Contacts:  
- Create, Read, Update, Delete  
- Health score tracking  
- Optional generation of dummy contacts using RandomUser API

Insights:  
- **Bar Chart** of average contact health scores per account (auto-refreshes after data changes)  

UX:  
- Dynamic content areas  
- Responsive chart display  

---

## Folder Structure

```
project/
│
├── templates/
│   └── dashboards.html      # Main HTML page with embedded JavaScript
│
├── .gitignore               # Files & Folders to be ignore by git
├── accountDAO_test.py       # Test script for accountDAO.py
├── accountDAO.py            # DAO logic for accounts table
├── ChatGPT_prompt.txt       # Initial prompt to start dashboard.html
├── contactDAO_test.py       # Test script for contactDAO.py
├── contactDAO.py            # DAO logic for contacts table
├── dbconfigpa.py            # Connection details for MySQL database, hosted on Python Anywhere
├── mysql.txt                # SQL statements to create & populate database tables
├── README.md.py             # This README file
├── requirements.txt         # Dependencies required on a fresh virtual environment
├── server_test.py           # Test script for server.py
├── server.py                # Flask backend server
```

---

## Setup Instructions

To run locally, follow the below instructions.
Alternatively, go to https://fdennehy.pythonanywhere.com/ to view the dashboard and interact with the database.

1. **Clone the repository**

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up the MySQL database**
   - Ensure your database is running
   - Create tables: `account`, `contact` (refer to mysql.txt)
   - Update your connection credentials in a config file, and update the DAO files if needed

5. **Run the Flask server**
```bash
python server.py
```

6. **Open the Dashboard**
   Navigate to `http://127.0.0.1:5000/` in your browser

---

## Acknowledgements

- Special thanks to my lecturer on the Web Services and Applications module, Andrew Beatty, from whom I acquired the skills necessary to put this project together.
- [ChatGPT](https://chatgpt.com/) was heavily used for puting together the dashboard.html (see ChatGPT_prompt.txt)
- [Random User Generator API](https://randomuser.me/) is used to generate dummy contacts.