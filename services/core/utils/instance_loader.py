import importlib


def get_instance(full_path):
    class_name = full_path.split(".")[-1]
    path = full_path[: -(len(class_name) + 1)]
    module = importlib.import_module(path)
    class_ = getattr(module, class_name)
    instance = class_()
    return instance
