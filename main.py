from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from utilities import send_text
from in_memory_db import create_table, insert_row, get_row, delete_row

# setup app and CORS
app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Our Easy Registry API')

sms_ns = api.namespace('sms', description='Send and recieve SMS texts')
phone_message_model = api.model('Phone Message Model', {
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


db_ns = api.namespace('db', description='Database commands')
create_table_model = api.model('Create Table Model', {
    'table_name': fields.String(required=True),
    'fields': fields.List(fields.String(), required=True)
})
get_row_model = api.model('Get Row Model', {
    'table_name': fields.String(required=True),
    'column': fields.String(required=True),
    'value': fields.String(required=True)
})
insert_row_model = api.model('Insert Row Model', {
    'table_name': fields.String(required=True),
    'columns': fields.List(fields.String(), required=True),
    'values': fields.List(fields.String(), required=True)
})


@db_ns.route('/')
class DB(Resource):
    @db_ns.expect(create_table_model)
    def put(self):
        '''Create a table'''
        body = request.get_json()
        table_name = body.get('table_name')
        fields = body.get('fields')
        create_table(table_name, fields)

    @db_ns.expect(insert_row_model)
    def post(self):
        '''Insert a row into a table'''
        body = request.get_json()
        table_name = body.get('table_name')
        columns = body.get('columns')
        values = body.get('values')
        
        data = {}
        for key, val in zip(columns, values):
            data[key] = val

        insert_row(table_name, **data)


@db_ns.route('/<table_name>/<column>/<value>')
class DBGet(Resource):
    def get(self, table_name, column, value):
        '''Gets a row from a table by the value of a column'''
        data = {column: value}
        return get_row(table_name, **data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001)
