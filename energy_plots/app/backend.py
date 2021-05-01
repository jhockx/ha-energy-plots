from time import sleep

from app import app


def main_thread():
    while True:
        app.logger.info('Hello from the main thread!')
        sleep(10)
