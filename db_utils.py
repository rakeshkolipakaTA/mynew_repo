def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)

def divide(a, b):
    return a / b
