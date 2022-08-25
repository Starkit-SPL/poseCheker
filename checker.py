from tabnanny import check
from constants import jointsRanges, jointsNames
from interpolation import Head, LAnkle, RAnkle
import glob
from pathlib import Path
 
    
class Limits_:

    def __init__(self, value, limit):
            self.value = value
            self.limit = limit
    
    
def checkJointPose(pose, jointPose, Limits_):
    """check joints onto allowed interval"""
    value = pose[jointPose]
    local_range = Limits_.limit.getValueRange(Limits_.value)
    if value >= max(local_range):
        value = max(local_range)
    elif value <= min(local_range):
        value = min(local_range)
    return value
    
            
def checkPoseReality(pose):
    pose[1] = checkJointPose(pose, 1, Limits_(value=pose[jointsNames.index('HeadPitch')], limit=Head))
    pose[12] = checkJointPose(pose, 12, Limits_(value=pose[jointsNames.index('LAnklePitch')], limit=LAnkle))
    pose[17] = checkJointPose(pose, 17, Limits_(value=pose[jointsNames.index('RAnklePitch')], limit=RAnkle))
    for i in range(23):
        cur = pose[i]
        range_ = jointsRanges[i]
        if cur >= max(range_):
            cur = max(range_)
        if cur <= min(range_):
            cur = min(range_)
        pose[i] = cur
            
for filename in glob.glob('test/*.txt'):
    pose = []
    with open(Path(Path.cwd(), filename), 'r') as f:
        for line in f:
            pose.append(int(float(line)))
        
        
    with open(Path(Path.cwd(), filename), 'w') as f:
        checkPoseReality(pose)
        pose[-1] = 100
        pose[-2] = 100
        for tmp in pose:
            f.write(str(int(tmp)) + '\n')