from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from utilities import send_text

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Our Easy Registry API')

sms_ns = api.namespace('sms', description='Send and recieve SMS texts')
phone_message_model = api.model('Phone Message', {
    'phone_number': fields.Integer(required=True, example=17143335555, description="A phone number including country code"),
    'message': fields.String(required=True, description="The message to send to the number")
})


@sms_ns.route('/')
class SMS(Resource):
    '''Enables two factor authentication.'''
    @sms_ns.expect(phone_message_model)
    def post(self):
        '''Send a text message'''
        body = request.get_json()
        phone_number = body.get('phone_number')
        message = body.get('message')
        response = send_text(phone_number, message)
        if response.status_code == 200:
            return f"Sent {message} to {phone_number}"
        else:
            return f"Failed to send {message} to {phone_number}: {response.body}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001)
