import pytest
from calnd import DateConvert

dateObj = DateConvert(date="01/01/2021")


# def test_datein():
#     assert dateObj.datein() == "01/01/2021"

def test_assignDate():
    assert dateObj.assignDate() == "01 January, 2021"

def test_getVar():
    assert dateObj.getVar("day") == "01"
    assert dateObj.getVar("month") == "January"
    assert dateObj.getVar("year") == "2021"
    assert dateObj.getVar("date") == ["01", "01", "2021"]

def test_setVar():
    dateObj.setVar("day", "02")
    assert dateObj.getVar("day") == "02"
    dateObj.setVar("month", "02")
    assert dateObj.getVar("month") == "02"
    dateObj.setVar("year", "2022")
    assert dateObj.getVar("year") == "2022"
    dateObj.setVar("date", ["02", "02", "2022"])
    assert dateObj.getVar("date") == ["02", "02", "2022"]

pytest.main(["-v", "-s", "--tb=line", "-rN", r"C:\Coding\Python\calender_test.py"])