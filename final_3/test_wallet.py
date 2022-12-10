from wallet import *
import os
import pytest


def test_check_create():
    assert check_create('budget.json') == os.getcwd() + '\\' + 'budget.json'
    
    f_name = 'changed_name.changed_extension'
    assert check_create(f_name) == os.getcwd() + '\\' + f_name
    # removing newly created file
    f = os.getcwd() + '\\' + f_name
    os.remove(f)


def test_add_flow():
    date_stamp = str(datetime.now())
    assert add_flow("test_purpose", 25.50) == {"test_purpose":[25.50,date_stamp]}
    assert add_flow("", 0) == {"":[0,date_stamp]}



pytest.main(["--tb=line", "-v", "-rN", __file__ ])