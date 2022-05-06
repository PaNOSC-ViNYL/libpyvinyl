# Created by Mads Bertelsen and modified by Juncheng E
# Further modified by Shervin Nourbakhsh

import math
import numpy
from libpyvinyl.AbstractBaseClass import AbstractBaseClass

from pint.unit import Unit
from pint.quantity import Quantity
import pint.errors

# typing
from typing import Union, Any, Tuple, List, Dict, Optional

# ValueTypes: TypeAlias = [str, bool, int, float, object, pint.Quantity]
ValueTypes = Union[str, bool, int, float, pint.Quantity]


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
        :param unit: physical units returning the parameter value
        :param comment: brief description of the parameter

        """
        self.name: str = name
        self.__unit: Union[str, Unit] = Unit(unit) if unit != None else ""
        self.comment: Union[str, None] = comment
        self.__value: Union[ValueTypes, None] = None
        self.__intervals: List[Tuple[Quantity, Quantity]] = []
        self.__intervals_are_legal: Union[bool, None] = None
        self.__options: List = []
        self.__options_are_legal: Union[bool, None] = None
        self.__value_type: Union[ValueTypes, None] = None

    @classmethod
    def from_dict(cls, param_dict: Dict):
        """
        Helper class method creating a new object from a dictionary providing
         - name: str MANDATORY
         - unit: str
         - comment: str
         - ...

        This class method is mainly used to allow dumping and loading the class from json
        """
        if "name" not in param_dict:
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
    def unit(self, uni: str) -> None:
        """
        Assignment of the units

        :param uni: unit

        A pint.Unit is used if the string is recognized as a valid unit in the registry.
        It is stored as a string otherwise.
        """
        try:
            self.__unit = Unit(uni)
        except pint.errors.UndefinedUnitError:
            self.__unit = uni

    @property
    def value_no_conversion(self) -> ValueTypes:
        """
        Returning the object stored in value with no conversions
        """
        return self.__value

    @property
    def pint_value(self) -> Quantity:
        """Returning the value as a pint object if available, an error otherwise"""
        if not isinstance(self.__value, Quantity):
            raise TypeError("The parameter value is not of pint.Quantity type")
        return self.__value

    @property
    def value(self) -> ValueTypes:
        """
        Returns the magnitude of a Quantity or the stored value otherwise
        """
        if isinstance(self.__value, Quantity):
            return self.__value.m_as(self.__unit)
        else:
            return self.__value

    @staticmethod
    def __is_type_compatible(t1: type, t2: Union[None, type]) -> bool:
        """
        Check type compatibility

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

        # promote any int or float to pint.Quantity
        if t1 == float or t1 == int or t1 == numpy.float64:
            t1 = Quantity
        if t2 == float or t2 == int or t2 == numpy.float64:
            t2 = Quantity

        if "quantity" in str(t1):
            t1 = Quantity
        if "quantity" in str(t2):
            t2 = Quantity

        if t1 == t2:
            return True

        return False

    def __to_quantity(self, value: Any) -> Union[Quantity, Any]:
        """
        Converts value into a pint.Quantity if this Parameter is defined to be a Quantity.
        It returns value unaltered otherwise.
        """

        if self.__value_type == Quantity and not isinstance(value, Quantity):
            return Quantity(value, self.__unit)

        return value

    def __set_value_type(self, value: Any) -> None:
        """
        Sets the type for the parameter.
        It should always be preceded by a __check_compatibility to avoid chaning the type for the Parameter

        :param value: a value that might be assigned as Parameter value or in an interval or option
        :type value: any type

        It will raise an exception if the type is not coherent to what previously is declared.
        """
        if (
            hasattr(value, "__iter__")
            and not isinstance(value, str)
            and not isinstance(value, Quantity)
        ):
            value = value[0]

        # if an integer has units, then it is a quantity -> promotion
        if isinstance(value, int) and self.__unit != "":
            self.__value_type = Quantity
        # if value is a float, than can be used as a quantity -> promotion
        elif isinstance(value, float):
            self.__value_type = Quantity
        else:  # cannot be treated as a quantity
            self.__value_type = type(value)

    def __check_compatibility(self, value: Any) -> None:
        """
        Raises an error if this parameter and the given value are not of the same type or compatible
        :param value: a value that might be assigned as Parameter value or in an interval or option
        :type value: any type

        It will raise an exception if the type is not coherent to what previously is declared.
        """

        vtype = type(value)
        assert vtype is not None
        v = value
        # First case: value is a list, it might be good to double check
        # that all the members are of the same type
        if isinstance(value, list):
            vtype = type(value[0])
            for v in value:
                if not self.__is_type_compatible(vtype, type(v)):
                    raise TypeError(
                        "Iterable object passed as value for the parameter, but it is made of inhomogeneous types: ",
                        vtype,
                        type(v),
                    )
        elif isinstance(value, dict):
            raise NotImplementedError("Dictionaries are not accepted")

        # check that the value is compatible with what previously defined
        if not self.__is_type_compatible(vtype, self.__value_type):
            raise TypeError(
                "New value of type {} is different from {} previously defined".format(
                    type(value), self.__value_type
                )
            )

    @value.setter
    def value(self, value: ValueTypes) -> None:
        """
        Sets value of this parameter if value is legal,
        an exception is raised otherwise.

        :param value: value
        :type value: str | boolean | int | float | object | pint.Quantity
        If value is a float, it is internally converted to a pint.Quantity
        """
        if (
            self.__unit is not None
            and isinstance(value, pint.Quantity)
            and value.check(self.__unit) is False
        ):
            raise pint.errors.DimensionalityError(value.units, self.__unit)

        self.__check_compatibility(value)
        self.__set_value_type(value)
        value = self.__to_quantity(value)
        if self.is_legal(value):
            self.__value = value
        else:
            raise ValueError("Value of parameter '" + self.name + "' illegal.")

    def add_interval(
        self,
        min_value: Union[ValueTypes, None],
        max_value: Union[ValueTypes, None],
        intervals_are_legal: bool,
    ) -> None:
        """
        Sets an interval for this parameter: [min_value, max_value]
        The interval is closed on both sides: min_value and and max_value are included.


        :param min_value: minimum value of the interval, None for infinity
        :param max_value: maximum value of the interval, None for infinity

        :param intervals_are_legal: if not done previously, it defines if all the intervals of this parameter should be considered as allowed or forbidden intervals.

        """

        if min_value is None:
            min_value = -math.inf
        if max_value is None:
            max_value = math.inf

        self.__check_compatibility(min_value)
        self.__check_compatibility(max_value)

        self.__set_value_type(min_value)  # it could have been max_value

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
            (self.__to_quantity(min_value), self.__to_quantity(max_value))
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

    def add_option(self, option: Any, options_are_legal: bool) -> None:
        """
        Sets allowed values for this parameter

        :param option: a discrete allowed or forbidden value
        :param options_are_legal: defines if the given option is for a legal or illegal discrete value
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

        self.__check_compatibility(option)
        self.__set_value_type(option)  # it could have been max_value

        if isinstance(option, list):
            for op in option:
                self.__options.append(self.__to_quantity(op))
        else:
            self.__options.append(self.__to_quantity(option))

        # if the option has been added after assignement of the value of the parameter,
        # the latter should be checked
        if not self.value_no_conversion is None:
            if self.is_legal(self.value) is False:
                raise ValueError(
                    "Value "
                    + str(self.value)
                    + " is now illegal based on the newly added option"
                )

    def get_options(self):
        return self.__options

    def get_options_are_legal(self):
        return self.__options_are_legal

    def get_intervals(self):
        return self.__intervals

    def get_intervals_are_legal(self):
        return self.__intervals_are_legal

    def is_legal(self, values: Union[ValueTypes, None] = None) -> bool:
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

            value = self.__to_quantity(values)

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

    def print_parameter_constraints(self) -> None:
        """
        Print the legal and illegal intervals of this parameter. FIXME
        """
        print(self.name)
        print("intervals:", self.__intervals)
        print("intervals are legal:", self.__intervals_are_legal)
        print("options", self.__options)
        print("options are legal:", self.__options_are_legal)

    def clear_intervals(self) -> None:
        """
        Clear the intervals of this parameter.
        """
        self.__intervals = []

    def clear_options(self) -> None:
        """
        Clear the option values of this parameter.
        """
        self.__options = []

    def print_line(self) -> str:
        """
        returns string with one line description of parameter
        """
        if self.__unit is None or self.__unit == Unit(""):
            unit_string = ""
        else:
            unit_string = "[" + str(self.__unit) + "] "

        if self.value_no_conversion is None:
            string = self.name.ljust(40) + " "
        else:
            string = self.name.ljust(35) + " "
            string += str(self.value).ljust(10) + " "

        string += unit_string.ljust(20) + " "
        if self.comment is not None:
            string += self.comment
        string += 3 * " "

        for interval in self.__intervals:
            legal = "L" if self.__intervals_are_legal else "I"
            intervalstr = legal + "[" + str(interval[0]) + ", " + str(interval[1]) + "]"
            string += intervalstr.ljust(10)

        if len(self.__options) > 0:
            values = "("
            for option in self.__options:
                values += str(option) + ", "
            values = values.strip(", ")
            values += ")"
            string += values

        return string

    def __repr__(self) -> str:
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
