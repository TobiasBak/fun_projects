_NON_REPLICATED_ID = 0
import time


def get_new_id():
    global _NON_REPLICATED_ID
    _NON_REPLICATED_ID += 1
    return _NON_REPLICATED_ID


def current_milli_time():
    return round(time.time() * 1000)
