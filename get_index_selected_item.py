import curses

def get_index_selected_item(index_selected_item: int, c: int, number_of_items: int, number_of_items_by_line: int):
    if c == curses.KEY_LEFT:
        index_selected_item = index_selected_item - 1 if index_selected_item > 0 else number_of_items - 1
        if index_selected_item % number_of_items_by_line == number_of_items_by_line - 1:
            index_selected_item = (index_selected_item + number_of_items_by_line) % number_of_items
    elif c == curses.KEY_RIGHT:
        index_selected_item = index_selected_item + 1 if index_selected_item < number_of_items - 1 else 0
        if index_selected_item % number_of_items_by_line == 0:
            index_selected_item = (index_selected_item - number_of_items_by_line) % number_of_items
    elif c == curses.KEY_UP:
        index_selected_item = index_selected_item - number_of_items_by_line if index_selected_item - number_of_items_by_line >= 0 else number_of_items - number_of_items_by_line + index_selected_item
    elif c == curses.KEY_DOWN:
        index_selected_item = index_selected_item + number_of_items_by_line if index_selected_item < number_of_items - number_of_items_by_line else index_selected_item % number_of_items_by_line
    return index_selected_item
