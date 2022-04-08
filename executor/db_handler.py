import sqlite3

class DB_Handler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.__create_tables()

    def __create_tables(self):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS gesture_app_mapper(gesture_id integer, app_id integer)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS app_info(app_id integer, app_path text, canonical_app_name text, common_app_name text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS special_gesture_info(app_id integer, gesture_id integer, command text, system_hook text, hook_value text)''')
        connection.commit()

    """
    Operations on gesture
    """
    def add_gesture(self, request):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("insert into gesture_app_mapper values (?, ?)", (request['gesture_id'], request['app_id']))
        cur.execute("insert into app_info values (?, ?, ?, ?)", (request['app_id'], request['app_path'], request['canonical_app_name'], request['common_app_name']))
        connection.commit()

    def get_gesture_details(self, gesture_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select app_id from gesture_app_mapper where gesture_id=:gesture_id",{"gesture_id": gesture_id})
        app_id = cur.fetchone()
        if app_id == None:
            return ""
        app_id = app_id[0]    
        cur.execute("select * from app_info where app_id=:app_id",{"app_id": app_id})
        record = cur.fetchone()
        response = {}
        response['app_id'] = record[0]
        response['app_path'] = record[1]
        response['canonical_app_name'] = record[2]
        response['common_app_name'] = record[3]
        return response

    def delete_gesture(self, gesture_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select app_id from gesture_app_mapper where gesture_id=:gesture_id",{"gesture_id": gesture_id})
        app_id = cur.fetchone()
        if app_id == None:
            return ""
        app_id = app_id[0]
        cur.execute("delete from gesture_app_mapper where gesture_id=:gesture_id",{"gesture_id": gesture_id})
        cur.execute("delete from app_info where app_id=:app_id",{"app_id": app_id})
        connection.commit()

    """
    Operations for app info
    """
    def get_app_details(self, gesture_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select app_id from gesture_app_mapper where gesture_id=:gesture_id",{"gesture_id": gesture_id})
        app_id = cur.fetchone()
        if app_id == None:
            return "", ""
        app_id = app_id[0]
        cur.execute("select * from app_info where app_id=:app_id",{"app_id": app_id})
        record = cur.fetchone()
        return record[0], record[3]

    def get_app_path(self, app_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select app_path from app_info where app_id=:app_id",{"app_id": app_id})
        return cur.fetchone()[0]

    def get_canonical_app_name(self, app_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select canonical_app_name from app_info where app_id=:app_id",{"app_id": app_id})
        return cur.fetchone()[0]

    def get_app_list(self):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select * from gesture_app_mapper")
        records = cur.fetchall()
        cur.execute("select common_app_name from app_info")
        app_names = cur.fetchall()
        response = {}
        for rec, app_name in zip(records, app_names):
            gesture_id = rec[0]
            app_id = rec[1]
            name = app_name[0]
            response[gesture_id] = {'app_id': app_id, 'app_name': name}
        return response

    """
    Operations for special gesture info
    """
    def add_special_gesture_details(self, request):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("insert into special_gesture_info values (?, ?, ?, ?, ?)", (request['app_id'], request['gesture_id'], request['command'], request['system_hook'], request['hook_value']))
        connection.commit()

    def get_special_gesture_details(self, app_id, gesture_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("select * from special_gesture_info where app_id=:app_id and gesture_id=:gesture_id",{"app_id": app_id, "gesture_id": gesture_id})
        record = cur.fetchone()
        if record == None:
            return ""
        response = {}
        response['app_id'] = record[0]
        response['gesture_id'] = record[1]
        response['command'] = record[2]
        response['system_hook'] = record[3]
        response['hook_value'] = record[4]
        return response

    def delete_special_gesture_details(self, app_id, gesture_id):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        cur.execute("delete from special_gesture_info where app_id=:app_id and gesture_id=:gesture_id",{"app_id": app_id, "gesture_id": gesture_id})
        connection.commit()

"""
gesture_app_mapper = {
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

app_info = {
    1: "/Applications/Microsoft\ Outlook.app",
    2: "/Applications/Safari.app",
    3: "/Applications/GarageBand.app",
    4: "/Applications/Trello.app"
}

canonical_app_name = {
    1: "Microsoft\ Outlook",
    2: "Safari",
    3: "GarageBand",
    4: "Trello"
}

def get_app_details(gesture_id):
    if gesture_id in gesture_app_mapper:
        app_id = gesture_app_mapper[gesture_id]
        app_name = canonical_app_name[app_id]
        return app_id, app_name
    else:
        return None, None

def get_app_path(app_id):
    if app_id in app_info:
        return app_info[app_id]
    else:
        return None

def get_canonical_app_name(app_id):
    if app_id in canonical_app_name:
        return canonical_app_name[app_id]
    else:
        return None
"""        