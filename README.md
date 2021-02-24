# fs2012_flow_sensor  

Firmware, Python library, PyQt GUI for working with the FS2012 flow sensors. 

![screenshot_1](images/flow_sensor_app.png)


## Requirements

* [pyserial](https://pythonhosted.org/pyserial/)
* [pyqt5](https://pypi.org/project/PyQt5/)


## Installation

Navigate to the directory that houses `setup.py` and install in editable mode:
```bash
cd fs2012_flow_sensor/software/fs2012_flow_sensor
pip install -e .
```

## `DataReader` Example

The below code snippet can be found in `examples/data_reader_example.py`:

```python
import time
from fs2012_flow_sensor import DataReader

port = '/dev/ttyUSB0'
reader = DataReader(port)
reader.start()
for i in range(75):
    print(reader.get_data())
    time.sleep(0.1)
reader.stop()
```

## Running the `pyqt` GUI 
The script runs from anywhere:

```bash
flow_sensor_app /dev/ttyUSB0
```

## Running the live plot
The script runs from anywhere:
```bash
flow_sensor_live_plot
```