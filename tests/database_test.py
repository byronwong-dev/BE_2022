from exceptions import NoAccountFound
from services.database import Database
from datetime import datetime, timedelta
import pytest

def test_database_can_insert_deposit():

    Database.deposit('abc123', 100.25)

    assert next(iter(Database.store['deposits']))['amount'] == 100.25

def test_database_can_retrieve_deposit_data():
    Database.store['deposits'] = [
        {
            'reference_code': 'abc123',
            'amount': 1030.20,
            'datetime': f"{datetime.now()}"
        },
        {
            'reference_code': 'abc123',
            'amount': 100.50,
            'datetime': f"{datetime.now() + timedelta(seconds=10)}"
        },

    ]

    allDeposits = Database.retrieveAll('abc123')
    assert len(allDeposits) == 2
    assert next(iter(allDeposits))['amount'] in [1030.20, 100.50]

def test_exception_raise_when_not_deposit_data():
    
    Database.store['deposits'] = [
        {
            'reference_code': 'abc123',
            'amount': 1030.20,
            'datetime': f"{datetime.now()}"
        },
        {
            'reference_code': 'abc123',
            'amount': 100.50,
            'datetime': f"{datetime.now() + timedelta(seconds=10)}"
        },

    ]

    try:
        Database.retrieveAll('def456')
        pytest.fail('Failed to throw exception')
    except NoAccountFound:
        assert True
    except Exception:
        assert False
