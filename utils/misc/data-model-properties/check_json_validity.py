import os
import json

def is_valid_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json.load(file)
            return True
    except (ValueError, UnicodeDecodeError):
        return False

def validate_json_files_in_folder(folder_path):

    with open("json_validity.txt", 'a') as out_file:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.jsonld'):
                    file_path = os.path.join(root, file_name)
                    if not is_valid_json(file_path):
                        out_file.write(f"{file_path}: Invalid JSON\n")

if __name__ == "__main__":
    folder_paths = ["../../../../agri-voc/data-models", "../../../../agri-voc/base-schemas", "../../../../agri-voc/examples"]
    output_file = "json_validity.txt"
    list(map(validate_json_files_in_folder, folder_paths))
    # validate_json_files_in_folder(folder_path, output_file)
    print(f"Validation results written to {output_file}")

