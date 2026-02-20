from __future__ import annotations

import logging
import os
import sys
from typing import Optional


def _parse_bool(value: Optional[str]) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def configure_logging() -> bool:
    """Configure logging based on DEBUG=<bool>. Returns True if enabled."""
    enabled = _parse_bool(os.getenv("DEBUG"))
    if not enabled:
        logging.disable(logging.CRITICAL)
        return False

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(filename)s:%(lineno)d %(message)s",
    )
    _install_excepthook()
    return True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def _install_excepthook() -> None:
    def _excepthook(exctype, value, tb):
        if exctype is KeyboardInterrupt:
            sys.__excepthook__(exctype, value, tb)
            return
        logging.getLogger().error("Unhandled exception", exc_info=(exctype, value, tb))

    sys.excepthook = _excepthook
