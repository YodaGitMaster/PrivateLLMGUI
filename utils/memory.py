import os
from datetime import datetime
import yaml
import re
class ChatMemory:
    def __init__(self):
        self.log_folder = 'chats'
        self.config_folder = 'configs'

    def write_to_file(self, message, title):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        title =  re.sub(r'[^a-zA-Z0-9\s]', ' ', title)
        print(title)
        self.log_filename = f'{title} {current_datetime}.log'
        self.log_filepath = os.path.join(self.log_folder, self.log_filename)

        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        with open(self.log_filepath, 'a') as file:
            file.write(f"{message}\n")

    def list_log_files(self):
        if not os.path.exists(self.log_folder):
            return []

        log_files = [file for file in os.listdir(self.log_folder) if file.endswith('.log')]
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.log_folder, x)), reverse=True)
        return log_files

    def read_log_file(self, log_file):
        log_filepath = os.path.join(self.log_folder, log_file)

        if not os.path.exists(log_filepath):
            return f"Log file '{log_file}' not found."

        with open(log_filepath, 'r') as file:
            content = file.read()
            return content

    def list_configurations(self):
        if not os.path.exists(self.config_folder):
            return []

        config_files = [file for file in os.listdir(self.config_folder) if file.endswith('.yaml')]
        config_names = [os.path.splitext(file)[0].capitalize() for file in config_files]
        return config_names

    def read_configuration(self, config_name):
        config_filename = f"{config_name.lower()}.yaml"
        config_filepath = os.path.join(self.config_folder, config_filename)

        if not os.path.exists(config_filepath):
            return f"Configuration file '{config_filename}' not found."

        with open(config_filepath, 'r') as file:
            config_content = yaml.safe_load(file)
            return config_content
