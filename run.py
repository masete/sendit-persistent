from api.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


"""
export FLASK_ENV=DEVELOPMENT
echo $FLASK_ENV
"""
