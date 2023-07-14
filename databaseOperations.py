from database import DatabaseManager, UserMain, UserOptional

def getInfo():
    db_manager = DatabaseManager()
    session = db_manager.session
    result = []
    
    user_main_data = session.query(UserMain.chat_id, UserMain.first_name, UserMain.username).all()
    user_optional_data = session.query(UserOptional.chat_id, UserOptional.official_name, UserOptional.group).all()

    for user_main_row in user_main_data:
        chat_id = user_main_row.chat_id
        first_name = user_main_row.first_name
        username = user_main_row.username
        
        official_name = ""
        group = ""
        
        for user_optional_row in user_optional_data:
            if user_optional_row.chat_id == chat_id:
                official_name = user_optional_row.official_name or ""
                group = user_optional_row.group or ""
                break
        
        result.append((chat_id, first_name, username, official_name, group))
    
    db_manager.close()
    return result
