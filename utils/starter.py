from asyncio import sleep
from random import uniform
from data import config
from utils.core import logger
import asyncio
from utils.steamify import SteamifyBot


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    steamify = SteamifyBot(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'

    await sleep(uniform(*config.DELAYS['ACCOUNT']))

    while True:
        try:
            if await steamify.login() is None:
                return

            await steamify.random_wait()
            logger.info(f"Thread {thread} | {account} | Retrieving account state...")
            balance, sparks, tickets, farm_status, started_at, total_duration = await steamify.get_status()

            logger.success(
                f"Thread {thread} | {account} | Current balance: {balance} | Sparks: {sparks} | Tickets: {tickets} | Farm status: {farm_status}")

            # claim daily
            await steamify.random_wait()
            await steamify.claim_daily()

            # claim sparks
            await steamify.claim_sparks()

            # perform tasks
            await steamify.random_wait()
            await steamify.perform_tasks()

            # play game
            await steamify.play_case_game()

            # farm
            await handle_farm(steamify, thread, account)

            await sleep(30)
        except Exception as e:
            logger.error(f"Thread {thread} | {account} | Error: {e}")
            await asyncio.sleep(120)


async def handle_farm(steamify, thread, account):
    while True:
        await steamify.random_wait()
        balance, sparks, tickets, farm_status, started_at, total_duration = await steamify.get_status()

        if farm_status == 'completed':
            await steamify.random_wait()
            claimed = await steamify.claim()
            logger.success(f"Thread {thread} | {account} | Claimed {claimed} in rewards")
        elif farm_status == 'available':
            await steamify.random_wait()
            await steamify.start_farm()
            logger.success(f"Thread {thread} | {account} | Started farming")
        elif farm_status == 'in_progress':
            await steamify.random_wait()
            sleepTime = steamify.calcSleep(started_at, total_duration)
            logger.success(f"Thread {thread} | {account} | Sleeping for {sleepTime}")
            await sleep(sleepTime + uniform(*config.DELAYS['CLAIM']))
            return
        else:
            raise Exception("unknown farm status")
