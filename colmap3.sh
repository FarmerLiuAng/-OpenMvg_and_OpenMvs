# The project folder must contain a folder "images" with all the images.
starttime=$(date +%Y-%m-%d\ %H:%M:%S)
DATASET_PATH=$1
RESULT_PATH=$2
PHOTO_SIZE=$3
'''
. /mnt/md0/liuang/anaconda3/etc/profile.d/conda.sh
conda activate casmvsnet_pl

mkdir $RESULT_PATH
mkdir $RESULT_PATH/sfm
mkdir $RESULT_PATH/sfm/matches

echo "0.Intrinsics analysis"
/opt/openmvg/bin/openMVG_main_SfMInit_ImageListing -i $DATASET_PATH/images -o $RESULT_PATH/sfm/matches -f $PHOTO_SIZE -c 1 -g 0
echo "1.Compute features"
/opt/openmvg/bin/openMVG_main_ComputeFeatures -i $RESULT_PATH/sfm/matches/sfm_data.json -o $RESULT_PATH/sfm/matches -m AKAZE_FLOAT -n 2
echo "2.Compute matches"
/opt/openmvg/bin/openMVG_main_ComputeMatches -i $RESULT_PATH/sfm/matches/sfm_data.json -o $RESULT_PATH/sfm/matches 
'''
echo "3.Incremental reconstruction"
/opt/openmvg/bin/openMVG_main_IncrementalSfM -i $RESULT_PATH/sfm/matches/sfm_data.json -m $RESULT_PATH/sfm/matches -o $RESULT_PATH/sfm  

mkdir $DATASET_PATH/sparse
mkdir $DATASET_PATH/sparse/0

echo "openMVGformat to Colmap"
openMVG_main_openMVG2Colmap -i $RESULT_PATH/sfm/sfm_data.bin -o $DATASET_PATH/sparse/

echo "modify camstxt"
python changeCam.py --root_dir $DATASET_PATH --size $PHOTO_SIZE

echo "colmap2mvsnet 2"
python colmap2mvsnet2.py  --dense_folder $DATASET_PATH  --max_d 48

echo "---cascade_pl---"
python ./cascade_pl_4.12_colmap_depth/eval.py --root_dir /mnt/md0/liuang/mvg/MVGdata --depth_dir $RESULT_PATH/depth \
--point_dir $RESULT_PATH/point --colmap_dir $RESULT_PATH/colmap/sparse  --save_visual



echo "---OpenMVS---"
cd $RESULT_PATH
/usr/local/bin/OpenMVS/InterfaceCOLMAP -i ./colmap -o scene.mvs
echo "ReconstructMesh 3"
/usr/local/bin/OpenMVS/ReconstructMesh scene.mvs  --smooth 5
echo "---RefineMesh---"
/usr/local/bin/OpenMVS/RefineMesh scene_mesh.mvs
echo "TextureMesh 4"
/usr/local/bin/OpenMVS/TextureMesh scene_mesh.mvs --export-type obj --decimate 0.25 --cost-smoothness-ratio 5 --resolution-level 0

mkdir openmvs
mv scene* openmvs

rm -rf InterfaceCOLMAP*
rm -rf ReconstructMesh*
rm -rf RefineMesh*
rm -rf TextureMesh*


echo "Done! 5"
ttime=`date +"%Y-%m-%d %H:%M:%S"`
echo $starttime
echo $ttime
