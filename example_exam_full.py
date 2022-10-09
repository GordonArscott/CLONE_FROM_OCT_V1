import os
from test_eval import Question


class Question1(Question):

    def __init__(self):
        self.name = 'fix_is_store_open'
        self.total_points = 10
        self.case_points = self.total_points / len(self.get_tests())
        self.exempted = [4]

    def solution(self, current_time, opening_times):
        current_time = current_time.replace(':', '')
        opening_time_list = opening_times.replace(':', '').split('-')
        start = opening_time_list[0]
        end = opening_time_list[1]
        # you can also explictly convert to int, strings work though:
        if current_time > '2359' or start > '2359' or end > '2359':
            return 'invalid time'
        else:
            return start <= current_time <= end

    def get_tests(self):
        return [
            ("00:00", "01:00-23:59"),
            ("07:00", "00:00-23:59"),
            ("06:34", "06:01-06:59"),
            ("01:00", "01:00-01:00"),
            ("25:00", "23:00-26:00")
        ]


class Question2(Question):

    def __init__(self):
        self.name = 'fix_my_function'
        self.total_points = 10
        self.case_points = self.total_points / len(self.get_tests())
        self.exempted = []

    def write_files(self):
        lines = [
            'price: 0',
            'product: shoe',
            'product: shoe, price: 5',
            'product: umbrella, price: 5',
            'price: 2, product: stroopwafels'
        ]
        for i, line in enumerate(lines):
            with open(os.path.dirname(os.path.abspath(__file__)) +
                      f'/test_files/single_order/order{i + 1}.txt', 'w') as fo:
                fo.write(line)

    def solution(self, filename):
        with open(filename, 'r') as f:
            x = f.read()
        if 'price' in x:
            if 'umbrella' in x:
                return 'umbrella'
            elif 'shoe' in x:
                return 'shoe'
            else:
                return False
        elif 'price' not in x and ('umbrella' in x or 'shoe' in x):
            return 'no price'
        else:
            return False

    def get_tests(self):
        return [
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/single_order/order1.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/single_order/order2.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/single_order/order3.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/single_order/order4.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/single_order/order5.txt')
        ]


class Question3(Question):

    def __init__(self):
        self.name = 'sentiment_score'
        self.total_points = 20
        self.case_points = self.total_points / len(self.get_tests())
        self.exempted = []

    def solution(self, tweet):
        positive = ['yay', 'happy', 'like', ':)', 'good', 'interesting']
        negative = ['oof', 'sad', 'boring', ':(', 'bad', 'interesting']
        negators = ['not', 'jk']
        tokens = tweet.split()
        tweet_length = len(tokens)
        sentiment_score = 0
        negator_present = False
        if not tweet:
            return 0.0
        for token in tweet.split():
            if token in positive:
                sentiment_score += 1
            if token in negative:
                sentiment_score -= 1
            if token in negators:
                negator_present = True
        if negator_present:
            sentiment_score *= -1
        return sentiment_score / tweet_length

    def get_tests(self):
        return [
            ("boo"),
            ("yay im super happy :)"),
            ("the movie was really nice and interesting :)"),
            ("the movie was good and bad and sad :("),
            ("very good and interesting movie , jk :)")
        ]


class Question4(Question):

    def __init__(self):
        self.name = 'reduce_frequencies'
        self.total_points = 20
        self.case_points = self.total_points / len(self.get_tests())
        self.exempted = []

    def solution(self, worker_output):
        frequencies = {}
        for worker in worker_output:
            for word, count in worker.items():
                if word not in frequencies:
                    frequencies[word] = count
                else:
                    frequencies[word] += count
        if not frequencies:
            return 0
        else:
            return max(frequencies.values())

    def get_tests(self):
        return [
            ([{}]),
            ([{'hello': 4, 'stuff': 1, 'things': 0, 'more': 10}]),
            ([{'stuff': 2, 'more': 1}, {'stuff': 1, 'and': 1}]),
            ([{'no': 0}]),
            ([{'stuff': 1, 'more': 1}])
        ]


class Question5(Question):

    def __init__(self):
        self.name = 'n_unique_words'
        self.total_points = 20
        self.case_points = self.total_points / len(self.get_tests())
        self.exempted = []

    def write_files(self):
        lines = [
            'Foo',
            'this is a text with a bunch of words and a bunch of periods. ' +
            'This. Is. Great.',
            'Really great, Absolutely great text, Really, really good',
            'A short      text ... Periods , commas ,  and spaces      ' +
            'everything .',
            'THESE are MANY words and THEY ARE words AND more WORDS'
        ]
        for i, line in enumerate(lines):
            with open(os.path.dirname(os.path.abspath(__file__)) +
                      f'/test_files/sents/sent{i + 1}.txt', 'w') as fo:
                fo.write(line)

    def solution(self, file_name):
        unique_words = []
        with open(file_name) as file_contents:
            file_input = file_contents.read()
        clean_text = file_input.lower().replace('.', '').replace(',', '')
        for word in clean_text.split():
            if word not in unique_words:
                unique_words.append(word)
        return len(unique_words)

    def get_tests(self):
        return [
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/sents/sent1.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/sents/sent2.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/sents/sent3.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/sents/sent4.txt'),
            (os.path.dirname(os.path.abspath(__file__)) + '/test_files/sents/sent5.txt')
        ]


class Question6(Question):

    def __init__(self):
        self.name = 'best_ds_student'
        self.total_points = 20
        self.case_points = self.total_points / len(self.get_tests())
        self.exempted = [2, 5]

    def solution(self, grades, ds_courses):
        student_avg = {}
        for student, course_grades in grades.items():
            if student not in student_avg:
                student_avg[student] = []
            for course, grade in course_grades:
                if course in ds_courses:
                    student_avg[student].append(grade)

        best_student, best_average = '', 0
        for student, avg in student_avg.items():
            student_average = sum(avg) / len(avg) + min(avg) / 20 * len(avg) 
            student_average += len(avg) / 1000
            if student_average > best_average:
                best_average = student_average
                best_student = student

        return best_student

    def get_tests(self):
        return [
            ({
                'Robin Doe': [
                    ['Data Processing', 10.0],
                    ['Machine Learning', 7.5]
                ]
            }, ['Data Processing']),
            ({
                'Morgan Free': [
                    ['Data Processing', 9.0],
                    ['Machine Learning', 7.5]
                ],
                'Alex Foo': [
                    ['Data Processing', 8.5],
                    ['Marketing', 9.5]
                ],
                'Robin Doe': [
                    ['Data Processing', 7.5],
                    ['Marketing', 9.5]
                ],
                'Taylor Sec': [
                    ['Data Processing', 6.5],
                    ['Marketing', 10.0]
                ]}, ['Data Processing', 'Machine Learning']),
            ({
                'Robin Doe': [
                    ['Data Processing', 10.0],
                    ['Machine Learning', 7.5]
                ],
                'Alex Foo': [
                    ['Data Processing', 8.5],
                    ['Ethics', 9.5]
                ],
                'Morgan Free': [
                    ['Data Processing', 3.5],
                    ['Marketing', 1.5]
                ],
                'Taylor Sec': [
                    ['Data Processing', 6.5],
                    ['Marketing', 10.0],
                    ['Linear Algebra', 10.0],
                    ['Quantum Physics', 9.0]
                ]}, ['Data Processing', 'Machine Learning', 'Ethics']),
            ({
                'Taylor Sec': [
                    ['Data Processing', 9.5]
                ],
                'Alex Foo': [
                    ['Data Processing', 8.5],
                    ['Marketing', 9.5],
                    ['Ethics', 9.5]
                ],
                'Morgan Free': [
                    ['Data Processing', 9.0]
                ],
                'Robin Doe': [
                    ['Data Processing', 8.5],
                ]}, ['Data Processing', 'Machine Learning', 'Ethics']),
            ({
                'Morgan Free': [
                    ['Data Processing', 10.0],
                    ['Machine Learning', 2.0],
                    ['Ethics', 8.10]
                ],
                'Taylor Sec': [
                    ['Data Processing', 10.0],
                    ['Ethics', 3.333333333333333333334]
                ]}, ['Data Processing', 'Machine Learning', 'Ethics'])
        ]