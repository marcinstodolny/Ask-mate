import data_manager


def sort_list(sort_by="submission_time", order_direction="DESC", limit=""):
    return data_manager.get_sorted_data(sort_by, order_direction, limit)


def exchange_search_phrases_with_marked_one(message, search_phrases, element):
    for i, item in enumerate(message):
        message[i][f'{element}'] = item[f'{element}'].replace(search_phrases, f'<mark>{search_phrases}</mark>')


def exchange_search_phrases(titles, answers, question_messages, search_phrases):
    exchange_search_phrases_with_marked_one(titles, search_phrases, 'title')
    exchange_search_phrases_with_marked_one(answers, search_phrases, 'message')
    exchange_search_phrases_with_marked_one(question_messages, search_phrases, 'message')


def exchange_question_newlines_to_html(question):
    question['message'] = question['message'].replace('<', '').replace('&#60;', '   ').replace('\n', '<br>')


def exchange_string_newlines_to_html(table):
    for i, item in enumerate(table):
        table[i]['message'] = item['message'].replace('<', '').replace('&#60;', '').replace('\n', '<br>')


def exchange_newlines(question, answers, comments):
    exchange_question_newlines_to_html(question)
    exchange_string_newlines_to_html(answers)
    exchange_string_newlines_to_html(comments)
