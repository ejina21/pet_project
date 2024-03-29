import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as booking_router
from app.config import settings
from app.database import engine
from app.hotels.router import router as hotel_router
from app.images.router import router as images_router
from app.importer.router import router as import_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.router import router_users, router_auth
from app.prometheus.router import router as prometheus_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    logger.info("Service exited")


app = FastAPI(
    lifespan=lifespan,
    title="Бронирование Отелей",
    version="0.1.0",
    root_path="/api",
)

app.include_router(booking_router)
app.include_router(router_users)
app.include_router(router_auth)
app.include_router(hotel_router)

app.include_router(pages_router)
app.include_router(images_router)
app.include_router(prometheus_router)
app.include_router(import_router)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}",
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

# Подключение эндпоинта для отображения метрик для их дальнейшего сбора Прометеусом
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response
