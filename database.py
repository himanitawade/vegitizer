from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://gxc6jbmuarolf7577bdt:pscale_pw_55uMvagh0XxezA7T0Q7U9rzt8secCvVinAb7CXliAWO@ws.connect.psdb.cloud/vegitizerwebapp?charset=utf8mb4"
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
