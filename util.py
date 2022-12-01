import data_manager


def sort_list(sort_by="submission_time", order_direction="DESC", limit=""):
    return data_manager.get_sorted_data(sort_by, order_direction, limit)


def exchange_search_phrases_with_marked_one(message, search_phrases, element):
    for i, item in enumerate(message):
        message[i][f'{element}'] = item[f'{element}'].replace(search_phrases, f'<mark>{search_phrases}</mark>')
