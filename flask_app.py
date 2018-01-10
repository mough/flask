from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/bananas')
def hello_bananas():
    return 'Hello from Flask! Also, bananas!'


if __name__ == "__main__":
    app.run()
