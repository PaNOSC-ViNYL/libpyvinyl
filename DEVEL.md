# Contributing

## How to test

Minimally needed:
```
pip install -e ./
cd tests/unit
python Test.py
```

Recommended:

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

## Git workflow
1. Branch from the current `master` branch
2. Develop into the newly created branch
3. Create appropriate unit tests in [tests/unit/](https://github.com/PaNOSC-ViNYL/libpyvinyl/tree/master/tests/unit)
4. Test current development as indicated in [Testing](https://github.com/PaNOSC-ViNYL/libpyvinyl#testing).
5. `git rebase -i master` w.r.t. current master to include the latest updates and squashing commits to a minimum. See also [here](https://opensource.com/article/20/4/git-rebase-i).
6. Push your `BRANCH` to the upstream repo: `git push -f upstream BRANCH`.
7. Create a pull request (PR) to the `master` branch on the GitHub page.
8. PR should be reviewed and approved and be passing all CI tests.
9. If passing all tests, Choose `Rebase and merge` to merge the PR with no further squashing.
