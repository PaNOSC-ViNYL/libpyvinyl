# Created by Mads Bertelsen and modified by Juncheng E
# Further modified by Shervin Nourbakhsh
from typing import Union

import math
from libpyvinyl.AbstractBaseClass import AbstractBaseClass

# importing units using the pint package from the __init__.py of this module
# from . import ureg, Q_

from pint.unit import Unit
from pint.quantity import Quantity


class Parameter(AbstractBaseClass):
    """
    Description of a single parameter.

    The parameter is defined by:
     - name: when added to a parameter collection, it can be accessed by this name
     - value: can be a boolean, a string, a pint.Quantity, an int or float (the latter internally converted to pint.Quantity)
     - unit: a string that is internally converted into a pint.Unit
     - comment: a string with a brief description of the parameter and additional informations
    """

    def __init__(
        self,
        name: str,
        unit: str = "",
        comment: Union[str, None] = None,
    ):
        """
        Creates parameter with given name, optionally unit and comment

        :param name: name of the parameter
        :type name: str

        :param unit: physical units returning the parameter value
        :type unit: str

        :param comment: brief description of the parameter
        :type comment: str

        """
        self.name = name
        self.__unit = Unit(unit) if unit != None else ""
        self.comment = comment
        self.__value = None
        self.__intervals = []
        self.__intervals_are_legal = None
        self.__options = []
        self.__options_are_legal = None
        self.__value_type = None

    @classmethod
    def from_dict(cls, param_dict):
        """
        Helper class method creating a new object from a dictionary providing
         - name: str MANDATORY
         - unit: str
         - comment: str
         - ...
        """
        if not "name" in param_dict:
            raise KeyError(
                "name is a mandatory element of the dictionary, but has not been found"
            )
        param = cls(
            param_dict["name"], param_dict["_Parameter__unit"], param_dict["comment"]
        )
        for key in param_dict:
            param.__dict__[key] = param_dict[key]

        # set the value type, making the necessary promotions
        param.__set_value_type(param.value)
        for interval in param.__intervals:
            param.__set_value_type(interval[0])
            param.__set_value_type(interval[1])
        for option in param.__options:
            param.__set_value_type(option)
        return param

    @property
    def unit(self) -> str:
        """Returning the units as a string"""
        return str(self.__unit)

    @unit.setter
    def unit(self, uni):
        # check if it is a valid unit, otherwise just store the string! FIXME
        self.__unit = Unit(uni)

    @property
    def value_no_conversion(self):
        """
        Returning the object stored in value with no conversions
        """
        return self.__value

    @property
    def value(self):
        if isinstance(self.__value, Quantity):
            return self.__value.m_as(self.__unit)
        else:
            return self.__value

    def _to_quantity(self, value: any) -> Union[Quantity, type(value)]:
        """
        Returns pint.Quantity if value can be interpreted as a physical quantity,
        returns value otherwise.

        Integers are interpreted as physical quantities only if a unit is defined.
        This is to avoid interpreting booleans as quantities.
        pint.Quantity raises an error if a True or False value are given
        """

        a = value
        if self.__value_type == Quantity and type(value) != Quantity:
            a = Quantity(value, self.__unit)

        return a

    def __set_value_type(self, value):
        """
        Sets the type for the parameter, done only the first time.
        Then it will raise an exception if the type is not coherent to what is declared.
        """
        vtype = type(value)
        if self.__is_type_compatible(vtype, self.__value_type):
            if vtype is int and self.__unit != "":
                self.__value_type = Quantity
            elif vtype is float:
                self.__value_type = Quantity
            else:
                print("Vtype: ", vtype)
                self.__value_type = vtype

        else:  # type(value) != self.__value_type:
            raise TypeError(
                "New value of type %s is different from %s previously defined"
                % (type(value), self.__value_type)
            )

    @value.setter
    def value(self, value):
        """
        Sets value of this parameter if value is legal,
        an exception is raised otherwise.

        :param value: value
        :type value: str | boolean | int | float | object | pint.Quantity
        If value is a float, it is internally converted to a pint.Quantity
        """
        self.__set_value_type(value)
        value = self._to_quantity(value)

        if self.is_legal(value):
            self.__value = value
        else:
            raise ValueError("Value of parameter '" + self.name + "' illegal.")

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

        if min_value is None:
            min_value = -math.inf
        if max_value is None:
            max_value = math.inf

        self.__set_value_type(min_value)
        self.__set_value_type(max_value)

        if self.__intervals_are_legal is None:
            self.__intervals_are_legal = intervals_are_legal
        else:
            if self.__intervals_are_legal != intervals_are_legal:
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

        self.__intervals.append(
            [self._to_quantity(min_value), self._to_quantity(max_value)]
        )

        # if the interval has been added after assignement of the value of the parameter,
        # the latter should be checked
        if not self.value_no_conversion is None:
            if self.is_legal(self.value) is False:
                raise ValueError(
                    "Value "
                    + str(self.value)
                    + " is now illegal based on the newly added interval"
                )

    def add_option(self, option, options_are_legal):
        """
        Sets allowed values for this parameter
        """

        if self.__options_are_legal is None:
            self.__options_are_legal = options_are_legal
        else:
            if self.__options_are_legal != options_are_legal:
                print("ERROR: All options should be either legal or illegal.")
                print(
                    "         This option is declared differently w.r.t. to the previous ones"
                )
                # should it throw an expection?
                raise ValueError("Parameter", "options", "multiple validities")

        if isinstance(option, list):
            for op in option:
                self.__set_value_type(op)
                self.__options.append(self._to_quantity(op))
        else:
            self.__set_value_type(option)
            self.__options.append(self._to_quantity(option))

        # if the option has been added after assignement of the value of the parameter,
        # the latter should be checked
        if not self.value_no_conversion is None:
            if self.is_legal(self.value) is False:
                raise ValueError(
                    "Value "
                    + str(self.value)
                    + " is now illegal based on the newly added option"
                )

    @classmethod
    def __is_type_compatible(self, t1: type, t2: type) -> bool:  # self is not needed...
        """
        Check type compatiblity

        :param t1: first type
        :type t1: type

        :param t2: second type
        :type t2: type

        :return: bool

        True if t1 and t2 are of the same type or if one is int and the other float
        False otherwise
        """
        if t1 == type(None) or t2 == type(None):
            return True
        if t1 == None or t2 == None:
            return True

        # promote any float to pint.Quantity
        if t1 == float:
            t1 = Quantity
        if t2 == float:
            t2 = Quantity

        if "quantity" in str(t1):
            t1 = Quantity
        if "quantity" in str(t2):
            t2 = Quantity

        if t1 == t2:
            return True

        # consider int always compatible with Quantities
        if (t1 == int and t2 == Quantity) or (t1 == Quantity and t2 == int):
            return True

        return False

    def is_legal(self, values=None):
        """
        Checks whether or not given or contained value is legal given constraints.

        """

        if values is None:
            values = self.__value

        if (
            not hasattr(values, "__iter__")
            or isinstance(values, str)
            or isinstance(values, Quantity)
        ):
            #            print(str(hasattr(values, "__iter__")) + str(values))
            # first if types are compatible

            if self.__is_type_compatible(type(values), self.__value_type) is False:
                return False

            value = self._to_quantity(values)

            # obvious, if no conditions are defined, the value is always legal
            if len(self.__options) == 0 and len(self.__intervals) == 0:
                return True

            # first check if the value is in any defined discrete value
            for option in self.__options:
                if option == value:
                    return self.__options_are_legal

            # secondly check if it is in any defined interval
            for interval in self.__intervals:
                if interval[0] <= value <= interval[1]:
                    return self.__intervals_are_legal

            # at this point the value has not been found in any interval
            # if intervals where defined and were forbidden intervals, the value should be accepted
            if len(self.__intervals) > 0:
                return not self.__intervals_are_legal

            # if there where no intervals defined, then it depends if the discrete values were forbidden or allowed
            return not self.__options_are_legal

        # else
        # all values have to be True

        for value in values:
            if not self.is_legal(value):
                return False

        return True

    def print_paramter_constraints(self):
        """
        Print the legal and illegal intervals of this parameter. FIXME
        """
        print(self.name)
        print("intervals:", self.__intervals)
        print("intervals are legal:", self.__intervals_are_legal)
        print("options", self.__options)
        print("options are legal:", self.__options_are_legal)

    def clear_intervals(self):
        """
        Clear the intervals of this parameter.
        """
        self.__intervals = []

    def clear_options(self):
        """
        Clear the option values of this parameter.
        """
        self.__options = []

    def print_line(self):
        """
        returns string with one line description of parameter
        """
        if self.__unit is None:
            unit_string = ""
        else:
            unit_string = "[" + str(self.__unit) + "]"

        if self.value_no_conversion is None:
            string = self.name.ljust(20)
        else:
            string = self.name.ljust(15)
            string += str(self.value).ljust(5)

        string += unit_string.ljust(10)
        if self.comment is not None:
            string += self.comment
        string += 3 * " "

        for interval in self.__intervals:
            legal = "L" if self.__intervals_are_legal else "I"
            interval = legal + "[" + str(interval[0]) + ", " + str(interval[1]) + "]"
            string += interval.ljust(10)

        if len(self.__options) > 0:
            values = "("
            for option in self.__options:
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
        if self.value_no_conversion is None:
            string += " without set value.\n"
        else:
            string += " with value: " + str(self.value) + "\n"

        if self.__unit is not None:
            string += " [" + str(self.__unit) + "]\n"

        if self.comment is not None:
            string += " " + self.comment + "\n"

        if len(self.__intervals) > 0:
            string += (
                "  Legal intervals:\n"
                if self.__intervals_are_legal
                else "  Illegal intervals:\n"
            )
        for interval in self.__intervals:
            string += "    [" + str(interval[0]) + "," + str(interval[1]) + "]\n"

        if len(self.__options) > 0:
            string += "  Allowed values:\n"  # FIXME
        for option in self.__options:
            string += "    " + str(option) + "\n"

        return string
