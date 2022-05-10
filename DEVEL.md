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



## Testing

A simple `pytest` command will run the unittests and integration tests.
```
pytest ./
```

You should see a test report similar to this:

```
=============================================================== test session starts ================================================================
platform linux -- Python 3.8.10, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/juncheng/Projects/libpyvinyl
collected 100 items

integration/plusminus/tests/test_ArrayCalculators.py .                                                                                       [  1%]
integration/plusminus/tests/test_Instrument.py .                                                                                             [  2%]
integration/plusminus/tests/test_NumberCalculators.py ...                                                                                    [  5%]
integration/plusminus/tests/test_NumberData.py ...........                                                                                   [ 16%]
unit/test_BaseCalculator.py ..........                                                                                                       [ 26%]
unit/test_BaseData.py ...........................                                                                                            [ 53%]
unit/test_Instrument.py .......                                                                                                              [ 60%]
unit/test_Parameters.py ........................................                                                                             [100%]

=============================================================== 100 passed in 0.56s ================================================================
```

You can also run unittests only:

```
pytest tests/unit
```

Or to run integration tests only:

```
pytest tests/integration
```
