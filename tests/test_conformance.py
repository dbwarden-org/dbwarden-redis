"""Verified (Approved) conformance suite.

These run DBWarden's shared conformance harness so a reviewer can confirm the
plugin respects the contract. Keep them green in public CI to qualify for the
Verified badge.
"""

from __future__ import annotations

import pytest
from dbwarden import plugin_conformance as conformance

import dbwarden_redis

DISTRIBUTION = "dbwarden-redis"
PACKAGE = "dbwarden_redis"

# This is a library-style plugin that does not register hooks or object handlers.
# Users import migration_lock / sync_migration_lock directly.
VALUE_HOOKS: tuple[str, ...] = ()
OBJECT_TYPES: tuple[str, ...] = ()


def test_entry_point_is_declared() -> None:
    conformance.assert_entry_point_declared(DISTRIBUTION)


def test_import_has_no_side_effects() -> None:
    conformance.assert_import_has_no_side_effects(PACKAGE)


@pytest.mark.skip(reason="library-style plugin; setup() has no hooks to register")
def test_setup_registers_hooks() -> None:
    conformance.assert_setup_registers(
        dbwarden_redis.setup,
        plugin=DISTRIBUTION,
        value_hooks=VALUE_HOOKS,
        object_types=OBJECT_TYPES,
    )


def test_hook_signature_compliance() -> None:
    conformance.assert_hook_signatures(dbwarden_redis.setup)


def test_core_imports_resolve() -> None:
    conformance.assert_core_imports_resolve(PACKAGE)


def test_api_version_is_declared() -> None:
    conformance.assert_api_version_declared(PACKAGE)


def test_idempotent_setup() -> None:
    conformance.assert_idempotent_setup(dbwarden_redis.setup, plugin=DISTRIBUTION)
