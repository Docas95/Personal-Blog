# this is the file that makes our website run
from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
