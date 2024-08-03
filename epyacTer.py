import json
from difflib import get_close_matches
from typing import List, Optional, Dict

def load_data(file_path: str) -> Dict:
    """Load the knowledge base from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_data(file_path: str, data: Dict):
    """Save the knowledge base to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    """Find the best matching question from the knowledge base."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None

def get_response(question: str, knowledge_base: Dict) -> Optional[str]:
    """Get the response for a specific question."""
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def find_best_match_task(user_question: str, questions: List[str]) -> Optional[str]:
    """Find the best matching question from the knowledge base."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None


def get_task(question: str, knowledge_base: Dict) -> Optional[str]:
    """Get the response for a specific question."""
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

#def add_task(user_input):
#        knowledge_base = load_data('knowledge_base.json')
#        if user_input.lower() == 'addtsk':
#            while True:    
#                print("please write the task ")
#                print("Enter 'quit' to exit the program in task!!! please")
#                task_value = (input("Enter task : ")).strip()
#                task_date = (input("Enter the date  : ")).strip()
#                best_match = find_best_match(user_input, [q["task"] for q in knowledge_base["questions"]])
#                knowledge_base["questions"].append({"task": task_value, "in_task": task_date})
#                if best_match:
#                    answer = get_response(best_match, knowledge_base)
#                    print(f'epyac: <<< {answer}')
#                save_data('knowledge_base.json', knowledge_base)
#                print("New task added successfully!")
#                if task_value or task_date  == "quit":
#                   break
#                print('type addtsk for it again ')

def culc(user_input):
        if user_input.lower() == 'culc':
            while True:    
                print("please write mathematical process: ")
                print("Enter 'quit' to exit the program in oberations!!! please")
                first_value = float(input("Enter first value: "))
                oberation = (input("Enter oberation like + - * / % : "))
                second_value = float(input("Enter second value: "))
                if oberation == "+":
                    result = first_value + second_value
                elif oberation == "-":
                    result = first_value - second_value
                elif oberation == "*":
                    result = first_value * second_value
                elif oberation == "/":
                    result = first_value / second_value
                elif oberation == "%":
                    result = first_value % second_value
                elif oberation or str(second_value) or str(first_value) == "quit":
                    break
                print(result)


def epyac_bot():
    knowledge_base = load_data('knowledge_base.json')

    print("Welcome to Epyac AI! Type 'help' for commands or 'quit' to exit.")
    
    while True:
        user_input = input('>>>  ').strip()

        if user_input.lower() == 'help':
            print('Commands:')
            print('  "quit" to exit')
            print('  Type your question to get a response.')
            print('  Type "add" to add a new question and answer.')
            print('  Type "culc" to calculate the result of the arithmetic expression.')
            continue

        if user_input.lower() == 'quit':
            print("Exiting Epyac AI. Goodbye!")
            break

        if user_input.lower() == 'culc':
            culc(user_input)

        #if user_input.lower() == 'addtsk':   Error in here
        #    add_task(user_input)
            
        if user_input.lower() == 'add':
            new_question = input("Enter new question: ").strip()
            new_answer = input("Enter answer for the new question: ").strip()
            knowledge_base["questions"].append({"question": new_question, "answer": new_answer})
            save_data('knowledge_base.json', knowledge_base)
            print("New question added successfully!")
            continue

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_response(best_match, knowledge_base)
            print(f'epyac: <<< {answer}')
        else:
            print("I don't know the answer. Would you like to add it? (yes/no)")
            add_response = input(">>> ").strip().lower()
            if add_response == 'yes':
                new_answer = input("Type the answer or 'skip' to ignore:  ").strip()
                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_data('knowledge_base.json', knowledge_base)
                    print("epyac: Thanks! I have added a new response.")
                else:
                    print("epyac: Response skipped.")
            else:
                print("epyac: Okay, let me know if you have any questions.")

if __name__ == '__main__':
    epyac_bot()