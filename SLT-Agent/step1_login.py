from http import cookies
import sys
from time import time

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtCore import QUrl, QTimer

from config import ERP_LOGIN_URL, SUCCESS_REDIRECT_KEYWORDS
from step2_sync import sync_employee


class ERPLoginWindow(QWebEngineView):
    def __init__(self):
        super().__init__()

        # -------------------------------
        # Window setup
        # -------------------------------
        self.setWindowTitle("SLT Agent - ERP Login")
        self.resize(1100, 700)

        # -------------------------------
        # Internal flags
        # -------------------------------
        self.cookies = []
        self.login_detected = False   # one-time guard

        # -------------------------------
        # Cookie store (ERP session)
        # -------------------------------
        profile = QWebEngineProfile.defaultProfile()
        self.cookie_store = profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)

        # -------------------------------
        # URL change listener
        # -------------------------------
        self.urlChanged.connect(self.on_url_change)

        # -------------------------------
        # Load ERP login page
        # -------------------------------
        self.load(QUrl(ERP_LOGIN_URL))

    # ==================================================
    # Cookie collection
    # ==================================================
    def on_cookie_added(self, cookie):
        try:
            cookie_data = {
                "name": bytes(cookie.name()).decode(),
                "value": bytes(cookie.value()).decode(),
                "domain": cookie.domain()
            }
            if cookie_data not in self.cookies:
                self.cookies.append(cookie_data)
        except Exception as e:
            print("Cookie parse error:", e)

    # ==================================================
    # Login success detection (ONE TIME)
    # ==================================================
    def on_url_change(self, url):
        url_str = url.toString()
        print("URL:", url_str)

        if self.login_detected:
            return

        for keyword in SUCCESS_REDIRECT_KEYWORDS:
            if keyword in url_str:
                self.login_detected = True
                print("✅ ERP Login Successful")
                self.login_success()
                break

    # ==================================================
    # After login success
    # ==================================================
    # In your step1_login.py, after login success:
    def on_login_success(self):
        cookies = []
        cookie_store = self.web_view.page().profile().cookieStore()
    
        def extract_cookies(cookie):
            cookies.append({
                "name": cookie.name().data().decode(),
                "value": cookie.value().data().decode(),
                "domain": cookie.domain(),
                "path": cookie.path(),
                "secure": cookie.isSecure(),
                "httpOnly": cookie.isHttpOnly()
            })
    
        cookie_store.loadAllCookies()
    # Wait for cookies to load
        time.sleep(1)
    
    # Print for debugging
        print("🍪 Extracted cookies:")
        for c in cookies:
            print(f"  {c['name']}: {c['value'][:20]}... (domain: {c['domain']})")
    
        success = sync_employee(cookies)
    # ... rest of your code
    def login_success(self):
        print("➡️ Fetching employee details from ERP...")
        QTimer.singleShot(1500, self.sync_and_close)

    # ==================================================
    # STEP-2 only (NO background start here)
    # ==================================================
    def sync_and_close(self):
        user_agent = self.page().profile().httpUserAgent()
        print(f"🕵️ Captured User-Agent: {user_agent[:30]}...")
        success = sync_employee(self.cookies, user_agent=user_agent)

        if success:
            print("✅ Employee synced & device bound")
        else:
            print("❌ Employee sync failed")

        self.close()


# ==================================================
# PUBLIC FUNCTION (USED BY main.py)
# ==================================================
def start_login_ui():
    app = QApplication(sys.argv)
    window = ERPLoginWindow()
    window.show()
    app.exec()
