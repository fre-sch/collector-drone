from UserDict import UserDict


class DotDict(UserDict):

    def __getitem__(self, name):
        if name in self:
            return UserDict.__getitem__(self, name)

        current_data = self
        for chunk in name.split('.'):
            if chunk not in current_data:
                return None
            current_data = current_data[chunk]
        return current_data
