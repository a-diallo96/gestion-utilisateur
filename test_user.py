from tinydb.storages import MemoryStorage
from user import User
import pytest
from tinydb import TinyDB, table

"""création d'une fixture pour pouvoir utiliser ces fonctions
 dans d'autre fonctions de test empecher le duplication"""

@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

@pytest.fixture
def user(setup_db):
    u = User(first_name="aissatou", last_name="diallo",
             phone_number="0642865423",
             address="75 avenue de saige, 33600 Pessac")
    u.save()
    return u

def test_full_name(user):
    assert user.full_name == "aissatou diallo"


def test__check_phone_number(setup_db):
    u_good = User(first_name="aisu", last_name="diao",
             phone_number="0754980934",
             address="75 avenue de saige, 33600 Pessac")

    u_bad = User(first_name="abdoulaye", last_name="dbo",
             phone_number="aaaa",
             address="75 avenue de saige, 33600 Pessac")
    with pytest.raises(ValueError) as err:
        u_bad._check_phone_number()
    assert  "invalid" in str(err.value)
    u_good.save(validate_data=True)
    u_good.exists() is True

def test__check_names_empty(setup_db):
    user_bad = User(first_name="" , last_name="diallo",phone_number="1234567890",address="2rue des marechal 42200")
    with pytest.raises(ValueError) as err:
        user_bad._check_names()
    assert "le prenom et le nom de famille ne peuve,t pas être vide" in str(err.value)

def test__check_names_invalid_characters(setup_db):
    user_bad = User(first_name="aicha&é*$ù(3#)", last_name="#***$&{}",phone_number="1234567890",address="2rue des marechal 42200")
    with pytest.raises(ValueError) as err:
        user_bad._check_names()
    assert "nom invalide" in str(err.value)


def test_exists(user):
    assert user.exists() is True


def test_delete():
    user_test = User(first_name="aissatou", last_name="diallo",
                phone_number="0642865423",
                address="75 avenue de saige, 33600 Pessac")
    user_test.save()
    first = user_test.delete()
    second = user_test.delete()
    assert len(first)>0
    assert isinstance(first,list)
    assert len(second)==0
    assert isinstance(second,list)


def test_save(setup_db):
    user_first = User(first_name="dicko", last_name="diallo",
                     phone_number="0642865409",
                     address="75 avenue de saige, 33600 Pessac")

    user_second = User(first_name="dicko", last_name="diallo",
                     phone_number="0642865409",
                     address="75 avenue de saige, 33600 Pessac")
    first = user_first.save()
    second = user_second.save()
    assert isinstance(first,int)
    assert  isinstance(second,int)
    assert (first !=-1)
    assert (second == -1)

def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert(user.db_instance["first_name"] == "aissatou")
    assert (user.db_instance["last_name"] == "diallo")
    assert (user.db_instance["phone_number"] == "0642865423")
    assert (user.db_instance["address"] == "75 avenue de saige, 33600 Pessac")