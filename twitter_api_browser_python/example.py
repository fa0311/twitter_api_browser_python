import asyncio
from datetime import datetime

from main import TwitterAPIBrowser


async def main() -> None:
    user_data_dir = "./.data"
    async with TwitterAPIBrowser(user_data_dir=user_data_dir) as browser:
        await browser.login()
        inject = await browser.inject()

        while True:
            print("=" * 20)
            operation = input(
                "Choose operation [CreateTweet, HomeTimeline, UserByScreenName, CreateRetweet, FavoriteTweet, SearchTimeline, UsersByRestIds, exit]: "
            )
            if operation == "CreateTweet":
                res = await inject.request(
                    "CreateTweet",
                    {
                        "tweet_text": f"Hello, World! {datetime.now().isoformat()}",
                        "dark_request": False,
                        "media": {"media_entities": [], "possibly_sensitive": False},
                        "semantic_annotation_ids": [],
                        "disallowed_reply_options": None,
                    },
                )
                print(res)
            elif operation == "HomeTimeline":
                res = await inject.request(
                    "HomeTimeline",
                    {
                        "count": 20,
                        "includePromotedContent": True,
                        "latestControlAvailable": True,
                        "withCommunity": True,
                    },
                )
                print(res)
            elif operation == "UserByScreenName":
                res = await inject.request(
                    "UserByScreenName",
                    {
                        "screen_name": "elonmusk",
                        "withSafetyModeUserFields": True,
                        "withSuperFollowsUserFields": True,
                        "withBirdwatchPivots": False,
                    },
                    {
                        "withAuxiliaryUserLabels": True,
                    },
                )
                print(res)
            elif operation == "CreateRetweet":
                res = await inject.request(
                    "CreateRetweet",
                    {
                        "tweet_id": "1987547856664993831",
                        "dark_request": False,
                    },
                )
                print(res)
            elif operation == "FavoriteTweet":
                res = await inject.request(
                    "FavoriteTweet",
                    {"tweet_id": "1987547856664993831"},
                )
                print(res)
            elif operation == "SearchTimeline":
                res = await inject.request(
                    "SearchTimeline",
                    {
                        "rawQuery": "from:elonmusk",
                        "count": 20,
                        "querySource": "typed_query",
                        "product": "Top",
                        "withGrokTranslatedBio": False,
                    },
                )
                print(res)
            elif operation == "UsersByRestIds":
                res = await inject.request(
                    "UsersByRestIds",
                    {
                        "userIds": ["900282258736545792"],
                    },
                )
                print(res)
            elif operation == "exit":
                return


if __name__ == "__main__":
    asyncio.run(main())
