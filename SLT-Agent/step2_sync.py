import json
import uuid
import platform
import requests
from datetime import datetime
from config import ERP_BASE_URL, STORAGE_PATH

# 🔐 ADMIN API KEY (ONLY ON SERVER / BUILD SYSTEM)
ADMIN_API_KEY = "YOUR_ADMIN_API_KEY"
ADMIN_API_SECRET = "YOUR_ADMIN_API_SECRET"

def sync_employee(cookies, user_agent=None):
    try:
        session = requests.Session()
        if user_agent:
            print(f"🕵️ Using User-Agent: {user_agent[:30]}...")
            session.headers.update({"User-Agent": user_agent})
        
        # ----------------------------- 
        # DEBUG: Print received cookies
        # ----------------------------- 
        print("🔍 Received cookies:")
        for c in cookies:
            print(f"  - {c['name']}: domain={c.get('domain')}, path={c.get('path')}")
        
        # ----------------------------- 
        # Attach cookies properly
        # ----------------------------- 
        sid_token = None
        
        for c in cookies:
            # Set cookie with correct domain
            domain = c.get("domain", "erp.sltechsoft.com")
            if domain.startswith("."):
                domain = domain[1:]
            
            session.cookies.set(
                name=c["name"],
                value=c["value"],
                domain=domain,
                path=c.get("path", "/"),
                secure=c.get("secure", True)
            )
            
            if c["name"] == "sid":
                sid_token = c["value"]
        
        print(f"🔑 SID Token: {sid_token[:20] if sid_token else 'NOT FOUND'}")
        
        if not sid_token:
            print("❌ No session ID (sid) found in cookies")
            return False
        
        # ----------------------------- 
        # STEP 1: Get CSRF Token
        # ----------------------------- 
        print("🔐 Fetching CSRF token...")
        csrf_response = session.get(
            f"{ERP_BASE_URL}/api/method/frappe.auth.get_logged_user",
            headers={"Accept": "application/json"}
        )
        
        # Extract CSRF token from response cookies
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name == "csrf_token":
                csrf_token = cookie.value
                print(f"✅ CSRF Token found: {csrf_token[:20]}...")
                break
        
        # If not in cookies, check X-Frappe-CSRF-Token header
        if not csrf_token and "X-Frappe-CSRF-Token" in csrf_response.headers:
            csrf_token = csrf_response.headers["X-Frappe-CSRF-Token"]
            print(f"✅ CSRF Token from header: {csrf_token[:20]}...")
        
        if not csrf_token:
            print("⚠️ CSRF token not found, trying without it...")
        
        # ----------------------------- 
        # STEP 2: Set headers with CSRF
        # ----------------------------- 
        session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        })
        
        if csrf_token:
            session.headers.update({"X-Frappe-CSRF-Token": csrf_token})
        
        # ----------------------------- 
        # STEP 3: Get logged-in user
        # ----------------------------- 
        print("👤 Getting logged-in user...")
        user_response = session.get(f"{ERP_BASE_URL}/api/method/frappe.auth.get_logged_user")
        
        print(f"📡 Status: {user_response.status_code}")
        
        if user_response.status_code == 403:
            print("❌ 403 Forbidden - Trying alternative method...")
            # Try using /api/method/frappe.handler.printview instead
            user_response = session.get(f"{ERP_BASE_URL}/api/method/frappe.sessions.get_current_user")
        
        if user_response.status_code != 200:
            print(f"❌ Failed to get user. Status: {user_response.status_code}")
            print(f"Response: {user_response.text[:500]}")
            return False
        
        email = user_response.json().get("message")
        if not email:
            print("❌ Logged-in user not found in response")
            print("Response:", user_response.text)
            return False
        
        print("✅ Logged-in user:", email)
        
        # ----------------------------- 
        # Find Employee
        # ----------------------------- 
        employee = find_employee(session, email)
        
        # ----------------------------- 
        # AUTO CREATE EMPLOYEE (IF MISSING)
        # ----------------------------- 
        if not employee:
            print("⚠️ Employee missing, auto-creating...")
            employee = create_employee_note(email)
            if not employee:
                print("❌ Employee auto-create failed")
                return False
        
        # ----------------------------- 
        # Create device.json
        # ----------------------------- 
        device_data = {
            "employee_id": employee["name"],
            "employee_name": employee["employee_name"],
            "email": email,
            "department": employee.get("department"),
            "designation": employee.get("designation"),
            "device_id": str(uuid.uuid4()),
            "machine_name": platform.node(),
            "os": platform.platform(),
            "first_login": datetime.now().isoformat(),
            # 🆕 Store session for future use
            "sid": sid_token,
            "csrf_token": csrf_token
        }
        
        with open(STORAGE_PATH, "w", encoding="utf-8") as f:
            json.dump(device_data, f, indent=2)
        
        print("✅ device.json created")
        print(json.dumps({k: v for k, v in device_data.items() if k not in ['sid', 'csrf_token']}, indent=2))
        return True
        
    except Exception as e:
        print("❌ sync_employee error:", e)
        import traceback
        traceback.print_exc()
        return False


# ==================================================
# HELPERS
# ==================================================
def find_employee(session, email):
    filters = [
        ["user_id", "=", email],
        ["personal_email", "=", email],
        ["company_email", "=", email],
    ]
    
    for f in filters:
        try:
            r = session.get(
                f"{ERP_BASE_URL}/api/resource/Employee",
                params={
                    "filters": json.dumps([f]),
                    "fields": json.dumps(["name", "employee_name", "department", "designation"])
                }
            )
            
            if r.status_code == 200:
                data = r.json().get("data", [])
                if data:
                    print(f"✅ Employee found via: {f[0]}")
                    return data[0]
            else:
                print(f"⚠️ Employee search failed for {f[0]}: {r.status_code}")
        except Exception as e:
            print(f"⚠️ Error searching employee by {f[0]}: {e}")
    
    return None


def create_employee_note(email):
    headers = {
        "Authorization": f"token {ADMIN_API_KEY}:{ADMIN_API_SECRET}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "doctype": "Employee",
        "employee_name": email.split("@")[0].title(),
        "user_id": email,
        "company_email": email,
        "status": "Active"
    }
    
    try:
        r = requests.post(
            f"{ERP_BASE_URL}/api/resource/Employee",
            headers=headers,
            json=payload
        )
        
        if r.status_code in (200, 201):
            print("✅ Employee auto-created")
            return r.json()["data"]
        
        print(f"❌ Employee create failed ({r.status_code}):", r.text)
    except Exception as e:
        print("❌ Employee creation error:", e)
    
    return None