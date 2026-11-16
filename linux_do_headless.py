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
        # The API request context shares the browser's cookie jar. Authenticate the
        # fixture using its password, then let the real browser perform the visit.
        csrf = page.request.get(f"{FORUM}/session/csrf.json").json()["csrf"]
        login = page.request.post(
            f"{FORUM}/session",
            headers={"X-CSRF-Token": csrf, "X-Requested-With": "XMLHttpRequest"},
            form={"login": "ci_reader", "password": os.environ["FIXTURE_PASSWORD"]},
        )
        assert login.ok, f"Fixture login returned HTTP {login.status}"
        payload = login.json()
        assert not payload.get("error"), f"Fixture login rejected: {payload.get('error')}"
        current = page.request.get(f"{FORUM}/session/current.json")
        assert current.ok and current.json()["current_user"]["username"] == "ci_reader"
        page.goto(f"{FORUM}/latest")
        link = page.get_by_role("link", name=TARGET, exact=True).first
        expect(link).to_be_visible(timeout=30000)

        # Register before opening the topic so the first acknowledgement is captured.
        with page.expect_response(lambda r: r.request.method == "POST" and
                                  r.url.split("?")[0] == f"{FORUM}/topics/timings",
                                  timeout=90000) as timing:
            page.bring_to_front()
            link.click()
            post = page.locator("#post_1")
            expect(post).to_be_visible()
            post.scroll_into_view_if_needed()
        assert timing.value.ok, f"Read acknowledgement returned {timing.value.status}"
        print(f"Browser opened fixture as ci_reader; Discourse acknowledged HTTP {timing.value.status}")
        browser.close()


if __name__ == "__main__":
    main()
