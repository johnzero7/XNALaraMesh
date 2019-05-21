# <pep8 compliant>

"""ASCII operations module."""


def readline(file):
    """Read a line and strip spaces."""
    line = file.readline()
    line = line.strip()
    return line


def getFloat(value):
    """Read value and returns a float. If error return NaN."""
    if value:
        try:
            return float(value)
        except ValueError:
            return float('NaN')
    return value


def getInt(value):
    """Read value and returns a int. If error return None."""
    try:
        return int(value)
    except ValueError:
        return None


def ignoreComment(line):
    """Read line. Ignore comment."""
    line = line.replace('#', ' ')
    line = line.split()[0]
    return line


def ignoreStringComment(line):
    """Read line. Ignore comment."""
    line = line.split('#')[0].strip()
    return line


def readInt(file):
    """Read line. Return Int."""
    line = readline(file)
    value = ignoreComment(line)
    number = getInt(value)
    return number


def readString(file):
    """Read line. Ignore Comments."""
    # String Lenght
    line = readline(file)
    string = ignoreStringComment(line)
    return string


def splitValues(line):
    """Read line. Return value list."""
    line = line.replace('#', ' ')
    values = line.split()
    return values
