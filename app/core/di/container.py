from dependency_injector import containers, providers

from core.di import redis
from core.config import settings
from core.redis import AsyncRedis


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        packages=['api'],
        auto_wire=True,
    )
    redis_pool = providers.Resource(
        redis.init_redis_pool,
        host=settings.REDIS_HOST,
        password=settings.REDIS_PASSWORD,
    )

    redis_service = providers.Factory(
        AsyncRedis,
        redis=redis_pool,
    )
