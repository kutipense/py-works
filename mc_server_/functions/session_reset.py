def session_reset(*args, cursor=None):
    cursor.execute("UPDATE liste SET control = 0")
    return 'SESSION_HAS_RESETED'
