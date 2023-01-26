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

from prettytable import PrettyTable


# NAMED TUPLE DEFINITION

ComplexityMetrics = namedtuple("CodeMetrics",
                               ["name", "complexity",
                                "complexityLetter", "is_method",
                                "class_name", "startLine"])

LineMetric = namedtuple("LineMetric",
                        ["nbLines", "nbLineSource",
                         "nbBlankLine", "nbCommentLines",
                         "nbMultiCommentLines"])

FolderResult = namedtuple("FolderResult",
                          ["filePath", "nbLines",
                           "commentPercentage", "maintenanceLetter",
                           "complexity_Violations_nb", "complexity",
                           "complexity_Violations"])


# -------------------------------------------------------------------
#                          CLASS CODE METRICS
# -------------------------------------------------------------------


class CodeMetrics():
    _MAX_COMPLEXITY_LETTER = "A"
    _MAX_MAINTENANCE_LETTER = "A"
    _MIN_COMMENT_RATIO = 30 
    _VALID_LETTERS = ["A", "B", "C", "D", "E"]
    _VALID_RANGE = {"min": 0, "max": 100}

    def chk_complexity(self, value2test):
        # Valid IO
        CodeMetrics._verifyLetter(value2test, self._VALID_LETTERS)
        # assess
        return value2test <= self._MAX_COMPLEXITY_LETTER

    def chk_maintenance(self, value2test):
        # Valid IO
        CodeMetrics._verifyLetter(value2test, self._VALID_LETTERS)
        # assess
        return value2test <= self._MAX_MAINTENANCE_LETTER

    def chk_comments(self, value2test):
        # Valid IO
        CodeMetrics._verifyRange(value2test, self._VALID_RANGE)
        # assess
        return value2test >= self._MIN_COMMENT_RATIO

    @staticmethod
    def _verifyLetter(item2check, validList):
        assert isinstance(item2check, (str)), "the Value shall be a string"
        if item2check not in validList:
            msg = ("The Letter is not in the authorized list ",
                   f"({validList}) "
                   f"Current :{item2check}")
            raise ValueError(msg)
        pass

    @staticmethod
    def _verifyRange(item2check, validRange) -> None:

        assert isinstance(item2check, 
                          (int, float)), "the Value shall be an int"

        if (item2check < validRange['min'] or
           item2check > validRange['max']):
            msg = ("The value is not in the valid range "
                   f"ie. [{validRange['min']},{validRange['max']}]")
            raise ValueError(msg)

        pass

# -------------------------------------------------------------------
#                          CLASS FILE ANALYSIS
# -------------------------------------------------------------------


class FileAnalysis(CodeMetrics):

    # ---------- CREATOR -------------

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

        # initalisation with super class
        super().__init__()

    def __str__(self) -> str:
        """Overload the print method"""

        CI = self.complexity

        my_table = PrettyTable()

        my_table.field_names = ["Item Name", "Class",
                                "Complexity Letter", "Line"]

        for item in CI:
            my_table.add_row([item.name, item.class_name, f"{item.complexityLetter} ({item.complexity})", item.startLine])  # noqa: E501

        msg = (
            f"Code Metrics for {self.fileName}:\n"
            f"\t- Path: {self.fileFolder}\n"
            f"\t- Maintenability: {self.maintenanceLetter} ({self.maintenanceIndex})\n"  # noqa: E501
            f"\t- Comment Percentage: {self.commentsPercentage} %\n"
            f"\t- Complexity:\n"
        )

        return msg + str(my_table)

    @property
    def complexity(self) -> List[namedtuple]:
        """Complexity as namedtuple with associated information"""

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

        return round(radon.metrics.mi_visit(data, multi=True),1)

    @property
    def maintenanceLetter(self) -> str:
        """Provide de maintenance letter (eg. A= Good, E = Bad)

        Returns:
            str: maintenance letter (A to E)
        """
        return radon.metrics.mi_rank(self.maintenanceIndex)

    @property
    def lineMetrics(self) -> namedtuple:
        """Line of code metric including comment multiline
         comment line, blanck line and source code line"""

        loc_metric = radon.raw.analyze(self._readFile())

        return LineMetric(
            nbLines=loc_metric.loc,
            nbLineSource=loc_metric.sloc,
            nbBlankLine=loc_metric.blank,
            nbCommentLines=loc_metric.comments,
            nbMultiCommentLines=loc_metric.multi,
            )

    @property
    def nbLines(self) -> int:
        """number of lines in the file

        Returns:
            int: number of lines
        """

        # get the line metrics
        metrics = self.lineMetrics

        return metrics.nbLines

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

    def isValid(self) -> bool:
        """Check if a file is ok against code metrics

        Args:

        Returns:
            bool: code metrics assessment as boolean
        """

        # Evaluate code metrics
        chk_maintenance = self.chk_maintenance(self.maintenanceLetter)  # noqa: E501
        chk_commentPercentage = self.chk_comments(self.commentsPercentage)  # noqa: E501
        chk_complexity = self.getInvalidItems() == []

        return chk_maintenance and chk_commentPercentage and chk_complexity

    def getInvalidItems(self,
                        ) -> List[namedtuple]:  # noqa: E501
        """Provide the list of functions or methods with inappropriate
        complexity

        Args:

        Returns:
            List: List of namedtuple of the function with inappropriate
            complexity
        """

        # calculate complexity index
        CI = self.complexity

        invalidElement = [item for item in CI
                          if not self.chk_complexity(item.complexityLetter)]   # noqa: E501
        return invalidElement

    def getNumberInvalidItems(self,
                              ) -> int:
        """Provide the number of Invalid Items

        Returns:
            int: _description_
        """
        return len(self.getInvalidItems())

    def getListInvalidItems(self,
                            ) -> List[str]:
        """Provide the list of Invalid items (functions and Class method)
        that violate the complexity rules

        Args:

        Returns:
            List[str]: list of Items a list of string with line number
        """

        res = []
        for item in self.getInvalidItems():
            if item.is_method:
                res.append(item.class_name +
                           "." +
                           item.name +
                           f" (L{item.startLine})" +
                           f" - {item.complexityLetter} ({item.complexity})")
            else:
                res.append(item.name +
                           f" (L{item.startLine})" +
                           f" - {item.complexityLetter} ({item.complexity})")
        return res


# -------------------------------------------------------------------
#                       FOLDER ANALYSIS
# -------------------------------------------------------------------


class FolderAnalysis(CodeMetrics):
    def __init__(self, folderPath: str) -> None:
        """create a Folder Analysis object

        Args:
            folderPath (str): folder path (absolute or relative)
        """
        if not (os.path.isdir(folderPath)):
            msg = f"{folderPath} is not a valid folder path"
            raise ValueError(msg)
        self.folderPath = os.path.abspath(folderPath)

        # initalisation with super class
        super(self).__init__()

    def __str__(self) -> str:

        msg = (
            "CODE METRICS ANALYSIS for "
            f"{self.folderPath}\n"
        )

        status = self.getResults()

        my_table = PrettyTable()

        my_table.field_names = ["File Name", "Number of Lines", "Comment %",
                                "Maintenance", "Complexity Violation"]

        for item in status:
            my_table.add_row([item.filePath,
                              item.nbLines,
                              item.commentPercentage,
                              item.maintenanceLetter,
                              item.complexity_Violations_nb])

        return msg+str(my_table)

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
        """List of all function and method of the file with the complexity
        information"""

        complexityList = []

        for filePath in self.listFiles:
            # todo add parameters
            newList = [filePath, FileAnalysis(filePath).complexity]
            complexityList.append(newList)
        return complexityList

    @property
    def maintenanceLetter(self) -> List:
        """Maintenance Letter of all Python files

        Returns:
            List: list of all filePath with the maintenance Letter
        """
        res = [[filePath, FileAnalysis(filePath).maintenanceLetter]
               for filePath in self.listFiles]
        return res

    @property
    def commentPercentage(self):
        """Comment Percentage for all Python file in the directorie
        (including subdirectories)
        """
        res = [[filePath, FileAnalysis(filePath).commentsPercentage]
               for filePath in self.listFiles]
        return res

    def getResults(self,
                   ) -> List:
        """Provide the list of code metrics for all analyzed python files

        Args:

        Returns:
            List: list of namedtuple
        """

        list_results = []

        for filePath in self.listFiles:
            newRes = FolderResult(filePath=os.path.relpath(filePath,
                                                           self.folderPath),
                                  nbLines=FileAnalysis(filePath).nbLines,
                                  commentPercentage=FileAnalysis(filePath).commentsPercentage,  # noqa: E501
                                  maintenanceLetter=FileAnalysis(filePath).maintenanceLetter,  # noqa: E501
                                  complexity_Violations_nb=FileAnalysis(filePath).getNumberInvalidItems(),  # noqa: E501
                                  complexity_Violations=FileAnalysis(filePath).getListInvalidItems(),  # noqa: E501
                                  complexity=FileAnalysis(filePath).complexity
                                  )
            list_results.append(newRes)

        # res = [[os.path.relpath(filePath, self.folderPath),
        #         FileAnalysis(filePath).commentsPercentage,
        #         FileAnalysis(filePath).maintenanceLetter,
        #         FileAnalysis(filePath).getListInvalidItems(max_complexityLetter)  # noqa: E501
        #         ]
        #        for filePath in self.listFiles]

        return list_results

    def isValid(self,
                ) -> bool:
        """Check if all Python files in the path (including subdirectories)
        are valid against code metrics

        Args:

        Returns:
            bool: boolean Ture if OK false if not valid
        """

        res = all([FileAnalysis(filePath).isValid()
                   for filePath in self.listFiles])
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
