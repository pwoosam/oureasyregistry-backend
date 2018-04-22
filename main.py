from flask import Flask
from utilities import send_text

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def welcome_page():
    return ""


@app.route('/send_text/<int:phone_number>/<message>')
def send_message_to_number(phone_number: int, message: str):
    send_text(phone_number, message)
    return f"Sent {message} to {phone_number}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="9001")
