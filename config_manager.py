"""
مدير تكوين تطبيق Streamlit
يستخدم لمنع استدعاء set_page_config() أكثر من مرة في التطبيق
"""

class ConfigManager:
    """مدير تكوين التطبيق لمنع استدعاء set_page_config() أكثر من مرة"""
    
    _instance = None
    _page_config_set = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def set_page_config_if_needed(self, **kwargs):
        """
        تعيين تكوين الصفحة إذا لم يتم تعيينه بالفعل
        
        المعلمات:
            **kwargs: معلمات لدالة st.set_page_config()
        
        العوائد:
            bool: True إذا تم تعيين التكوين، False إذا كان التكوين معينًا بالفعل
        """
        import streamlit as st
        
        if not ConfigManager._page_config_set:
            st.set_page_config(**kwargs)
            ConfigManager._page_config_set = True
            return True
        return False
    
    def is_page_config_set(self):
        """التحقق مما إذا كان تكوين الصفحة قد تم تعيينه بالفعل"""
        return ConfigManager._page_config_set
