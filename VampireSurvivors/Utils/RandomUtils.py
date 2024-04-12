_NON_REPLICATED_ID = 0


def get_new_id():
    global _NON_REPLICATED_ID
    _NON_REPLICATED_ID += 1
    return _NON_REPLICATED_ID
