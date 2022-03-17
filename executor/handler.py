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
        