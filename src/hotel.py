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
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    args = reqparse.RequestParser()
    args.add_argument('nome', type=str, required=True, help='This fild cannot be blank')
    args.add_argument('estrelas', type=float, required=True, help='This fild cannot be blank')
    args.add_argument('diaria', type=float, required=True, help='This fild cannot be blank')
    args.add_argument('cidade', type=str, required=True, help='This fild cannot be blank')
            
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        
        return {'message':'Hotel not found.'},404

    def post(self, hotel_id):

        if(HotelModel.find_hotel(hotel_id)):
            return {'message': f'Hotel ID {hotel_id} already exists.'}, 400
        
        dados = Hotel.args.parse_args()
        hotel = HotelModel(hotel_id, **dados) #conseito *args **kwargs
        try:
            hotel.save_hotel()
        except:
            return {'message':'An error ocurrent trying to save dada.'}, 500
        return hotel.json()


    def put(self, hotel_id):
        dados = Hotel.args.parse_args()

        finded_hotel = HotelModel.find_hotel(hotel_id)

        if finded_hotel:
            finded_hotel.update_hotel(**dados)
            finded_hotel.save_hotel()
            return finded_hotel.json(), 200

        hotel = HotelModel(hotel_id, **dados) #conseito *args **kwargs

        try:
            hotel.save_hotel()
        except:
            return {'message':'An error ocurrent trying to save dada.'}, 500

        return hotel.json(), 201 # created

    def delete(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message':'An error ocurrent trying to delete dada.'}, 500
        
            return {'massage': 'Hotel deleted.'}
        return {'massage': 'Hotel not found.'}, 404