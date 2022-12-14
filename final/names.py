"""Map variable names and string names to unique integers.

Used in the Logic Simulator project. Most of the modules in the project
use this module either directly or indirectly.

Classes
-------
Names - maps variable names and string names to unique integers.
"""


from typing import Type, List


class Names:
    """Map variable names and string names to unique integers.

    This class deals with storing grammatical keywords and user-defined words,
    and their corresponding name IDs, which are internal indexing integers. It
    provides functions for looking up either the name ID or the name string.
    It also keeps track of the number of error codes defined by other classes,
    and allocates new, unique error codes on demand.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    unique_error_codes(self, num_error_codes): Returns a list of unique integer
                                               error codes.

    query(self, name_string): Returns the corresponding name ID for the
                        name string. Returns None if the string is not present.

    lookup(self, name_string_list): Returns a list of name IDs for each
                        name string. Adds a name if not already present.

    get_name_string(self, name_id): Returns the corresponding name string for
                        the name ID. Returns None if the ID is not present.
    """

    def __init__(self):
        """Initialise names list."""
        self.error_code_count = 0  # how many error codes have been declared
        # initialise a private list to store names
        self.__names_list = []

    def unique_error_codes(self, num_error_codes):
        """Return a list of unique integer error codes.

        Args
        num_error_codes - number of error codes present

        returns: list with unique integer error codes
        """
        if not isinstance(num_error_codes, int):
            raise TypeError("Expected num_error_codes to be an integer.")
        self.error_code_count += num_error_codes
        return range(self.error_code_count - num_error_codes,
                     self.error_code_count)

    def query(self, name_string):
        """Return the corresponding name ID for name_string.

        If the name string is not present in the names list, return None.

        Args:
        name_string - the name to be queried


        returns: the ID for name_string
        """
        if type(name_string) != str:
            raise TypeError
        if name_string in self.__names_list:
            return self.__names_list.index(name_string)
        else:
            return None

    def lookup(self, name_string_list):
        """Return a list of name IDs for each name string in name_string_list.

        If the name string is not present in the names list, add it.

        Args
        name_string_list - list of names to be looked up or added

        returns: a list of name IDs
        """
        results = []
        for name_string in name_string_list:
            if name_string in self.__names_list:
                results.append(self.__names_list.index(name_string))
            else:
                self.__names_list.append(name_string)
                # can do this return as the append will always be on the end
                results.append(len(self.__names_list) - 1)
        return results

    def get_name_string(self, name_id):
        """Return the corresponding name string for name_id.

        If the name_id is not an index in the names list, return None.

        Args:
        name_id: the ID of the name to be returned


        returns: the name corresponding to the ID
        """
        if type(name_id) != int:
            raise TypeError
        if name_id < len(self.__names_list):
            return self.__names_list[name_id]
        else:
            return None
