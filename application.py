import logging
from meme_generator import create_app

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    application = create_app()
    application.run()
