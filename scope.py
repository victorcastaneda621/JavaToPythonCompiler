from classes import *

class Scope:
    def __init__(self):
        self.all_classes = {}
        self.locals_stack = []
        self.current_class = None

    def register_class(self, class_node):
        fields = {m.name for m in class_node.member_list if isinstance(m, Field)}
        self.all_classes[class_node.name] = fields

    def enter_method(self, method_node):
        self.locals_stack = []
        new_scope = {p.name for p in method_node.params_list}
        self.locals_stack.append(new_scope)

    def add_local(self, var_name):
        if self.locals_stack:
            self.locals_stack[-1].add(var_name)

    def is_local(self, name):
        for scope in self.locals_stack:
            if name in scope:
                return True
        return False

    def is_field(self, name):
        if self.current_class in self.all_classes:
            return name in self.all_classes[self.current_class]
        return False