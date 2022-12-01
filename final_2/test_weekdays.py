import pytest
import datetime
from weekdays import *


def test_validate_date():
    regex = datetime.datetime.strptime
    assert regex('2020-08-03', '%Y-%m-%d')
    try:
        assert regex('2020-08', '%Y-%m-%d')
        assert regex('2020/08/03', '%Y-%m-%d')
        assert regex('2020-13-32', '%Y-%m-%d')
    except ValueError: pass

def test_get_date_splitted():
    assert get_date_splitted('2022-10-27') == ['2022','10','27']
    assert get_date_splitted('2022-10-27a') == ['2022','10','27a']
    assert get_date_splitted('') == ['']

def test_get_weekday_num():
    assert get_weekday_num(2022,11,1) == 1
    assert get_weekday_num(2022,12,25) == 6

def test_get_weekday_name():
    assert get_weekday_name(0) == 'Monday'
    assert get_weekday_name(6) == 'Sunday'

def test_get_period_years():
    assert get_period_years(2022,11,1,2) == {2021 : '0', 2020: '6'}
    assert get_period_years(2022,12,25,5) == {2021 : '5', 2020: '4', 2019 : '2', 2018 : '1', 2017 : '0'}

def test_get_table():
    dictionary = {2021 : '5', 2020: '4', 2019 : '2', 2018 : '1', 2017 : '0'}
    assert get_table(dictionary) == \
        {'monday' : [2017], 'tuesday' : [2018], 'wednesday' : [2019], 'thursday' : [] ,'friday' : [2020], 'saturday' : [2021], 'sunday' : []}


pytest.main(["-v", "--tb=line", "-rN", __file__])
