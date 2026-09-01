# dbwarden-redis

[![Python](https://img.shields.io/badge/Python-3.12.7%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/dbwarden-org/dbwarden-redis/test.yml?logo=github&logoColor=white&style=for-the-badge)](https://github.com/dbwarden-org/dbwarden-redis/actions/workflows/test.yml)

Redis-backed distributed migration locking for [DBWarden](https://dbwarden.emiliano-go.com).

When multiple application replicas could trigger migrations concurrently, this plugin provides a Redis-based distributed lock that ensures only one migration process runs at a time across all instances.

## Installation

```bash
dbwarden plugin add dbwarden-redis
```

Or manually:

```bash
pip install dbwarden-redis
```

## Usage

### Async (FastAPI, etc.)

```python
from redis.asyncio import Redis
from dbwarden_redis import migration_lock

redis = Redis.from_url("redis://localhost:6379")

async with migration_lock(redis):
    # Only one migration process runs at a time
    await run_migration()
```

### Sync (CLI, scripts)

```python
from redis import Redis
from dbwarden_redis import sync_migration_lock

redis = Redis.from_url("redis://localhost:6379")

with sync_migration_lock(redis):
    run_migration()
```

### Options

```python
async with migration_lock(
    redis,
    key="my_custom_lock",  # Redis key (default: "dbwarden_migrate")
    ttl=120,  # Lock TTL in seconds (default: 60)
):
    await run_migration()
```

## How it works

1. **Acquire**: `SET key token NX EX ttl` (atomic; fails if key already exists)
2. **Hold**: The lock is held for the duration of the context manager
3. **Release**: A Lua script deletes the key only if the current caller still owns the token (safe against TTL expiry and concurrent acquisition)

If the process crashes while holding the lock, Redis releases it automatically after the TTL expires.

## Database lock vs Redis lock

| Aspect | Database lock (core) | Redis lock (this plugin) |
|--------|---------------------|--------------------------|
| Scope | CLI commands (`migrate`, `rollback`) | Any code path you wrap |
| Storage | `dbwarden_lock` table in the target database | Redis key |
| TTL | Heartbeat-based stale detection | Configurable TTL (default 60s) |
| External dependency | None (uses the database itself) | Redis required |
| Best for | Single-instance deployments | Multi-instance / multi-replica deployments |

Both locks can be used independently or together. The database lock protects the CLI; the Redis lock protects any entry point you wrap.

## License

MIT
