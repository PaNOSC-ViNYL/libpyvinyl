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

Developement workflow
---------------------

 1. branch from current master
 #. develop into newly created branch
 #. create appropriate unit tests in tests/unit/
 #. test current developement as indicated in [How to test](#How to test)
 #. rebase w.r.t. current master to include latest updates
 #. create a pull request (PR)
 #. PR should be reviewed and approved and be passing all CI tests
 #. branch is further rebased w.r.t. current master to include latest changes and squashing commits to a minimum
	Features or logically splitted changes should be kept in separate commits.
	Rebased branch is forced pushed
 #. If passing all tests, the branch can be rebased and merged with no further squashing.

