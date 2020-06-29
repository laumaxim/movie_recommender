from flask import Flask, render_template, request
from . import recommender as rec

app = Flask(__name__)
#making this file the 'center' of the appication
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


#python decorator
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
    user_input = request.args.to_dict() # arguments should unique
    movie_dict = {}
    for x in user_input.keys():
        if x == 'algo':
            algo_choice = int(user_input[x])
        else:
            movieid = int(x)
            rating = float(user_input[x])
            movie_dict[movieid] = rating

    # What we need to do:
        # 1. We need a function that takes in arguments.
        # 2. This function needs to make sense of the incoming strings
             # 2a. String matching? Cleaning? RegEx?
             # 2b. Or maybe you decide to not give them free-text fields.
        # 3. Function needs to convert input somehow to NumPy array.
        # 4. Use pre-trained to model and transform this array.
        # 5. The result of that you multiply with the original model components.
             # SANITY CHECK: have a np.array with shape (1, ~9719)
        # 6. Sort by highest values.
        # 7. And finally, map back to titles.


    # movies_list = recommender.nmf(user_movies, user_ratings) <- What we want!

    if algo_choice == 0:
        movies_list = rec.cosim_predict(movie_dict)
    elif algo_choice == 1:
        movies_list = rec.get_top_predict(movie_dict)
    else:
        pass
    return render_template('results.html', movies_html = movies_list)
