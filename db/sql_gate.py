from hashlib import sha256
from sqlite3.dbapi2 import Connection as Con
from typing import Any


def hasher(a: str):
    return sha256(bytes(a, 'utf-8')).hexdigest()


def nn(a):
    return a is not None


def construct_select(con: Con, base_table: str, fields: list[str] = None, where: dict[str, Any] = None):
    if fields is None:
        fields = ['*']
    if where is None:
        where = {}

    call = f"""SELECT {', '.join(fields)} FROM {base_table} WHERE"""

    where_exists = False
    args = []
    for n, (arg, val) in enumerate(where.items()):
        if nn(val):
            where_exists = True
            call += f""" {arg}=? and"""
            args.append(val)
    return con.execute(call[:(-4 if where_exists else -6)], args)


def construct_insert(con: Con, base_table: str, values: dict[str, Any] = None):
    cur = con.cursor()
    fields = list()
    args = list()
    for k, v in values.items():
        if nn(v):
            fields.append(k)
            args.append(v)

    call = f"""INSERT INTO {base_table} ({', '.join(fields)}) VALUES ({', '.join('?' * len(args))})"""

    cur.execute(call, args)
    con.commit()
    return cur.lastrowid


def construct_update(con: Con, base_table: str, fields: list[tuple[str, str, Any]], where: dict):
    """
    :param con: Connestion
    :param base_table: Table
    :param fields: Name, Operator, Value
    :param where: Specification
    :return: user_id
    """
    args = list()
    call = f"""UPDATE {base_table} SET """
    call += ', '.join([(f"""{k} {op} ?""", args.append(v))[0] for k, op, v in fields if nn(v)])
    call += """ WHERE """
    call += ', '.join([(f"""{k} = ?""", args.append(v))[0] for k, v in where.items() if nn(v)])
    cur = con.cursor()
    cur.execute(call, args)
    con.commit()
    return cur.lastrowid


def get_users(con: Con, user_id=None, email=None, password: str = None):
    """
    :param con: Connection
    :param user_id: user_id
    :param email: email
    :param password: password(not hashed)
    :return: users by args
    """
    attrs = {'id': user_id,
             'email': email,
             'password': hasher(password) if nn(password) else None}
    return construct_select(con, 'users', where=attrs).fetchall()


def add_user(con: Con, email: str, password: str, username: str = None):
    attrs = {
        'email': email,
        'password': hasher(password),
        'username': username
    }
    return construct_insert(con, 'users', attrs)


def add_money(con: Con, user_id: int, money: int):
    return construct_update(con, 'users', [('money', '= money + ', money)], {'id': user_id})
