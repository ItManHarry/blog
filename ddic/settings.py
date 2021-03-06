'''
    Flask配置
'''
import os
#开发数据库
dev_db = os.getenv('DEVELOP_DB')
#生产数据库
pro_db = os.getenv('PRODUCT_DB')
class BaseConfig():
    # 系统秘钥(session等使用必须配置)
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey0001')
    #print('SECRET_KEY is : %s' %SECRET_KEY)
    # Bootstrap加载本地资源
    BOOTSTRAP_SERVE_LOCAL = True
    #分页显示,每页的数量
    ITEM_COUNT_PER_PAGE=10
    #主题列表
    BLOG_THEMES = {
        'bootstrap':'Default',
        'cyborg':'Cyborg',
        #'solar':'Solar',
        'united':'United',
        'minty':'Minty',
        'sketchy':'Sketchy',
        #'morph':'Morph',
        'spacelab':'Spacelab'
    }
#开发环境配置
class DevConfig(BaseConfig):
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL', dev_db)
#正式环境配置
class ProConfig(BaseConfig):
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL', pro_db)
#配置映射
config = {
    'dev_config':DevConfig,
    'pro_config':ProConfig
}