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
  
  camstxtpath = args.root_dir + '/sparse/'
  print(camstxtpath)
  with open(camstxtpath + "cameras.txt","r") as f: 
    para1 = f.readlines()[0:3]
    f.seek(0,0)
    para2 = f.readlines()[3:-1]
    f.close()
  para2str = "".join(para2)  
  p = para2str.split(" ")
  os.remove(camstxtpath + "cameras.txt")
  
  camspath = args.results_dir + '/sfm/cams/'
  list = os.listdir(camspath)
  length = str(len(list))
  print("length:",length)
  p12 = para1[2]
  p12 = p12[:-2] + length + "\n"
  f = open(camstxtpath+"cameras.txt","w")
  f.write(str(para1[0])+str(para1[1])+p12)
  for file in list:
    num = 0
    if(file != 'pair.txt'):   
      if file[4] != '0':
        num = file[4] + file[5] + file[6] + file[7]
      elif file[5] != '0':
        num = file[5] + file[6] + file[7]
      elif file[6] != '0':
        num = file[6] + file[7]
      else:
        num = file[7]
    p[0] = num
    p2 = " ".join(p)
    f.write(p2)
  f.close() 
   