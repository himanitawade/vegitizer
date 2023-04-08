from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://3pp3x53q6e904br93px7:pscale_pw_kjC25WE4MayogwMbyF8e7IZPNU8vxaSk9bsMlHlMFo5@aws.connect.psdb.cloud/vegitizerwebapp?charset=utf8mb4"
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
