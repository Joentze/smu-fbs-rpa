import time
import json
from pprint import pprint
from playwright.sync_api import Playwright, sync_playwright
from get_co_booker import get_co_booker
from room_book_post import book_room
# generate inspector to get automated actions from playwright, run this:
# playwright codegen --device="iPhone 13" https://fbs.intranet.smu.edu.sg

auth_content = {}


def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(headless=False, slow_mo=200)
    context = browser.new_context(**playwright.devices["iPhone 13"])
    page = context.new_page()

    page.goto("https://login2.smu.edu.sg/adfs/ls/?SAMLRequest=hZLLboMwEEV%2FBXkfzCMhqRWQaLJopLRFgXbRTWVgEiwZm3pMH39fEvpIN6nkna%2FPnTnyEnkrO5b2tlE7eOkBrfPeSoXsdBGT3iimOQpkireAzFYsT2%2B3LHA91hltdaUlcVJEMFZotdIK%2BxZMDuZVVPCw28aksbZDRum%2BRFcoa7gC62Lbu1D3Lh5o3oiy1BJs4yJqesQHNLvPC%2BKsh3mE4kfyL0fqg1DBOYHXe6QSKXE265g8B4toHnlXUTWLgoovYF%2BXnHteOa3D0K%2F9%2BRBD7GGj0HJlYxJ4QTjxpsMp%2FJB5CzabPREn%2B9ruWqhaqMNlFeUYQnZTFNlkHP4RDJ4GHwIkWR6FslOxOVN8Gcu%2FvZLkP4v4Y3FJz6rG3o7dDezNOtNSVB9OKqV%2BWxngFmLiE5qMT%2F7%2Bg%2BQT&RelayState=ss%3Amem%3A57d833b617546aeaabd7398be26ddc9da55305a11069d068471893d306792e05")

    page.get_by_placeholder(
        "username@smu.edu.sg").fill("")

    page.get_by_placeholder("").click()

    page.get_by_placeholder("Password").fill("Password5%")

    page.get_by_role("button", name="Sign in").click()
    page.wait_for_load_state("networkidle")
    page.on("requestfinished", get_auth_content)
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="MAKE A NEW BOOKING ").click()
    # get client token
    token = page.evaluate("""() => {
  return localStorage.getItem("$OS_Users$FBSMobile_UI$ClientVars$ClientToken")
}""")
    page.wait_for_load_state("networkidle")
    context.close()
    browser.close()
    auth_content["client_token"] = token


def get_auth_content(request):
    try:
        global auth_content
        headers = request.all_headers()
        if "cookie" not in auth_content:
            auth_content["cookie"] = headers["cookie"]
        if "x-csrftoken" not in auth_content:
            auth_content["x-csrftoken"] = headers["x-csrftoken"]
        if "outsystems-request-token" not in auth_content:
            auth_content["outsystems-request-token"] = headers["outsystems-request-token"]
        # print(auth_content)
    except Exception as error_message:
        print("error: ", error_message)


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
    config = {
        "building": "Lee Kong Chian School of Business",
        "facility": "LKCSB GSR 2-10",
        "date": "13/04/2023",
        "start_time": "09:00",
        "end_time": "10:00",
        "co_booker_email": "",
        "purpose": "to see behind walls things to come"
    }
    facility_obj = {}

    response = get_co_booker(config["co_booker_email"], auth_content)
    response = json.loads(str(response))
    co_booker = response["data"]["GetCoBookerDetailsResponseCS"]["ResultObject"]["List"][0]
    with open("rooms.json", "r") as file:
        obj = json.load(file)
    for facility in obj[config["building"]]:
        if config["facility"] in facility:
            facility_obj = facility
            break

    book_response = book_room(auth_content=auth_content, space_name=config["facility"], space_id=facility_obj[config["facility"]], building_name=config["building"], date=config[
                              "date"], start_datetime=config["start_time"], end_datetime=config["end_time"], cobooker=co_booker, purpose=config["purpose"])
    print(book_response)
