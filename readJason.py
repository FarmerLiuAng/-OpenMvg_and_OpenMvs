import json 
import os
from argparse import ArgumentParser

def getparse():
  parser = ArgumentParser()
  parser.add_argument('--root_dir', type=str,
                        default='/mnt/md0/liuang/mvg/MVGdata/lanqiu',
                        help='root directory of dataset')
  parser.add_argument('--results_dir', type=str,
                        default='/mnt/md0/liuang/mvg/MVGresults/lanqiu',
                        help='root of results')
  return parser.parse_args()
  
if __name__ == "__main__":
  args = getparse()
  with open(args.results_dir + '/sfm/cameras.json') as file:
    jasondata = json.load(file)# all dict
    file.close()  
  ex_data = jasondata['extrinsics'] # extrinsics list


  in_data = jasondata['intrinsics'] # intrinsics list
  in_val = dict(dict(dict(dict(in_data[0])["value"])["ptr_wrapper"])["data"]) 
  flen = in_val["focal_length"]
  in_x = in_val["principal_point"][0]
  in_y = in_val["principal_point"][1]
  i = 0
  if not os.path.exists(args.results_dir + "/sfm/cams"):
    os.mkdir(args.results_dir + "/sfm/cams")
  os.chdir(args.results_dir + "/sfm/cams")
  for dic in ex_data:
     key = dict(ex_data[i])["key"]
     val = dict(dic['value']) # value dict
   
     rot = val['rotation'] #rotation list
     cen = val['center'] #center list
     if key >= 1000:
       str1 = "0000" + str(key) + "_cams.txt" 
       f = open(str1 , "w" )
     elif key >= 100:
       str1 = "00000" + str(key) + "_cams.txt"
       f = open(str1 , "w" )
     elif key >= 10:
       str1 = "000000" + str(key) + "_cams.txt"
       f = open(str1 , "w" )
     else:
       str1 = "0000000" + str(key) + "_cams.txt"
       f = open(str1 , "w" )
     f.write("extrinsic\n")
     f.write(str(rot[0][0])+str(" ")+str(rot[1][0])+str(" ")+str(rot[2][0])+"\n")
     f.write(str(rot[0][1])+str(" ")+str(rot[1][1])+str(" ")+str(rot[2][1])+"\n")
     f.write(str(rot[0][2])+str(" ")+str(rot[1][2])+str(" ")+str(rot[2][2])+"\n")
     f.write("0.0 0.0 0.0 1.0"+"\n"+"\n") 
     f.write("intrinsic"+"\n")
     f.write(str(flen) + " 0.0 " + str(in_x) + "\n")
     f.write("0.0 " + str(flen) + str(" ") + str(in_y) + "\n")
     f.write("0.0 0.0 1.0\n\n")
     f.close()
     i += 1
     