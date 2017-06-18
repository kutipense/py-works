from functions.registration import new_record
from functions.uid_query import uid_query
from uuid import uuid1


def inc(uid, counter, cursor=None):
    cursor.execute(
        "UPDATE participant_list SET counter = ?, control = 1 WHERE uid = ?", (counter + 1, uid))
    return counter + 1


def uid_increment(uid, cursor=None):
    result = "SESSION_IS_NOT_OVER_YET"
    query = uid_query(uid, cursor)
    if query == None:
        uniqe_id = str(uuid1())
        new_record(uniqe_id, *["YTUIEEECS" for i in range(5)], uid, counter=1, control=1, cursor=cursor)
        result = "NEW_RECORD_WITHOUT_NUMBER"
    elif query[-1] == 0:
        new_counter = inc(uid, query[-2], cursor=cursor)
        result = "COUNTER_INCREASED_%s" % new_counter
    return result
