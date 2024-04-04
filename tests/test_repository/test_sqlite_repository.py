import pytest
import sqlite3
import os

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass
from datetime import datetime


TEST_DB_PATH = r'tests\test_repository\test_db\test.db'


@pytest.fixture
def custom_class():
    @dataclass
    class Custom():
        float_field: float = 4.2
        str_field: str = "some_str"
        date_field: str = datetime.now().isoformat(sep='\t', timespec='minutes')
        pk: int = 0
    return Custom


@pytest.fixture
def repo(custom_class):
    with sqlite3.connect(TEST_DB_PATH) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS custom")
    with sqlite3.connect(TEST_DB_PATH) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE custom(float_field, str_field, date_field)")
    con.close()
    return SQLiteRepository(db_file=TEST_DB_PATH, cls=custom_class)


def test_crud(repo, custom_class):
    new_obj = custom_class(
        1., "2", datetime.now().isoformat(sep='\t', timespec='minutes'))
    
    pk = repo.add(new_obj)
    assert pk == new_obj.pk
    
    obj_get = repo.get(pk)
    assert obj_get is not None
    assert obj_get.pk == new_obj.pk
    assert obj_get.float_field == new_obj.float_field
    assert obj_get.str_field == new_obj.str_field
    assert obj_get.date_field == new_obj.date_field
    
    obj_upd = custom_class(
        1.1, "2.1", datetime.now().isoformat(sep='\t', timespec='minutes'), pk)
    repo.update(obj_upd)
    assert repo.get(pk) == obj_upd
    
    repo.delete(pk)
    assert repo.get(pk) is None
    

def test_obj_adapter(repo, custom_class):
    obj = repo._obj_adapter(42, (4.2, "some_str", datetime.now().isoformat(sep='\t', timespec='minutes')))
    assert obj.pk == 42
    assert obj.float_field == 4.2
    assert obj.str_field == "some_str"
    assert obj.date_field == datetime.now().isoformat(sep='\t', timespec='minutes')


####################

def test_exception_add_with_pk(repo, custom_class):
    with pytest.raises(ValueError):
        repo.add(custom_class(pk=7))


def test_exception_add_cls_no_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_exception_update_unexistent(repo, custom_class):
    with pytest.raises(ValueError):
        repo.update(custom_class(str_field='unexistent'))


def test_exception_update_without_pk(repo, custom_class):
    with pytest.raises(ValueError):
        repo.update(custom_class(pk=0))


def test_get_unexistent(repo):
    assert repo.get(4242) is None


def test_exception_delete_unexistent(repo):
    with pytest.raises(ValueError):
        repo.delete(1337)


def test_get_all(repo, custom_class):
    obj_list = [custom_class(float_field=float(f)) for f in range(7)]
    for obj in obj_list:
        repo.add(obj)
    assert obj_list == repo.get_all()


def test_get_all_with_condition(repo, custom_class):
    obj_list = []
    for i in range(11):
        o = custom_class(float_field=float(i), str_field='tmp')
        repo.add(o)
        obj_list.append(o)
    assert obj_list == repo.get_all({'str_field': 'tmp'})
    assert obj_list[4] == repo.get_all({'float_field': 4.})[0]


def test_get_all_substr(repo, custom_class):
    obj_list = [custom_class(str_field=str(f)+'smth') for f in range(7)]
    for obj in obj_list:
        repo.add(obj)
    assert obj_list == repo.get_all_substr({'str_field' : 'smth'})
