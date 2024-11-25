from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'owner_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self): # FINI
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        try:
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {"error": "Invalid place id"}, 404
            if review_data['owner_id'] != current_user['id']:
                return {"error": "Unauthorized action"}, 403

            review = facade.create_review(review_data)
            return {
                "id": review['id'],
                "text": review['text'],
                "rating": review['rating'],
                "owner_id": review['owner_id'],
                "place_id": review['place_id']
            }, 201
        except Exception as e:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        if not reviews:
            return {'message': 'No reviews found'}, 404
        return [{"id": review.id, "text": review.text, "rating": review.rating, "owner_id": review.owner_id } for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id): # FINI
        """Update a review's information"""
        current_user = get_jwt_identity()
        review_data = api.payload

        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404

        if not current_user['is_admin']:
            if existing_review.owner_id != current_user['id']:
                return {'error': 'You cant update someone else review'}, 403

        try:
            facade.update_review(review_id, api.payload)
        except Exception as e:
            return {"error": "Invalid input data"}, 400

        return {"message": "Review updated successfully"}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id): # FINI
        """Delete a review"""
        current_user = get_jwt_identity()
        existing_review = facade.get_review(review_id)

        if not existing_review:
            return {'error': 'Review not found'}, 404

        if not current_user["is_admin"]:
            if existing_review.owner_id != current_user['id']:
                return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)

        if not reviews:
            return {'message': 'No reviews found for this place'}, 404

        return [{"id": review.id, "text": review.text, "rating": review.rating, "owner_id": review.owner_id } for review in reviews], 200
