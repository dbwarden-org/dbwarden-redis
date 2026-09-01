from __future__ import annotations

__version__ = "0.1.0"

DBWARDEN_PLUGIN_API = 1


def setup(registrar) -> None:
    """Register this plugin with DBWarden.

    This is a value-only plugin that provides ``migration_lock`` and
    ``sync_migration_lock`` as importable utilities. It does not register
    any hooks; users import the lock functions directly.
    """
