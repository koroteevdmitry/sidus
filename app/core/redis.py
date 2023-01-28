from typing import Any, Union

from aioredis import Redis


class AsyncRedis:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def set(self, key: str, value: Union[str, dict]) -> None:
        if isinstance(value, dict):
            await self._redis.hset(key, mapping={str(k): str(v) for k, v in value.items()})
        else:
            await self._redis.set(key, value)
        await self._redis.close()

    async def get(self, key, dict_value: bool = False) -> Any:
        result = await self._redis.hgetall(key) if dict_value else await self._redis.get(key)
        await self._redis.close()
        return result

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)
        await self._redis.close()
