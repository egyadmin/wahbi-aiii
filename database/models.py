"""
نماذج البيانات لنظام إدارة المناقصات
"""

import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger('tender_system.models')

class User:
    """نموذج المستخدم"""
    
    def __init__(self, id=None, username=None, password=None, full_name=None, email=None, role=None, status=None):
        """تهيئة نموذج المستخدم"""
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role
        self.status = status
        self.created_at = None
        self.updated_at = None
    
    @staticmethod
    def authenticate(username, password, db):
        """مصادقة المستخدم"""
        try:
            query = "SELECT * FROM users WHERE username = ? AND password = ? AND status = 'نشط'"
            result = db.fetch_one(query, (username, password))
            
            if result:
                user = User()
                user.id = result[0]
                user.username = result[1]
                user.password = result[2]
                user.full_name = result[3]
                user.email = result[4]
                user.role = result[5]
                user.status = result[6]
                user.created_at = result[7]
                user.updated_at = result[8]
                
                return user
            
            return None
        except Exception as e:
            logger.error(f"خطأ في مصادقة المستخدم: {str(e)}")
            return None
    
    @staticmethod
    def get_by_id(user_id, db):
        """الحصول على المستخدم بواسطة المعرف"""
        try:
            query = "SELECT * FROM users WHERE id = ?"
            result = db.fetch_one(query, (user_id,))
            
            if result:
                user = User()
                user.id = result[0]
                user.username = result[1]
                user.password = result[2]
                user.full_name = result[3]
                user.email = result[4]
                user.role = result[5]
                user.status = result[6]
                user.created_at = result[7]
                user.updated_at = result[8]
                
                return user
            
            return None
        except Exception as e:
            logger.error(f"خطأ في الحصول على المستخدم: {str(e)}")
            return None
    
    @staticmethod
    def get_all(db):
        """الحصول على جميع المستخدمين"""
        try:
            query = "SELECT * FROM users"
            results = db.fetch_all(query)
            
            users = []
            for result in results:
                user = User()
                user.id = result[0]
                user.username = result[1]
                user.password = result[2]
                user.full_name = result[3]
                user.email = result[4]
                user.role = result[5]
                user.status = result[6]
                user.created_at = result[7]
                user.updated_at = result[8]
                
                users.append(user)
            
            return users
        except Exception as e:
            logger.error(f"خطأ في الحصول على المستخدمين: {str(e)}")
            return []
    
    def save(self, db):
        """حفظ المستخدم"""
        try:
            if self.id:
                # تحديث مستخدم موجود
                data = {
                    'username': self.username,
                    'password': self.password,
                    'full_name': self.full_name,
                    'email': self.email,
                    'role': self.role,
                    'status': self.status,
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                db.update('users', data, f"id = {self.id}")
                return self.id
            else:
                # إنشاء مستخدم جديد
                data = {
                    'username': self.username,
                    'password': self.password,
                    'full_name': self.full_name,
                    'email': self.email,
                    'role': self.role,
                    'status': self.status
                }
                
                self.id = db.insert('users', data)
                return self.id
        except Exception as e:
            logger.error(f"خطأ في حفظ المستخدم: {str(e)}")
            return None
    
    def delete(self, db):
        """حذف المستخدم"""
        try:
            if self.id:
                db.delete('users', f"id = {self.id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"خطأ في حذف المستخدم: {str(e)}")
            return False


class Project:
    """نموذج المشروع"""
    
    def __init__(self, id=None, name=None, client=None, description=None, start_date=None, end_date=None, status=None, created_by=None):
        """تهيئة نموذج المشروع"""
        self.id = id
        self.name = name
        self.client = client
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.created_by = created_by
        self.created_at = None
        self.updated_at = None
    
    @staticmethod
    def get_by_id(project_id, db):
        """الحصول على المشروع بواسطة المعرف"""
        try:
            query = "SELECT * FROM projects WHERE id = ?"
            result = db.fetch_one(query, (project_id,))
            
            if result:
                project = Project()
                project.id = result[0]
                project.name = result[1]
                project.client = result[2]
                project.description = result[3]
                project.start_date = result[4]
                project.end_date = result[5]
                project.status = result[6]
                project.created_by = result[7]
                project.created_at = result[8]
                project.updated_at = result[9]
                
                return project
            
            return None
        except Exception as e:
            logger.error(f"خطأ في الحصول على المشروع: {str(e)}")
            return None
    
    @staticmethod
    def get_all(db):
        """الحصول على جميع المشاريع"""
        try:
            query = "SELECT * FROM projects"
            results = db.fetch_all(query)
            
            projects = []
            for result in results:
                project = Project()
                project.id = result[0]
                project.name = result[1]
                project.client = result[2]
                project.description = result[3]
                project.start_date = result[4]
                project.end_date = result[5]
                project.status = result[6]
                project.created_by = result[7]
                project.created_at = result[8]
                project.updated_at = result[9]
                
                projects.append(project)
            
            return projects
        except Exception as e:
            logger.error(f"خطأ في الحصول على المشاريع: {str(e)}")
            return []
    
    def save(self, db):
        """حفظ المشروع"""
        try:
            if self.id:
                # تحديث مشروع موجود
                data = {
                    'name': self.name,
                    'client': self.client,
                    'description': self.description,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'status': self.status,
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                db.update('projects', data, f"id = {self.id}")
                return self.id
            else:
                # إنشاء مشروع جديد
                data = {
                    'name': self.name,
                    'client': self.client,
                    'description': self.description,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'status': self.status,
                    'created_by': self.created_by
                }
                
                self.id = db.insert('projects', data)
                return self.id
        except Exception as e:
            logger.error(f"خطأ في حفظ المشروع: {str(e)}")
            return None
    
    def delete(self, db):
        """حذف المشروع"""
        try:
            if self.id:
                db.delete('projects', f"id = {self.id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"خطأ في حذف المشروع: {str(e)}")
            return False


class Document:
    """نموذج المستند"""
    
    def __init__(self, id=None, project_id=None, name=None, file_path=None, document_type=None, description=None, uploaded_by=None):
        """تهيئة نموذج المستند"""
        self.id = id
        self.project_id = project_id
        self.name = name
        self.file_path = file_path
        self.document_type = document_type
        self.description = description
        self.uploaded_by = uploaded_by
        self.uploaded_at = None
    
    @staticmethod
    def get_by_id(document_id, db):
        """الحصول على المستند بواسطة المعرف"""
        try:
            query = "SELECT * FROM documents WHERE id = ?"
            result = db.fetch_one(query, (document_id,))
            
            if result:
                document = Document()
                document.id = result[0]
                document.project_id = result[1]
                document.name = result[2]
                document.file_path = result[3]
                document.document_type = result[4]
                document.description = result[5]
                document.uploaded_by = result[6]
                document.uploaded_at = result[7]
                
                return document
            
            return None
        except Exception as e:
            logger.error(f"خطأ في الحصول على المستند: {str(e)}")
            return None
    
    @staticmethod
    def get_by_project(project_id, db):
        """الحصول على المستندات بواسطة معرف المشروع"""
        try:
            query = "SELECT * FROM documents WHERE project_id = ?"
            results = db.fetch_all(query, (project_id,))
            
            documents = []
            for result in results:
                document = Document()
                document.id = result[0]
                document.project_id = result[1]
                document.name = result[2]
                document.file_path = result[3]
                document.document_type = result[4]
                document.description = result[5]
                document.uploaded_by = result[6]
                document.uploaded_at = result[7]
                
                documents.append(document)
            
            return documents
        except Exception as e:
            logger.error(f"خطأ في الحصول على المستندات: {str(e)}")
            return []
    
    def save(self, db):
        """حفظ المستند"""
        try:
            if self.id:
                # تحديث مستند موجود
                data = {
                    'project_id': self.project_id,
                    'name': self.name,
                    'file_path': self.file_path,
                    'document_type': self.document_type,
                    'description': self.description
                }
                
                db.update('documents', data, f"id = {self.id}")
                return self.id
            else:
                # إنشاء مستند جديد
                data = {
                    'project_id': self.project_id,
                    'name': self.name,
                    'file_path': self.file_path,
                    'document_type': self.document_type,
                    'description': self.description,
                    'uploaded_by': self.uploaded_by
                }
                
                self.id = db.insert('documents', data)
                return self.id
        except Exception as e:
            logger.error(f"خطأ في حفظ المستند: {str(e)}")
            return None
    
    def delete(self, db):
        """حذف المستند"""
        try:
            if self.id:
                db.delete('documents', f"id = {self.id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"خطأ في حذف المستند: {str(e)}")
            return False


"""
نماذج قاعدة البيانات للتسعير
"""
import sqlite3
from datetime import datetime

class PricingItem:
    """نموذج بند التسعير"""
    def __init__(self, db):
        self.db = db

    def create_table(self):
        """إنشاء جدول بنود التسعير"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS pricing_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                code TEXT NOT NULL,
                description TEXT NOT NULL,
                unit TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        """)

    def add_item(self, project_id, item_data):
        """إضافة بند جديد"""
        sql = """
            INSERT INTO pricing_items (
                project_id, code, description, unit, 
                quantity, unit_price, total_price, category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            project_id,
            item_data['code'],
            item_data['description'],
            item_data['unit'],
            item_data['quantity'],
            item_data['unit_price'],
            item_data['total_price'],
            item_data.get('category')
        )
        return self.db.execute(sql, values)

    def get_project_items(self, project_id):
        """جلب بنود المشروع"""
        sql = "SELECT * FROM pricing_items WHERE project_id = ?"
        return self.db.fetch_all(sql, (project_id,))

    def update_item(self, item_id, item_data):
        """تحديث بند"""
        sql = """
            UPDATE pricing_items 
            SET code=?, description=?, unit=?, quantity=?,
                unit_price=?, total_price=?, category=?
            WHERE id=?
        """
        values = (
            item_data['code'],
            item_data['description'],
            item_data['unit'],
            item_data['quantity'],
            item_data['unit_price'],
            item_data['total_price'],
            item_data.get('category'),
            item_id
        )
        return self.db.execute(sql, values)

    def delete_item(self, item_id):
        """حذف بند"""
        sql = "DELETE FROM pricing_items WHERE id = ?"
        return self.db.execute(sql, (item_id,))


class Risk:
    """نموذج المخاطرة"""
    
    def __init__(self, id=None, project_id=None, name=None, category=None, probability=None, impact=None, risk_level=None, mitigation_strategy=None, created_by=None):
        """تهيئة نموذج المخاطرة"""
        self.id = id
        self.project_id = project_id
        self.name = name
        self.category = category
        self.probability = probability
        self.impact = impact
        self.risk_level = risk_level
        self.mitigation_strategy = mitigation_strategy
        self.created_by = created_by
        self.created_at = None
        self.updated_at = None
    
    @staticmethod
    def get_by_project(project_id, db):
        """الحصول على المخاطر بواسطة معرف المشروع"""
        try:
            query = "SELECT * FROM risks WHERE project_id = ?"
            results = db.fetch_all(query, (project_id,))
            
            risks = []
            for result in results:
                risk = Risk()
                risk.id = result[0]
                risk.project_id = result[1]
                risk.name = result[2]
                risk.category = result[3]
                risk.probability = result[4]
                risk.impact = result[5]
                risk.risk_level = result[6]
                risk.mitigation_strategy = result[7]
                risk.created_by = result[8]
                risk.created_at = result[9]
                risk.updated_at = result[10]
                
                risks.append(risk)
            
            return risks
        except Exception as e:
            logger.error(f"خطأ في الحصول على المخاطر: {str(e)}")
            return []
    
    def save(self, db):
        """حفظ المخاطرة"""
        try:
            if self.id:
                # تحديث مخاطرة موجودة
                data = {
                    'project_id': self.project_id,
                    'name': self.name,
                    'category': self.category,
                    'probability': self.probability,
                    'impact': self.impact,
                    'risk_level': self.risk_level,
                    'mitigation_strategy': self.mitigation_strategy,
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                db.update('risks', data, f"id = {self.id}")
                return self.id
            else:
                # إنشاء مخاطرة جديدة
                data = {
                    'project_id': self.project_id,
                    'name': self.name,
                    'category': self.category,
                    'probability': self.probability,
                    'impact': self.impact,
                    'risk_level': self.risk_level,
                    'mitigation_strategy': self.mitigation_strategy,
                    'created_by': self.created_by
                }
                
                self.id = db.insert('risks', data)
                return self.id
        except Exception as e:
            logger.error(f"خطأ في حفظ المخاطرة: {str(e)}")
            return None



class Report:
    """نموذج التقرير"""
    
    def __init__(self, id=None, name=None, project_id=None, report_type=None, period=None, file_path=None, created_by=None, status=None):
        """تهيئة نموذج التقرير"""
        self.id = id
        self.name = name
        self.project_id = project_id
        self.report_type = report_type
        self.period = period
        self.file_path = file_path
        self.created_by = created_by
        self.status = status
        self.created_at = None
        self.updated_at = None
    
    @staticmethod
    def get_by_project(project_id, db):
        """الحصول على التقارير بواسطة معرف المشروع"""
        try:
            query = "SELECT * FROM reports WHERE project_id = ?"
            results = db.fetch_all(query, (project_id,))
            
            reports = []
            for result in results:
                report = Report()
                report.id = result[0]
                report.name = result[1]
                report.project_id = result[2]
                report.report_type = result[3]
                report.period = result[4]
                report.file_path = result[5]
                report.created_by = result[6]
                report.status = result[7]
                report.created_at = result[8]
                report.updated_at = result[9]
                
                reports.append(report)
            
            return reports
        except Exception as e:
            logger.error(f"خطأ في الحصول على التقارير: {str(e)}")
            return []
    
    def save(self, db):
        """حفظ التقرير"""
        try:
            if self.id:
                # تحديث تقرير موجود
                data = {
                    'name': self.name,
                    'project_id': self.project_id,
                    'report_type': self.report_type,
                    'period': self.period,
                    'file_path': self.file_path,
                    'status': self.status,
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                db.update('reports', data, f"id = {self.id}")
                return self.id
            else:
                # إنشاء تقرير جديد
                data = {
                    'name': self.name,
                    'project_id': self.project_id,
                    'report_type': self.report_type,
                    'period': self.period,
                    'file_path': self.file_path,
                    'created_by': self.created_by,
                    'status': self.status
                }
                
                self.id = db.insert('reports', data)
                return self.id
        except Exception as e:
            logger.error(f"خطأ في حفظ التقرير: {str(e)}")
            return None