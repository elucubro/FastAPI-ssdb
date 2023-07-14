from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

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


@app.get("/student/{student_name}/skills")
async def read_student(student_name: str, q: str | None = None):
    if q:
        return {"student_name": student_name, "q": q}
    cursor.execute("select name from skill where id in (select skill_id from student_skill where student_id = (select id from student where name = %s));",(student_name,))
    return {"thing1": cursor.fetchall()}