from bottle import route, run


@route('/')
def hello_worl():
    return 'Hello'


if __name__ == '__main__':
    run()
