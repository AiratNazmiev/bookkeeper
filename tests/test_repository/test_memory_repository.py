import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.repository_factory import repository_factory


@pytest.fixture
def custom_class():
    class Custom():
        pk = 0

    return Custom


@pytest.fixture
def repo():
    return MemoryRepository()

# TODO: некоторые тесты могут быть общимим для обеих БД,
# см. @pytest.mark.parametrize


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for _ in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
    assert repo.get_all({'test': 'test'}) == objects


def test_get_all_substr(repo, custom_class):
    obj_list = [custom_class() for _ in range(7)]
    for i, obj in enumerate(obj_list):
        obj.str_field = str(i)+'smth'
        repo.add(obj)
    assert obj_list == repo.get_all_substr({'str_field': 'smth'})


def test_factory(custom_class):
    repo_factory = repository_factory()
    repo = repo_factory(custom_class)

    test_crud(repo, custom_class)
