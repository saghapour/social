class Bunchify:
    def __init__(self, dictionary: dict):
        self.__allkeys = []
        self.__dict = dictionary
        self.__bunchify(dictionary)

    def __bunchify(self, d: dict):
        for k, v in d.items():
            if isinstance(v, dict):
                setattr(self, k, Bunchify(v))
                self.__allkeys.append(k)
            else:
                setattr(self, k, v)
                self.__allkeys.append(k)

    def keys(self):
        return self.__allkeys

    def has_key(self, key):
        return key in self.__dict.keys()

    def __getitem__(self, item):
        if item not in self.__dict.keys():
            raise ValueError(f"{item} is not in config file.")
        return self.__getattribute__(item)

    def get(self, path):
        pass
