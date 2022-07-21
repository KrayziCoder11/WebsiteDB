from website import create_app

#creates the app
app = create_app()

#runs the app
#debug is set to true which debugs the code every time its run (helpful for implementation, not production)
if __name__ == '__main__':
    app.run(debug = True)
