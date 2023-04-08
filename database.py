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
