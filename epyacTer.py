import json
import subprocess
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

def open_program(program_name: str):
    """Open a program using its command."""
    knowledge_base = load_data('knowledge_base.json')
    programs = knowledge_base.get("programs", {})
    
    command = programs.get(program_name)
    if command:
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"Opening {program_name}...")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open {program_name}: {e}")
    else:
        print(f"Program '{program_name}' not found.")

def add_program(program_name: str, command: str):
    """Add a new program to the knowledge base."""
    knowledge_base = load_data('knowledge_base.json')
    programs = knowledge_base.get("programs", {})
    
    programs[program_name] = command
    knowledge_base["programs"] = programs
    save_data('knowledge_base.json', knowledge_base)
    print(f"Program '{program_name}' added successfully.")

def culc(user_input: str):
    """Perform arithmetic calculations based on user input."""
    if user_input.lower() == 'culc':
        while True:
            print("Please write a mathematical operation.")
            print("Enter 'quit' to exit the calculator.")
            try:
                first_value = float(input("Enter first value: "))
                operation = input("Enter operation (+, -, *, /, %): ").strip()
                second_value = float(input("Enter second value: "))
                
                if operation == "+":
                    result = first_value + second_value
                elif operation == "-":
                    result = first_value - second_value
                elif operation == "*":
                    result = first_value * second_value
                elif operation == "/":
                    result = first_value / second_value
                elif operation == "%":
                    result = first_value % second_value
                else:
                    print("Invalid operation.")
                    continue
                
                print(f"Result: {result}")
            except ValueError:
                print("Invalid input. Please enter numerical values.")
            except ZeroDivisionError:
                print("Division by zero is not allowed.")
            
            if input("Type 'quit' to exit or press Enter to continue: ").strip().lower() == 'quit':
                break

def epyac_bot():
    """Main function for the Epyac AI chatbot."""
    knowledge_base = load_data('knowledge_base.json')

    print("Welcome to Epyac AI! Type 'help' for commands or 'quit' to exit.")
    
    while True:
        user_input = input('>>> ').strip()

        if user_input.lower() == 'help':
            print('Commands:')
            print('  "quit" to exit')
            print('  Type your question to get a response.')
            print('  Type "add" to add a new question and answer.')
            print('  Type "culc" to calculate the result of the arithmetic expression.')
            print('  Type "open" to open a program.')
            print('  Type "addprog" to add a new program.')
            continue

        if user_input.lower() == 'quit':
            print("Exiting Epyac AI. Goodbye!")
            break

        if user_input.lower() == 'culc':
            culc(user_input)
            continue

        if user_input.lower().startswith('open '):
            program_name = user_input[5:].strip()
            open_program(program_name)
            continue

        if user_input.lower().startswith('addprog '):
            _, program_name, command = user_input.split(maxsplit=2)
            add_program(program_name, command)
            continue

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
                new_answer = input("Type the answer or 'skip' to ignore: ").strip()
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
