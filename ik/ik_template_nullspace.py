import numpy as np
from numpy.core.defchararray import join
from pybullet_tools.utils import connect, disconnect, set_joint_positions, wait_if_gui, set_point, load_model,\
                                 joint_from_name, link_from_name, get_joint_info, HideOutput, get_com_pose, wait_for_duration
from pybullet_tools.transformations import quaternion_matrix
from pybullet_tools.pr2_utils import DRAKE_PR2_URDF
import time
import sys
### YOUR IMPORTS HERE ###
import math
from pybullet_tools.utils import wait_for_user
#########################

from utils import draw_sphere_marker

def get_ee_transform(robot, joint_indices, joint_vals=None):
    # returns end-effector transform in the world frame with input joint configuration or with current configuration if not specified
    if joint_vals is not None:
        set_joint_positions(robot, joint_indices, joint_vals)
    ee_link = 'l_gripper_tool_frame'
    pos, orn = get_com_pose(robot, link_from_name(robot, ee_link))
    res = quaternion_matrix(orn)
    res[:3, 3] = pos
    return res

def get_joint_axis(robot, joint_idx):
    # returns joint axis in the world frame
    j_info = get_joint_info(robot, joint_idx)
    jt_local_pos, jt_local_orn = j_info.parentFramePos, j_info.parentFrameOrn
    H_L_J = quaternion_matrix(jt_local_orn) # joint transform in parent link CoM frame
    H_L_J[:3, 3] = jt_local_pos
    parent_link_world_pos, parent_link_world_orn = get_com_pose(robot, j_info.parentIndex)
    H_W_L = quaternion_matrix(parent_link_world_orn) # parent link CoM transform in world frame
    H_W_L[:3, 3] = parent_link_world_pos
    H_W_J = np.dot(H_W_L, H_L_J)
    R_W_J = H_W_J[:3, :3]
    joint_axis_local = np.array(j_info.jointAxis)
    joint_axis_world = np.dot(R_W_J, joint_axis_local)
    return joint_axis_world

def get_joint_position(robot, joint_idx):
    # returns joint position in the world frame
    j_info = get_joint_info(robot, joint_idx)
    jt_local_pos, jt_local_orn = j_info.parentFramePos, j_info.parentFrameOrn
    H_L_J = quaternion_matrix(jt_local_orn) # joint transform in parent link CoM frame
    H_L_J[:3, 3] = jt_local_pos
    parent_link_world_pos, parent_link_world_orn = get_com_pose(robot, j_info.parentIndex)
    H_W_L = quaternion_matrix(parent_link_world_orn) # parent link CoM transform in world frame
    H_W_L[:3, 3] = parent_link_world_pos
    H_W_J = np.dot(H_W_L, H_L_J)
    j_world_posi = H_W_J[:3, 3]
    return j_world_posi

def set_joint_positions_np(robot, joints, q_arr):
    # set active DOF values from a numpy array
    q = [q_arr[0, i] for i in range(q_arr.shape[1])]
    set_joint_positions(robot, joints, q)


def get_translation_jacobian(robot, joint_indices):
    J = np.zeros((3, len(joint_indices)))
    ### YOUR CODE HERE ###
    # delta_val = 1e-4 * 1.0
    # ori_pos = get_ee_transform(robot, joint_indices, joint_vals=q[0,:])
    eof_pos = get_ee_transform(robot, joint_indices)[:3,3]
    for i in range( len(joint_indices) ):
        # new_q = q.copy()
        # new_q[0,i] += delta_val
        joint_pos = get_joint_position(robot=robot, joint_idx=joint_indices[i])
        joint_axis = get_joint_axis(robot=robot, joint_idx=joint_indices[i])
        # new_pos = get_ee_transform(robot, joint_indices, joint_vals=new_q[0,:])
        # dx = np.linalg.norm(new_pos[:3,3]-ori_pos[:3,3])
        # J[:,i] = np.cross(joint_axis,joint_pos)*dx / delta_val
        # print ( joint_pos.shape )
        J[:,i] = np.cross(joint_axis,joint_pos-eof_pos)
    ### YOUR CODE HERE ###
    return J

def get_jacobian_pinv(J):
    J_pinv = []
    ### YOUR CODE HERE ###
    damp_lambda = math.sqrt( 1e-5 )
    J_pinv = J.T@np.linalg.inv(J@J.T+damp_lambda**2 * np.eye(3))
    ### YOUR CODE HERE ###
    return J_pinv

def get_NullMat(J,Jpinv):
    return np.eye(7) - Jpinv @ J
def get_dq2(q , joint_limit_list): # joint_limits[ joint_names[i] ]
    dq = np.zeros( (len(joint_limit_list),) )
    for i in range( len(joint_limit_list) ):
        expect_val_l = joint_limit_list[i][0]
        expect_val_u = joint_limit_list[i][1]
        if ( joint_limit_list[i][0] > joint_limit_list[i][1] ): # Invalid limit
            expect_val_l = -math.pi
            expect_val_u = math.pi
        # print ( (expect_val_u-q[i]) / (q[i]-expect_val_l) )
        dq[i] = math.log( (expect_val_u-q[i]+1e-7) / (q[i]-expect_val_l+1e-7)  )
    return dq

def tuck_arm(robot):
    joint_names = ['torso_lift_joint','l_shoulder_lift_joint','l_elbow_flex_joint',\
        'l_wrist_flex_joint','r_shoulder_lift_joint','r_elbow_flex_joint','r_wrist_flex_joint']
    joint_idx = [joint_from_name(robot, jn) for jn in joint_names]
    set_joint_positions(robot, joint_idx, (0.24,1.29023451,-2.32099996,-0.69800004,1.27843491,-2.32100002,-0.69799996))

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Specify which target to run:")
        print("  'python3 ik_template.py [target index]' will run the simulation for a specific target index (0-4)")
        exit()
    test_idx = 0
    try:
        test_idx = int(args[0])
    except:
        print("ERROR: Test index has not been specified")
        exit()

    # initialize PyBullet
    connect(use_gui=True, shadows=False)
    # load robot
    with HideOutput():
        robot = load_model(DRAKE_PR2_URDF, fixed_base=True)
        set_point(robot, (-0.75, -0.07551, 0.02))
    tuck_arm(robot)
    # define active DoFs
    joint_names =['l_shoulder_pan_joint','l_shoulder_lift_joint','l_upper_arm_roll_joint', \
        'l_elbow_flex_joint','l_forearm_roll_joint','l_wrist_flex_joint','l_wrist_roll_joint']
    joint_idx = [joint_from_name(robot, jn) for jn in joint_names]
    # intial config
    q_arr = np.zeros((1, len(joint_idx)))
    set_joint_positions_np(robot, joint_idx, q_arr)
    # list of example targets
    targets = [[-0.15070158,  0.47726995, 1.56714123],
               [-0.36535318,  0.11249,    1.08326675],
               [-0.56491217,  0.011443,   1.2922572 ],
               [-1.07012697,  0.81909669, 0.47344636],
               [-1.11050811,  0.97000718,  1.31087581]]
    # define joint limits
    joint_limits = {joint_names[i] : (get_joint_info(robot, joint_idx[i]).jointLowerLimit, get_joint_info(robot, joint_idx[i]).jointUpperLimit) for i in range(len(joint_idx))}
    q = np.zeros((1, len(joint_names))) # start at this configuration
    target = targets[test_idx]
    # draw a blue sphere at the target
    draw_sphere_marker(target, 0.05, (0, 0, 1, 1))
    
    ### YOUR CODE HERE ###

    error_eps = 1e-2
    alpha = 5e-2
    error_min = 999
    # beta = 5e-2 # Failed 3,4
    beta = 1e-2
    joint_limits_list = [joint_limits[joint_names[i]] for i in range( len(joint_idx) )]
    while ( True ):
        x_cur = get_ee_transform(robot, joint_idx, q[0,:])[:3,3]
        dx = target - x_cur
        error = np.linalg.norm(dx)
        error_min = min( error_min , error )
        print ( error_min )
        if ( error < error_eps ):
            break
        J = get_translation_jacobian(robot, joint_idx)
        Jpinv = get_jacobian_pinv(J)
        # print( (Jpinv @ dx).shape , get_NullMat(J,Jpinv).shape, get_dq2(q[0,:],joint_limits_list).shape)
        dq = Jpinv @ dx + beta * get_NullMat(J,Jpinv) @ get_dq2(q[0,:],joint_limits_list)

        if ( np.linalg.norm(dq) > alpha):
            dq = alpha * dq / np.linalg.norm(dq)
        q = q - dq
        for i in range( len(joint_idx) ):
            if ( joint_limits[ joint_names[i] ][1] < joint_limits[ joint_names[i] ][0] ):
                q[0,i] = q[0,i] if q[0,i] < math.pi else math.pi - 2e-5
                q[0,i] = q[0,i] if q[0,i] > -math.pi else -math.pi + 2e-5
            else:
                if q[0,i] > joint_limits[ joint_names[i] ][1]:
                    q[0,i] = joint_limits[ joint_names[i] ][1] - 2e-4
                if q[0,i] < joint_limits[ joint_names[i] ][0]:
                    q[0,i] = joint_limits[ joint_names[i] ][0] + 2e-4
    
    ### YOUR CODE HERE ###
    print ( "Middle Joint vals= " , np.round( np.mean(joint_limits_list,axis=1),3) )
    print ( "Configuration for " , test_idx , " is: " , np.round(q,3) )

    wait_if_gui()
    disconnect()

if __name__ == '__main__':
    main()
