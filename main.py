
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Student Management API",
    description="CRUD API for managing students",
    version="1.0.0"
)


# =========================================================
# PYDANTIC MODELS
# =========================================================

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    course: str = Field(..., min_length=1)
    age: int


class Student(StudentCreate):
    id: int


# =========================================================
# IN-MEMORY DATABASE
# =========================================================

students = []

next_id = 1


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Student Management API is running",
        "docs": "/docs"
    }


# =========================================================
# CREATE STUDENT
# POST /students
# =========================================================

@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(student_data: StudentCreate):

    global next_id

    # Check if email already exists
    for student in students:

        if student.email == student_data.email:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

    # Create new student
    new_student = Student(
        id=next_id,
        name=student_data.name,
        email=student_data.email,
        course=student_data.course,
        age=student_data.age
    )

    students.append(new_student)

    next_id += 1

    return new_student

# =========================================================
# GET ALL STUDENTS
# GET /students
# =========================================================

@app.get(
    "/students",
    response_model=list[Student]
)
def get_students():

    return students


# =========================================================
# SEARCH STUDENTS BY COURSE
#
# IMPORTANT:
# THIS MUST COME BEFORE /students/{student_id}
#
# GET /students/search?course=Python
# =========================================================

@app.get(
    "/students/search",
    response_model=list[Student]
)
def search_students(course: str):

    results = []

    for student in students:

        if course.lower() in student.course.lower():
            results.append(student)

    return results


# =========================================================
# GET STUDENT BY ID
# GET /students/{student_id}
# =========================================================

@app.get(
    "/students/{student_id}",
    response_model=Student
)
def get_student(student_id: int):

    for student in students:

        if student.id == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# =========================================================
# UPDATE STUDENT
# PUT /students/{student_id}
# =========================================================

@app.put(
    "/students/{student_id}",
    response_model=Student
)
def update_student(
    student_id: int,
    student_data: StudentCreate
):

    for index, student in enumerate(students):

        if student.id == student_id:

            updated_student = Student(
                id=student_id,
                name=student_data.name,
                email=student_data.email,
                course=student_data.course,
                age=student_data.age
            )

            students[index] = updated_student

            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# =========================================================
# DELETE STUDENT
# DELETE /students/{student_id}
# =========================================================

@app.delete(
    "/students/{student_id}"
)
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student.id == student_id:

            students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student_id": student_id
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )
