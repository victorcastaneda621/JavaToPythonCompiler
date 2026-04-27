from classes import *

class Scope:
    def __init__(self):
        self.all_classes = {}
        self.locals_stack = []
        self.current_class = None

    def register_class(self, class_node):
        fields = {m.name for m in class_node.member_list if isinstance(m, Field)}
        self.all_classes[class_node.name] = {
            "fields": fields,
            "parent": class_node.parent if class_node.parent != '_no_set' else None
        }

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

    def is_field(self, name, c_class=None):
        if not c_class:
            c_class = self.current_class
        
        if c_class not in self.all_classes:
            return False
            
        if name in self.all_classes[c_class]["fields"]:
            return True
            
        parent_class = self.all_classes[c_class]["parent"]
        if parent_class:
            return self.is_field(name, parent_class)
            
        return False