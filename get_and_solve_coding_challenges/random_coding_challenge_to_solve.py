from os import listdir, system, path
from sys import argv
from random import randrange


def ask_question(commandline: list, question_index: int, question: str, question_list: list[str]) -> str:
    try:
        answer = (int(commandline[question_index]) if int(commandline[question_index]) <= len(question_list) else 0)
    except ValueError:
        answer = 0
    except IndexError:
        print(f"{question}")
        for index, value in enumerate(question_list):
            print(f"{index}: {value}")
        try:
            user_input = int((input()))
        except ValueError:
            user_input = 0
        answer = user_input if user_input <= len(question_list) else 0
    if answer == 0:
        answer = randrange(1, len(question_list))
    return question_list[answer]


def main(args):
    questions = ["What website do you want a problem from?",
                 "What difficulty do you want to solve?",
                 "What language do you want to use?",
                 "What IDE do you use?"]
    if not path.isdir("./PROBLEMS"):
        print("There is no scraped problems to solve!")
        return
    question = ["random"] + listdir("./PROBLEMS")
    if len(question) < 2:
        print("There is no scraped problems to solve!")
        return
    website = ask_question(args, 0, questions[0], question)
    question = ["random"] + listdir(f"./PROBLEMS/{website}")
    if len(question) < 2:
        print(f"There is no scraped {website} problems to solve!")
        return
    difficulty = ask_question(args, 1, questions[1], question)
    if not path.isdir("./TEMPLATES"):
        print("There is no templates to create a problem from!")
        return
    question = listdir("./TEMPLATES")
    if len(question) < 1:
        print("There is no templates to create a problem from!")
        return
    for index, language in enumerate(question):
        question[index] = language.split(".")[-1]
    question.insert(0, "random")
    language = ask_question(args, 2, questions[2], question)
    question = ["random", "codium", "code", "subl", "atom", "vim"]
    ide = ask_question(args, 3, questions[3], question)
    try:
        solved = [s.split(".")[0] for s in listdir("./SOLVED/")]
        problems = [p.split(".")[0] for p in listdir(f"./PROBLEMS/{website}/{difficulty}/") if p.split(".")[0] not in solved]
        problem = problems[randrange(0, len(problems))]
        with open(f"./TEMPLATES/template.{language}", "r", encoding="utf-8") as file:
            template = file.readlines()
        with open(f"./PROBLEMS/{website}/{difficulty}/{problem}.md", "r", encoding="utf-8") as file:
            description = file.readlines()
        with open(f"./{problem}.{language}", "w", encoding="utf-8") as file:
            file.writelines(template[0])
            file.writelines(description)
            file.writelines(template[2:])
        system(f"{ide} ./{problem}.{language}")
    except ValueError:
        print(f"Already solved all {difficulty} problems from {website}")
    except FileNotFoundError:
        print(f"Invalid options. Could not open ./PROBLEMS/{website}/{difficulty}/")


if __name__ == "__main__":
    main(argv[1:])
