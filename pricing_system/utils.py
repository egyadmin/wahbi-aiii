
import os
import requests

def download_image(url, save_path):
    """تحميل صورة من URL وحفظها في المسار المحدد"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # التأكد من وجود المجلد
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # حفظ الصورة
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"خطأ في تحميل الصورة: {e}")
        return False
