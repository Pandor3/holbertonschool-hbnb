from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            create_new_amenity = facade.create_amenity(amenity_data)
            return {"id": create_new_amenity.id, "Amenity successfully created": create_new_amenity.name}, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        return [{"id": index.id, "List of amenities retrieved successfully": index.name} for index in facade.get_all_amenities()], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return [{"id": amenity.id, "name": amenity.name}], 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return updated_amenity.to_dict(), 200
