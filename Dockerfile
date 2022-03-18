heroku login
heroku container:login
heroku create
# Creating app... done, ⬢ your-app-name
heroku container:push web --app computer-science-flash-cards-main
heroku container:release web --app computer-science-flash-cards-main
heroku open --app computer-science-flash-cards-main