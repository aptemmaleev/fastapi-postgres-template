import asyncio
import os
import uvicorn

from app.logger import setup
from app.settings import SETTINGS


async def main():
    os.system("clear")  # Setup logger
    setup()
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(
        app="app.api.server:app",
        loop=loop,
        host=SETTINGS.API_HOST,
        port=SETTINGS.API_PORT,
        reload=False,
        log_level=SETTINGS.LOGGING_LEVEL.lower(),
    )
    server = uvicorn.Server(config)
    loop.create_task(server.serve())


async def debug_main():
    os.system("clear")
    # Setup logger
    setup()
    # Run server
    uvicorn.run(
        app="app.api.server:app",
        host=SETTINGS.API_HOST,
        port=SETTINGS.API_PORT,
        log_level=SETTINGS.LOGGING_LEVEL.lower(),
        reload=True,
        reload_includes=["app"],
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
