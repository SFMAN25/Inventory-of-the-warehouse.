import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# الربط بـ Firebase باستخدام الـ Secret (أهم خطوة للأتمتة)
def init_app():
    firebase_config = os.environ.get('FIREBASE_JSON')
    if firebase_config:
        cred_dict = json.loads(firebase_config)
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        return firestore.client()
    return None

db = init_app()

def run_tracker():
    # بنجيب البيانات من الـ Collection اللي أنت عملتها
    logs_ref = db.collection("activity_logs")
    targets = logs_ref.where("action", "==", "بدء مراقبة").stream()
    
    for target in targets:
        data = target.to_dict()
        url = data.get('target_link')
        
        options = Options()
        options.add_argument("--headless") # ضروري عشان يشتغل على سيرفر GitHub
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(url)
            # تحديث الحالة في الداتابيز فوراً
            logs_ref.document(target.id).update({"action": "متصل الآن 🟢"})
        except:
            logs_ref.document(target.id).update({"action": "فشل الفحص ❌"})
        finally:
            driver.quit()

if __name__ == "__main__":
    run_tracker()
