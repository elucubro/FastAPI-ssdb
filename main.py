from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

origins = ["*"]



conn = psycopg2.connect(
    host="192.168.0.7",
    database="ssdb",
    user="xescr",
    password="xeschewmonster23"
)

cursor = conn.cursor()


class Student(BaseModel):
    name: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/student/{student_name}/skills")
async def read_student(student_name: str, q: str | None = None):
    if q:
        return {"student_name": student_name, "q": q}
    cursor.execute("select name from skill where id in (select skill_id from student_skill where student_id = (select id from student where name = %s));",(student_name,))
    return {"thing1": cursor.fetchall()}

@app.get("/student/{student_name}")
async def read_student(student_name: str, q: str | None = None):
    if q:
        return {"student_name": student_name, "q": q}
    cursor.execute("select name, level FROM student_skill JOIN skill ON student_skill.student_id = (SELECT id FROM student WHERE name = %s) AND student_skill.skill_id = skill.id;",(student_name,))
    skills = cursor.fetchall()
    skills = dict(skills)
    cursor.execute("select name from project where id in (select project_id from student_project where student_id = (select id from student where name = %s));",(student_name,))
    projects = cursor.fetchall()
    projects = ([row[0] for row in projects]) # converting to actual list
    print(projects)
    list7 = []
    for i in range(len(list(skills))):
        x = i - 1
        list7.append({"axis": list(skills)[x], "values": list(skills.values())[x]})
    graph = {"className": student_name, "axes": list7}
    print(graph)
    print({"skills": skills, "name": student_name, "projects": projects, "graph": graph})
    return {"skills": skills, "name": student_name, "projects": projects, "graph": graph}