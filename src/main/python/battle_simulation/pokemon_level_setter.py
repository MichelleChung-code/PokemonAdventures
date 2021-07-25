# Just committing how to use @property to achieve getter and setter

class PokemonLevel:
    def __init__(self):
        self._level = 1

    @property
    def level(self):
        """ getter function for level """
        return self._level

    @level.setter
    def level(self, lvl):
        """ setter function for level """
        val_bool = (1 <= lvl <= 100) and (isinstance(lvl, int))
        if not val_bool:
            raise ValueError('Level must be an integer between 1 and 100')
        self._level = lvl


if __name__ == '__main__':
    zzz = PokemonLevel()
    zzz.level = 10
    print(zzz.level)
