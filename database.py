from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      row_as_dict = row._mapping
      jobs.append(row_as_dict)
  return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    val = {'id': id}
    query = text("select * from jobs where id = :id")
    result = conn.execute(query, val)
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      value = rows[0]._asdict()
      return value


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    val = {
      'job_id': job_id,
      'full_name': data['full_name'],
      'email': data['email'],
      'linkedin_url': data['linkedin_url'],
      'education': data['education'],
      'work_experience': data['work_experience'],
      'resume_url': data['resume_url']
    }
    query = text(
      "INSERT INTO applications(job_id,full_name,email,linkedin_url,education,work_experience,resume_url) VALUES (:job_id,:full_name,:email,:linkedin_url,:education,:work_experience,:resume_url)"
    )

    conn.execute(query, val)

def load_veg_from_db():
  with engine.connect() as conn:
    query = text("select * from veg")
    result = conn.execute(query)
    results = []
    for row in result.all():
      row_as_dict = row._mapping
      results.append(row_as_dict)
  return (results)

def load_non_veg_from_db():
  with engine.connect() as conn:
    query = text("select * from non_veg")
    result = conn.execute(query)
    results = []
    for row in result.all():
      row_as_dict = row._mapping
      results.append(row_as_dict)
  return results
  
def add_feedback_to_db(name, email, message):
    with engine.connect() as conn:
        val = {
            'name': name,
            'email': email,
            'message': message
        }
        query = text(
            "INSERT INTO feedbacks (name, email, message) VALUES (:name, :email, :message)"
        )

        conn.execute(query, val)