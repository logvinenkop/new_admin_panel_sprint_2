import sys, logging


def log():
    _log_handler = logging.StreamHandler(sys.stdout)
    _log_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)-7.7s]  %(message)s")
    )
    _log = logging.getLogger("migration")
    _log.setLevel(logging.DEBUG)
    if not _log.hasHandlers():
        _log.addHandler(_log_handler)
    return _log
