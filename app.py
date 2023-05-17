from flask import Flask, render_template, jsonify, request, session
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
from recommender import get_substitute
from flask_session import Session
from youtube_search import youtube_search

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)


@app.route("/api/jobs")
def list_jos():
  return jsonify(load_jobs_from_db())


@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)

  return render_template('application_submitted.html',
                         application=data,
                         job=job)


#@app.route("/enter_meat" )
#def get_meat_selection():
 # return render_template('enter_meat.html')
@app.route("/enter_meat", methods=['GET', 'POST'])
def get_meat_selection():
    if request.method == 'POST':
        meat = request.form.get('meat')
        substitutes = get_substitute(meat)
        session['substitutes'] = substitutes
        return render_template('enter_meat.html', result=meat, result_items=substitutes)
    return render_template('enter_meat.html')

@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    # Retrieve the list of items from the session
    items = session.get('items', [])
    
    # Build the search string
    search_string = 'vegetarian+recipes+with' + '+'.join(items)

    # Perform the YouTube search and get the video id
    videos = youtube_search(search_string)
    video_id = videos[0].split(' ')[-1][1:-1] if videos else None

    # Render the template with the video id
    return render_template('recipes.html', video_id=video_id)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)