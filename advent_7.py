import time

# #
# class base_dir():
#     # content:
#     dir_name: str

#     def __init__(self, dir_name: str):
#         self.dir_name = dir_name
#         self.content: dir_content = {}

#     def cd(target:str):
#         pass

#     def ls():
#         pass

#     @property
#     def folder_size(self):
#         pass


# class folder(base_dir):

#     def __init__(self, dir_name: str):
#         super().__init__(dir_name=dir_name)
#         self.parent

# dir_content = dict[str, folder]

# class input_component(TypedDict):
#     command: str
#     target: str


# class parser():

#     current_dir: folder | base_dir

#     def __init__(self, start_folder: str = "/"):
#         self.current_folder = base_dir(start_folder)
#         pass

#     def parse_input(self, input: str):
#         inputs =  input.split(" ")
#         parsed_input: input_component = input_component(command=inputs[0], target=)


#     def handle_cd(input: str):
#         pass

#     def handle_dir(input: str):
#         pass

#     def handle_ls(input:str):
#         pass


with open("advent_7.txt", "r") as f:
    d = f.read().splitlines()

# will use this just to have file name to reference, and size, could just be a dict really, but want it nice and static and easily typed
class file:
    # obvious properties
    filename: str
    size: int
    parent: str

    def __init__(self, filename, size, parent):
        self.filename = filename
        self.size = size
        self.parent = parent

class folder:
    foldername: str
    files: dict[str, file]
    dirs: dict

    def __init__(self, foldername, parent):
        self.foldername = foldername
        self.parent = parent
        self.files = {}
        self.dirs = {}

    @property
    def dir_size(self):
        size = 0
        for file in self.files:
            size += self.files[file].size

        for dira in self.dirs:
            size += self.dirs[dira].dir_size
        
        return size



class file_system:
    system: folder
    cwd: folder

    def __init__(self):
        self.system = folder(foldername="/", parent=None)
        self.cwd = self.system

    def handle_dir(self, output: str):
        split_output = output.split(" ")

        dir_type = split_output[0]
        dir_name = split_output[1]
        parent = self.cwd

        parent.dirs[dir_name] = (folder(foldername=dir_name, parent=parent))

    def handle_file(self, output: str):
        split_output = output.split(" ")

        file_size = split_output[0]
        file_name = split_output[1]
        parent = self.cwd

        parent.files[file_name] = (file(filename=file_name, size=int(file_size), parent=parent))



    def handle_cd(self, target: str):
        if target == "..":
            self.cwd = self.cwd.parent
        elif target == "/":
            self.cwd = self.system
        else:
            try:
                self.cwd = self.cwd.dirs[target]
            except:
                self.cwd.dirs.append(folder(foldername=target, parent=self.cwd))
                self.cwd = self.cwd.dirs

    # think it's kind of fine doing nothing really
    def handle_ls(self):
        pass

    def handle_input(self, input: str):
        split_input = input.split(" ")

        if split_input[1] == "cd":
            self.handle_cd(split_input[2])
        elif split_input[1] == "ls":
            self.handle_ls()
        else:
            print("INVALID INPUT")


FS = file_system()

# this is like the mock cmd lol
for i in d:
    # for inputs
    if (i[0] == "$"):
        FS.handle_input(i)
    # for outputs
    else:
        # so we can figure out what we're dealing with easy
        prefix = i.split(" ")[0]
        # if we encounter a dir
        if prefix == "dir":
            FS.handle_dir(i)
        # or a file
        else:
            FS.handle_file(i)

print("done loading file system")


all_nums = []
global last_called_dir
last_called_dir = ""
def check_part_one_criteria_on_dir(dir: folder):
    global last_called_dir
    # time.sleep(1)
    print("*****")
    print("")
    print(f"LAST CALLED DIR IS {last_called_dir}")
    print("")
    print(f"READING SIZE FOR {dir.foldername}")
    if dir.dir_size <= 100000:
        num = dir.dir_size
    else:
        num = 0
    # time.sleep(1)
    print("")
    print(f"SIZE IS {num}")
    dir_list = []
    for i in dir.dirs:
        dir_list.append(dir.dirs[i])
    
    # time.sleep(1)
    print("")
    print(f"FOUND SUBDIRECTORIES: {dir_list}")
    all_nums.append(num)
    print("*****")
    last_called_dir = dir.foldername
    # time.sleep(1)
    if len(dir_list) != 0:
        print(f"FINDING SIZE FOR SUBDIRECTORIES")
        list(map(check_part_one_criteria_on_dir, dir_list))

check_part_one_criteria_on_dir(FS.system)

print(all_nums)
