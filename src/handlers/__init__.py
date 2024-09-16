from aiogram import Router
from .users import router as users_router
from .admins import router as admins_router
from .groups import router as groups_router


main_router = Router()


main_router.include_routers(
    admins_router,
    groups_router,
    users_router,
)
