import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import time

# 1. الربط بالسكرت اللي إحنا عملناه
firebase_config = os.environ.get('FIREBASE_JSON')
cred_dict = json.loads(firebase_config)
cred = credentials.Certificate(cred_dict)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. وظيفة الفحص الفوري (Listener)
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name in ['ADDED', 'MODIFIED']:
            data = change.document.to_dict()
            if data.get('action') == "بدء مراقبة":
                print(f"🚀 اكتشاف طلب فحص فوري لـ: {data.get('target_name')}")
                # هنا بنشغل السيلينيوم (نفس الكود اللي فات)
                # وبعد ما يخلص نحدث الحالة
                change.document.reference.update({"action": "متصل الآن 🟢"})

# 3. تشغيل المراقبة المستمرة
print("📡 البوت الآن في وضع الاستعداد الفوري...")
query = db.collection("activity_logs").where("action", "==", "بدء مراقبة")
query.on_snapshot(on_snapshot)

# خليه شغال ميفصلش
while True:
    time.sleep(1)
