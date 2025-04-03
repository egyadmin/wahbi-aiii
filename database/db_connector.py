"""
موصل قاعدة البيانات لنظام إدارة المناقصات
"""

import os
import sqlite3
import logging

logger = logging.getLogger('tender_system.database')

class DatabaseConnector:
    """فئة موصل قاعدة البيانات"""
    
    def __init__(self, config):
        """تهيئة موصل قاعدة البيانات"""
        self.config = config
        self.db_config = config.get_database_config()
        self.db_path = self.db_config.get('path')
        self.connection = None
        self.cursor = None
        
        # إنشاء قاعدة البيانات إذا لم تكن موجودة
        self._initialize_database()
    
    def _initialize_database(self):
        """تهيئة قاعدة البيانات"""
        try:
            # التأكد من وجود المجلد
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # إنشاء الاتصال
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            
            # إنشاء الجداول إذا لم تكن موجودة
            self._create_tables()
            
            # إضافة بيانات افتراضية إذا كانت قاعدة البيانات فارغة
            self._add_default_data()
            
            logger.info(f"تم تهيئة قاعدة البيانات بنجاح: {self.db_path}")
        except Exception as e:
            logger.error(f"خطأ في تهيئة قاعدة البيانات: {str(e)}")
            raise
    
    def _create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        # جدول المشاريع المحفوظة
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            project_code TEXT,
            project_description TEXT,
            boq_data TEXT NOT NULL,
            total_cost REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # جدول المستخدمين
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول المشاريع
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT NOT NULL,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # جدول المستندات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            document_type TEXT NOT NULL,
            description TEXT,
            uploaded_by INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (uploaded_by) REFERENCES users (id)
        )
        ''')
        
        # جدول بنود التسعير
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            item_number TEXT NOT NULL,
            description TEXT NOT NULL,
            unit TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # جدول الموارد البشرية
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS human_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            daily_cost REAL NOT NULL,
            skills TEXT,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول المعدات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            daily_cost REAL NOT NULL,
            status TEXT NOT NULL,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول المواد
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            supplier TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول المخاطر
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            probability TEXT NOT NULL,
            impact TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            mitigation_strategy TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # جدول التقارير
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_id INTEGER,
            report_type TEXT NOT NULL,
            period TEXT,
            file_path TEXT,
            created_by INTEGER,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # حفظ التغييرات
        self.connection.commit()
    
    def _add_default_data(self):
        """إضافة بيانات افتراضية"""
        # التحقق من وجود مستخدمين
        self.cursor.execute("SELECT COUNT(*) FROM users")
        user_count = self.cursor.fetchone()[0]
        
        if user_count == 0:
            # إضافة مستخدم افتراضي (admin/admin)
            self.cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin', 'مدير النظام', 'admin@example.com', 'مدير', 'نشط'))
            
            # إضافة مستخدمين إضافيين
            self.cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', ('user1', 'password', 'أحمد محمد', 'ahmed@example.com', 'مستخدم', 'نشط'))
            
            self.cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', ('user2', 'password', 'سارة أحمد', 'sara@example.com', 'مستخدم', 'نشط'))
            
            # حفظ التغييرات
            self.connection.commit()
            
            logger.info("تم إضافة بيانات المستخدمين الافتراضية")
        
        # التحقق من وجود مشاريع
        self.cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = self.cursor.fetchone()[0]
        
        if project_count == 0:
            # إضافة مشاريع افتراضية
            self.cursor.execute('''
            INSERT INTO projects (name, client, description, start_date, end_date, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('مشروع تطوير الطريق السريع', 'وزارة النقل', 'مشروع تطوير وتوسعة الطريق السريع', '2025-01-15', '2025-12-31', 'نشط', 1))
            
            self.cursor.execute('''
            INSERT INTO projects (name, client, description, start_date, end_date, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('مشروع بناء المدرسة الثانوية', 'وزارة التعليم', 'مشروع بناء مدرسة ثانوية جديدة', '2025-02-01', '2025-08-30', 'نشط', 1))
            
            self.cursor.execute('''
            INSERT INTO projects (name, client, description, start_date, end_date, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('مشروع تجديد المستشفى', 'وزارة الصحة', 'مشروع تجديد وتطوير المستشفى', '2024-10-15', '2025-03-15', 'مكتمل', 1))
            
            # حفظ التغييرات
            self.connection.commit()
            
            logger.info("تم إضافة بيانات المشاريع الافتراضية")
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الاستعلام: {str(e)}")
            self.connection.rollback()
            raise
    
    def fetch_one(self, query, params=None):
        """جلب صف واحد"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query, params=None):
        """جلب جميع الصفوف"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def insert(self, table, data):
        """إدراج بيانات"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, list(data.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"خطأ في إدراج البيانات: {str(e)}")
            self.connection.rollback()
            raise
    
    def update(self, table, data, condition):
        """تحديث بيانات"""
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        try:
            self.cursor.execute(query, list(data.values()))
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"خطأ في تحديث البيانات: {str(e)}")
            self.connection.rollback()
            raise
    
    def delete(self, table, condition):
        """حذف بيانات"""
        query = f"DELETE FROM {table} WHERE {condition}"
        
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"خطأ في حذف البيانات: {str(e)}")
            self.connection.rollback()
            raise
    
    def close(self):
        """إغلاق الاتصال"""
        if self.connection:
            self.connection.close()
            logger.info("تم إغلاق الاتصال بقاعدة البيانات")