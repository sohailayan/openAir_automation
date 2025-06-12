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
    # Wait for the timesheet link (date range pattern) to appear
        self.page.wait_for_selector("role=link[name=/\\d{2}-\\d{2}-\\d{2} to \\d{2}-\\d{2}-\\d{2}/]", timeout=10000)

    # Now fetch the matching links
        locator = self.page.get_by_role("link", name=re.compile(r"\d{2}-\d{2}-\d{2} to \d{2}-\d{2}-\d{2}"))
        print(f"✅ Found {locator.count()} timesheet links.")
        locator.last.click()
    
    def select_client_project(self, label):
        self.page.locator('select[aria-label="Select Client : Project"]').select_option(label=label)

    def select_task(self, label):
        self.page.wait_for_selector('select[aria-label="Select Task"]')
        self.page.locator("select[aria-label='Select Task']").nth(0).select_option(label=label)

    def fill_hours(self, hours="8"):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in weekdays:
            label_regex = re.compile(f"^Number of hours for {day}")
            self.page.get_by_label(label_regex).nth(0).fill(hours)

    def fill_notes(self, note="Working on AI-CoE Project and learning playwright automation"):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in weekdays:
            self.page.get_by_role("cell", name=re.compile(f"Additional time entry.*{day}")).get_by_label(re.compile("Additional time entry")).nth(0).click()
            self.page.locator("#tm_notes").fill(note)
            self.page.get_by_role("button", name="OK", exact=True).click()

    def save_timesheet(self):
        self.page.locator("#timesheet_savebutton").click()
        self.page.wait_for_timeout(3000)

    def submit_timesheet(self):
        # If there's a separate submit button, use it; otherwise, use save
        try:
            self.page.locator("#save_grid_submit").click()
        except Exception:
            pass
        self.page.wait_for_timeout(3000)

    def is_submission_successful(self):
        # Implement a check for a confirmation message or success indicator
        return self.page.locator("text=Timesheet was submitted successfully").is_visible(timeout=5000) 