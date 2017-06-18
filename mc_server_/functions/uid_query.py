def uid_query(uid, cursor=None):
    cursor.execute("SELECT * FROM participant_list WHERE uid = ?", (uid,))
    result = cursor.fetchone()
    return result
