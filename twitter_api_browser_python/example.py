import asyncio
from datetime import datetime

from main import TwitterAPIBrowser


async def main() -> None:
    user_data_dir = "./.data"
    async with TwitterAPIBrowser(user_data_dir=user_data_dir) as browser:
        await browser.login()
        inject = await browser.inject()
        await inject.request(
            "CreateTweet",
            {
                "tweet_text": f"Hello, World! {datetime.now().isoformat()}",
                "dark_request": False,
                "media": {"media_entities": [], "possibly_sensitive": False},
                "semantic_annotation_ids": [],
                "disallowed_reply_options": None,
            },
        )


if __name__ == "__main__":
    asyncio.run(main())
