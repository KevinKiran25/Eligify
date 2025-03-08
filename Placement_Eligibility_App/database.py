from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

#db connection
class database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.cursor = self.connection.cursor()
        
        db_name = "placement_db"
        query = f"create database if not exists {db_name}"
        self.cursor.execute(query)
        self.connection.commit()

        self.connection.database = db_name

    def execute(self,query,parmas=()):
        self.cursor.execute(query,parmas)
        self.connection.commit()

    def fetchall(self,query,parmas=()):
        self.cursor.execute(query,parmas)
        return self.cursor.fetchall()
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()



def tables_creation():
    db = database()

    tables = ["""
                create table if not exists Students(student_id int auto_increment primary key,
              name varchar(100), age int, gender ENUM('Male', 'Female', 'Other') not null,
              email varchar(100) unique, phone varchar(15),enrollment_year int,
              course_batch varchar(50), city varchar(100) ,graduation_year int)    
            """,
            """
                create table if not exists programming(programming_id int auto_increment primary key,
                student_id int unique, language varchar(52),problems_solved int, assessments_completed int,
                mini_projects int ,certifications_earned int,latest_project_score int,
                FOREIGN KEY(student_id) REFERENCES Students(student_id) ON DELETE CASCADE)
            """,
            """
                create table if not exists soft_skills(soft_skill_id int auto_increment primary key,
                student_id int,communication int, teamwork int,presentation int,leadership int ,
                critical_thinking int ,interpersonal_skills int,
                FOREIGN KEY(student_id) REFERENCES Students(student_id) ON DELETE CASCADE)
            """,
            """
                create table if not exists Placements(placement_id int auto_increment primary key,
                student_id int, mock_interview_score int,internships_completed int,placement_status ENUM('Ready', 'Not Ready', 'Placed') not null,
                company_name varchar(100), placement_package int ,interview_rounds_cleared int,placement_date date,
                FOREIGN KEY(student_id) REFERENCES Students(student_id) ON DELETE CASCADE)

            """]
    
    for quries in tables:
        db.execute(quries)
    print('tables and database created sucessfully.......')
    db.close_connection()

if __name__ == "__main__":
    tables_creation()