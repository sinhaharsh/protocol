import logging
from pathlib import Path

INFO_FORMATTER = '%(filename)s:%(name)s:%(funcName)s:%(lineno)d: %(message)s'
"""Debug file formatter."""

ERROR_FORMATTER = '%(asctime)s - %(levelname)s - %(message)s'
"""Log file and stream output formatter."""

ROOT_FOLDER = Path.home() / '.protocol'
"""Root folder for mrQA."""
if not ROOT_FOLDER.exists():
    ROOT_FOLDER.mkdir(parents=True, exist_ok=True)

WARN_FILE = ROOT_FOLDER / 'warn.log'
"""Debug file name."""

ERROR_FILE = ROOT_FOLDER / 'error.log'
"""Log file name."""


def init_log_files(log, mode='w'):
    """
    Initiate log files.

    Parameters
    ----------
    log : logging.Logger
        The logger object.
    mode : str, (``'w'``, ``'a'``)
        The writing mode to the log files.
        Defaults to ``'w'``, overwrites previous files.    """

    # db = logging.FileHandler(WARN_FILE, mode=mode)
    # db.setLevel(logging.DEBUG)
    # db.setFormatter(logging.Formatter(INFO_FORMATTER))

    error = logging.FileHandler(ERROR_FILE, mode=mode)
    error.setLevel(logging.ERROR)
    error.setFormatter(logging.Formatter(ERROR_FORMATTER))

    # log.addHandler(db)
    log.addHandler(error)
