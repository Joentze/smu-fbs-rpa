from requests import post

co_booker_url = "https://fbsm.intranet.smu.edu.sg/FBSMobile_UI/screenservices/FBSMobile_UI/BookingFlow/BookingDetails/ActionGetCoBookerDetailsCS"


def get_co_booker(email: str, auth_content: object):
    response = post(url=co_booker_url, headers={
        "Cookie": auth_content["cookie"],
        "X-CSRFToken": auth_content["x-csrftoken"],
        "OutSystems-Request-Token": auth_content["outsystems-request-token"]
    }, json={
        "versionInfo": {
            "moduleVersion": "QJG2Q876EagFQgHilCXaDQ",
            "apiVersion": "FO2HRGlWTHC2cL9BTvnvYQ"
        },
        "viewName": "BookingFlow.Booking",
        "inputParameters": {
            "GetCoBookerDetailsRequestCS": "AdHoc",
            "SearchValue": email,
            "StartDateTimeText": "2023-04-12 21:30",
            "EndDateTimeText": "2023-04-12 22:30",
            "ClientToken": auth_content["client_token"]
        }
    }, timeout=10000)
    return response.text
