import contextlib
import importlib
import inspect
import io
import os
import pathlib

from numpy.testing import assert_equal


class Question(object):
    """How to use the exam structure:

    Every question needs to be defined as a class QuestionN(Question) where N
    is the question number. These should be stored in a separate .py file
    so that Evaluator can load the classes from that one dynamically.

    The attributes are as follows, which need to be updated per question:

    Attributes
    ----------
    name : str
        The function name (AS SPECIFIED IN THE EXAM!).
    total_points : int
        The points for this question.
    case_points : int
        Points per case, automatically calculated by total / number of tests.
    excepted : list
        A list of indices which case to exempt. Say that case nr 4 was bogus,
        and you wanna drop it, then it's nr - 1 (because indices), so [3].

    There are several functions below the __init__ that also require updating:
    - solution
        This one is just a copy paste of the solution code, make sure the
        variables after `self` also correspond to the ones in the function.
    - get_tests
        This can be whatever is required to generate the input to the functions
        used as test cases, but always has to be a list (case per element) of
        tuples (variable input per element). There are some examples of how
        to handle stuff for files and for the same type of input for different
        cases below.
    - write_files
        If the questions requires certain file contents to be written, this
        function needs to make sure they are present in ./test_files.
    """


    def __init__(self, verbose=True):
        """Template class for questions."""
        self.name = ''
        self.total_points = 10
        self.case_points = self.total_points / len(self.get_tests())
        self.excepted = []

    def solution(self, *args, **kwargs):
        return 0

    def get_tests(self):
        return [None]

    def write_files(self):
        return


class Evaluator(object):

    def __init__(self, verbose=True):
        """If verbose is set, prints report per test instance."""
        self.verbose = verbose
        self.registry = {}

    def _capture_student_output(self, answer, test):
        """Runs student function, captures prints, writes, and errors."""
        # NOTE: this makes sure whatever students write goes to dump folder
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/dump')
        try:
            with contextlib.redirect_stdout(io.StringIO()):  # mute output
                if isinstance(test, tuple):  # meaning there are multiple args
                    output = answer(*test)
                else:
                    output = answer(test)
        except ModuleNotFoundError as p:  # needs to be installed server-side
            print("Student package not installed:", p)
            output = p
        except Exception as e:  # if there is some error in student code
            output = e
        os.chdir('../')  # change back to orginal dir
        return output

    def _test_answer(self, question, answer, test):
        from copy import deepcopy
        question.write_files()  # required files for assignment (./test_files)
        test = deepcopy(test)  # make sure tests are 'clean'
        if isinstance(test, tuple):  # meaning there are multiple args
            correct_output = question.solution(*test)
        else:  # NOTE: you can't do this in a one-liner because of * context
            correct_output = question.solution(test)
        student_output = self._capture_student_output(answer, test)
        try:  # numpy assert_equal of correct and student output
            assert_equal(correct_output, student_output)
            output_match = True  # assert_equal is none by default
        except AssertionError as e:  # this fires if correct != student output
            print(e)  # print optional
            output_match = False
        return output_match, correct_output, student_output

    def _report(self, correct_output, student_output, test_id, q, valid):
        """Print formatting of output, points, etc."""
        # NOTE: it might be wortwhile to neatly wrap this around score_question
        # so it doesn't print a question nr. (etc.) per case
        print("Question:", q.name, "-- case:", test_id)
        print("Correct output:\t {", repr(correct_output), "}")
        print("Your output:\t {", repr(student_output), "}")
        if valid == True:
            print("Output", test_id, "correct, points +", q.case_points)
        else:
            print("No points")
        print("\n")

    def _register(self, question, test_id, valid):
        """This records the partial points per student into self.registry."""
        assert test_id != 6  # NOTE: might have more than 5 at some point
        # the registry sturcture is rather detailed because we want to have
        # stats per question for analysis later on
        if not self.registry.get(question.name):
            self.registry[question.name] = {test_id: [valid]}
        elif not self.registry[question.name].get(test_id):
            self.registry[question.name][test_id] = [valid]
        else:
            self.registry[question.name][test_id].append(valid)
    def _score_question(self, question, answer):
        """Per question and answer, score if output is same per test cases."""
        tests, total_points = question.get_tests(), int(question.total_points)
        for test_id, test in enumerate(tests):
            test_id += 1
            if test_id in question.exempted:  # list of exempted question ids
                if self.verbose:
                    print("Test case exempted, full points.")
                    continue
                valid = True  # set questions to always be correct if exempted
            else:
                valid, correct_output, student_output = \
                    self._test_answer(question, answer, test)
                if not valid:  # if code errors or output format is incorrect
                    total_points -= question.case_points
            self._register(question, test_id, valid)  # record points per q
            if self.verbose:  # print report line
                self._report(correct_output, student_output, test_id,
                             question, valid)
        return total_points

    def _load_module(self, module_path, namespace):
        """This is a stringified version of `from module_path import *`."""
        loader = importlib.machinery.SourceFileLoader(namespace, module_path)
        return loader.load_module()

    def run(self, exam_path, answer_path):
        """Main evaluation pipeline: loads answers and solutions and scores."""
        # lines below import the solution classes and answer functions 
        exam_questions = self._load_module(exam_path, namespace="question")
        student_answers = self._load_module(answer_path, namespace="answer")

        # instantiates class, ignores those without name arg, and sorts by name
        questions = sorted(
            [_cls() for _, _cls in
             inspect.getmembers(exam_questions, inspect.isclass)
             if _cls().name],
            key=lambda x: x.name)
        # same process for functions, sort by name guarantees they match above
        answers = sorted(
            [func for _, func in
             inspect.getmembers(student_answers, inspect.isfunction)
             ],
            key=lambda x: x.__name__)

        # because both are sorted by name (alphabetically) rather than question
        # order, the line above sorts them according to the class names, which
        # captures the order (Question1, Question2, etc.)
        for qcls, afunc in sorted(
         zip(questions, answers), key=lambda x: x[0].__class__.__name__):
            self._score_question(qcls, afunc)
        # NOTE: requirements here are that class names always include numbers,
        # and that class.name always matches the name of the answer function
        # (and vice versa). If this changes, change this!
        return self.registry


def test_evals():
    script_dir = pathlib.Path(__file__).parent
    registry_result = Evaluator().run("example_exam_full.py","example_answers_full.py")
    #print(registry_result)
    nightmare = list(registry_result.values())
    for index, x in enumerate(nightmare): #This is basically all the tests for each question.
        #print(x) 
        for y in x.values(): #This is a log of each test that's in the question
            #print(y)
            assert y[0] == True #Basically asserting that every single question is correctamundo
            #lookup_error(y[0])
        #print(registry_result.values())


#def lookup_error(tester):
#    try:
#        assert tester == True, "Disaster"
#    except AssertionError as error_assert:
#        print("this is a nightmare: ", error_assert)


if __name__ == "__main__":
    test_evals()
# if __name__ == "__main__":
#     script_dir = pathlib.Path(__file__).parent
#     Evaluator().run("example_exam.py","example_answers.py")
