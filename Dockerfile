heroku login
heroku container:login
heroku create
# Creating app... done, ⬢ your-app-name
heroku container:push web --app
heroku container:release web --app
heroku open --app