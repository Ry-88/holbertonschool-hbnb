from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

def get_current_user_id():
    ident = get_jwt_identity()
    return ident if isinstance(ident, str) else ident.get("id")

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Register a new review"""
        user_id = get_current_user_id()

        place = facade.get_place(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 400
        if getattr(place, "owner_id", None) == user_id:
            return {"error": "You cannot review your own place"}, 400
        
        all_reviews = facade.get_reviews_by_place(data["place_id"])
        for review in all_reviews:
            user_id_cmp = review.get("user_id")
            if not user_id_cmp:
                continue  
            if user_id_cmp == user_id:
                return {"error": "You have already reviewed this place"}, 400
        
        try:
            data = request.json
            review_obj = facade.create_review(data)
            return {
                "Review id": str(review_obj.id),
                "text": review_obj.text,
                "rating": int(review_obj.rating),
                "user_id": str(review_obj.user.id),
                "place_id": str(review_obj.place.id)
            }, 201
        except Exception as e:
            return {'message': str(e)}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                "Review id": str(r.id),
                "text": r.text,
                "rating": int(r.rating),
                "user_id": str(r.user.id),
                "place_id": str(r.place.id)
            }
            for r in reviews
        ], 200



@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.expect(review_model,validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403
        
        try:
            data = request.json
            review_obj = facade.update_review(review_id, data)
            if review_obj:
                return {"message": "Review updated successfully"}, 200
            else:
                return {'message': 'Review not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {'message': 'Review not found'}, 404

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)

        return [
            {
                "Review id": str(r.id),
                "text": r.text,
                "rating": int(r.rating),
                "user_id": str(r.user.id),
                "place_id": str(r.place.id)
            }
            for r in reviews
        ], 200