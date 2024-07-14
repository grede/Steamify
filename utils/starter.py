from asyncio import sleep
from random import uniform
from data import config
from utils.core import logger
import asyncio
from aiohttp.client_exceptions import ContentTypeError
from utils.steamify import SteamifyBot


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    steamify = SteamifyBot(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'

    await sleep(uniform(*config.DELAYS['ACCOUNT']))

    while True:
        try:
            if await steamify.login() is None:
                return

            await sleep(uniform(2, 8))
            logger.info(f"Thread {thread} | {account} | Retrieving account state...")
            balance, claimable, farm_status, started_at, total_duration = await steamify.getStatus()

            logger.success(
                f"Thread {thread} | {account} | Current balance: {balance} | Claimable balance: {claimable} | Farm status: {farm_status}")

            if (farm_status == 'completed'):
                await sleep(uniform(2, 8))
                claimed = await steamify.claim()
                logger.success(f"Thread {thread} | {account} | Claimed {claimed} in rewards")
            elif (farm_status == 'available'):
                await sleep(uniform(2, 8))
                await steamify.startFarm()
                logger.success(f"Thread {thread} | {account} | Started farming")
            elif (farm_status == 'in_progress'):
                await sleep(uniform(2, 8))
                sleepTime = steamify.calcSleep(started_at, total_duration)
                logger.success(f"Thread {thread} | {account} | Sleeping for {sleepTime}")
                await sleep(sleepTime + uniform(*config.DELAYS['CLAIM']))
            else:
                raise Exception("unknown farm status")

            await sleep(30)
        except ContentTypeError as e:
            logger.error(f"Thread {thread} | {account} | Error: {e}")
            await asyncio.sleep(120)

        except Exception as e:
            logger.error(f"Thread {thread} | {account} | Error: {e}")
            await asyncio.sleep(120)
