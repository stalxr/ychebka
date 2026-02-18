import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oooshoes.settings")
django.setup()

from django.db import connection

with connection.cursor() as c:
    c.execute("select current_database(), current_user, current_schema()")
    print("DB:", c.fetchone())

    c.execute("show search_path")
    print("search_path:", c.fetchone())

    c.execute(
        "select column_name from information_schema.columns "
        "where table_schema='public' and table_name='Orders' "
        "order by ordinal_position"
    )
    print("COLUMNS:", [r[0] for r in c.fetchall()])
