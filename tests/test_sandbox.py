# """test_class_parametrization.py"""
# import pytest

# @pytest.mark.parametrize(
#     ("param1", "param2"),
#     [
#         ("a", "b"),
#         ("c", "d"),
#     ],
# )
# class TestGroup:
#     """A class with common parameters, `param1` and `param2`."""
    
#     @pytest.fixture
#     def my_filepath(self, tmpdir):
#         print(tmpdir)
#         return tmpdir.mkdir("sub").join("testCurrentTicketCount.txt")

#     @pytest.fixture
#     def fixt(self,param1,my_filepath) -> int:
#         """This fixture will only be available within the scope of TestGroup"""
#         print("fixture",param1)
#         return 123

#     def test_one(self,fixt: int, param1: str, param2: str) -> None:
#         print("\ntest_one", param1, param2, fixt)

#     def test_two(self, param1: str, param2: str,fixt) -> None:
#         print("\ntest_two", param1, param2)
        
# class Testgroup2:
#     def test_one2(self):
#         print("test 2")
        
# class Testgroup6:
#     def test_one2(self):
#         print("test 2")
#         assert False