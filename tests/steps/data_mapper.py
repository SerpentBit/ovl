class Group:
    def __init__(self, data=None):
        self.data = data or {}
        if "data" in data.keys():
            raise KeyError("Group cannot contain a key 'data'")

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        if item == "data":
            return self.data
        return self.data[item]


class DataMapper:
    def __init__(self, groups=None):
        self.data_groups = groups or {}

    @property
    def groups(self):
        return self.data_groups

    def __setitem__(self, key, value):
        self.data_groups[key] = value
