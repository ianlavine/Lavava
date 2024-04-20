import pytest

def track_changes(*attribute_names):
    def class_decorator(cls):
        original_init = cls.__init__

        def make_getter(attribute_name):
            storage_name = '_' + attribute_name
            def getter(self):
                return getattr(self, storage_name)
            return getter

        def make_setter(attribute_name):
            storage_name = '_' + attribute_name
            def setter(self, value):
                self.tracked_attributes.add(attribute_name)
                setattr(self, storage_name, value)
            return setter

        for attribute_name in attribute_names:

            # Setting the property on the class
            getter_func = make_getter(attribute_name)
            setter_func = make_setter(attribute_name)
            setattr(cls, attribute_name, property(getter_func, setter_func))

        # Modify the __init__ to initialize properties
        def new_init(self, *args, **kwargs):
            self.tracked_attributes = set()

            for attribute_name in attribute_names:
                storage_name = '_' + attribute_name
                setattr(self, storage_name, None)

            original_init(self, *args, **kwargs)
            self.clear()

        def clear(self):
            self.tracked_attributes.clear()
        
        cls.__init__ = new_init
        cls.clear = clear
        return cls
    
    return class_decorator

class ReferenceClass:
    def __init__(self):
        self.var = 0

@track_changes("base_variable", "reference")
class BaseClass(JsonableTracked):
    def __init__(self, reference: ReferenceClass):
        self.base_variable = 0
        self.reference = reference
        self.untracked = "hello"

@track_changes("child_variable")
class ChildClass(BaseClass):
    def __init__(self, reference: ReferenceClass):
        super().__init__(reference)
        self.child_variable = 0
        self.bean = "beani"

def test_base_class():
    ref = ReferenceClass()
    base = BaseClass(ref)

    base.base_variable = 5
    base.reference.var = 5
    assert base.tracked_attributes == {"base_variable"}

    base.clear()
    base.reference = ReferenceClass()
    base.untracked = "hi"
    assert base.tracked_attributes == {"reference"}


def test_child_class():
    ref = ReferenceClass()
    child = ChildClass(ref)

    child.base_variable = 5
    child.child_variable = 5
    assert child.tracked_attributes == {"base_variable", "child_variable"}

    child.clear()
    assert child.tracked_attributes == set()