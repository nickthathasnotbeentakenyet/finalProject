from FinalProject import *
import pytest

def test_get_user_answer():
    assert get_user_answer('Y') == True
    assert get_user_answer('yEs') == True
    assert get_user_answer('yes') == True
    assert get_user_answer('') == True
    assert get_user_answer("no") == False
    assert get_user_answer("765677skdjhsmnshh09-sdfsd") == False

def test_count_files():
    assert count_files(['one','two','three']) == 3
    assert count_files([]) == 0
    assert count_files(['','\n']) == 2

pytest.main(["-v", "--tb=line", "-rN", __file__])