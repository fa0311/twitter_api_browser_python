import asyncio
from datetime import datetime

from playwright.async_api import async_playwright


async def main() -> None:
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            headless=False,
            user_data_dir="./.data",
            viewport=None,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        page = await context.new_page()

        await page.goto("https://x.com")
        await page.wait_for_url("https://x.com/home", timeout=0)
        path = "twitter_api_browser_python/inject/setup.js"

        with open(path, "r", encoding="utf-8") as f:
            inject_script = f.read()

        await page.evaluate(inject_script)
        res = await page.evaluate(
            "globalThis.elonmusk_114514_request",
            {
                "data": {
                    "variables": {
                        "tweet_text": f"Hello, World! {datetime.now().isoformat()}",
                        "dark_request": False,
                        "media": {"media_entities": [], "possibly_sensitive": False},
                        "semantic_annotation_ids": [],
                        "disallowed_reply_options": None,
                    },
                    "features": {
                        "premium_content_api_read_enabled": False,
                        "communities_web_enable_tweet_community_results_fetch": True,
                        "c9s_tweet_anatomy_moderator_badge_enabled": True,
                        "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
                        "responsive_web_grok_analyze_post_followups_enabled": True,
                        "responsive_web_jetfuel_frame": True,
                        "responsive_web_grok_share_attachment_enabled": True,
                        "responsive_web_edit_tweet_api_enabled": True,
                        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                        "view_counts_everywhere_api_enabled": True,
                        "longform_notetweets_consumption_enabled": True,
                        "responsive_web_twitter_article_tweet_consumption_enabled": True,
                        "tweet_awards_web_tipping_enabled": False,
                        "responsive_web_grok_show_grok_translated_post": False,
                        "responsive_web_grok_analysis_button_from_backend": True,
                        "creator_subscriptions_quote_tweet_preview_enabled": False,
                        "longform_notetweets_rich_text_read_enabled": True,
                        "longform_notetweets_inline_media_enabled": True,
                        "payments_enabled": False,
                        "profile_label_improvements_pcf_label_in_post_enabled": True,
                        "responsive_web_profile_redirect_enabled": False,
                        "rweb_tipjar_consumption_enabled": True,
                        "verified_phone_label_enabled": False,
                        "articles_preview_enabled": True,
                        "responsive_web_grok_community_note_auto_translation_is_enabled": False,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "freedom_of_speech_not_reach_fetch_enabled": True,
                        "standardized_nudges_misinfo": True,
                        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                        "responsive_web_grok_image_annotation_enabled": True,
                        "responsive_web_grok_imagine_annotation_enabled": True,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                        "responsive_web_enhance_cards_enabled": False,
                    },
                    "queryId": "MtyT_TbO2PpwaFHNPK2qoQ",
                },
                "headers": {"content-type": "application/json"},
                "method": "POST",
                "path": "/graphql/MtyT_TbO2PpwaFHNPK2qoQ/CreateTweet",
            },
        )
        print(res)

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
