import logging

def battle_log_msg(msg):
    """
    Writes INFO level logging within a battle.  For maintaining the same logging style.
    Args:
        msg: <str> message to log
    """
    logging.info('>>> {}'.format(msg))

def unittest_failure_msg(msg):
    """
    Sets up the message format for when unittests fail.
    Args:
        msg: <str> message to throw when unittests fail
    """
    return 'Unexpected Behaviour: {}'.format(msg)
