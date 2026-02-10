import requests, os
from config import ERP_BASE_URL

def upload_file(session, file_path, doctype, docname):
    url = f"{ERP_BASE_URL}/api/method/upload_file"

    with open(file_path, "rb") as f:
        files = {
            "file": (os.path.basename(file_path), f)
        }

        data = {
            "doctype": doctype,
            "docname": docname,
            "is_private": 1
        }

        r = session.post(url, files=files, data=data)

    if r.status_code in (200, 201):
        print("⬆️ Uploaded to ERP:", file_path)
        return True

    print("❌ Upload failed:", r.text)
    return False
