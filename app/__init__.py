from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # 加载数据库配置
    from config import db_config
    app.config.from_object(db_config)
    db.init_app(app)
    # 自动创建所有表
    with app.app_context():
        db.create_all()
    return app