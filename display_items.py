import curses
import math

def display_items(stdscr, items: list, maxX: int, maxY: int, number_of_items_by_line: int, index_selected_item: int, title: str = "", index: int = -1, subtitle: str = "", user_answer_index: int = -1, valid_answer_index: int = -1):
    number_of_lines = math.ceil(len(items) / number_of_items_by_line)
    middle_height = maxY // 2
    middle_width = maxX // 2
    length_line = 0

    i = 0
    k = 0
    while i < number_of_lines:
        yStartStr = middle_height - (number_of_lines // 2) * 5 + i * 5
        for j in range(number_of_items_by_line):
            if k + j < len(items):
                length_line += len(items[k + j])
                if j > 0:
                    length_line += 2
        xStartStr = middle_width - length_line // 2

        for j in range(number_of_items_by_line):
            if k < len(items):
                pair_number = 0
                if k == index_selected_item:
                    pair_number = 1
                if k == user_answer_index and valid_answer_index != user_answer_index:
                    pair_number = 4
                if k == valid_answer_index:
                    pair_number = 5
                stdscr.addstr(yStartStr, xStartStr, items[k], curses.color_pair(pair_number))
                xStartStr += len(items[k]) + 2
                k += 1

        length_line = 0
        i += 1
    if title != "":
        if index != -1:
            title = f"| Question {index + 1}: {title} |"
        else:
            title = f"| {title} |"
        stdscr.addstr(middle_height - (number_of_lines // 2) * 5 - 5, middle_width - len(title) // 2, title, curses.A_BOLD)
        stdscr.addstr(middle_height - (number_of_lines // 2) * 5 - 6, middle_width - len(title) // 2, '-' * len(title))
        stdscr.addstr(middle_height - (number_of_lines // 2) * 5 - 4, middle_width - len(title) // 2, '-' * len(title))
        if subtitle != "":
            stdscr.addstr(middle_height - (number_of_lines // 2) * 5 - 2, middle_width - 1, "->", curses.color_pair(1))
    if subtitle != "":
        pair = 3 if "correct" in subtitle else 2
        stdscr.addstr(middle_height - (number_of_lines // 2) * 5 + number_of_lines * 5, middle_width - len(subtitle) // 2, subtitle, curses.color_pair(pair))
