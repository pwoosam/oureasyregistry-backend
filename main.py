from flask import Flask, request, abort
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from utilities import send_text
from peewee import SqliteDatabase, Model, CharField, BooleanField, DecimalField

# setup app and CORS
app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Our Easy Registry API')

db = SqliteDatabase('ezregistry.db')

class Item(Model):
    name = CharField()
    price = DecimalField()
    url = CharField()
    is_purchased = DecimalField()

    class Meta:
        database = db

db.connect()
db.create_tables([Item])

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
create_item_model = api.model('Create Item Model', {
    'name': fields.String(required=True),
    'price': fields.Float(required=True),
    'url': fields.String(required=True)
})
update_item_model = api.model('Insert Row Model', {
    'name': fields.String(required=True),
    'is_purchased': fields.Boolean(required=True)
})
delete_item_model = api.model('Delete Item Model', {
    'name': fields.String(required=True)
})
item_model = api.model('Item Model', {
    'name': fields.String(required=True),
    'price': fields.Float(required=True),
    'url': fields.String(required=True),
    'is_purchased': fields.Boolean(required=True)
})


@db_ns.route('/item')
class DB(Resource):
    @db_ns.marshal_list_with(item_model)
    def get(self):
        '''Get all items'''
        items = Item.select()
        x = []
        for item in items:
            x.append({
                'name': str(item.name),
                'price': float(item.price),
                'url': str(item.url),
                'is_purchased': bool(item.is_purchased)
            })

        return x

    @db_ns.expect(update_item_model)
    def put(self):
        '''Update an existing item'''
        body = request.get_json()
        name = body.get('name')
        is_purchased = body.get('is_purchased')
        item = Item.select().where(Item.name == name)
        item.is_purchased = is_purchased
        item.save()

    @db_ns.expect(create_item_model)
    def post(self):
        '''Create a new item'''
        body = request.get_json()
        name = body.get('name')
        price = body.get('price')
        url = body.get('url')
        
        item = Item.create(name=name, price=price, url=url, is_purchased=False)
        item.save()


@db_ns.route('/<name>')
class DBGet(Resource):
    @db_ns.marshal_with(item_model, envelope='resource')
    def get(self, name):
        '''Gets a single item by name'''
        try:
            item = Item.select().where(Item.name == name).get()
        except Exception:
            return abort(404)
        return {
            'name': str(item.name),
            'price': float(item.price),
            'url': str(item.url),
            'is_purchased': bool(item.is_purchased)
        }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001)
