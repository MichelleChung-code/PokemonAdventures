import logging
import time
import functools
import getpass

ext_data = {'user': getpass.getuser()}


class BattleError(Exception):
    """An exception class for Battle"""
    pass


def battle_timing_decorator(func):
    """ Decorator to time individual battle execution """

    @functools.wraps(func)  # carry over docstrings and metadata of the input function
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func_result = func(*args, **kwargs)
        t2 = time.time()

        res_str = f'{func.__name__} time taken: {(t2 - t1) * 1000} ms'
        battle_log_msg(res_str)
        print(res_str)

        return func_result

    return wrapper


def battle_log_msg(msg):
    """
    Writes INFO level logging within a battle.  For maintaining the same logging style.
    Args:
        msg: <str> message to log
    """
    logging.info('>>> {}'.format(msg), extra=ext_data)


def unittest_failure_msg(msg):
    """
    Sets up the message format for when unittests fail.
    Args:
        msg: <str> message to throw when unittests fail
    """
    return 'Unexpected Behaviour: {}'.format(msg)
