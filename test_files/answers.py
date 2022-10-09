def arithmetics(expression):
    """
    ('60 + 27')
    ('60 - 27')
    ('60 / 27')
    ('60 * 27')
    ('11 + 12')
    """
    num1 = int(expression[0:2])
    op = expression[3]
    num2 = int(expression[5:])
    if op == '+': return num1 + num2
    elif op == '-': return num1 - num2
    elif op == '*': return num1 * num2
    elif op == '/': return num1 // num2
    else: return -1


def written_by(author, book_list):
    """
    ("", [])
    ("Milan Kundra", [
                   ['War and Peace', 'Leo Tolstoy', 'The Russian Messenger'],\
                   ['Don Quixote', 'Miguel de Cervantes',
                    'Francisco de Robles'],\
                   ['The Stranger', 'Albert Camus', 'Hamish Hamilton'],
                   ['The Plague', 'albert camus', 'Gallimard']])
    ("Leo Tolstoy", [
                   ['War and Peace', 'Leo Tolstoy', 'The Russian Messenger'],\
                   ['Don Quixote', 'Miguel de Cervantes',
                    'Francisco de Robles'],\
                   ['The Stranger', 'Albert Camus', 'Hamish Hamilton'],
                   ['The Plague', 'albert camus', 'Gallimard']])
    ("LEO TOLSTOY", [
                   ['War and Peace', 'Leo Tolstoy', 'The Russian Messenger'],\
                   ['Don Quixote', 'Miguel de Cervantes',
                    'Francisco de Robles'],\
                   ['The Stranger', 'Albert Camus', 'Hamish Hamilton'],
                   ['The Plague', 'albert camus', 'Gallimard']])
    ("Albert Camus", [
                   ['War and Peace', 'Leo Tolstoy','The Russian Messenger'],\
                   ['Don Quixote', 'Miguel de Cervantes',
                    'Francisco de Robles'],\
                   ['The Stranger', 'Albert Camus', 'Hamish Hamilton'],
                   ['The Plague', 'albert camus', 'Gallimard']])
    """
    books = []
    for book in book_list:
        if book[1].lower() == author.lower():
            books.append(book[0])
    return books

def calculate_bill(order):
    """
    ('./orders/order0')
    ('./orders/order1')
    ('./orders/order2')
    ('./orders/order3')
    ('./orders/order4')
    """
    cost = 0
    for line in open(order):
        if line.strip() == '': continue
        line = line.split()
        cost += float(line[1]) * float(line[2])
    
    return cost

def word_keys(text):
    """
    ('')
    ('there is so much')
    ('there is so so much to decompress here and there')
    ('There is so SO much to decompress here and there')
    ('      one      two     ')
    """ 
    key_dict = {}
    last_id = 0
    
    for w in text.strip().split():
        w = w.lower()
        if w not in key_dict:
            last_id += 1
            key_dict[w] = last_id
    return key_dict

def compress_text(text, compress_key):
    """
    ("", {'decompress': 6, 'here': 7, 'is': 2, 'much': 4, 'so': 3, \
          'there': 1, 'to': 5})
    ("how much is there", \
               {'decompress': 6, 'here': 7, 'is': 2, 'much': 4, 'so': 3, \
                'there': 1, 'to': 5})
    (" much is there  ", \
               {'decompress': 6, 'here': 7, 'is': 2, 'much': 4, 'so': 3, \
                'there': 1, 'to': 5})
    ("how much is there", {})
    ("there is so so much here to   decompress", \
               {'decompress': 6, 'here': 7, 'is': 2, 'much': 4, 'so': 3, \
                'there': 1, 'to': 5})
    """
    compressed = ""
    for word in text.strip().lower().split():
        if word in compress_key:
            compressed += str(compress_key[word]) + " "
        else:
            compressed += word + " "
    return compressed.strip()

def final_average(grades):
    """
    ([])
    ([['deep learning', 6.0], ['statistics', 7.0]])
    ([['statistics', 3.5], ['deep learning', 6.0],
                    ['statistics', 7.0]])
    ([['statistics', 7.0], ['deep learning', 6.0],
                    ['statistics', 3.5]])
    ([['statistics', 7.0], ['deep learning', 6.0],
                    ['statistics', 7.0]])
    """
    if len(grades) == 0: 
        return 0

    courses = {}
    for g in grades:
        if g[0] not in courses: courses[g[0]] = []
        courses[g[0]].append(g[1])

    total = 0
    for c in courses:
        total += max(courses[c])
    return total/len(courses)