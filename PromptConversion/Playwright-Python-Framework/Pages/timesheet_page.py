from playwright.sync_api import Page, expect
import re

class TimesheetPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_timesheets(self):
        self.page.wait_for_selector("text=Timesheets", timeout=60000)
        self.page.get_by_role("link", name="Timesheets", exact=True).click()
        self.page.get_by_role("link", name="Open", exact=True).first.click()

    def open_latest_timesheet(self):
        self.page.wait_for_selector("role=link[name=/\\d{2}-\\d{2}-\\d{2} to \\d{2}-\\d{2}-\\d{2}/]", timeout=10000)
        locator = self.page.get_by_role("link", name=re.compile(r"\d{2}-\d{2}-\d{2} to \d{2}-\d{2}-\d{2}"))
        print(f"Found {locator.count()} timesheet links.")
        locator.last.click()
    
    def select_client_project(self, label):
        print(f"Selecting Client:Project label: {label}")
        self.page.locator('select[aria-label="Select Client : Project"]').select_option(label=label)
        print("Selected Client:Project.")

    def select_task(self, label):
        print(f"Trying to select task label: {label}")
        self.page.wait_for_selector('select[aria-label="Select Task"]', timeout=10000)
        try:
            self.page.locator("select[aria-label='Select Task']").first.select_option(label=label)
            print(f"Successfully selected task label: {label}")
        except Exception as e:
            print(f"Failed to select task label: {label}\nError: {e}")
            options = self.page.locator("select[aria-label='Select Task'] option").all_inner_texts()
            print("Available task options:")
            for opt in options:
                print(f"- {opt}")
            raise e

    def fill_hours(self, hours="8"):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in weekdays:
            label_regex = re.compile(f"^Number of hours for {day}")
            if isinstance(hours, dict):
                self.page.get_by_label(label_regex).nth(0).fill(hours)
            else:
                value = hours
                self.page.get_by_label(label_regex).nth(0).fill(value)
                print(f"Filled {value} hrs for {day}")
        print("Finished filling hours.")

    def fill_notes(self, note="Working on AI-CoE Project and learning playwright automation"):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in weekdays:
            self.page.get_by_role("cell", name=re.compile(f"Additional time entry.*{day}")).get_by_label(re.compile("Additional time entry")).nth(0).click()
            self.page.locator("#tm_notes").fill(note)
            self.page.get_by_role("button", name="OK", exact=True).click()
        print("Filled notes for all weekdays.")

    def save_timesheet(self):
        self.page.locator("#timesheet_savebutton").click()
        self.page.wait_for_timeout(3000)
        print("Timesheet saved.")

    def submit_timesheet(self):
        try:
            self.page.locator("#save_grid_submit").click()
        except Exception:
            pass
        self.page.wait_for_timeout(3000)
        print("Timesheet submitted (if submission button available).")

    def is_submission_successful(self):
        return self.page.locator("text=Timesheet was submitted successfully").is_visible(timeout=5000)
