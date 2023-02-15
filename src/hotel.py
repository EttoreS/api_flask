from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id':101,
        'nome':'Alpha Hotel',
        'estrelas': 4.5,
        'diaria': 420.5,
        'cidade':'São Paulo'
    },
    {
        'hotel_id':102,
        'nome':'Bravo Hotel',
        'estrelas': 4.8,
        'diaria': 520.5,
        'cidade':'Rio de Janeiro'
    },
    {
        'hotel_id':103,
        'nome':'Delta Hotel',
        'estrelas': 2.5,
        'diaria': 120.5,
        'cidade':'São Paulo'
    },
    {
        'hotel_id':104,
        'nome':'F Hotel',
        'estrelas': 2.5,
        'diaria': 120.5,
        'cidade':'Manaus'
    }
]

class Hoteis(Resource):

    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):

    args = reqparse.RequestParser()
    args.add_argument('nome')
    args.add_argument('estrelas')
    args.add_argument('diaria')
    args.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if(hotel['hotel_id'] == hotel_id):
                return hotel
        return None
             
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message':'Hotel not found.'},404

    def post(self, hotel_id):
        
        dados = Hotel.args.parse_args()

        hotel_objetio = HotelModel(hotel_id, **dados) #conseito *args **kwargs
        new_hotel = hotel_objetio.json()

        hoteis.append(new_hotel)

        return new_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.args.parse_args()

        hotel_objetio = HotelModel(hotel_id, **dados) #conseito *args **kwargs
        new_hotel = hotel_objetio.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200

        hoteis.append(new_hotel)

        return new_hotel, 201 # created

    def delete(self, hotel_id):

        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'massage': 'Hotel deleted.'}