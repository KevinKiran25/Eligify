# Placement Eligibility App  

This is a **Streamlit-based web application** that helps analyze student **placement readiness** using SQL insights, programming performance, and soft skills.  

---

## Features  
- ✅ **Placement Eligibility Check** – Filter students based on scores, internships, and programming skills.  
- ✅ **SQL Insights Dashboard** – View **placement, programming, and soft skills insights.**  
- ✅ **Interactive & User-Friendly** – Built using **Streamlit** for easy use.  
- ✅ **Database-Driven** – Uses **MySQL** for structured data storage.  

---

## 🛠 Setup Instructions  

# Step 1
### ** Install Dependencies**  
pip install -r requirements.txt

# Step 2
### ** Set Up MySQL Database** 
#### Modify the .env file with your MySQL credentials:
DB_HOST=localhost  
DB_USER=root  
DB_PASSWORD=yourpassword  
DB_NAME=placement_db  
#### Then, create the database and tables by running:
python database.py

# Step 3
## To insert 500+ fake student records into the database, run:
python faker_data.py
#### **Note:** If you want to add **500+ more records**, simply run `faker_data.py` again.

# Step 4
## To launch the Streamlit web app, run:
streamlit run app.py


Now, open localhost in your browser and explore the app!

# Technologies Used
Python (Data Processing & Streamlit UI)
Streamlit (Web Framework for UI)
MySQL (Database for storing student & placement data)
Faker (Generates synthetic student data)
Pandas (Handles SQL query results & displays in Streamlit)




