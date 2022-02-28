How to test
------------------------------

Minimally needed:
```
pip install -e ./
cd tests/unit
python Test.py
```

Recommended:
```
pip install --user pytest
pip install -e ./
cd tests
# Test all
pytest ./
# Unit test only
pytest ./unit
# Integration test only
pytest ./integration
```
