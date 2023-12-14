import os
import os
import json
import touch
class InMemoryFileSystem:
    def __init__(self):
        self.current_directory = '***add your parent directory absolute path here**'
        self.file_system = {}

    def mkdir(self, directory_name):
        path = os.path.join(self.current_directory, directory_name)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

    def cd(self, path):
        if path == '/':
            self.current_directory = '/'
        elif path.startswith('/'):
            self.current_directory = path
        else:
            new_path = os.path.join(self.current_directory, path)
            self.current_directory = os.path.normpath(new_path)

    def ls(self, path='.'):
        arr = os.listdir(self.current_directory)
        print(arr)



    def grep(self, pattern, file_path):
        abs_path = self.get_absolute_path(file_path)
        if abs_path not in self.file_system or not self.file_system[abs_path]:
            print("File not found or empty.")
            return

        file_content = self.file_system[abs_path]
        matching_lines = [line for line in file_content if pattern in line]
        for line in matching_lines:
            print(line)

    def cat(self, file_path):
        with open(file_path, 'r') as f:
            print(f.read())


    def touch(self, file_path):
        touch.touch(file_path)

    def echo(self, text, file_path):
        abs_path = self.ls(self.current_directory)
        if file_path not in abs_path:
            print("File not found.")
            return

        self.file_system[abs_path].append(text)

    def mv(self, source_path, dest_path):
        source_abs_path = self.get_absolute_path(source_path)
        dest_abs_path = self.get_absolute_path(dest_path)

        if source_abs_path not in self.file_system:
            print("Source path not found.")
            return

        self.file_system[dest_abs_path] = self.file_system.pop(source_abs_path)

    def cp(self, source_path, dest_path):
        source_abs_path = self.get_absolute_path(source_path)
        dest_abs_path = self.get_absolute_path(dest_path)

        if source_abs_path not in self.file_system:
            print("Source path not found.")
            return

        self.file_system[dest_abs_path] = self.file_system[source_abs_path].copy()

    def rm(self, path):
        abs_path = self.get_absolute_path(path)
        if abs_path not in self.file_system:
            print("Path not found.")
            return

        del self.file_system[abs_path]

    def get_absolute_path(self, path):
        if path.startswith('/'):
            return path
        else:
            return os.path.normpath(os.path.join(self.current_directory, path))

    def save_state(self, save_path):
        with open(save_path, 'w') as file:
            json.dump(self.file_system, file)
        print(f"File system state saved to {save_path}")

    def load_state(self, load_path):
        if os.path.exists(load_path):
            with open(load_path, 'r') as file:
                self.file_system = json.load(file)
            print(f"File system state loaded from {load_path}")
        else:
            print(f"No state file found at {load_path}")

if __name__ == "__main__":
    file_system = InMemoryFileSystem()

    while True:
        user_input = input("Enter command: ")
        if user_input.lower() == 'exit':
            break

        try:
            command, *args = user_input.split()
            if command == 'save_state':
                file_system.save_state(args[0])
            elif command == 'load_state':
                file_system.load_state(args[0])
            elif command == 'ls' and not args:
                file_system.ls()
            else:
                getattr(file_system, command)(*args)
        except Exception as e:
            print(f"Error: {e}")