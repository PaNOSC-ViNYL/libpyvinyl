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
        self.value = None
        self.legal_intervals = []
        self.illegal_intervals = []
        self.options = []

    @classmethod
    def from_dict(cls, param_dict):
        param = cls(param_dict['name'], param_dict['unit'],
                    param_dict['comment'])
        for key in param_dict:
            param.__dict__[key] = param_dict[key]
        return param

    def add_legal_interval(self, min_value, max_value):
        """
        Sets a legal interval for this parameter, None for infinite
        """
        if min_value is None:
            min_value = -math.inf
        if max_value is None:
            max_value = math.inf

        self.legal_intervals.append([min_value, max_value])

    def add_illegal_interval(self, min_value, max_value):
        """
        Sets an illegal interval for this parameter, None for infinite
        """
        if min_value is None:
            min_value = -math.inf
        if max_value is None:
            max_value = math.inf

        self.illegal_intervals.append([min_value, max_value])

    def add_option(self, option):
        """
        Sets allowed values for this parameter
        """
        if isinstance(option, list):
            self.options += option
        else:
            self.options.append(option)

    def set_value(self, value):
        """
        Sets value of this parameter if value is legal, otherwise warning is shown

        This could be expanded to raise an exception, or such could be in is_legal
        """
        if self.is_legal(value):
            self.value = value
        else:
            print("WARNING: Value of parameter '" + self.name
                  + "' illegal, ignored.")

    def is_legal(self, value=None):
        """
        Checks whether or not given or contained value is legal given constraints.

        Illegal intervals have the highest priority to be checked. Then it will check the
        legal intervals and options. The overlaps among the constrains will be overridden by
        the constrain of higher priority.
        """
        if value is None:
            value = self.value

        for illegal_interval in self.illegal_intervals:
            if illegal_interval[0] < value < illegal_interval[1]:
                return False

        is_outside_a_legal_interval = False
        is_inside_a_legal_interval = False
        for legal_interval in self.legal_intervals:
            if legal_interval[0] < value < legal_interval[1]:
                is_inside_a_legal_interval = True
            else:
                is_outside_a_legal_interval = True

        if is_outside_a_legal_interval and not is_inside_a_legal_interval:
            return False

        # checked intervals, can return if options not used (frequent case)
        if len(self.options) == 0:
            return True

        for option in self.options:
            if option == value:
                # If the value matches any option, it is legal
                return True

        # Since no options matched the parameter, it is illegal
        return False

    def print_paramter_constraints(self):
        """
        Print the legal and illegal intervals of this parameter.
        """
        print(self.name)
        print('illegal intervals:', self.illegal_intervals)
        print('legal intervals:', self.legal_intervals)
        print('options', self.options)

    def clear_legal_intervals(self):
        """
        Clear the legal intervals of this parameter.
        """
        self.legal_intervals = []

    def clear_illegal_intervals(self):
        """
        Clear the illegal intervals of this parameter.
        """
        self.illegal_intervals = []

    def clear_options(self):
        """
        Clear the option values of this parameter.
        """
        self.options = []

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

        for legal_interval in self.legal_intervals:
            interval = "L[" + str(legal_interval[0]) + ", " + str(
                legal_interval[1]) + "]"
            string += interval.ljust(10)

        for illegal_interval in self.illegal_intervals:
            interval = "I[" + str(illegal_interval[0]) + ", " + str(
                illegal_interval[1]) + "]"
            string += interval.ljust(10)

        if len(self.options) > 0:
            values = "("
            for option in self.options:
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

        if len(self.legal_intervals) > 0:
            string += "  Legal intervals:\n"
        for legal_interval in self.legal_intervals:
            string += "    [" + str(legal_interval[0]) + "," + str(
                legal_interval[1]) + "]\n"

        if len(self.illegal_intervals) > 0:
            string += "  Illegal intervals:\n"
        for illegal_interval in self.illegal_intervals:
            string += "    [" + str(illegal_interval[0]) + ", " + str(
                illegal_interval[1]) + "]\n"

        if len(self.options) > 0:
            string += "  Allowed values:\n"
        for option in self.options:
            string += "    " + str(option) + "\n"

        return string
