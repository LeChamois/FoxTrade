import json
import tabulate

def load_json_content(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)
    
def show_table(data: list[dict]):
    print(tabulate.tabulate(data, headers='keys', tablefmt='grid'))