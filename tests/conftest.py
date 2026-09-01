from __future__ import annotations

import pytest
from dbwarden.plugin import HookRegistry, ObjectPluginRegistry, PluginRegistrar

import dbwarden_redis

PLUGIN_NAME = "dbwarden-redis"


@pytest.fixture(autouse=True)
def register_plugin():
    """Register this plugin the way core does at CLI startup."""
    HookRegistry.clear()
    ObjectPluginRegistry.clear()
    dbwarden_redis.setup(PluginRegistrar(PLUGIN_NAME))
    yield
    HookRegistry.clear()
    ObjectPluginRegistry.clear()
