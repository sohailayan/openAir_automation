import time
import pytest
import sys
import getpass
from Pages.openair_login_page import OpenAirLoginPage
from Pages.timesheet_page import TimesheetPage

def test_openair_sso_timesheet(page):
    login = OpenAirLoginPage(page)
    timesheet = TimesheetPage(page)

    # Step 0: Take user inputs
    print("Enter your Microsoft email:")
    sys.stdout.flush()
    email = input()

    print("Enter your Microsoft password (input hidden):")
    sys.stdout.flush()
    password = getpass.getpass()

    print("Enter the Client:Project label (e.g., Internal IN : IN.AI CoE):")
    sys.stdout.flush()
    client_project_label = input()

    print("Enter the Task label (e.g., 2: Development):")
    sys.stdout.flush()
    task_label = input()

    # Ask for custom hour input
    print("\nI'll fill 8 hours each weekday as default.")
    print("Do you want to fill hours manually for each day? (yes/no):")
    sys.stdout.flush()
    custom_hours_choice = input().strip().lower()

    custom_hours = None
    if custom_hours_choice == "yes":
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        print("\nPlease enter hours for each weekday, separated by commas (e.g., 4, 4, 12, 12, 8):")
        print("Days:", ", ".join(weekdays))
        sys.stdout.flush()
        hours_input = input().strip()
        try:
            hours_list = [x.strip() for x in hours_input.split(',')]
            if len(hours_list) != 5:
                raise ValueError("You must provide exactly 5 values.")
            custom_hours = dict(zip(weekdays, hours_list))
        except Exception as e:
            print(f"Invalid input: {e}. Falling back to default hours (8 each day).")

    # Step 1: Go to SSO login
    login.goto()
    login.enter_company_id("Valtech")

    with page.expect_navigation():
        login.click_sign_in()

    # Step 2: Microsoft login
    assert login.is_on_microsoft_login(), "Not redirected to Microsoft login page."
    login.enter_email(email)
    login.enter_password(password)

    # Step 3: Show MFA code if available
    try:
        page.wait_for_selector("#validEntropyNumber", timeout=10000)
        mfa_code = login.get_mfa_code()
        if mfa_code:
            print(f"\nAuthentication code: {mfa_code}\n")
        else:
            print("\nCould not fetch MFA code.\n")
        sys.stdout.flush()
    except Exception as e:
        print(f"\nError waiting for MFA code: {e}\n")

    # Step 4: Wait for 2FA and dashboard
    login.wait_for_2fa(timeout=60)
    assert login.wait_for_dashboard(timeout=10), "Login failed or dashboard not loaded."

    # Step 5: Timesheet fill
    timesheet.goto_timesheets()
    timesheet.open_latest_timesheet()
    timesheet.select_client_project(label=client_project_label)
    timesheet.select_task(label=task_label)
    timesheet.fill_hours(hours=custom_hours)
    timesheet.fill_notes()
    timesheet.save_timesheet()

    page.wait_for_timeout(3000)
