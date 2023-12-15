from flask import Flask, render_template, request
from . import recommender as rec

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#the app.route decorator make the output of index() 'route to '/'
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/impressum')
def impressum():
    return render_template('impressum.html')


@app.route('/movies')
def movies():
    movies=[]
    user_input = request.args.to_dict()
    if 'movielist' in user_input:
        movielist = user_input['movielist']
        ids = list(map(int, movielist.split(',')))
        titles = rec.movieId_to_title(ids)
        movies = zip(titles,ids)
    return render_template('movies.html', movies_html=movies)


@app.route('/results')
def results():
    user_input = request.args.to_dict() # arguments should be unique
    movie_dict = {}
    for x in user_input.keys():
        if x == 'algo':
            algo_choice = int(user_input[x])
        else:
            movieid = int(x)
            rating  = float(user_input[x])
            movie_dict[movieid] = rating

    if algo_choice == 0:
        movies_list = rec.cosim_predict(movie_dict)
    elif algo_choice == 1:
        movies_list = rec.get_top_predict(movie_dict)
    else:
        pass
    return render_template('results.html', movies_html = movies_list)
