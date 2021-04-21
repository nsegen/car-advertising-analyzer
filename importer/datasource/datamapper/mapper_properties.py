class BaseProperty:
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        self.check_value(instance)
        
        return instance.__dict__[self._name]

    def check_value(self, instance):
        pass

class SimpleProperty(BaseProperty):
    def __init__(self, source_path):
        self._source_path = source_path

    def check_value(self, instance):
        if self._name not in instance.__dict__:
            instance.__dict__[self._name] = instance.parser.get_value(self._source_path)
    
class CompositeProperty(BaseProperty):
    def __init__(self, sources_path):
        self._sources_path = sources_path

    def check_value(self, instance):
        if self._name in instance.__dict__:
            return
        parsed_value = {}

        for dest, src in self._sources_path:
            parsed_value[dest] = instance.parser.get_value(src)        
        instance.__dict__[self._name] = parsed_value
