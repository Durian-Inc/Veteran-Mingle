import functools

import sqlite3 as sql

from flask import render_template


def uses_template(template):
    """Wrap a function to add HTML template rendering functionality."""
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            template_path = template
            ctx = func(*args, **kwargs)
            if type(ctx) is dict:
                try:
                    return render_template(template_path,
                                           veteran=ctx['veteran'])
                except KeyError:
                    try:
                        return render_template(template_path,
                                               organization=ctx['organization'])
                    except KeyError:
                        pass
            else:
                return ctx
        return wrapped
    return wrapper

# Database functions:

def get_veteran(uname):
    DATABASE = 'app/database/vets.db'
    vet = None
    command = "SELECT * FROM veterans where username = '%s' " %uname
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(command)
        vet = cur.fetchone()
        cur.close()
    return vet
    