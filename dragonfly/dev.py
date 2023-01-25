"""
------------------- TOOLS FOR DEVELOPMENT -------------------
"""


# IMPORT MODULE
import os
import ast
from collections import namedtuple
from typing import List

from .utils import ImmutableClass

from radon.visitors import ComplexityVisitor

import radon.complexity
import radon.metrics
import radon.raw

# NAMED TUPLE DEFINITION

ComplexityMetrics = namedtuple("CodeMetrics",
                               ["name", "complexity",
                                "complexityLetter", "is_method",
                                "class_name", "startLine"])

LineMetric = namedtuple("LineMetric",
                        ["nbLines", "nbLineSource",
                         "nbBlankLine", "nbCommentLines",
                         "nbMultiCommentLines"])

# CLASS MODULE ANALYSIS


class FileAnalysis(ImmutableClass):

    MAX_COMPLEXITY_LETTER = "A"
    MAX_MAINTENACE_LETTER = "A"
    MIN_COMMENT_RATION = 30  # percentage
    _LIST_LETTERS = ["A", "B", "C", "D", "E"]

    def __init__(self, filePath: str) -> None:
        """Create a FileAnalysis object based on a filePath

        Args:
            filePath (str): path of the file to analyze (absolute or relative)

        Raises:
            ValueError: if the file path is not a string or an existing file
        """
        # check if filepath is a existing file
        if not (os.path.isfile(filePath)):
            msg = f"{filePath} is not a valid path"
            raise ValueError(msg)
        elif not filePath.endswith(".py"):
            msg = f"The file {filePath} is not a Python file (*.py)"
            raise ValueError(msg)
        self.filePath = os.path.abspath(filePath)

    def __str__(self) -> str:
        """Overload the print method"""

        CI = self.complexity

        complexitymsg = [(f"\t\t - {item.name}: {item.complexityLetter}"
                          f" ({item.complexity})"
                          f" (class: {item.class_name})\n")
                         for item in CI]
        complexitymsg = "".join(complexitymsg)

        msg = (
            f"Code Metrics for {self.fileName}:\n"
            f"\t- Path: {self.fileFolder}\n"
            f"\t- Maintenability: {self.maintenanceLetter} ({self.maintenanceIndex})\n"  # noqa: E501
            f"\t- Comment Percentage: {self.commentsPercentage} %\n"
            f"\t- Complexity:\n"
        )

        return msg+complexitymsg

    @property
    def complexity(self) -> List[namedtuple]:

        # read file :
        data = self._readFile()

        # calculate all metrics for all functions and methods
        # in the python file
        evaluation = ComplexityVisitor.from_code(data)

        # initiate
        result = []

        # function
        result.extend(_collectInfo(evaluation.functions, self.filePath))

        # Class
        list_classes = evaluation.classes
        for classItem in list_classes:
            result.extend(_collectInfo(classItem.methods, self.filePath))

        # clean result of empty lists
        while [] in result:
            result.remove([])

        return result

    @property
    def fileName(self) -> str:
        """File name with its extension"""
        dir, fileName = os.path.split(self.filePath)
        return fileName

    @property
    def fileFolder(self):
        """path of the folder of the analyzed file"""
        dir, file = os.path.split(self.filePath)
        return dir

    @property
    def numberOfClasses(self):
        """Provide the number of Classes defintion in a file

        Returns:
            int: number of Classes
        """
        # read file
        data = self._readFile()

        tree = ast.parse(data)
        return sum(isinstance(exp, ast.ClassDef) for exp in tree.body)

    @property
    def numberOfFunctions(self):
        """Provide the number of Classes defintion in a file

        Returns:
            int: number of Classes
        """
        with open(self.filePath) as f:
            tree = ast.parse(f.read())
        return sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)

    @property
    def maintenanceIndex(self) -> float:
        """provide the maintenance index

        see : https://radon.readthedocs.io/en/latest/intro.html#maintainability-index # noqa: E501

        Returns:
            float: _description_
        """
        data = self._readFile()

        return radon.metrics.mi_visit(data, multi=True)

    @property
    def maintenanceLetter(self) -> str:
        """Provide de maintenance letter (eg. A= Good, E = Bad)

        Returns:
            str: maintenance letter (A to E)
        """
        return radon.metrics.mi_rank(self.maintenanceIndex)

    @property
    def lineMetrics(self) -> namedtuple:

        loc_metric = radon.raw.analyze(self._readFile())

        return LineMetric(
            nbLines=loc_metric.loc,
            nbLineSource=loc_metric.sloc,
            nbBlankLine=loc_metric.blank,
            nbCommentLines=loc_metric.comments,
            nbMultiCommentLines=loc_metric.multi,
            )

    @property
    def commentsPercentage(self) -> float:
        """Provide the percentage of comments

        Returns:
            float: percentage of comments line per effective lines
                    (blank lines are removed)
        """

        # get the line metrics
        metrics = self.lineMetrics

        # calculate the effective metrics
        effectiveLines = (metrics.nbCommentLines +
                          metrics.nbMultiCommentLines +
                          metrics.nbLineSource)
        commentsLines = (metrics.nbCommentLines + metrics.nbMultiCommentLines)

        return round(100 * (commentsLines / effectiveLines), 1)

    def _readFile(self):
        """PRIVATE FUNCTION - read the data

        Returns:
            str : all data of the Python file
        """
        with open(self.filePath, 'r') as file:
            data = file.read()
        return data

    def isValid(self,
                max_complexityLetter: str = MAX_COMPLEXITY_LETTER,
                max_maintenanceLetter: str = MAX_MAINTENACE_LETTER,
                min_commentPercentage: float = MIN_COMMENT_RATION) -> bool:
        """Check if a file is ok against code metrics

        Args:
            max_complexityLetter (str, optional): maximum complexity letter.
                Defaults to MAX_COMPLEXITY_LETTER ("A").
            max_maintenanceLetter (str, optional): maximum maintenance letter.
                Defaults to MAX_MAINTENACE_LETTER ("A").
            min_commentPercentage (float, optional): minimum ration of comment
                Defaults to MIN_COMMENT_RATION (30%).

        Returns:
            bool: code metrics assessment as boolean
        """

        # I/O MANAGEMENT

        assert isinstance(max_maintenanceLetter, str), "max_maintenanceLetter shall be a string"  # noqa: E501
        assert max_maintenanceLetter in self._LIST_LETTERS, f"Letter shall be part of {self._LIST_LETTERS}"  # noqa: E501

        assert isinstance(min_commentPercentage, (int, float)), "min_commentPercentage shall be a numeric"  # noqa: E501
        assert min_commentPercentage >= 0 and min_commentPercentage <= 100

        # Evaluate code metrics
        chk_maintenance = self.maintenanceLetter <= max_maintenanceLetter
        chk_commentPercentage = (self.commentsPercentage >=
                                 min_commentPercentage)
        chk_complexity = self.getInvalidItem(max_complexityLetter=max_complexityLetter) == []  # noqa: E501

        return chk_maintenance and chk_commentPercentage and chk_complexity

    def getInvalidItem(self,
                       max_complexityLetter: str = MAX_COMPLEXITY_LETTER) -> List[namedtuple]:  # noqa: E501
        """Provide the list of functions or methods with inappropriate
        complexity

        Args:
            max_complexityLetter (str, optional): maximum complexity letter
                Defaults to MAX_COMPLEXITY_LETTER ("A").

        Returns:
            List: List of namedtuple of the function with inappropriate
            complexity
        """

        # IO MANAGEMENT
        assert isinstance(max_complexityLetter, str), "max_maintenanceLetter shall be a string"  # noqa: E501
        assert max_complexityLetter in self._LIST_LETTERS, f"Letter shall be part of {self._LIST_LETTERS}"  # noqa: E501

        # calculate complexity index
        CI = self.complexity

        invalidElement = [item for item in CI
                          if item.complexityLetter > max_complexityLetter]
        return invalidElement


# FOLDER ANALYSIS


class FolderAnalysis(ImmutableClass):

    def __init__(self, folderPath: str) -> None:
        if not (os.path.isdir(folderPath)):
            msg = f"{folderPath} is not a valid folder path"
            raise ValueError(msg)
        self.folderPath = os.path.abspath(folderPath)
        pass

    @property
    def listFiles(self) -> List[str]:
        """List all python files in directory including subdirectories

        Returns:
            List[str]: list of all files with absolute path
        """

        pythonFiles = [os.path.join(root, name)
                       for root, dirs, files in os.walk(self.folderPath)
                       for name in files
                       if (name.endswith((".py")) and  # only python files
                           name != "__init__.py" and  # remove __init__
                           not ("test" in name.lower())  # remove test file
                           )]
        return pythonFiles

    @property
    def complexity(self) -> List:

        complexityList = []

        for filePath in self.listFiles:
            newList = [filePath, FileAnalysis(filePath).complexity]
            complexityList.append(newList)
        return complexityList

    @property
    def maintenanceLetter(self):
        res = [[filePath, FileAnalysis(filePath).maintenanceLetter]
               for filePath in self.listFiles]
        return res

    @property
    def commentPercentage(self):
        res = [[filePath, FileAnalysis(filePath).commentsPercentage]
               for filePath in self.listFiles]
        return res

# -------------------- UTILS -------------------------


def _collectInfo(items, pythonFile):
    """PRIVATE FUNCTION - use to collect Cycloamtic complexity

    Args:
        items (list): list of complexity result
        pythonFile (string): path of the file

    Returns:
        list : list of namedtuples
    """
    info = []
    for item in items:
        info.append(ComplexityMetrics(
                    name=item.name,
                    complexity=item.complexity,
                    complexityLetter=radon.complexity.cc_rank(item.complexity),
                    is_method=item.is_method,
                    class_name=item.classname,
                    startLine=item.lineno))
    return info
