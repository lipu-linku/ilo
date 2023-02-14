"""
Create and configure a Logger for ilo Linku.
To use the logger:
  - Run `configure_logger()` once, close to the start of runtime
  - Run `logging.getLogger("ilo")` in any module that intends to log
"""


import logging
from functools import partial

LOG_FORMAT = (
    "[%(asctime)s] [%(filename)22s:%(lineno)-4s] [%(levelname)8s]   %(message)s"
)


def configure_logger(
    logger: str,
    log_level: int = logging.DEBUG,
    stacktrace_level: int = logging.ERROR,
) -> None:
    _log = logging.getLogger(logger)
    _log.setLevel(log_level)
    # level set on a per-logger basis to avoid 'discord' logger

    logging.basicConfig(format=LOG_FORMAT)
    if stacktrace_level > logging.NOTSET:
        if stacktrace_level <= logging.DEBUG:
            _log.debug = partial(_log.debug, exc_info=True, stack_info=True)
        if stacktrace_level <= logging.INFO:
            _log.info = partial(_log.info, exc_info=True, stack_info=True)
        if stacktrace_level <= logging.WARNING:
            _log.warning = partial(_log.warning, exc_info=True, stack_info=True)
        if stacktrace_level <= logging.ERROR:
            _log.error = partial(_log.error, exc_info=True, stack_info=True)
        if stacktrace_level <= logging.CRITICAL:
            _log.critical = partial(_log.critical, exc_info=True, stack_info=True)
            _log.fatal = partial(_log.fatal, exc_info=True, stack_info=True)
