from libpyvinyl import BaseCalculator, CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData


class PlusCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: DataCollection,
                 input_keys=['input1', 'input2'],
                 output_keys=['plus_result'],
                 output_filenames=[],
                 parameters=None):
        """A python object calculator example"""
        if parameters is None:
            self.__init_parameters()
        self.__name = name
        self.__input = input
        assert len(input_keys) == 2
        self.__input_keys = input_keys
        self.__base_dir = './'
        assert len(output_keys) == 1
        self.__output_keys = output_keys
        assert len(output_filenames) == 0
        self.__output_filenames = output_filenames

    def __init_parameters(self):
        parameters = CalculatorParameters()
        times = parameters.new_parameter(
            "plus_times", comment="How many times to do the plus")
        times.value = 1
        self.parameters = parameters

    @property
    def name(self):
        return self.__name

    @property
    def input(self):
        return self.__input

    @property
    def base_dir(self):
        return self.__base_dir

    @base_dir.setter
    def base_dir(self, value):
        self.set_base_dir(value)

    def set_base_dir(self, value):
        self.__base_dir = value

    @property
    def input_keys(self):
        return self.__input_keys

    @property
    def output_keys(self):
        return self.__output_keys

    @property
    def output_filenames(self):
        """Native calculator file names"""
        return self.__output_filenames

    def backengine(self):
        input_num0 = self.input[self.input_keys[0]].get_data()['number']
        input_num1 = self.input[self.input_keys[1]].get_data()['number']
        output_num = input_num0 + input_num1
        if self.parameters['plus_times'].value > 1:
            for i in range(self.parameters['plus_times'].value - 1):
                output_num += input_num1
        data_dict = {'number': output_num}
        key = self.output_keys[0]
        output_data = NumberData.from_dict(data_dict, key)
        self.output = DataCollection(output_data)
        return self.output

    def saveH5(self, fname: str, openpmd: bool = True):
        raise NotImplementedError
