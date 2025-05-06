from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Awaitable, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LogMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        update_json = event.model_dump(mode="json", exclude_unset=True)
        logger.info(f"New update: {update_json}")

        return await handler(event, data)
