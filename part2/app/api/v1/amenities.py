from flask import request
from flask_restx import Namespace, Resource, fields
from ..services import amenities as svc

ns = Namespace("amenities", description="Amenity management")

amenity_out = ns.model("Amenity", {
    "id": fields.String,
    "name": fields.String,
    "description": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})

amenity_in = ns.model("AmenityCreate", {
    "name": fields.String(required=True),
    "description": fields.String,
})

amenity_upd = ns.model("AmenityUpdate", {
    "name": fields.String,
    "description": fields.String,
})

@ns.route("/")
class AmenityList(Resource):
    @ns.marshal_list_with(amenity_out, code=200, description="List of amenities")
    def get(self):
        body, status = svc.list_amenities()
        return body, status

    @ns.expect(amenity_in, validate=True)
    @ns.marshal_with(amenity_out, code=201, description="Amenity created")
    def post(self):
        data = request.get_json() or {}
        body, status = svc.create_amenity(data)
        return body, status

@ns.route("/<string:amenity_id>")
@ns.param("amenity_id", "Amenity identifier")
class AmenityItem(Resource):
    @ns.marshal_with(amenity_out, code=200, description="Amenity by id")
    def get(self, amenity_id):
        body, status = svc.get_amenity(amenity_id)
        return body, status

    @ns.expect(amenity_upd, validate=True)
    @ns.marshal_with(amenity_out, code=200, description="Amenity updated")
    def put(self, amenity_id):
        data = request.get_json() or {}
        if not any(k in data for k in ("name", "description")):
            return {"error": "No updatable fields provided"}, 400
        body, status = svc.update_amenity(amenity_id, data)
        return body, status
