from functions.pNumber_query import phoneNumber_query
from functions.uid_query import uid_query


def new_record(*args, counter=0, control=0, cursor=None):
    cursor.execute("INSERT INTO participant_list VALUES (?,?,?,?,?,?,?,?,?)", (*args, counter, control))
    return 0


def update_record(*args, cursor=None):
    cursor.execute("UPDATE participant_list SET name = ?, mail = ?,school = ?, department = ?, grade = ? , uid= ? WHERE phoneNumber = ?", (*args[1:], args[0]))
    return 0


def delete_and_record(*args, counter, control, cursor=None):
    uid = args[-1]
    cursor.execute("DELETE FROM participant_list WHERE uid = ?", (uid,))
    cursor.execute("INSERT INTO participant_list VALUES (?,?,?,?,?,?,?,?,?)", (*args, counter, control,))
    return 0


def registration(*args, cursor=None):
    result = None
    phoneNumber, uid = args[0], args[-1]
    query_number = phoneNumber_query(phoneNumber, cursor=cursor)
    query_uid = uid_query(uid, cursor=cursor)
    if query_uid == None and query_number == None:
        new_record(*args, cursor=cursor)
        result = "NEW_RECORD"
    elif query_uid != None and query_number == None:
        counter, control = query_uid[-2], query_uid[-1]
        delete_and_record(*args, counter, control, cursor=cursor)
        result = "RECORD_UPDATED"
    elif query_uid != None and query_number[0] != query_uid[0]:
        result = "RECORDED_CARD"
    else:
        update_record(*args, cursor=cursor)
        result = "RECORD_UPDATED"
    return result
