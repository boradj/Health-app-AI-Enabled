# this module contains the pretrained ai, this module needs to import the permissions for accelerometer and gyro from the phone
# also it needs to import permissons such as tesnorflow etc.
import managingDb
#from plyer import accelerometer
#from plyer import gyroscope
import datetime
import time

import numpy as np
import tensorflow as tf

from plyer import accelerometer
from plyer import gyroscope


# this function contains the ai, and takes input such from accelerometer and gyro
# def gruResponse( time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z ):

#     """Ai goes here"""


#     #This will contain the output response of the gru after calculation, like sitting running walking
#     output = "sitting"

#     managingDb.storeProfile(time, output)


#     # returning the output
#     return output

# setting a global variable
GruOutput = ""


# global variable declared to resolve "local variable 'time' referenced
# before assignment"
t = time


# this function starts to feed sensors data into the ai model
def feedAI():
    # commenting below as they are already enabled in allow section
    # accelerometer.enable()
    # gyroscope.enable()

    # Load TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path="lstm.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    while True:

        # calling global variable for time
        global t

        # frequency of 50hz, hence setting a cycle of 0.02 seconds
        t.sleep(0.02)

        t = datetime.datetime.now()

        # gets accelerometers data in tuple format in 3 axes (x,y,z)
        # taking input in the form of list
        [acc_x, acc_y, acc_z] = accelerometer.acceleration

        # gets gyrometers data in tuple format in 3 axes
        # taking input in the form of list
        [gyr_x, gyr_y, gyr_z] = gyroscope.rotation

        # input converted into  a single array
        ai_input = [acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z]
        # below function will store AI output into profile database
        # and will also return output
        #gruResponse(time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z)

        # Test model on random input data.
        input_shape = input_details[0]['shape']

        input_data = ai_input
        #input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        #interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # This will contain the output response of the gru after calculation, like sitting running walking
        global GruOutput
        GruOutput = output_data

        #managingDb.storeProfile(time, GruOutput)

        # returning the final output
        return GruOutput


# this is to settingScreen reset the GruOutpu
# feedAI()
