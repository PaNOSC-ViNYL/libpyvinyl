from libpyvinyl.BaseCalculator import BaseCalculator, Parameters
import numpy
import h5py

class RandomImageCalculator(BaseCalculator):
    def __init__(self, parameters=None, dumpfile=None, input_path=None, output_path=None):
        
        super().__init__(parameters=parameters, dumpfile=dumpfile, output_path=output_path)
               
    def backengine(self):
        tmpdata = numpy.random.random((self.parameters.grid_size_x, self.parameters.grid_size_y))
        
        self._set_data(tmpdata)
        return 0
    
    def saveH5(self, openpmd=False):
        with h5py.File(self.output_path, "w") as h5:
            ds = h5.create_dataset("/data", data=self.data)    
            
            h5.close()

