import logging

def battle_log_msg(msg):
    """
    Writes INFO level logging for within a battle.  For maintaining the same logging style.
    Args:
        msg: <str> message to log 
    """
    logging.info('>>> {}'.format(msg))

