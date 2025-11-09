import asyncio
import json
from typing import TypeVar

from aiofiles import open
from playwright.async_api import Page, async_playwright

T = TypeVar("T")


async def load_script(path: str) -> str:
    dir = "./twitter_api_browser_python/inject/"
    async with open(f"{dir}{path}", "r", encoding="utf-8") as f:
        return await f.read()


def one(data: list[T], name: str = "item") -> T:
    if len(data) == 0:
        raise ValueError(f"No {name} found")
    if len(data) > 1:
        raise ValueError(f"Multiple {name} found")
    return data[0]


class TwitterAPIBrowser:
    def __init__(self, user_data_dir: str = "./.data"):
        self.user_data_dir = user_data_dir

    async def __aenter__(self):
        self.playwright_manager = async_playwright()
        self.playwright = await self.playwright_manager.__aenter__()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            headless=False,
            user_data_dir=self.user_data_dir,
            viewport=None,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.playwright_manager.__aexit__(exc_type, exc, tb)

    async def login(self):
        await self.page.goto("https://x.com/login")
        await self.page.wait_for_url("https://x.com/home", timeout=0)

    async def inject(self, sleep: int = 5):
        inject_setup_script = await load_script("setup.js")
        inject_operation_script = await load_script("operation.js")
        inject_init_state_script = await load_script("init_state.js")
        await self.page.add_init_script(inject_operation_script)
        await self.page.add_init_script(inject_init_state_script)
        await self.page.goto("https://x.com/home")
        await self.page.evaluate(inject_setup_script)
        await asyncio.sleep(sleep)
        operation_list = await self.page.evaluate(
            "globalThis.elonmusk_114514_operation"
        )
        init_state = await self.page.evaluate("globalThis.elonmusk_114514_init_state")
        return TwitterAPIRequest(operation_list, init_state, self.page)


class TwitterAPIRequest:
    def __init__(self, operation_list: list[dict], init_state: str, page: Page):
        self.operation_list = operation_list
        self.init_state = init_state
        self.page = page

    async def graphql(self, method: str, body: dict, path: str):
        args = {
            "headers": {"content-type": "application/json"},
            "method": method,
            "path": path,
        }
        if method == "GET":
            params = {k: json.dumps(v) for k, v in body.items()}
            args.update({"params": params})
        elif method == "POST":
            args.update({"data": body})

        res = await self.page.evaluate("globalThis.elonmusk_114514_request", args)
        return res

    async def request(
        self,
        operation: str,
        variables: dict,
        fieldToggles: dict[str, bool] = {},
    ):
        method_map = {
            "query": "GET",
            "mutation": "POST",
        }
        exp = one(
            [x for x in self.operation_list if x["operationName"] == operation],
            name="operation",
        )
        queryId: str = exp["queryId"]
        operationType: str = exp["operationType"]
        featureSwitches: list[str] = exp["metadata"]["featureSwitches"]
        allowFieldToggles: list[str] = exp["metadata"]["fieldToggles"]
        fieldToggles = {k: v for k, v in fieldToggles.items() if k in allowFieldToggles}

        method = method_map[operationType]
        flag = {
            **self.init_state["featureSwitch"]["defaultConfig"],
            **self.init_state["featureSwitch"]["user"],
            **self.init_state["featureSwitch"]["debug"],
            **self.init_state["featureSwitch"]["customOverrides"],
        }
        featureSwitchesMap = {
            k: v["value"] for k, v in flag.items() if k in featureSwitches
        }
        body = {
            "variables": variables,
            "queryId": queryId,
        }
        if featureSwitchesMap:
            body.update({"features": featureSwitchesMap})
        if fieldToggles:
            body.update({"fieldToggles": fieldToggles})

        return await self.graphql(
            method=method,
            body=body,
            path=f"/graphql/{queryId}/{operation}",
        )
