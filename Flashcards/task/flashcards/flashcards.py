import json
import os
import sys
from random import randint
from io import StringIO
import argparse


class Card:

    def __init__(self, term, definition):
        self.term = term
        self.definition = definition
        self.mistakes = 0

    def print_term(self):
        print(self.term)

    def print_definition(self):
        print(self.definition)

    def get_definition(self):
        return self.definition

    def get_term(self):
        return self.term

    def get_mistakes(self):
        return self.mistakes

    def set_mistakes(self, amount):
        self.mistakes = amount

    def mistake_made(self):
        self.mistakes = self.mistakes + 1


def create_new_card(num):
    global cards
    print("The term for card #" + str(num) + ":")
    duplicate_term = True

    while duplicate_term:
        term = input()
        if len(cards) == 0:
            break
        duplicate_term = False
        for card in cards:
            if card.get_term() == term:
                print('The term "' + card.get_term() + '" already exists. Try again:')
                duplicate_term = True
    print("The definition for card #" + str(num) + ":")

    duplicate_definition = True
    while duplicate_definition:
        definition = input()
        if len(cards) == 0:
            break

        duplicate_definition = False
        for card in cards:
            if card.get_definition() == definition:
                print('The definition "' + card.get_definition() + '" already exists. Try again:')
                duplicate_definition = True

    new_card = Card(term, definition)
    cards.append(new_card)
    print('The pair ("{}":"{}") has been added'.format(term, definition))


def remove_specific_card():
    global cards

    print_and_log("Which card?")
    card_to_remove = input()
    log_action(card_to_remove)

    for card in cards:
        if card.get_term() == card_to_remove:
            cards.remove(card)
            print_and_log("The card has been removed")
            return

    print_and_log("Can't remove '{}': there is no such card.".format(card_to_remove))


def evaluate_specific_card(number):
    valid_answer_found = False
    print_and_log('Print the definition of "' + cards[number - 1].get_term() + '":')
    user_input = input()
    log_action(user_input)
    if user_input == cards[number - 1].get_definition():
        print_and_log("Correct!")
    else:

        cards[number - 1].mistake_made()

        for card in cards:
            if card.get_definition() == user_input:
                print_and_log('Wrong. The right answer is "' + cards[
                    number - 1].get_definition() + '", but your definition is correct for "' + card.get_term() + '".')
                valid_answer_found = True
        if not valid_answer_found:
            print_and_log("Wrong. The right answer is " + cards[number - 1].get_definition() + ".")


def import_from_file(file_name=""):
    if file_name == "" or file_name is None:
        print_and_log("File name:")
        file_name = input()
        log_action(file_name)

    if not os.path.isfile(file_name):
        print_and_log("File not found.")
        return

    with open(file_name, "r") as import_file:
        import_dict = json.load(import_file)

        count = 0
        for item in import_dict:
            term = item.get("term")
            definition = item.get("definition")
            mistakes = item.get("mistakes")
            temp_card = Card(term, definition)
            temp_card.set_mistakes(mistakes)

            contained = False
            for card in cards:
                if card.get_term() == term:
                    contained = True
            if not contained:
                cards.append(temp_card)
            count = count + 1

        print_and_log("{} cards have been loaded.".format(str(count)))


def obj_dict(obj):
    return obj.__dict__


def create_log():
    print_and_log("File name:")
    file = input()
    log_action(file)
    with open(file, "w") as opened_file:
        opened_file.write(mem_file.getvalue())
    print_and_log("The log has been saved.")


def export_to_file(file_name=""):
    if file_name == "" or file_name is None:
        print_and_log("File name:")
        file_name = input()
        log_action(file_name)
    with open(file_name, "w") as export_file:
        json.dump(cards, export_file, default=obj_dict)
        print_and_log("{} cards have been saved.".format(str(len(cards))))


def create_single_card():
    global cards, mem_file
    duplicate_term = True
    print_and_log("The card:")
    while duplicate_term:

        term = input()
        log_action(term)
        if len(cards) == 0:
            break

        duplicate_term = False
        for card in cards:
            if card.get_term() == term:
                print_and_log("The card {} already exists. Try again:".format(term))
                duplicate_term = True

    print_and_log("The definition of the card:")
    duplicate_definition = True
    while duplicate_definition:
        definition = input()
        log_action(definition)
        if len(cards) == 0:
            break
        duplicate_definition = False
        for card in cards:
            if card.get_definition() == definition:
                print_and_log("The definition {} already exists. Try again:".format(definition))
                duplicate_definition = True

    temp_card = Card(term, definition)
    cards.append(temp_card)
    print_and_log('The pair ("{}:{}") has been added'.format(term, definition))


def ask_multiple(amount_to_ask):
    for count in range(0, amount_to_ask):
        card_number = randint(0, len(cards))
        evaluate_specific_card(card_number)


def print_and_log(param):
    global mem_file
    mem_file.write(param + "\n")
    print(param)


def log_action(string):
    mem_file.write(string + "\n")


def initialize_program():
    global args
    parser = argparse.ArgumentParser(description="This program imports and exports flashcards")
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")

    args = parser.parse_args()

    if args.import_from is not None:
        import_from_file(args.import_from)


cards = list()
mem_file = StringIO()

initialize_program()

while True:
    print_and_log("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")

    user_action = input()
    log_action(user_action)

    if user_action == "exit":
        if args.export_to is not None:
            export_to_file(args.export_to)
        print_and_log("Bye bye!")
        sys.exit()

    if user_action == "add":
        create_single_card()

    if user_action == "add_multiple":
        print_and_log("Input the number of cards:")
        amount_to_create = int(input())
        log_action(amount_to_create)

        for i in range(1, amount_to_create + 1):
            create_new_card(i)

    if user_action == "remove":
        remove_specific_card()

    if user_action == "import":
        import_from_file()

    if user_action == "ask":
        print_and_log("How many times to ask?")
        amount_to_ask = int(input())
        log_action(str(amount_to_ask))
        ask_multiple(amount_to_ask)

    if user_action == "export":
        export_to_file()

    if user_action == "reset stats":
        for card in cards:
            card.set_mistakes(0)
        print_and_log("Card statistics have been reset.")

    if user_action == "log":
        create_log()

    if user_action == "hardest card":
        hardest_cards = list()
        hardest_cards.clear()
        most_mistakes = -1
        for card in cards:
            if card.get_mistakes() > most_mistakes:
                most_mistakes = card.get_mistakes()

        for card in cards:
            if card.get_mistakes() == most_mistakes and card.get_mistakes() != 0:
                hardest_cards.append(card)

        if len(hardest_cards) == 0:
            print_and_log('There are no cards with errors.')

        if len(hardest_cards) == 1:
            print_and_log('The hardest card is "{term}". You have {n} errors answering it'.format(
                term=hardest_cards[0].get_term(), n=hardest_cards[0].get_mistakes()))

        if len(hardest_cards) > 1:
            print("The hardest cards are ", end="")
            mem_file.write("The hardest cards are ")

            counter = 0
            for card in hardest_cards:
                if counter != 0:
                    print(",", end="")
                    mem_file.write(",")
                print('"{}"'.format(card.get_term()), end="")
                mem_file.write('"{}", '.format(card.get_term()))
                counter = counter + 1
            print(".")
            mem_file.write(".")
