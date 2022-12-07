from functools import partial

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


def get_full_file_path_for_folder(dir: folder, path="") -> str:

    path = f"{path}/{dir.foldername}"

    if dir.foldername == "/":
        return path
    else:
        return get_full_file_path_for_folder(dir.parent, path)


all_nums = {}
def check_part_one_criteria_on_dir(dir: folder, filter_num:int):
    if dir.dir_size <= filter_num:
        num = dir.dir_size
    else:
        num = 0
    dir_list = []
    for i in dir.dirs:
        dir_list.append(dir.dirs[i])
    all_nums[get_full_file_path_for_folder(dir=dir, path="")] = num
    if len(dir_list) != 0:
        list(map(partial(check_part_one_criteria_on_dir, filter_num=filter_num), dir_list))

check_part_one_criteria_on_dir(FS.system,100000)

check_part_one_criteria_on_dir(FS.system,7000000000000)

print(all_nums)
