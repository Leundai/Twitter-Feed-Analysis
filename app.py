import os
from api import create_app

app = create_app()

if __name__ == "__main__":
    if os.environ.get("DEBUG", "False") == "True":
        print("Running prod")
        app.run()
    else:
        print("Running dev")
        app.run(debug=True)
