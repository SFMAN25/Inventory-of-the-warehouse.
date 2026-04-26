def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            data = change.document.to_dict()
            if data.get('action') == "بدء مراقبة":
                print(f"🚀 فحص فوري مطلوب لـ: {data.get('target_name')}")
                # هنا بنشغل السيلينيوم فوراً
                result = check_status(data.get('target_link'))
                # تحديث النتيجة
                change.document.reference.update({"action": result})

# تشغيل المستمع الفوري
query = db.collection("activity_logs").where("action", "==", "بدء مراقبة")
query.on_snapshot(on_snapshot)

# السكريبت يفضل شغال مبيقفلش
import time
while True:
    time.sleep(1)
