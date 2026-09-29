from flask import Blueprint, jsonify, request

from models.customer import Customer
from services.customer_service import CustomerService
from repos.customer_repository import CustomerRepository

customer_controller = Blueprint(
    "customer_controller",
    __name__
)
customer_repository = CustomerRepository()
customer_service = CustomerService(
    customer_repository
)

# GET /api/customers
@customer_controller.route("/customers", methods=["GET"])
def get_all_customers():
    customers = customer_service.get_all_customers()
    return jsonify([customer.to_dict() for customer in customers]), 200

# GET /api/customers/<id>
@customer_controller.route("/customers/<string:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = customer_service.get_customer_by_id(customer_id)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer.to_dict()), 200


# POST /api/customers
@customer_controller.route("/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    if "id" not in data or "name" not in data:
        return jsonify({"error": "id and name are required"}), 400
    
    customer = Customer(data["id"], data["name"])
    created_customer = customer_service.create_customer(customer)
    
    return jsonify(created_customer.to_dict()), 201

# PUT /api/customers/<id>
@customer_controller.route("/customers/<string:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    if "name" not in data:
        return jsonify({"error": "name is required"}), 400
    
    customer = customer_service.update_customer(customer_id, data["name"])
    
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    
    return jsonify(customer.to_dict()), 200

# DELETE /api/customers/<id>
@customer_controller.route("/customers/<string:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    deleted = customer_service.delete_customer(customer_id)
    
    if not deleted:
        return jsonify({"error": "Customer not found"}), 404
    
    return jsonify({"message": "Customer deleted successfully"}), 200
