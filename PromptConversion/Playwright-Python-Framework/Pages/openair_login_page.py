from playwright.sync_api import Page, expect
import re
import time

class OpenAirLoginPage:
    SSO_URL = "https://auth.netsuitesuiteprojectspro.com/login_sso"
    MFA_CODE = "#validEntropyNumber"

    def __init__(self, page: Page):
        self.page = page

    def get_mfa_code(self):
        try:
            self.page.wait_for_selector(self.MFA_CODE, timeout=10000)
            return self.page.inner_text(self.MFA_CODE)
        except Exception:
            return None

    def goto(self):
        self.page.goto(self.SSO_URL)

    def enter_company_id(self, company_id: str):
        self.page.get_by_role("textbox", name="Company ID").fill(company_id)

    def click_sign_in(self):
        self.page.get_by_text("Remember Me Sign in").click()
        self.page.get_by_role("button", name="Sign in").click()

    def is_on_microsoft_login(self):
        return "login.microsoftonline.com" in self.page.url

    def enter_email(self, email: str):
        self.page.get_by_role("textbox", name="someone@example.com").fill(email)
        self.page.get_by_role("button", name="Next").click()

    def enter_password(self, password: str):
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    def wait_for_2fa(self, timeout=60):
        print("🛡️ Waiting for MFA to complete or dashboard to load (max 60s)...")
        try:
            self.page.wait_for_url("**/dashboard.pl**", timeout=timeout*1000)
            print("✅ MFA completed early, continuing...")
            return True
        except Exception:
            print("⏳ MFA not completed within 60s, proceeding anyway...")
            return False

    def extract_2fa_code(self):
        # Try to extract the 2FA code if present
        try:
            code = self.page.locator("[id*=\"idRichContext_DisplaySign\"]").inner_text()
            print(f"🔑 2FA Code: {code}")
        except Exception:
            print("2FA code not found or not required.")

    def wait_for_dashboard(self, timeout=60):
        self.page.wait_for_url("**/dashboard.pl**", timeout=timeout*1000)
        return "dashboard.pl" in self.page.url 