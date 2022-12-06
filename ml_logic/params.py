import os
import numpy as np

LOCAL_DATA_PATH = os.path.expanduser(os.environ.get("LOCAL_REGISTRY_PATH"))

TARGET = 'In_Out'
N_TARGETS = 1
N_FEATURES = 24
input_length = 5
output_length = 1

N_TRAIN = 60
N_TEST = 40

oslo_lat = 59.919602443955355
oslo_lon = 10.752152108688852
