# Getting started with Flask and Heroku

Instruction for deploying this small web application written in Flask to a Heroku cloud.
The app asks the user for a list of movies, then asks to rate those movies as "Top" or "Flop", good or bad movies respectively.
The app utilizes a dataset of movies and movie ratings made by humans on an online website.
The user has a choice of two methods of recommendation: simply a list of top-rated, but unwatched movies or a list of recommended movies created by collaborative filtering. Cosine similarity is used to compare the user rating to the ratings in the dataset and the most similiar movies are then recommended.

Follow the steps below to run the app.

## Requirements

- free heroku account
- heroku cli installed and set up locally 

## Instructions

1. clone the repository

2. create a new heroku app

```bash
heroku create <my-app-name>
```

3. test the app locally

```bash
heroku local web
```

on windows use 

```bash
heroku local web -f Procfile.windows
```

4. push code to heroku

```bash
git push heroku master
```

5. open website in browser

```bash
heroku open
```


## Further Ressources

- [Official python heroku tutorial](https://devcenter.heroku.com/articles/getting-started-with-python) using Django

The dataset:
> F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. <https://doi.org/10.1145/2827872>