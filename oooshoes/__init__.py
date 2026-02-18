import os

engine = os.getenv("DB_ENGINE") or os.getenv("MYSQL_ENGINE") or ""
engine = engine.lower()

if "mysql" in engine:
    import pymysql
    pymysql.install_as_MySQLdb()
