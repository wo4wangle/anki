# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import time

from sqlite3 import dbapi2 as sqlite

DBError = sqlite.Error

class DB:
    def __init__(self, path, timeout=0):
        self._db = sqlite.connect(path, timeout=timeout)
        self._db.text_factory = self._textFactory
        self._path = path
        self.echo = os.environ.get("DBECHO")
        self.mod = False

    def execute(self, sql, *a, **ka):
        """The result of execute on the database with sql query and either ka if it exists, or a. 
        
        If insert, update or delete, mod is set to True
        If self.echo, prints the execution time
        """
        s = sql.strip().lower()
        # mark modified?
        for stmt in "insert", "update", "delete":
            if s.startswith(stmt):
                self.mod = True
        t = time.time()
        if ka:
            # execute("...where id = :id", id=5)
            res = self._db.execute(sql, ka)
        else:
            # execute("...where id = ?", 5)
            res = self._db.execute(sql, a)
        if self.echo:
            #print a, ka
            print(sql, "%0.3fms" % ((time.time() - t)*1000))
            if self.echo == "2":
                print(a, ka)
        return res

    def executemany(self, sql, l):
        """The result of executmany on the database with sql query and l list.
        
        Mod is set to True
        If self.echo, prints the execution time
        """
        self.mod = True
        t = time.time()
        self._db.executemany(sql, l)
        if self.echo:
            print(sql, "%0.3fms" % ((time.time() - t)*1000))
            if self.echo == "2":
                print(l)

    def commit(self):
        """Commit database.
         If self.echo, prints the execution time."""
        t = time.time()
        self._db.commit()
        if self.echo:
            print("commit %0.3fms" % ((time.time() - t)*1000))

    def executescript(self, sql):
        """executescript with sql on the database.
         If self.echo, prints sql
        set mod to True."""
        self.mod = True
        if self.echo:
            print(sql)
        self._db.executescript(sql)

    def rollback(self):
        """rollback on the db"""
        self._db.rollback()

    def scalar(self, *a, **kw):
        """The first value of the first tuple of the result, if it exists. None otherwise."""
        res = self.execute(*a, **kw).fetchone()
        if res:
            return res[0]
        return None

    def all(self, *a, **kw):
        """The list of rows of the answer."""
        return self.execute(*a, **kw).fetchall()

    def first(self, *a, **kw):
        """The first row of the answer."""
        c = self.execute(*a, **kw)
        res = c.fetchone()
        c.close()
        return res

    def list(self, *a, **kw):
        """The list of first elements of tuples of the answer."""
        return [x[0] for x in self.execute(*a, **kw)]

    def close(self):
        """Close the underlying database."""
        self._db.close()

    def set_progress_handler(self, *args):
        self._db.set_progress_handler(*args)

    def __enter__(self):
        self._db.execute("begin")
        return self

    def __exit__(self, exc_type, *args):
        self._db.close()

    def totalChanges(self):
        return self._db.total_changes

    def interrupt(self):
        self._db.interrupt()

    def setAutocommit(self, autocommit):
        if autocommit:
            self._db.isolation_level = None
        else:
            self._db.isolation_level = ''

    # strip out invalid utf-8 when reading from db
    def _textFactory(self, data):
        return str(data, errors="ignore")
