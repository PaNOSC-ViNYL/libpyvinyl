#!/usr/bin/env python
"""Tests for `plusminus.NumberCalculators` package."""

import pytest
import h5py
from plusminus.NumberData import NumberData, TXTFormat, H5Format


def test_construct_NumberData():
    """Test the construction of NumberData"""
    my_data = NumberData.from_dict({"number": 1}, "input1")


def test_list_formats():
    """Test the construction of NumberData"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    my_data.list_formats()


def test_write_read_txt(tmpdir):
    """Test writing to a txt file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    my_data.write(file_name, TXTFormat)
    with open(file_name, "r") as f:
        assert float(f.read()) == 1
    read_data = NumberData.from_file(file_name, TXTFormat, "read_data")
    assert read_data.get_data()["number"] == 1


def test_write_read_h5(tmpdir):
    """Test writing to a h5 file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.h5")
    my_data.write(file_name, H5Format)
    with h5py.File(file_name, "r") as h5:
        assert h5["number"][()] == 1
    read_data = NumberData.from_file(file_name, H5Format, "read_data")
    assert read_data.get_data()["number"] == 1


def test_read_txt_write_h5(tmpdir):
    """Test read a txt file and write to a h5 file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    my_data.write(file_name, TXTFormat)
    read_data = NumberData.from_file(file_name, TXTFormat, "read_data")
    file_name = str(tmpdir / "test.h5")
    read_data.write(file_name, H5Format)
    with h5py.File(file_name, "r") as h5:
        assert h5["number"][()] == 1


def test_txt_file_write_h5(tmpdir):
    """Test write a txt file and write to a h5 file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    read_data = my_data.write(file_name, TXTFormat, "read_data")
    file_name = str(tmpdir / "test.h5")
    read_data.write(file_name, H5Format)
    with h5py.File(file_name, "r") as h5:
        assert h5["number"][()] == 1


def test_set_dict(tmpdir):
    """Test setting a dict mapping"""
    my_data = NumberData("input1")
    my_data.set_dict({"number": 1})
    file_name = str(tmpdir / "test.txt")
    my_data.write(file_name, TXTFormat)


def test_set_file_(tmpdir):
    """Test setting a file mapping"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    my_data.write(file_name, TXTFormat)
    new_data = NumberData("new_data")
    new_data.set_file(file_name, TXTFormat)
    assert new_data.get_data()["number"] == 1


def test_set_file_report_double_setting(tmpdir):
    """Test write a txt file and write to a h5 file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    my_data.write(file_name, TXTFormat)
    with pytest.raises(RuntimeError):
        my_data.set_file(file_name, TXTFormat)


def test_return_object_without_key(tmpdir):
    """Test write a txt file and write to a h5 file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    new_data = my_data.write(file_name, TXTFormat)
    assert new_data.key == "input1_to_TXTFormat"


def test_return_object_with_key(tmpdir):
    """Test write a txt file and write to a h5 file"""
    my_data = NumberData.from_dict({"number": 1}, "input1")
    file_name = str(tmpdir / "test.txt")
    key = "test"
    new_data = my_data.write(file_name, TXTFormat, key)
    assert new_data.key == key
