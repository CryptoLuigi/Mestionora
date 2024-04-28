import asyncio
import os
import pathlib

import dotenv
from discord import utils

from src import bot

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
assert TOKEN is not None, "TOKEN environment variable is not set"


async def main():
    extensions = pathlib.Path("src/extensions").glob("*.py")

    for extension in extensions:
        await bot.load_extension(f"src.extensions.{extension.stem}")

    utils.setup_logging()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
