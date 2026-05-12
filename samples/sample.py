# Sample code with intentional issues for the agent to review

def get_user(id):
    import sqlite3
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")  # SQL injection
    result = cursor.fetchone()
    conn.close()
    return result


def calculate_discount(price, pct):
    d = price * pct / 100
    r = price - d
    return r


def process_items(items):
    results = []
    for i in range(len(items)):  # should use enumerate or direct iteration
        item = items[i]
        if item != None:        # should use `is not None`
            results.append(item * 2)
    return results


class DataProcessor:
    def __init__(self):
        self.data = []

    def load(self, filename):
        f = open(filename)      # file handle never closed
        self.data = f.read().splitlines()

    def transform(self):
        pass                    # not implemented, no error raised
