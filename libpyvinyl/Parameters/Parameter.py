# Created by Mads Bertelsen and modified by Juncheng E

import math
from libpyvinyl.AbstractBaseClass import AbstractBaseClass


class Parameter(AbstractBaseClass):
    """
    Description of a single parameter
    """

    def __init__(self, name, unit=None, comment=None):
        """
        Creates parameter with given name, optionally unit and comment
        """
        self.name = name
        self.unit = unit
        self.comment = comment
        self._value = None
        self._intervals = []
        self._intervals_are_legal = None
        self._options = []
        self._options_are_legal = None

    @classmethod
    def from_dict(cls, param_dict):
        param = cls(param_dict["name"], param_dict["unit"], param_dict["comment"])
        for key in param_dict:
            param.__dict__[key] = param_dict[key]
        return param

    def add_interval(self, min_value, max_value, intervals_are_legal):
        """
        Sets an interval for this parameter: [min_value, max_value]
        The interval is closed on both sides: min_value and and max_value are included.

        :param min_value: minimum value of the interval
        :type min_value: float or None for infinite

        :param max_value: maximum value of the interval
        :type max_value: float or None for infinite

        :param intervals_are_legal: if not done previously, it defines if all the intervals of this parameter should be considered as allowed or forbidden intervals.
        :type intervals_are_legal: boolean

        """

        if self._intervals_are_legal is None:
            self._intervals_are_legal = intervals_are_legal
        else:
            if self._intervals_are_legal != intervals_are_legal:
                print("WARNING: All intervals should be either legal or illegal.")
                print(
                    "         Interval: ["
                    + str(min_value)
                    + ":"
                    + str(max_value)
                    + "] is declared differently w.r.t. to the previous intervals"
                )
                # should it throw an expection?
                raise ValueError("Parameter", "interval", "multiple validities")

        if min_value is None:
            min_value = -math.inf
        if max_value is None:
            max_value = math.inf

        self._intervals.append([min_value, max_value])

    def add_option(self, option, options_are_legal):
        """
        Sets allowed values for this parameter
        """
        if self._options_are_legal is None:
            self._options_are_legal = options_are_legal
        else:
            if self._options_are_legal != options_are_legal:
                print("WARNING: All options should be either legal or illegal.")
                print(
                    "         This option is declared differently w.r.t. to the previous ones"
                )
                # should it throw an expection?
                raise ValueError("Parameter", "options", "multiple validities")

        if isinstance(option, list):
            self._options += option
        else:
            self._options.append(option)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets value of this parameter if value is legal, otherwise warning is shown

        This could be expanded to raise an exception, or such could be in is_legal
        """
        if self.is_legal(value):
            self._value = value
        else:
            raise ValueError("Value of parameter '" + self.name + "' illegal.")

    def is_legal(self, values=None):
        """
        Checks whether or not given or contained value is legal given constraints.

        Illegal intervals have the highest priority to be checked. Then it will check the
        legal intervals and options. The overlaps among the constrains will be overridden by
        the constrain of higher priority.
        """

        truths = []
        if values is None:
            values = self._value

        if not hasattr(values, "__iter__") or isinstance(values, str):
            #            print(str(hasattr(values, "__iter__")) + str(values))
            value = values

            for option in self._options:
                if option == value:
                    #
                    return self._options_are_legal

            # Check illegal intervals
                if interval[0] < value < interval[1]:
                    #
            for interval in self._intervals:
                    return self._intervals_are_legal
            # T: are legal values
            # F: are illegal values
            # 0: empty list
            #
            # P I -> truth
            # T T -> F
            # F T -> F
            # 0 T -> F
            # T F -> T
            # F F -> T
            # 0 F -> T
            # T 0 -> F
            # F 0 -> T
            # 0 0 -> T

            return (not self._intervals_are_legal and len(self.intervals) > 0) or (
                len(self.intervals) == 0
                and (not self._options_are_legal or len(self.options) == 0)
            )

        # else
        for value in values:
            truths.append(self.is_legal(value))

        # all values have to be True
        for truth in truths:
            if truth is False:
                return False

        return True

    def print_paramter_constraints(self):
        """
        Print the legal and illegal intervals of this parameter.
        """
        print(self.name)
        print("intervals:", self._intervals)
        print("intervals are legal:", self._intervals_are_legal)
        print("options", self._options)
        print("options are legal:", self._options_are_legal)

    def clear_intervals(self):
        """
        Clear the intervals of this parameter.
        """
        self._intervals = []

    def clear_options(self):
        """
        Clear the option values of this parameter.
        """
        self._options = []

    def print_line(self):
        """
        returns string with one line description of parameter
        """
        if self.unit is None:
            unit_string = ""
        else:
            unit_string = "[" + self.unit + "]"

        if self.value is None:
            string = self.name.ljust(20)
        else:
            string = self.name.ljust(15)
            string += str(self.value).ljust(5)

        string += unit_string.ljust(10)
        if self.comment is not None:
            string += self.comment
        string += 3 * " "

        for interval in self._intervals:
            legal = "L" if self._intervals_are_legal else "I"
            interval = legal + "[" + str(interval[0]) + ", " + str(interval[1]) + "]"
            string += interval.ljust(10)

        if len(self._options) > 0:
            values = "("
            for option in self._options:
                values += str(option) + ", "
            values = values.strip(", ")
            values += ")"
            string += values

        return string

    def __repr__(self):
        """
        Returns string with thorough description of parameter
        """
        string = "Parameter named: '" + self.name + "'"
        if self.value is None:
            string += " without set value.\n"
        else:
            string += " with value: " + str(self.value) + "\n"

        if self.unit is not None:
            string += " [" + self.unit + "]\n"

        if self.comment is not None:
            string += " " + self.comment + "\n"

        if len(self._intervals) > 0:
            string += (
                "  Legal intervals:\n"
                if self._intervals_are_legal
                else "  Illegal intervals:\n"
            )
        for interval in self._intervals:
            string += "    [" + str(interval[0]) + "," + str(interval[1]) + "]\n"

        if len(self._options) > 0:
            string += "  Allowed values:\n"  # FIXME
        for option in self._options:
            string += "    " + str(option) + "\n"

        return string
