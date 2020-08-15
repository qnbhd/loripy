from .sandbox_exception import SandBoxException


class SandBox:
    cvs_table: dict
    functions_table: dict

    def __init__(self):
        self.cvs_table = dict()
        self.functions_table = dict()

    def add_variable(self, var_name, value):
        self.cvs_table[var_name] = value

    def add_function(self, function_name, function, function_keyword_args):
        self.functions_table[function_name] = {'function': function, 'args': function_keyword_args}

    def get_variable(self, variable):
        value = self.cvs_table.get(variable)
        if value is None:
            raise SandBoxException("Variable doesn't exception")
        return value

    def get_function(self, function):
        value = self.cvs_table.get(function)
        if value is None:
            raise SandBoxException("Function doesn't exception")
        return value

    def log(self):
        pass
