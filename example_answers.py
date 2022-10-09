def fix_is_store_open(current_time, opening_times):
    current_time = current_time.replace(':', '')
    opening_time_list = opening_times.replace(':', '').split('-')
    start = opening_time_list[0]
    end = opening_time_list[1]
    # you can also explictly convert to int, strings work though:
    if current_time > '2359' or start > '2359' or end > '2359':
        return 'invalid time'
    else:
        return start <= current_time <= end


def fix_my_function(filename):
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


def sentiment_score(tweet):
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


def reduce_frequencies(worker_output):
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


def n_unique_words(file_name):
    unique_words = []
    with open(file_name) as file_contents:
        file_input = file_contents.read()
    clean_text = file_input.lower().replace('.', '').replace(',', '')
    for word in clean_text.split():
        if word not in unique_words:
            unique_words.append(word)
    return len(unique_words)


def best_ds_student(grades, ds_courses):
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