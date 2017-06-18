from functions.uid_query import uid_query


def phoneNumber_query(number, cursor=None):
    cursor.execute(
        "SELECT * FROM participant_list WHERE phoneNumber = ?", (number,))
    result = cursor.fetchone()
    return result


def participant_info(number, uid, cursor=None):
    result = "NOT_FOUND"
    query = phoneNumber_query(number, cursor=cursor)
    if query == None:
        query = uid_query(uid, cursor=cursor)
    if query != None:
        result = ';'.join(query[1:-2])
    return result
