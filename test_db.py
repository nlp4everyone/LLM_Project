import torch
from torch.backends.cudnn import version
from torch.cuda import is_available,get_device_name
print(is_available())
print(get_device_name())
print(version())