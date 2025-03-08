from faker import Faker
import random
from database import database

fake = Faker('en_IN')

popular_cities = [
    "Chennai", "Thiruvananthapuram", "Bangalore","Hyderabad","Pune"
    "Mumbai", "Delhi", "Ahmedabad","Kolkata", "Surat", "Jaipur"
]

course_batch_codes = {
    "Python": "PY",
    "JavaScript": "JS",
    "Go": "GO",
    "Rust": "RS",
    "TypeScript": "TS",
    "Kotlin": "KT"
}

batch_suffix = ["A", "B", "C", "D"] 

def generate_profile():
    gender = random.choice(['Male', 'Female'])
    
    if gender == 'Male':
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()
    
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"
    city = random.choice(popular_cities)
    
    email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
    phone = f"+91{random.randint(9000000000, 9999999999)}"

    return {
        'full_name': full_name,
        'gender': gender,
        'city': city,
        'email': email,
        'phone': phone
    }

def insert_students_data(db,no_students=0):
    for _ in range(no_students):
        profile = generate_profile()
        age = random.randint(18,28)
        enrollment_year = random.randint(2018,2023)
        graduation_year = random.randint(int(enrollment_year+1.5),2025)
        lang= random.choice(list(course_batch_codes.keys()))
        course_batch = f"{course_batch_codes[lang]}-{enrollment_year}-{random.choice(batch_suffix)}"

        existing_student = db.fetchall("SELECT student_id FROM students WHERE email = %s", (profile['email'],))
        if existing_student:
            continue 

        values = (profile['full_name'], age, profile['gender'], profile['email'], profile['phone'], enrollment_year, course_batch, profile['city'], graduation_year)

        db.execute("""
                    insert into students(name,age,gender,email,phone,enrollment_year,course_batch,city,graduation_year)
                   values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,values)
        
def insert_programming_data(db):
    students = db.fetchall("select student_id,course_batch from students")

    for student in students:
        lang_code = student[1][:2]
        language = [language for language, prog in course_batch_codes.items() if prog == lang_code]

        existing_programming = db.fetchall("SELECT student_id FROM programming WHERE student_id = %s", (student[0],))
        if existing_programming:
            continue
        problems_solved = random.randint(0,100)
        assessments_completed = random.randint(0,10)
        mini_projects = random.randint(0,7)
        certifications_earned =random.randint(0,5)
        latest_project_score = (problems_solved * 0.3) + (assessments_completed * 5) + (mini_projects * 10)
        latest_project_score = min(100, int(latest_project_score))


        values = (student[0],language[0],problems_solved,assessments_completed,mini_projects,certifications_earned,latest_project_score)
        db.execute("""
                    insert into programming(student_id,language,problems_solved,assessments_completed,mini_projects,certifications_earned,latest_project_score)
                   values(%s,%s,%s,%s,%s,%s,%s)
                """,values)
        
def insert_soft_Skill(db):
    students = db.fetchall("select student_id from students")
    for student in students:
        
        communication = random.randint(40, 100)
        teamwork = communication - random.randint(0, 10)
        presentation = communication - random.randint(0, 15)
        leadership = random.randint(40, communication)
        critical_thinking = (communication + leadership) // 2
        interpersonal_skills = (teamwork + presentation) // 2
        
        values = (student[0],communication,teamwork,presentation,leadership,critical_thinking,interpersonal_skills)
        db.execute("""
                    insert into soft_skills(student_id,communication,teamwork,presentation,leadership,critical_thinking,interpersonal_skills)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,values)
        
def insert_placement_data(db):
    students = db.fetchall("select student_id from students")
    for student in students:    

        mock_interview_score = random.randint(30, 100)
        internships_completed = random.randint(0, 3)

        if mock_interview_score >= 90 and internships_completed >= 1:
            placement_status= "Placed"
            company_name = random.choice(["HCL", "TCS", "Infosys", "Wipro"])
            placement_package = random.randint(600000, 1200000)
            interview_rounds_cleared = random.randint(3, 6) 
            placement_date = fake.date_this_decade()
        elif mock_interview_score >= 75:
            placement_status ="Ready"
            company_name ="N/A"
            placement_package = 0
            interview_rounds_cleared = 0
            placement_date = None
        else:
            placement_status ="Not Ready"
            company_name="N/A"
            placement_package =0
            interview_rounds_cleared= 0
            placement_date = None



        values =(student[0],mock_interview_score,internships_completed,placement_status,company_name,placement_package,interview_rounds_cleared,placement_date)
        db.execute("""
                    insert into placements(student_id,mock_interview_score,internships_completed,placement_status,company_name,placement_package,interview_rounds_cleared,placement_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,values)

if __name__ =="__main__":
    db = database()
    insert_students_data(db,no_students=500)
    insert_programming_data(db)
    insert_soft_Skill(db)
    insert_placement_data(db)
    print('fake data inserted.....')
    db.close_connection()