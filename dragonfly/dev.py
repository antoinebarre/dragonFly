"""
######################################################################
                        DEVELOPMENT TOOLS
######################################################################
"""

# ----------------- Modules Import -----------------

from abc import ABC, abstractmethod
from typing import List, Any
import os
from collections import namedtuple
import hashlib
import ast
import datetime
import platform

from radon.visitors import ComplexityVisitor
import radon.complexity
import radon.metrics
import radon.raw
from rich.console import Console
from rich.style import Style
from rich.table import Table
from prettytable import PrettyTable

from .utils import ImmutableClass
from .utils import __readASCIIFile as readASCIIFile
from .constant import LINE_SIZE
from .utils import __validateFolder as validateFolder
from .utils import __validateFile as validateFile
from .utils import __validateFileExtension as validateFileExtension


# ------------------- LINTER OPTIONS ------------------
# pylint: disable=invalid-name

# ----------------- GLOBAL NAMEDTUPLE -----------------
_ListError = namedtuple("_ListError", (
    "criteria_title",
    "criteria_value",
    "detected_errors"
))

_ListResults = namedtuple("_ListResults", (
    "criteria_title",
    "criteria_value",
    "results"
))

__all__ = [
    "FileAnalysis",
    "FolderAnalysis",
]

# -------------------------------------------------------------------
#                       CRITERIA CLASSES
# -------------------------------------------------------------------


class CodeMetric(ABC):
    """ABSTRACT METHOD FOR CODE METRICS"""
    _VALID_LETTERS = ["A", "B", "C", "D", "E"]
    _VALID_RANGE = {"min": 0, "max": 100}

    def __init__(self, file_path: str) -> None:
        """Generic Creator for criteria

        Args:
            file_path (str): file path (absolute or relative)

        """
        # check if filepath is an existing file and check extension
        file_path = validateFile(file_path)
        file_path = validateFileExtension(file_path, ".py")
        self.filePath = file_path

    @property
    def data(self) -> str:
        """read the data of the Python file

        Returns:
            str : all data of the Python file
        """
        return readASCIIFile(self.filePath)

    @property
    @abstractmethod
    def title(self) -> str:
        """title of the code metric"""

    @property
    @abstractmethod
    def definition(self) -> str:
        """definition of the code metric"""

    @property
    @abstractmethod
    def criteria_value(self) -> Any:
        """criteria value of the code metric"""

    @abstractmethod
    def isValid(self) -> bool:
        """check if the file path is valid against the criteria"""

    @abstractmethod
    def toString(self) -> str:
        """export to string the result of the assessment"""

    @abstractmethod
    def calculateCriteria(self) -> Any:
        """calculate if the criteria is passed or failled"""

    @abstractmethod
    def exportErrors(self) -> _ListError:
        """export the error message"""

    @abstractmethod
    def exportCriteria(self) -> _ListResults:
        """export the criteria message"""

    def setCriteria(self, criteria) -> None:
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

        invalidElements = [item for item in res
                           if not (self._isValidCommplexity(
                                    item.complexityLetter,
                                    criteria))
                           ]
        return len(invalidElements) == 0

    @staticmethod
    def _isValidCommplexity(complexityValue: str,
                            criteria: str) -> bool:
        """PRIVATE METHOD - Compare two letters for complexity

        Args:
            complexityValue (str): value to assess
            criteria (str): complexity obkective

        Returns:
            bool: _description_
        """

        return complexityValue <= criteria

    def toString(self) -> str:
        """Export the result of file analysis as an ascii string

        Returns:
            str: file analysis result
        """

        # get the result for all methods and functions
        res = self.calculateCriteria()

        my_tableCI = PrettyTable()
        my_tableCI.field_names = ["Item Name", "Class",
                                  "Complexity Letter", "Line"]
        for item in res:
            my_tableCI.add_row([
                item.name,
                item.class_name,
                f"{item.complexityLetter} ({item.complexity})",
                item.startLine
            ]
            )

        return str(my_tableCI)

    def calculateCriteria(self) -> List[namedtuple]:
        """Calculate the complexity of all methods and functions of the file

        Returns:
            List[namedtuple]: complexity analysis
        """
        # read file :
        data = self.data

        # calculate all metrics for all functions and methods
        # in the python file
        evaluation = ComplexityVisitor.from_code(data)

        # initiate
        result = []

        # function
        result.extend(self._collect_info(evaluation.functions))

        # Class
        list_classes = evaluation.classes
        for classItem in list_classes:
            result.extend(self._collect_info(classItem.methods))

        # clean result of empty lists
        while [] in result:
            result.remove([])

        return result

    def exportErrors(self) -> _ListError:
        """ Export the Error list"""

        # initiate message
        msg = ""

        # get result
        results = self.calculateCriteria()

        # feed message
        for result in results:
            if not self._isValidCommplexity(
                result.complexityLetter,
                self.criteria_value
                 ):

                if result.is_method:
                    # result is a class method
                    itemName = f"{result.class_name}.{result.name} "
                else:
                    # result is a function
                    itemName = f"{result.name}"

                msg += (f"{itemName} " +
                        f"(L{result.startLine})" +
                        f" - {result.complexityLetter} ({result.complexity})" +
                        "\n"
                        )

        # create output object as namedtuple
        obj = _ListError(
            criteria_title=self.title,
            criteria_value="Max " + str(self.criteria_value),
            detected_errors=msg
        )

        return obj

    def exportCriteria(self) -> _ListResults:
        """Export the result of the assessment as _ListResult named tuple

        Returns:
            _ListResults: result of the assessment
        """
        # get result
        results = self.calculateCriteria()

        # get maximum value
        complexityValues = [result.complexity for result in results]
        complexityLetters = [result.complexityLetter for result in results]

        maxComplexity = max(complexityValues)
        maxComplexityLetter = max(complexityLetters)

        msg = f"Max {maxComplexityLetter} ({maxComplexity})"

        # create object
        obj = _ListResults(
            criteria_title=self.title,
            criteria_value="Max " + str(self.criteria_value),
            results=msg
        )

        return obj

    @staticmethod
    def _collect_info(items):
        """PRIVATE FUNCTION - use to collect Cyclomatic complexity

        Args:
            items (list): list of complexity result

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
    """Comment Ratio Class"""
    title = "Comment Ratio (%)"
    definition = ("The content of the Python file shall have a minimum"
                  " percentage of comments excluding the blank lines")
    criteria_value = 30

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
        commentsLines = loc_metric.comments + loc_metric.multi

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

    def exportErrors(self) -> _ListError:
        """ Export the Error list"""

        # get result
        result = self.calculateCriteria()

        obj = _ListError(
            criteria_title=self.title,
            criteria_value="Min " + str(self.criteria_value) + " %",
            detected_errors=str(result) + " %"
        )

        return obj

    def exportCriteria(self) -> _ListResults:
        """Export the result of the assessment as _ListResult named tuple

        Returns:
            _ListResults: result of the assessment
        """
        # get result
        result = self.calculateCriteria()

        # create object
        obj = _ListResults(
            criteria_title=self.title,
            criteria_value="Min " + str(self.criteria_value) + " %",
            results=str(result) + " %"
        )

        return obj


class Maintenability(CodeMetric):
    """
    Maintenability Critéria

    see : https://radon.readthedocs.io/en/latest/intro.html#maintainability-index # noqa: E501
    """
    title = "Maintenability"
    definition = ("The content of the Python file shall have a maximum"
                  " level of Maintenability")
    criteria_value = "A"

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

    def exportErrors(self) -> _ListError:
        """ Export the Errors list"""

        # get result
        result = self.calculateCriteria()

        obj = _ListError(
            criteria_title=self.title,
            criteria_value="Max " + str(self.criteria_value),
            detected_errors=str(result)
        )
        return obj

    def exportCriteria(self) -> _ListResults:
        """Export the result of the assessment as _ListResult named tuple

        Returns:
            _ListResults: result of the assessment
        """
        # get result
        result = self.calculateCriteria()

        # create object
        obj = _ListResults(
            criteria_title=self.title,
            criteria_value="Max " + str(self.criteria_value),
            results=str(result)
        )

        return obj

# -------------------------------------------------------------------
#                       FILE ANALYSIS
# -------------------------------------------------------------------


class FileAnalysis():
    """FileAnalysis Class used to assess individual Python file"""

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
        self.filePath = os.path.abspath(filePath)

# -------------------- FILE PROPERTIES ----------------------------

    @property
    def fileName(self) -> str:
        """File name with its extension"""
        _, fileName = os.path.split(self.filePath)
        return fileName

    @property
    def fileFolder(self):
        """path of the folder of the analyzed file"""
        directory, _ = os.path.split(self.filePath)
        return directory

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
        with open(self.filePath, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        return sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)

    @property
    def numberOfLines(self) -> int:
        """Number of lines (without blank line) of the file

        Returns:
            int: number of lines
        """
        nloc = 0
        with open(self.filePath, encoding="utf-8") as fp:
            for line in fp:
                if line.strip():
                    nloc += 1

        return nloc

    # -------------------- ANALYSIS --------------------

    def getValidationStatus(self) -> dict:
        """Calculate the validation status for
        the analyzed file against all criterias

        Returns:
            dict: dictionary with all criteria with a boolean
                (True: pass, False: fail)
        """

        # get data
        datas = self._data

        # initiate the output
        output = {}

        for data in datas:
            output[data.title] = data.isValid()

        return output

    def isValid(self) -> bool:
        """check if a file is valid against all criterias"

        Returns:
            bool: True if Ok else False
        """

        # get results
        res = self.getValidationStatus()

        return all(list(res.values()))

    # ------------------ EXPORT TO STRING -------------------------

    def exportToString(self) -> str:
        """export results to string"""

        # get data
        datas = self._data

        # initiate the outputs
        msgDetails = ""

        # Create table for Result
        my_tableResult = PrettyTable()
        my_tableResult.field_names = ["Criteria",
                                      "Expected Value",
                                      "Assessment"]

        for data in datas:

            # get result
            crit = data.exportCriteria()

            # Complete the result table
            my_tableResult.add_row([
                crit.criteria_title,
                crit.criteria_value,
                crit.results
            ])

            msgDetails += (">>> " + data.title +
                           "\n" + data.toString() + "\n\n")

        msg = (
            "File Description :\n".upper() +
            f"\t- File:              {self.fileName}\n" +
            f"\t- Path:              {self.fileFolder}\n" +
            f"\t- Last Modifcation:  {self.lastModificationDate}\n" +
            f"\t- CheckSum MD5:      {self.checksum_MD5}\n" +
            f"\t- SHA256:            {self.sha256}\n" +
            f"\t- Number of lines:   {self.numberOfLines}\n"
            "\n" +
            "File Assessment:\n".upper() +
            f"{my_tableResult}"
            "\n" +
            "File Metrics :\n".upper() +
            f"{msgDetails}"
        )

        return msg

    def exportStatus(self) -> list[namedtuple]:
        """ export a list of namedtuple with the synthetic
        output of the assessment of the file"""

        # initiate the status namedtuple
        FileStatus = namedtuple("fileStatus", [
                          "criteria",
                          "expected_value",
                          "assessment",
                          ])

        # get data
        datas = self._data

        # initiate res
        res = []

        for data in datas:

            # get result
            crit = data.exportCriteria()

            # feed the table
            res.append(FileStatus(
                criteria=crit.criteria_title,
                expected_value=crit.criteria_value,
                assessment=crit.results,
            ))

        return res

    def exportErrors(self) -> List[_ListError]:
        """Export the detected errors as a list"""

        ListErrors = []
        for data in self._data:
            if not data.isValid():
                ListErrors.append(data.exportErrors())
        return ListErrors

    # ---------------------- UTILS -----------------------

    def _readFile(self):
        """PRIVATE FUNCTION - read the data

        Returns:
            str : all data of the Python file
        """

        return readASCIIFile(self.filePath)


# -------------------------------------------------------------------
#                       FOLDER ANALYSIS
# -------------------------------------------------------------------


class FolderAnalysis(ImmutableClass):
    """Immutable Class for folder Analysis"""
    def __init__(self, folderPath: str,
                 max_complexity_letter: str = "B",
                 max_maintenance_letter: str = "A",
                 min_comment_ration: int = 30) -> None:
        """create a folder analysis class object

        Args:
            folderPath (str): folder path (absolute or relative)
            max_complexity_letter (str, optional): maximum complexity.
                 Defaults to "B".
            max_maintenance_letter (str, optional): maxim maintenance.
                 Defaults to "A".
            min_comment_ration (int, optional): Minimum COmment ratio
                 Defaults to 30.
        """

        self.folderPath = validateFolder(folderPath)

        # settings :
        self.max_complexity_letter = max_complexity_letter
        self.max_maintenance_letter = max_maintenance_letter
        self.min_comment_ration = min_comment_ration

        # collect all the results
        self._results = self._getResults()

        # initalisation with super class
        super().__init__()

    def __str__(self) -> str:
        """Export Folder analysis as a string

        Returns:
            str: string with the folder analysis outputs
        """

        # Create header
        header_msg = (
            "#"*LINE_SIZE + "\n" +
            "CODE METRICS ANALYSIS".center(LINE_SIZE) + "\n" +
            "#"*LINE_SIZE + "\n" +
            "\n" +
            "Folder Description :\n".upper() +
            f"\t- folder:{self.folderPath}\n" +
            f"\t- Platform: {self.platform_info}\n"
            "\n"
        )

        # initiate detailled message
        detailledAnalysis = ""

        # create a table for validation status
        my_tableST = PrettyTable()
        my_tableError = PrettyTable()
        results = self._results

        # fields = results[0].validStatus._fields
        # print(fields)
        my_tableST.field_names = (["file Name"] +
                                  list(results[0].validStatus.keys()))

        columnTitles = [
                    "File Name",
                    "Error Type",
                    "Expected Criteria",
                    "Error"
                ]
        my_tableError.field_names = columnTitles

        # Loop over result
        for result in results:
            status = [result.filePath] + [result.validStatus[item]
                                          for item in
                                          list(result.validStatus.keys())]

            # feed status
            my_tableST.add_row(status)

            # feed error
            if not result.isValid:
                for error in result.errorOutputs["errors"]:
                    my_tableError.add_row([
                            result.errorOutputs["relative Path"],
                            error.criteria_title,
                            error.criteria_value,
                            error.detected_errors
                                    ]
                            )

            # collect detailled analysis
            detailledAnalysis += (
                "-"*LINE_SIZE + "\n" +
                ">>> " + result.filePath.upper() + "\n" +
                result.stringInfo + "\n"
            )
            # create the global msg
            msg = (
                header_msg +
                ">>> RESULTS :\n" +
                f"{my_tableST}\n" +
                ">>> ERRORS :\n" +
                f"{my_tableError}\n" +
                "\n" +
                "@"*LINE_SIZE + "\n\n" +
                detailledAnalysis
                )
        return msg

    # -------------------- PROPERTIES ------------------------

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
                           not "test" in name.lower()  # remove test file
                           )]
        return pythonFiles


    @property
    def platform_info(self) -> str:
        """ Provide the platform info"""
        platform_info = platform.uname()
        mystr = (f"{platform_info.machine}"
                 f" - OS : {platform_info.system} {platform_info.version}")
        return mystr

    # -------------------- PROPERTIES ------------------------

    def _getResults(self,
                    ) -> List:
        """Provide the list of code metrics for all analyzed python files

        Args:

        Returns:
            List: list of namedtuple
        """

        # initiate results list and error list
        list_results = []
        list_errors = []

        # initiate the results namedtuple
        FolderResult = namedtuple("FolderResult", [
                          "filePath",
                          "stringInfo",
                          "isValid",
                          "validStatus",
                          "errorOutputs",
                          ])

        # initiate Console Output
        console = Console()

        # console output
        console.rule(title="[bold cyan]CODE CONFORMANCE ANALYSIS",
                     characters="=",
                     style=Style(color="cyan"))
        console.print(f"[bold]Platform :[/bold] {self.platform_info}")
        console.print(
            ("[bold]Root Folder :[/bold] [bold cyan]"
             f"{self.folderPath}[/bold cyan]")
        )
        console.print(f"[bold]Number of Elements :  {len(self.listFiles)}\n")

        for file_path in self.listFiles:

            # get relative path
            rel_path = os.path.relpath(file_path, self.folderPath)

            obj = FileAnalysis(file_path,
                               maxComplexityLetter=self.max_complexity_letter,
                               maxMaintenanceLetter=self.max_maintenance_letter,  # noqa: E501
                               minCommentRatio=self.min_comment_ration
                               )

            # collect info
            console.print(f"[cyan]>>> Analysis of {rel_path}...")
            console.print(self._createRichTableFromList(obj.exportStatus()))

            # get results
            validationResult = obj.getValidationStatus()

            # Collect errors
            if not obj.isValid():
                newError = {
                    "relative Path": rel_path,
                    "errors": obj.exportErrors()
                }
                list_errors.append(newError)
            else:
                newError = None

            # Collect outputs for a file
            newRes = FolderResult(filePath=rel_path,
                                  stringInfo=obj.exportToString(),
                                  isValid=all(list(validationResult.values())),
                                  validStatus=validationResult,
                                  errorOutputs=newError
                                  )

            list_results.append(newRes)

        # final consol output
        nbFalse = [item.isValid for item in list_results].count(False)

        if nbFalse == 0:
            # No Error detected
            console.rule(title=f"[bold green]{len(self.listFiles)} files OK",
                         characters="=",
                         style=Style(color="green"))
        else:
            # Errors detected
            # initiate table
            table = Table(title="Detailled Errors")

            # get the list of Column for the table
            # extend with the last result dict fields
            columnTitles = [
                "File Name",
                "Error Type",
                "Expected Criteria",
                "Error"
            ]
            # create columns
            for name in columnTitles:
                table.add_column(name, style="cyan")

            # feed with information
            for fileErrors in list_errors:
                # get the dictionaries of one file
                for error in fileErrors["errors"]:
                    table.add_row(
                        fileErrors["relative Path"],
                        error.criteria_title,
                        error.criteria_value,
                        error.detected_errors
                                )
            console.print(table)
            msg = f"[bold red]{nbFalse} erros over {len(self.listFiles)} files"
            console.rule(title=msg,
                         characters="=",
                         style=Style(color="red"))
        return list_results

    def isValid(self,
                ) -> bool:
        """Check if all Python files in the path (including subdirectories)
        are valid against code metrics

        Args:

        Returns:
            bool: boolean Ture if OK false if not valid
        """
        res = all([item.isValid
                   for item in self._results])
        return res

    def exit(self):
        """exit mode for continuous integration.
        If all Ok exit = 0 and if an error exit = 1"""

        return not self.isValid()

    # ---------------------- UTILS -----------------------

    @staticmethod
    def _createRichTableFromList(values: list[namedtuple]) -> Table:
        """ PRIVATE METHOD  - create a rich table from a list of namedtuple"""

        fieldsNames = values[0]._fields

        table = Table(*fieldsNames)

        for value in values:
            table.add_row(*list(value))

        return table
