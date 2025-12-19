from seleniumbase import SB
import random
import base64
import requests

# Fetching geolocation data
geo_info = requests.get("http://ip-api.com/json/").json()

lat = geo_info["lat"]
lon = geo_info["lon"]
timezone = geo_info["timezone"]
lang_code = geo_info["countryCode"].lower()

# Decoding a name using base64 and constructing URLs
encoded_name = "YnJ1dGFsbGVz"
decoded_name = base64.b64decode(encoded_name).decode("utf-8")
twitch_url = f"https://www.twitch.tv/{decoded_name}"
yt_url = f"https://www.youtube.com/@{decoded_name}/live"

# Infinite loop to keep trying the process
while True:
    with SB(uc=True, locale="en", ad_block=True, chromium_arg='--disable-webgl') as browser:
        wait_time = random.randint(450, 900)

        # Activate CDP mode and set location/timezone
        browser.activate_cdp_mode(twitch_url, tzone=f"{timezone}", geoloc=(lat, lon))

        browser.sleep(10)

        # Checking and clicking various buttons on the page
        if browser.cdp.is_element_present('button:contains("Start Watching")'):
            browser.cdp.click('button:contains("Start Watching")', timeout=4)
            browser.sleep(10)

        if browser.cdp.is_element_present('button:contains("Accept")'):
            browser.cdp.click('button:contains("Accept")', timeout=4)

        if browser.cdp.is_element_present("#live-channel-stream-information"):

            if browser.cdp.is_element_present('button:contains("Accept")'):
                browser.cdp.click('button:contains("Accept")', timeout=4)

            # Open a new driver for another session
            new_browser_1 = browser.get_new_driver(undetectable=True)
            new_browser_1.activate_cdp_mode(twitch_url, tzone=f"{timezone}", geoloc=(lat, lon))
            new_browser_1.sleep(10)

            if new_browser_1.cdp.is_element_present('button:contains("Start Watching")'):
                new_browser_1.cdp.click('button:contains("Start Watching")', timeout=4)
                new_browser_1.sleep(10)

            if new_browser_1.cdp.is_element_present('button:contains("Accept")'):
                new_browser_1.cdp.click('button:contains("Accept")', timeout=4)

            browser.sleep(10)

            new_browser_2 = browser.get_new_driver(undetectable=True)
            new_browser_2.activate_cdp_mode(yt_url, tzone=f"{timezone}", geoloc=(lat, lon))
            new_browser_2.sleep(10)

            if new_browser_2.cdp.is_element_present('button:contains("Accept")'):
                new_browser_2.cdp.click('button:contains("Accept")', timeout=4)
                new_browser_2.sleep(10)
            else:
                new_browser_2.sleep(10)
                new_browser_2.cdp.gui_press_key('K')

            browser.sleep(wait_time)
            browser.quit_extra_driver()

        else:
            break
