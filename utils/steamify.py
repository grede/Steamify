import random
from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestWebView
import asyncio
from urllib.parse import unquote, quote
from data import config
import aiohttp
import time
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector

def retry_async(max_retries=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            thread, account = args[0].thread, args[0].account
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.error(f"Thread {thread} | {account} | Error: {e}. Retrying {retries}/{max_retries}...")
                    await asyncio.sleep(10)
                    if retries >= max_retries:
                        break
        return wrapper
    return decorator

class SteamifyBot:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.account = session_name + '.session'
        self.thread = thread
        self.proxy = f"{config.PROXY_TYPES['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)

        if proxy:
            proxy = {
                "scheme": config.PROXY_TYPES['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='en'
        )

        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector,
                                             timeout=aiohttp.ClientTimeout(120))

    async def getStatus(self):
        resp = await self.session.get('https://api.app.steamify.io/api/v1/user/me')
        resp_json = await resp.json()

        if (resp.status != 200):
            respText = await resp.text()
            raise Exception(f"couldn't retrieve account status: {respText}")

        return int(resp_json.get('data').get('balance')), int(
            resp_json.get('data').get('farm').get('base_rewards')), resp_json.get('data').get('farm').get(
            'status'), resp_json.get('data').get('farm').get(
            'started_at'), resp_json.get('data').get('farm').get(
            'total_duration') if resp_json.get("success") else await resp.text()

    async def claim(self):
        logger.info(f"Thread {self.thread} | {self.account} | Claiming rewards...")
        resp = await self.session.get('https://api.app.steamify.io/api/v1/farm/claim')
        resp_json = await resp.json()

        if (resp.status != 200):
            respText = await resp.text()
            raise Exception(f"couldn't claim rewards: {respText}")

        return resp_json.get('data').get('claim').get('total_rewards') if resp_json.get("success") else await resp.text()

    async def startFarm(self):
        logger.info(f"Thread {self.thread} | {self.account} | Starting farm...")
        resp = await self.session.get('https://api.app.steamify.io/api/v1/farm/start')
        resp_json = await resp.json()

        if (resp.status != 200):
            respText = await resp.text()
            raise Exception(f"couldn't start farming: {respText}")

        return resp_json.get('data').get('farm').get('started_at'), resp_json.get('data').get('farm').get('total_duration') if resp_json.get("success") else await resp.text()

    async def logout(self):
        await self.session.close()

    async def login(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        query = await self.get_tg_web_data()

        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None

        self.session.headers['Authorization'] = 'Bearer ' + query
        return True

    @staticmethod
    def calcSleep(started_at, total_duration):
        return (started_at + total_duration) - int(time.time())

    async def get_tg_web_data(self):
        try:
            await self.client.connect()
            web_view = await self.client.invoke(RequestWebView(
                peer=await self.client.resolve_peer('steamify_bot'),
                bot=await self.client.resolve_peer('steamify_bot'),
                platform='android',
                from_bot_menu=False,
                url='https://t.me/steamify_bot/app'
            ))

            await self.client.disconnect()
            auth_url = web_view.url

            query = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            query_id = query.split('query_id=')[1].split('&user=')[0]
            user = quote(query.split("&user=")[1].split('&auth_date=')[0])
            auth_date = query.split('&auth_date=')[1].split('&hash=')[0]
            hash_ = query.split('&hash=')[1]

            return f"query_id={query_id}&user={user}&auth_date={auth_date}&hash={hash_}"
        except:
            return None