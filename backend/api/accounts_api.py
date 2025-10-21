from flask import Blueprint, request, jsonify
from accounts_controller import AccountController
from accounts_service import AccountService

# Blueprint for accounts endpoints
accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

# Initialize service and controller
service = AccountService()
controller = AccountController(service)

# Create account
@accounts_bp.post("/")
def create_account():
    data = request.get_json()
    return controller.create(data)

# Get single account by ID
@accounts_bp.get("/<int:account_id>")
def get_account(account_id):
    return controller.retrieve(account_id)

# List all accounts
@accounts_bp.get("/")
def list_accounts():
    return controller.list()

# Update account
@accounts_bp.put("/<int:account_id>")
def update_account(account_id):
    data = request.get_json()
    return controller.update(account_id, data)

# Delete account
@accounts_bp.delete("/<int:account_id>")
def delete_account(account_id):
    return controller.delete(account_id)
