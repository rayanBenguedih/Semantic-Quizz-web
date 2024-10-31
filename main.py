import curses
import math
import random
from fetch import getTwentyRandomArtists, generateQuestions
from display_items import display_items
from get_index_selected_item import get_index_selected_item
from fake_data import fake_artists, fake_questions

def main(argv):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    stdscr.keypad(True)

    c = -1

    api_artists = getTwentyRandomArtists()
    selected_artists = api_artists[:20]
    number_of_artists = len(selected_artists)
    number_of_themes_by_line = 4

    max_length = max(len(artist) for artist in selected_artists)
    artists = [f"{artist.center(max_length)}" for artist in selected_artists] # fill of spaces to have the same length

    lines = [artists[i:i + number_of_themes_by_line] for i in range(0, number_of_artists, number_of_themes_by_line)]
    max_line_length = max(len(' '.join(line)) for line in lines)

    curses.init_pair(0, 255, 0) # id 0, white text, black background
    curses.init_pair(1, 0, 255) # id 1, black text, white background
    curses.init_pair(2, curses.COLOR_RED, 0) # id 2, red text, white background
    curses.init_pair(3, curses.COLOR_GREEN, 0) # id 3, green text, white background
    curses.init_pair(4, 0, curses.COLOR_RED)
    curses.init_pair(5, 0, curses.COLOR_GREEN)

    index_selected_theme = 0
    index_selected_answer = 0

    number_of_questions = 0
    current_question = 0
    number_of_questions_by_line = 2

    questions = []
    valid_answers = []
    data = []

    user_answers = []

    state = 1

    while c != ord('q'):
        stdscr.clear()

        maxY, maxX = stdscr.getmaxyx()

        if c == 10: # Enter
            if (state == 2 and current_question < number_of_questions):
                if number_of_questions == 0:
                    break
                user_answers.append(index_selected_answer)
                if current_question == number_of_questions - 1:
                    state += 1
                    current_question = 0
                else:
                  current_question += 1
                  index_selected_answer = 0
            elif (state == 4 and current_question < number_of_questions):
                if current_question == number_of_questions - 1:
                    state += 1
                current_question += 1
            else:
              state += 1
        
        if state > 5:
            state = 1
            user_answers = []
            current_question = 0
            index_selected_theme = 0
            index_selected_answer = 0
            data = []
            questions = []
            valid_answers = []
            number_of_questions = 0
        
        if len(data) == 0 and state > 1:
            data = generateQuestions(selected_artists[index_selected_theme], 5, 25)
            number_of_questions = len(data)

        if (maxY > (5 * math.ceil(number_of_artists / number_of_themes_by_line) + 6) and maxX > max_line_length + number_of_themes_by_line):
            if state == 1:
                index_selected_theme = get_index_selected_item(index_selected_theme, c, number_of_artists, number_of_themes_by_line)
                display_items(stdscr, artists, maxX, maxY, number_of_themes_by_line, index_selected_theme, "Select a theme")
            elif state == 2:
                for i in range(number_of_questions):
                    current_data = data[i]
                    question = current_data["question"]
                    validAnswer = current_data["validAnswer"]
                    wrongAnswers = current_data["wrongAnswers"]
                    number_of_answers = len(wrongAnswers) + 1
                    random_index = random.randint(0, number_of_answers - 1)
                    valid_answers.append(random_index)
                    answers = wrongAnswers[:random_index] + [validAnswer] + wrongAnswers[random_index:]
                    questions.append({
                      "question": question,
                      "answers": answers
                    })
                
                if len(questions) == 0:
                    break
                question = questions[current_question]["question"]
                answers = questions[current_question]["answers"]

                max_length = max(len(answer) for answer in answers)
                answers = [f"{answer.center(max_length)}" for answer in answers] # fill of spaces to have the same length

                index_selected_answer = get_index_selected_item(index_selected_answer, c, len(answers), number_of_questions_by_line)
                display_items(stdscr, answers, maxX, maxY, number_of_questions_by_line, index_selected_answer, question, current_question)
            elif state == 3:
                see_result = "See results"
                stdscr.addstr(maxY // 2, maxX // 2 - len(see_result) // 2, see_result, curses.color_pair(1))
            elif state == 4:
                if len(questions) == 0:
                    break
                question = questions[current_question]["question"]
                answers = questions[current_question]["answers"]

                max_length = max(len(answer) for answer in answers)
                answers = [f"{answer.center(max_length)}" for answer in answers] # fill of spaces to have the same length

                user_answer = user_answers[current_question]
                valid_answer = valid_answers[current_question]

                subtitle = "Your answer is correct" if user_answer == valid_answer else "Your answer is wrong"

                display_items(stdscr, answers, maxX, maxY, number_of_questions_by_line, -1, question, current_question, subtitle, user_answer, valid_answer)
            elif state == 5:
                num_correct_answers = sum(1 for user, valid in zip(user_answers, valid_answers) if user == valid)
                total_score = f"Total score: {num_correct_answers}/{number_of_questions}"
                stdscr.addstr(maxY // 2, maxX // 2 - len(total_score) // 2, total_score, curses.A_BOLD)
            stdscr.addstr(0, 0, "Press Q to quit", curses.color_pair(1))
        else:
            strInfo = "Please enlarge the terminal"
            stdscr.addstr(maxY // 2, maxX // 2 - len(strInfo) // 2, strInfo)

        stdscr.refresh()

        c = stdscr.getch()

    # terminate curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    return 0
