from ctypes import *
from os import listdir
import os
import pathlib

so_file = pathlib.Path().absolute().__str__() + "/inpage-to-unicode/c-lib.so"
lib = CDLL(so_file)

# args = ["","test.inp", "test.txt"]

# args_bytes = []

# for arg in args:
#   args_bytes.append(arg.encode('utf-8'))

# args = (c_char_p * (len(args_bytes)+1))()
# args[:-1] = args_bytes

# print(my_functions.main(3, args))



def convert_file_to_unicode(filepath, output_dir):
  output_file_name = os.path.basename(filepath)
  if output_dir !="":
    output_file_name = output_dir + "/" + output_file_name.replace(".inp", ".txt")
  else:
    output_file_name = output_file_name.replace(".inp", ".txt")

  args = []
  args.append("")
  args.append(filepath)
  args.append(output_file_name)
  args_bytes = []

  for arg in args:
    args_bytes.append(arg.encode('utf-8'))

  args = (c_char_p * (len(args_bytes)+1))()
  args[:-1] = args_bytes
  lib.main(3, args)


folder_path = "/home/shaoormunir/Makhzan"
output_folder = "/home/shaoormunir/Makhzan-output"


files = [file_path for file_path in listdir(folder_path) if ".inp" in file_path]

for file_path in files:
  convert_file_to_unicode(folder_path+"/"+file_path, output_folder)

output_files = listdir(output_folder)

for file_path in output_files:
  with open(output_folder + "/" + file_path, encoding="utf-16") as f:
    data = f.read()

  data_decoded = data.encode("utf-8")

  with open (output_folder + "/" + file_path, "w") as f:
      f.write(data_decoded.decode("utf-8"))