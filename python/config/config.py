import configparser

section_name = 'simpleconfig'
conf_path = 'test.ini'

class SimpleConfig(object):
    def __init__(self, conf_path, section_name):
        self.conf_path = conf_path
        self.section_name = section_name
        self._config = self._load_all()

    def load(self, key, default=None):
        try:
            v = self._config.get(section_name, key)
            return v
        except configparser.NoOptionError as e:
            return default
        except configparser.NoSectionError as e:
            return default

    def save(self, key, value):
        if not self.section_name in self._config:
            self._config.add_section(section_name)
        self._config.set(self.section_name, key, value)
        with open(self.conf_path, 'w') as f:
            self._config.write(f)

    def _load_all(self):
        config = configparser.ConfigParser()
        config.read(self.conf_path, 'UTF-8')
        return config

common_config = None
def _singleton_config():
    global common_config
    global gorup_name
    global conf_path
    if common_config is None:
        common_config = SimpleConfig(conf_path, section_name)
    return common_config

def load(key, default=None):
    c = _singleton_config()
    return c.load(key, default)

def save(key, value):
    c = _singleton_config()
    c.save(key, value)
