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
                                "class_name"])

LineMetric = namedtuple("LineMetric",
                        ["nbLines", "nbLineSource",
                         "nbBlankLine", "nbCommentLines",
                         "nbMultiCommentLines"])

# CLASS MODULE ANALYSIS


class FileAnalysis(ImmutableClass):

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
        result.append(_collectInfo(evaluation.functions, self.filePath))

        # Class
        list_classes = evaluation.classes
        for classItem in list_classes:
            result.append(_collectInfo(classItem.methods, self.filePath))

        # clean result of empty lists
        while [] in result:
            result.remove([])

        return result

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
                    class_name=item.classname))
    return info
