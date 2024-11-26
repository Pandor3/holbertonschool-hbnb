from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')


place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.String(required=True, description='ID of the owner'),
    'id': fields.String(required=True, description='ID of the place'),
})

@api.route('/')
class PlaceList(Resource): # FINI
    @jwt_required()  # need access token
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        if place_data['owner_id'] != current_user['id']:
            return {'error': 'Unauthorized action.'}, 403

        try:
            place_data = facade.create_place(place_data)
            return {"title": place_data['title'],
                    "description": place_data['description'],
                    "price": place_data['price'],
                    "latitude": place_data['latitude'],
                    "longitude": place_data['longitude'],
                    "owner_id": place_data['owner_id'],
                    "id": place_data['id']}, 201
        except ValueError as e:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        if not places:
            return {'message': 'No places found'}, 404

        return [place.to_dict() for place in places], 200


@api.route('/<place_id>') # FINI
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def get(self, place_id):
        """Get place details by ID"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner_id != current_user['id']:
            return {'error': 'You are not the place owner'}, 403

        owner = facade.get_user(place.owner_id)
        if not owner:
            return {'error': "Owner not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            },
            "reviews": [{"id": review.id, "text": review.text, "rating": review.rating, "user_id": review.user_id} for review in place.reviews],
            "amenities": [{ "id": i.id, "name": i.name } for i in place.amenities]
        }, 200

    @api.expect(place_model) # FINI
    @jwt_required()  # need access token
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place_data = api.payload

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not current_user['is_admin']:
            if place.owner_id != current_user['id']:
                return {"message": "Unauthorized to update the place"}, 403

        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {'error': 'Place not found'}, 404

        return {"message": "Place updated successfully"}, 200

    @jwt_required()  # need access token
    @api.response(200, 'Place delete successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not current_user["is_admin"]:
            if current_user["id"] != place.owner_id:
                return {"error": "Unauthorized action"}, 403

        for review in place.reviews:
            facade.delete_review(review['id'])

        for amenity in place.amenities:
            facade.delete_amenity(amenity.id)

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200

@api.route("/<place_id>/add_amenity/<amenity_id>")
class PlaceAmenity(Resource):
    @jwt_required()
    @api.response(200, "Add amenity to place.")
    @api.response(404, "Place not found")
    @api.response(404, "Amenity not found")
    def post(self, place_id, amenity_id):
        """Associate an amenity to a place."""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Invalid place id"}

        if current_user["id"] != place.owner_id:
            return { "error": "Unauthorized action." }, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"message": "Add amenity to place"}

        place.amenities.append(amenity)
        return {"message": "Add amenity to place"}, 200
