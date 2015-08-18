class Phase:
    """This class serves as a layer of abstraction around phases during a script's execution.
    Each instance represents a "phase" of an install process.

    :param name: The name of this phase.
    :param method: The method for this phase.
    """

    def __init__(self, method, name):
        self._method = method
        self._name = name

    def name(self):
        """Gives the pretty name for this phase.

        :return: A string with the name of this phase plus " Phase"
        """
        return "{0} Phase".format(self._name)

    def method(self):
        """Exposes the method for this phase for calling

        :return: The stored method for this phase.
        """
        return self._method

    def hides(self, subject, directObject):
        """Detects if the subject hides the direct object. Does some metaprogramming gymnastics to get there.

        :param subject: The class that does the hiding.
        :param directObject: The class that gets hidden.

        :returns: Boolean if the directobject had its method hidden.
        """
        return getattr(subject, self._method.__name__) is not getattr(directObject, str(self._method.__name__))
