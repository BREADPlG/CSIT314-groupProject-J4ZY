import re
import uuid
from werkzeug.security import generate_password_hash
from backend.repository.db import get_conn
from flask import jsonify

class AccountController:
    def __init__(self, service):
        self.service = service

    # Create
    def create(self, payload: dict):
        required_fields = ["email", "password", "name", "phone", "role", "status"]
        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Validate email format
        if "@" not in payload["email"]:
            return jsonify({"error": "Invalid email address. Must contain '@'"}), 400

        # Validate password length
        if len(payload["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        conn = get_conn()
        cursor = conn.cursor()

        try:
            # Check for duplicate email
            cursor.execute("SELECT 1 FROM accounts WHERE email = ?", (payload["email"],))
            if cursor.fetchone():
                return jsonify({"error": "Email already registered"}), 409

            # Check for duplicate name
            cursor.execute("SELECT 1 FROM accounts WHERE name = ?", (payload["name"],))
            if cursor.fetchone():
                return jsonify({"error": "Name already taken"}), 409

            # Check for duplicate phone
            cursor.execute("SELECT 1 FROM accounts WHERE phone = ?", (payload["phone"],))
            if cursor.fetchone():
                return jsonify({"error": "Phone number already registered"}), 409

            # Hash password
            password_hash = generate_password_hash(payload["password"])

            # Generate unique ID
            account_id = str(uuid.uuid4())

            # Insert account into DB
            cursor.execute("""
                INSERT INTO accounts (id, email, password, name, phone, role, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                account_id,
                payload["email"],
                password_hash,
                payload["name"],
                payload["phone"],
                payload["role"],
                payload["status"]
            ))
            conn.commit()

            return jsonify({
                "message": "Account created successfully",
                "account": {
                    "id": account_id,
                    "email": payload["email"],
                    "name": payload["name"],
                    "phone": payload["phone"],
                    "role": payload["role"],
                    "status": payload["status"]
                }
            }), 201

        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()

    # Retrieve single account
    def retrieve(self, account_id):
        try:
            account = self.service.get_account_by_id(account_id)
            if not account:
                return jsonify({"error": "Account not found"}), 404
            return jsonify(account), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # List all accounts
    def list(self):
        try:
            accounts = self.service.list_accounts()
            return jsonify(accounts), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Update account
    def update(self, account_id, payload: dict):
        try:
            updated = self.service.update_account(account_id, **payload)
            return jsonify({"message": "Account updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Delete account
    def delete(self, account_id):
        try:
            deleted = self.service.delete_account(account_id)
            return jsonify({"message": "Account deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
