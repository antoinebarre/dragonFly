from abc import ABC, abstractmethod, abstractproperty
from typing import List, Any
import os
from collections import namedtuple
import textwrap

from radon.visitors import ComplexityVisitor
import radon.complexity
import radon.metrics
import radon.raw
import hashlib
import ast
import datetime
from rich.console import Console

from prettytable import PrettyTable


class CodeMetric(ABC):
    """ABSTRACT METHOD FOR CODE METRICS"""
    _VALID_LETTERS = ["A", "B", "C", "D", "E"]
    _VALID_RANGE = {"min": 0, "max": 100}

    def __init__(self, filePath: str) -> None:
        # check if filepath is a existing file
        if not (os.path.isfile(filePath)):
            msg = f"{filePath} is not a valid path"
            raise ValueError(msg)
        elif not filePath.endswith(".py"):
            msg = f"The file {filePath} is not a Python file (*.py)"
            raise ValueError(msg)
        self.filePath = os.path.abspath(filePath)

    @property
    def data(self) -> str:
        """read the data of the Python file

        Returns:
            str : all data of the Python file
        """
        with open(self.filePath, 'r') as file:
            data = file.read()
        return data

    @abstractproperty
    def title(self) -> str:
        pass

    @abstractproperty
    def definition(self) -> str:
        pass

    @abstractproperty
    def criteria_value(self) -> Any:
        pass

    @abstractmethod
    def isValid(self) -> bool:
        pass

    @abstractmethod
    def toString(self) -> str:
        pass

    @abstractmethod
    def calculateCriteria(self) -> Any:
        pass

    def exportCriteria(self) -> str:
        """Export the criteria information as a text"""
        msg = self.definition + f" [Value: {self.criteria_value}]"

        return '\n'.join(textwrap.wrap(msg, 40))

    def setCriteria(self,criteria) -> None:
        """ Change criteria Value"""
        self.criteria_value = criteria
        return self


    @staticmethod
    def _verifyLetter(item2check, validList):
        if not isinstance(item2check, (str)):
            raise TypeError("the Value shall be a string")

        if item2check not in validList:
            msg = ("The Letter is not in the authorized list ",
                   f"({validList}) "
                   f"Current :{item2check}")
            raise ValueError(msg)
        return item2check

    @staticmethod
    def _verifyRange(item2check, validRange) -> None:
        """ PRIVATE METHOD used to check if an item is a
        float or int and in the appropriate range"""

        if not isinstance(item2check,
                          (int, float)):
            raise TypeError("the Value shall be an int or float")

        if (item2check < validRange['min'] or
           item2check > validRange['max']):
            msg = ("The value is not in the valid range "
                   f"ie. [{validRange['min']},{validRange['max']}]")
            raise ValueError(msg)

        return item2check


class CyclomaticComplexity(CodeMetric):
    """Implement the Cyclomatic Complexity assessment of one python file"""
    title = "Cyclomatic Complexity"
    definition = ("All functions, Class, methods and properties"
                  "implemented in the file shall have a maximum"
                  " cyclomatic complexity.")
    criteria_value = "B"

    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)

    def isValid(self) -> bool:
        """check if the file is valid against cyclomatic complexity

        Returns:
            bool: boolean that provide
             the valid status against cyclomatic complexity
        """

        # assess the criteria value
        criteria = self._verifyLetter(self.criteria_value,
                                      self._VALID_LETTERS)

        # get the result for all methods and functions
        res = self.calculateCriteria()

        invalidElement = [item for item in res
                          if (item.complexityLetter >
                              criteria)]
        return len(invalidElement) == 0

    def toString(self):

        # get the result for all methods and functions
        res = self.calculateCriteria()

        my_tableCI = PrettyTable()
        my_tableCI.field_names = ["Item Name", "Class",
                                  "Complexity Letter", "Line"]
        for item in res:
            my_tableCI.add_row([item.name, item.class_name, f"{item.complexityLetter} ({item.complexity})", item.startLine])  # noqa: E501

        return str(my_tableCI)

    def calculateCriteria(self) -> List[namedtuple]:
        # read file :
        data = self.data

        # calculate all metrics for all functions and methods
        # in the python file
        evaluation = ComplexityVisitor.from_code(data)

        # initiate
        result = []

        # function
        result.extend(self._collectInfo(evaluation.functions, self.filePath))

        # Class
        list_classes = evaluation.classes
        for classItem in list_classes:
            result.extend(self._collectInfo(classItem.methods, self.filePath))

        # clean result of empty lists
        while [] in result:
            result.remove([])

        return result

    @staticmethod
    def _collectInfo(items, pythonFile):
        """PRIVATE FUNCTION - use to collect Cycloamtic complexity

        Args:
            items (list): list of complexity result
            pythonFile (string): path of the file

        Returns:
            list : list of namedtuples
        """

        ComplexityMetrics = namedtuple("CodeMetrics",
                                       [
                                        "name",
                                        "complexity",
                                        "complexityLetter",
                                        "is_method",
                                        "class_name",
                                        "startLine"
                                        ])

        info = []
        for item in items:
            info.append(ComplexityMetrics(
                        name=item.name,
                        complexity=item.complexity,
                        complexityLetter=radon.complexity.cc_rank(item.complexity),  # noqa: E501
                        is_method=item.is_method,
                        class_name=item.classname,
                        startLine=item.lineno))
        return info


class CommentRatio(CodeMetric):
    title = "Comment Ratio"
    definition = ("The content of the Python file shall have a minimum"
                  " percentage of comments excluding the blank lines")
    criteria_value = 30

    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)

    def calculateCriteria(self) -> float:
        "Calculate the Comment percentage of the file as a float"

        # get data
        data = self.data

        # get the analysis of the data
        loc_metric = radon.raw.analyze(data)

        # calculate the effective metrics
        effectiveLines = (loc_metric.comments +
                          loc_metric.multi +
                          loc_metric.sloc)
        commentsLines = (loc_metric.comments + loc_metric.multi)

        return round(100 * (commentsLines / effectiveLines), 1)

    def isValid(self) -> bool:
        """check if the file is valid against comment ratio

        Returns:
            bool: boolean that provide
             the valid status against cyclomatic complexity
        """

        # assess the criteria value
        criteria = self._verifyRange(self.criteria_value,
                                     self._VALID_RANGE)

        # get the result for all methods and functions
        res = self.calculateCriteria()

        return res >= criteria

    def toString(self):
        return f"Comment Ratio : {self.calculateCriteria()} %"


class Maintenability(CodeMetric):
    """ 
    Maintenability Critéria

    see : https://radon.readthedocs.io/en/latest/intro.html#maintainability-index # noqa: E501
    """
    title = "Maintenability"
    definition = ("The content of the Python file shall have a maximum"
                  " level of Maintenability")
    criteria_value = "A"

    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)

    def calculateCriteria(self) -> float:
        "Calculate maintenability as Letter"
        # get data
        data = self.data

        # get the analysis of the data
        maintenanceIndex = round(radon.metrics.mi_visit(data, multi=True), 1)

        return radon.metrics.mi_rank(maintenanceIndex)

    def isValid(self) -> bool:
        """check if the file is valid against comment ratio

        Returns:
            bool: boolean that provide
             the valid status against cyclomatic complexity
        """

        # assess the criteria value
        criteria = self._verifyLetter(self.criteria_value,
                                      self._VALID_LETTERS)

        # get the result for all methods and functions
        res = self.calculateCriteria()

        return res <= criteria

    def toString(self):
        return f"Maintenance Letter : {self.calculateCriteria()}"


class FileAnalysis():

    # ---------- CREATOR -------------

    def __init__(self, filePath: str,
                 maxComplexityLetter: str = "B",
                 maxMaintenanceLetter: str = "A",
                 minCommentRatio: float = 30,
                 ) -> None:
        """_summary_

        Args:
            filePath (str): file path (absolute or relative)
            maxComplexityLetter (str, optional): maximum Complexity Letter
                . Defaults to "B".
            maxMaintenanceLetter (str, optional): maximum Maintenace Letter
                . Defaults to "A".
            minCommentRatio (float, optional): minimum comment ratio
                . Defaults to 30.
        """

        # create data
        self._data = [
            Maintenability(filePath).setCriteria(maxMaintenanceLetter),
            CommentRatio(filePath).setCriteria(minCommentRatio),
            CyclomaticComplexity(filePath).setCriteria(maxComplexityLetter),
         ]

        # set file path (already checked)
        self.filepath = self.filePath = os.path.abspath(filePath)

        pass

# -------------------- FILE PROPERTIES ----------------------------

    @property
    def fileName(self) -> str:
        """File name with its extension"""
        _, fileName = os.path.split(self.filePath)
        return fileName

    @property
    def fileFolder(self):
        """path of the folder of the analyzed file"""
        dir, _ = os.path.split(self.filePath)
        return dir

    @property
    def checksum_MD5(self) -> str:
        """ Provide the checksum MD5 of the Python File"""
        data = self._readFile()

        return hashlib.md5(data.encode('utf-8')).hexdigest()

    @property
    def sha256(self) -> str:
        """ Provide the sha256 of the Python File"""
        data = self._readFile()

        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @property
    def lastModificationDate(self) -> datetime.datetime:
        """Provide the last modification date as datetime"""
        timestamp = os.path.getmtime(self.filePath)
        # convert timestamp into DateTime object
        datestamp = datetime.datetime.fromtimestamp(timestamp)

        return datestamp

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

    # -------------------- ANALYSIS --------------------

    def getValidationStatus(self) -> dict:

        # get data
        datas = self._data

        # initiate the output
        output = {}

        for data in datas:
            output[data.title] = data.isValid()

        return output

    def exportToString(self) -> str:

        # get data
        datas = self._data

        # initiate the outputs
        msgMetrics = ""
        msgCriteria = ""

        for data in datas:
            msgCriteria += "#" + data.exportCriteria() + "\n\n"
            msgMetrics += (">>> " + data.title +
                           "\n" + data.toString() + "\n\n")

        msg = (
            "File Description :\n".upper() +
            f"\t- File:              {self.fileName}\n" +
            f"\t- Path:              {self.fileFolder}\n" +
            f"\t- Last Modifcation:  {self.lastModificationDate}\n" +
            f"\t- CheckSum MD5:      {self.checksum_MD5}\n" +
            f"\t- SHA256:            {self.sha256}\n" +
            "\n" +
            "File Validation Criterias:\n".upper() +
            f"{msgCriteria}"
            "\n" +
            "File Metrics :\n".upper() +
            f"{msgMetrics}"
        )

        return msg

    # ---------------------- UTILS -----------------------

    def _readFile(self):
        """PRIVATE FUNCTION - read the data

        Returns:
            str : all data of the Python file
        """
        with open(self.filePath, 'r') as file:
            data = file.read()
        return data

c = FileAnalysis("dragonfly/dev.py",minCommentRatio=10)
print(c.getValidationStatus())
print(c.exportToString())