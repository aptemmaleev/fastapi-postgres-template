import asyncio
from app.__main__ import debug_main

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(debug_main())
    loop.run_forever()
