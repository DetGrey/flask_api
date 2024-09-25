import sqlite3
from data_dict import random_users

def reset_db():
    # Connect to db/file - both read or create if not exists
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS members')
    
    create_table()
    create_random_members()


def create_table():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            gender TEXT,
            email TEXT,
            phonenumber TEXT,
            address TEXT,
            nationality TEXT,
            active BOOLEAN,
            github_username TEXT
        )
        """
        
        # Execute the create table query
        cur.execute(create_table_query)


def create_random_members():
    members = random_users

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        create_table()
        
        # INSERT the 10 members
        for member in members:
            create_new_member(member)
        

def create_new_member(data):
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            
            cur.execute(
                '''
                INSERT OR IGNORE INTO members (first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    data.get('first_name', None),
                    data.get('last_name', None),
                    data.get('birth_date', None),
                    data.get('gender', None),
                    data.get('email', None),
                    data.get('phonenumber', None),
                    data.get('address', None),
                    data.get('nationality', None),
                    data.get('active', None),
                    data.get('github_username', None)
                )
            )
            return [201, {"message": "New member created successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def replace_member(member_id, data):
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            
            member = find_member_by_id(member_id)
            if not member:
                create_new_member(data)

            cur.execute('''
                UPDATE members
                SET first_name = ?, last_name = ?, birth_date = ?, gender = ?, email = ?, phonenumber = ?, address = ?, nationality = ?, active = ?, github_username = ?
                WHERE id = ?
            ''', (
                data.get('first_name', None),
                data.get('last_name', None),
                data.get('birth_date', None),
                data.get('gender', None),
                data.get('email', None),
                data.get('phonenumber', None),
                data.get('address', None),
                data.get('nationality', None),
                data.get('active', None),
                data.get('github_username', None),
                member_id
            ))
            return [201, {"message": "Member replaced successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
        

def update_member(member_id, data):
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            
            query = '''
            UPDATE members
            SET 
            '''

            i = 0
            for key,value in data.items():
                if key not in query:
                    if i > 0:
                        query+= ", "

                    if isinstance(value, str):
                        query += f'{key} = "{value}"'
                    else:
                        query += f'{key} = {value}'
                    i += 1

            query += f" WHERE id = {member_id}"
            print(query)

            cur.execute(query)
            return [200, {"message": "Member updated successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def select_members():
    try:
        with sqlite3.connect('database.db') as conn:
            # Set the row factory to sqlite3.Row - By setting conn.row_factory = sqlite3.Row, you tell SQLite to return rows as sqlite3.Row objects, which can be accessed like dictionaries.
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT * FROM members')

            # Fetch all rows and convert them to dictionaries
            members = [dict(row) for row in cur.fetchall()]
            
            return [200, members]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def delete_member_by_id(id):
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()

            cur.execute('DELETE FROM members WHERE id = ?', (id,))
            return [204, {"message": "Member deleted successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def find_member_by_id(id):
    try:
        with sqlite3.connect('database.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute('SELECT * FROM members WHERE id = ?', (id,))
            data = cur.fetchall()
            if data:
                return [200, [dict(row) for row in data][0] if data else []]
            else:
                return [404, {"message": "Member not found"}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

#create_random_members()