class cmd():
    def __init__(self, compiler: str):
        self.compiler = compiler
        self.source_files = []
        self.out = ""
        self.flags = []
        self.includes = []
