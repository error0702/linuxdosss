"""Open one fixture topic through the normal UI of the runner-local Discourse."""
import os
import shutil

from playwright.sync_api import expect, sync_playwright

FORUM = "http://localhost"
TARGET = "CI read receipt target"


def main():
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=shutil.which("google-chrome"))
        page = browser.new_page()
        page.goto(f"{FORUM}/login")
        page.locator("#login-account-name").fill("ci_reader")
        page.locator("#login-account-password").fill(os.environ["FIXTURE_PASSWORD"])
        page.locator("#login-button").click()
        expect(page.locator("#current-user")).to_be_visible(timeout=30000)
        identity = page.request.get(f"{FORUM}/session/current.json").json()
        assert identity["current_user"]["username"] == "ci_reader"

        page.goto(f"{FORUM}/latest")
        page.get_by_role("link", name=TARGET, exact=True).first.click()
        post = page.locator("#post_1")
        expect(post).to_be_visible()
        post.scroll_into_view_if_needed()
        # Observe the forum client's own acknowledgement after the post is displayed.
        with page.expect_response(lambda r: r.request.method == "POST" and
                                  r.url.split("?")[0] == f"{FORUM}/topics/timings",
                                  timeout=90000) as timing:
            page.bring_to_front()
        assert timing.value.ok, f"Read acknowledgement returned {timing.value.status}"
        print(f"Browser opened fixture as ci_reader; Discourse acknowledged HTTP {timing.value.status}")
        browser.close()


if __name__ == "__main__":
    main()
