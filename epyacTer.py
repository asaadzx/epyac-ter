import json 
import subprocess
import requests  # Import requests to interact with the Ollama API
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

def add_task(question: str, answer: str):
    """Add a new task to the knowledge base."""
    knowledge_base = load_data('knowledge_base.json')
    tasks = knowledge_base.get("tasks", {})
    
    tasks[question] = answer
    knowledge_base["tasks"] = tasks
    save_data('knowledge_base.json', knowledge_base)
    print(f"Task '{question}' added successfully.")

def show_tasks():
    """Show all tasks in the knowledge base."""
    knowledge_base = load_data('knowledge_base.json')
    tasks = knowledge_base.get("tasks", {})
    
    if tasks:
        print("Tasks:")
        for task, answer in tasks.items():
            print(f"- {task}: {answer}")
    else:
        print("No tasks found.")

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

def run_ollama(prompt):
    """Send a prompt to the Ollama API and return the response."""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.2:latest",  # Adjust the model if necessary
        "prompt": prompt
    }
    
    try:
        response = requests.post(url, json=data, stream=True)  # Enable streaming
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Initialize a variable to accumulate the generated text
        generated_text = ""

        # Read the response in chunks
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_line = line.strip()
                    parsed_line = json.loads(json_line)  # Use json.loads instead of requests.json.loads
                    generated_text += parsed_line.get("response", "")
                except ValueError:
                    return f"Error: Unable to decode JSON line. Raw line: {json_line}"

        return generated_text if generated_text else "No response generated."
        
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"  # Print HTTP error
    except Exception as e:
        return f"An error occurred: {e}"

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
            print('  Type "addtask" to add a new task.')
            print('  Type "tasks" to show tasks.')
            continue

        if user_input.lower() == 'quit':
            print("Exiting Epyac AI. Goodbye!")
            break

        if user_input.lower() == 'tasks':
            show_tasks()
            continue

        if user_input.lower() == 'addtask':
            new_question = input("Enter new task: ").strip()
            new_answer = input("Enter answer for the new task: ").strip()
            add_task(new_question, new_answer)
            continue

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

        # Call the Ollama function and print the response
        response = run_ollama(user_input)
        print(f"Ollama says: {response}")

if __name__ == '__main__':
    epyac_bot()
