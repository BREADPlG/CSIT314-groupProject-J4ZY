from backend.repository.db import get_conn

class AccountService:
    def __init__(self):
        pass

    # Create
    def create_account(self, email, password, name, phone, role, status):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO accounts (email, password, name, phone, role, status) VALUES (?, ?, ?, ?, ?, ?)",
                (email, password, name, phone, role, status)
            )
            conn.commit()
            account_id = cur.lastrowid
            return {"id": account_id, "email": email, "password": password, "name": name, "phone": phone, "role": role, "status": status }
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # Retrieve one
    def get_account_by_id(self, account_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE id = ? ORDER BY id ASC", (account_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_account_by_name(self, name):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE name = ? ORDER BY id ASC", (name,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_account_by_name(self, email):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE email = ? ORDER BY id ASC", (email,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    # Retrieve all
    def list_accounts(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM accounts ORDER BY id ASC")
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
    
    # Update
    def update_account(self, account_id, **updates):
        if not updates:
            raise ValueError("No fields to update")

        keys = list(updates.keys())
        values = list(updates.values())
        set_clause = ", ".join(f"{k}=?" for k in keys)
        values.append(account_id)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(f"UPDATE accounts SET {set_clause} WHERE id = ?", values)
        conn.commit()
        conn.close()
        return {"updated_id": account_id}

    # Delete
    def delete_account(self, account_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        if not deleted:
            raise ValueError("Account not found")
        return {"deleted_id": account_id}
