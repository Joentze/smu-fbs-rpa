from pprint import pprint
import datetime
import pytz
from requests import post
# datetime_str = '09/19/22 13:55:26'

# datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
book_url = "https://fbsm.intranet.smu.edu.sg/FBSMobile_UI/screenservices/FBSMobile_UI/BookingFlow/BookingDetails/ActionValidateAndCreateBookingCS"


def convert_to_utc(year: int, month: int, day: int, hour: int, minute: int):
    """convert timings to utc format"""
    datetime_str = datetime.datetime(
        year=year, month=month, day=day, hour=hour, minute=minute).astimezone(pytz.UTC).strftime("%Y-%m-%dT%I:%M:%SZ")
    return datetime_str


def book_room(auth_content: object, space_name: str, space_id: str, date: str, start_datetime: str, end_datetime: str, building_name: str, cobooker: object, purpose: str):
    date_split = date.split("/")
    start_hr, start_min = [int(num) for num in start_datetime.split(":")]
    end_hr, end_min = [int(num) for num in end_datetime.split(":")]
    day, month, year = [int(num) for num in date_split]
    start_tz_str = convert_to_utc(year, month, day, start_hr, start_min)
    end_tz_str = convert_to_utc(year, month, day, end_hr, end_min)
    dd, mm, yyyy = date_split
    booking_post_template = {
        "versionInfo": {
            "moduleVersion": "QJG2Q876EagFQgHilCXaDQ",
            "apiVersion": "2Ap4Kvvdlv8rXhcRvjeeLg"
        },
        "viewName": "BookingFlow.Booking",
        "inputParameters": {
            "ValidateAndCreateBookingRequestCS": {
                "CalendarProcessModels": {
                    "List": [
                        {
                            "SpaceID": space_id,
                            "SpaceName": space_name,
                            "StartDateTime": start_tz_str,
                            "EndDateTime": end_tz_str,
                            "StartTime": start_datetime,
                            "EndTime": end_datetime,
                            "UseType": "3159c813-a593-4aec-a8cf-a117d4770e41",
                            "CourseCode": "00000000-0000-0000-0000-000000000000",
                            "BookingUsage": "",
                            "Purpose": "study",
                            "IsSendCalendarInvite": False,
                            "ErrorMessage": "",
                            "EventID": "00000000-0000-0000-0000-000000000000",
                            "IsRequiredApproval": False,
                            "CoBookersList": {
                                "List": [
                                    cobooker
                                ]
                            },
                            "Status": "",
                            "BuildingName": building_name,
                            "BookingForName": "Self",
                            "UseTypeName": "AdHoc",
                            "CourseCodeName": "",
                            "BookingUsageName": "",
                            "DateText": f"{yyyy}-{mm}-{dd}",
                            "StartDateTimeText": f"{yyyy}-{mm}-{dd} {start_datetime}",
                            "EndDateTimeText": f"{yyyy}-{mm}-{dd} {end_datetime}",
                            "EventCodeName": "",
                            "BookingForID": "00000000-0000-0000-0000-000000000000",
                            "BookingForNameValue": "",
                            "ReasonForEditing": "",
                            "IsSpaceRequiredApproval": False
                        }
                    ]
                }
            },
            "ClientToken": auth_content["client_token"]
        }
    }
    response = post(url=book_url, headers={
        "Cookie": auth_content["cookie"],
        "X-CSRFToken": auth_content["x-csrftoken"],
        "OutSystems-Request-Token": auth_content["outsystems-request-token"]
    }, json=booking_post_template, timeout=10000)
    return response.text
