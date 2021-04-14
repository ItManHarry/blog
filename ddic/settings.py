'''
    配置文件
'''
import os
#开发数据库
dev_db = 'sqlite:///'+os.path.join('e:/python/development', 'db/data.db')
#生产数据库
pro_db = 'sqlite:///'+os.path.join('e:/python/development', 'db/data.db')
class BaseConfig():
    # 系统秘钥(session等使用必须配置)
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey0001')
    # Bootstrap加载本地资源
    BOOTSTRAP_SERVE_LOCAL = True

class DevConfig(BaseConfig):
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL', dev_db)

class ProConfig(BaseConfig):
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL', pro_db)

config = {
    'dev_config':DevConfig,
    'pro_config':ProConfig
}