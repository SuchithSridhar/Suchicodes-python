from suchiblog import create_app
import logging


if __name__ == '__main__':
    logging.basicConfig(filename="suchiblog/logs/logs.log", level=logging.INFO)

    app = create_app()
    app.run(debug=True)
