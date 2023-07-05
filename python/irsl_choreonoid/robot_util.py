import cnoid.Body
#import cnoid.Util

from .cnoid_util import *

import cnoid.IRSLUtil as iu
import cnoid.IKSolvers as IK

import numpy as np

def make_coordinates(coords_map):
    pos = None
    for key in ('position', 'translation', 'pos', 'trans'):
        if key in coords_map:
            pos = np.array(coords_map[key])
            break
    for key in ('q', 'quaternion'):
        if key in coords_map:
            q = np.array(coords_map[key])
            if pos is None:
                return iu.coordinates(q)
            else:
                return iu.coordinates(pos, q)
    for key in ('angle-axis', 'aa'):
        if key in coords_map:
            aa = coords_map[key]
            rot = iu.angleAxisNormalized(aa[3], np.array(aa[:3]))
            if pos is None:
                return iu.coordinates(rot)
            else:
                return iu.coordinates(pos, rot)
    for key in ('rotation', 'matrix', 'mat', 'rot'):
        if key in coords_map:
            rot = np.array(coords_map[key])
            if pos is None:
                return iu.coordinates(rot)
            else:
                return iu.coordinates(pos, rot)
    for key in ('rpy', 'RPY', 'roll-pitch-yaw'):
        if key in coords_map:
            if pos is None:
                ret = iu.coordinates()
            else:
                ret = iu.coordinates(pos)
            ret.setRPY(np.array(coords_map[key]))
            return ret
    if pos is not None:
        return iu.coordinates(pos)
    raise Exception('{}'.format(coords_map))

## add methods to choreonoid's class
def __joint_list(self):
    return [self.joint(idx) for idx in range(self.numJoints) ]
def __link_list(self):
    return [self.link(idx) for idx in range(self.numLinks) ]

cnoid.Body.Body.jointList = __joint_list
cnoid.Body.Body.linkList = __link_list
cnoid.Body.Body.angleVector = lambda self, vec = None: iu.angleVector(self) if vec is None else iu.angleVector(self, vec)
cnoid.Body.Link.getCoords = lambda self: iu.getCoords(self)
cnoid.Body.Link.setCoords = lambda self, cds: iu.setCoords(self, cds)
cnoid.Body.Link.getOffsetCoords = lambda self: iu.getOffsetCoords(self)
cnoid.Body.Link.setOffsetCoords = lambda self, cds: iu.setOffsetCoords(self, cds)

class RobotModel(object):
    def __init__(self, robot):
        self.item = None
        if isinstance(robot, BodyItem):
            self.robot = robot.body
            self.item = robot
        elif isinstance(robot, cnoid.Body.Body):
            self.robot = robot
        else:
            raise TypeError('')

        self.rleg_tip_link = None
        self.rleg_tip_to_eef = None
        self.lleg_tip_link = None
        self.lleg_tip_to_eef = None

        self.rarm_tip_link = None
        self.rarm_tip_to_eef = None
        self.larm_tip_link = None
        self.larm_tip_to_eef = None

        self.head_tip_link = None
        self.head_tip_to_eef = None
        self.torso_tip_link = None
        self.torso_tip_to_eef = None

    def init_ending(self):
        for limb in ('rleg', 'lleg', 'rarm', 'larm', 'head', 'torso'):
            eef = eval('self.%s_tip_to_eef'%(limb))
            if not eef is None:
                exec('self.%s_tip_to_eef_coords = iu.coordinates(self.%s_tip_to_eef)'%(limb, limb))
                exec('type(self).%s_end_coords = lambda self : self.%s_tip_link.getCoords().transform(self.%s_tip_to_eef_coords)'%(limb, limb, limb))
    #def robot(self):
    #    return robot

    #def links(self):
    #    num = self.robot.numLinks
    #    return [ self.robot.link(n) for n in range(num) ]
    def linkList(self):
        return self.robot.linkList()
    #def joint_list(self):
    #    num = self.robot.numJoints
    #    return [ self.robot.joint(n) for n in range(num) ]
    def jointList(self):
        return self.robot.jointList()
    #def angle_vector(self, angles = None):
    #    num = self.robot.numJoints
    #    if not (angles is None):
    #        if num != len(angles):
    #            raise TypeError('length of angles does not equal with robot.numJoints')
    #        for idx in range(num):
    #            self.robot.joint(idx).q = angles[idx]
    #        return None
    #    else:
    #        return np.array([ self.robot.joint(n).q for n in range(num) ])
    def angleVector(self, angles = None):
        return self.robot.angleVector(angles)

    def flush(self):
        if self.robot is not None:
            self.robot.calcForwardKinematics()
        if self.item is not None:
            self.item.notifyKinematicStateChange()
            MessageView.instance.flush()

    def default_pose__(self):
        pass

    def init_pose__(self):
        pass

    def set_pose(self, name):
        av = eval('self.%s_pose__()'%(name))
        self.angleVector(av)
        return self.angleVector()

    def end_effector_cnoid(self, limb):
        return eval('self.%s_end_effector_cnoid()'%(limb))

    def end_effector(self, limb):
        tip_link = eval('self.%s_tip_link'%(limb))
        tip_to_eef = eval('self.%s_tip_to_eef_coords'%(limb))
        cds = tip_link.getCoords()
        cds.transform(tip_to_eef)
        return cds

    ### Position
    def rleg_end_effector_cnoid(self):
        return self.rleg_tip_link.getPosition().dot(self.rleg_tip_to_eef)
    def lleg_end_effector_cnoid(self):
        return self.lleg_tip_link.getPosition().dot(self.lleg_tip_to_eef)
    def rarm_end_effector_cnoid(self):
        return self.rarm_tip_link.getPosition().dot(self.rarm_tip_to_eef)
    def larm_end_effector_cnoid(self):
        return self.larm_tip_link.getPosition().dot(self.larm_tip_to_eef)
    def head_end_effector_cnoid(self):
        return self.head_tip_link.getPosition().dot(self.head_tip_to_eef)
    def torso_end_effector_cnoid(self):
        return self.torso_tip_link.getPosition().dot(self.torso_tip_to_eef)

    def foot_mid_coords_cnoid(self, p = 0.5):
        return iu.Position_mid_coords(p, self.rleg_end_effector_cnoid(), self.lleg_end_effector_cnoid())

    def fix_leg_to_coords_cnoid(self, position, p = 0.5):
        mc = self.foot_mid_coords_cnoid(p)
        rL = self.robot.rootLink
        rL.setPosition(
            (iu.PositionInverse(mc).dot(position)).dot(rL.getPosition())
            )
        self.robot.calcForwardKinematics()

    ### coordinates
    def rleg_end_effector(self):
        return self.rleg_tip_link.getCoords().transform(self.rleg_tip_to_eef_coords)
    def lleg_end_effector(self):
        return self.lleg_tip_link.getCoords().transform(self.lleg_tip_to_eef_coords)
    def rarm_end_effector(self):
        return self.rarm_tip_link.getCoords().transform(self.rarm_tip_to_eef_coords)
    def larm_end_effector(self):
        return self.larm_tip_link.getCoords().transform(self.larm_tip_to_eef_coords)
    def head_end_effector(self):
        return self.head_tip_link.getCoords().transform(self.head_tip_to_eef_coords)
    def torso_end_effector(self):
        return self.torso_tip_link.getCoords().transform(self.torso_tip_to_eef_coords)

    def foot_mid_coords(self, p = 0.5):
        cds = self.end_effector('rleg')
        return cds.mid_coords(0.5, self.end_effector('lleg'))

    def fix_leg_to_coords(self, coords, p = 0.5):
        mc = self.foot_mid_coords(p)
        rL = self.robot.rootLink
        cds = mc.inverse_transformation()
        cds.transform(coords)
        cds.transform(rL.getCoords())
        rL.setCoords(cds)
        self.robot.calcForwardKinematics()

    def inverse_kinematics_cnoid(self, position, limb = 'rarm', weight = [1,1,1, 1,1,1], debug = False):
        constraints = IK.Constraints()
        ra_constraint = IK.PositionConstraint()
        ra_constraint.A_link =     eval('self.%s_tip_link'%(limb))
        ra_constraint.A_localpos = eval('self.%s_tip_to_eef'%(limb))
        #constraint->B_link() = nullptr;
        ra_constraint.B_localpos = position
        ra_constraint.weight = np.array(weight)
        constraints.push_back(ra_constraint)

        jlim_avoid_weight_old = np.zeros(6 + self.robot.getNumJoints())
        ##dq_weight_all = np.ones(6 + self.robot.getNumJoints())
        dq_weight_all = np.append(np.zeros(6), np.ones(self.robot.getNumJoints()))

        d_level = 0
        if debug:
            d_level = 1

        loop = IK.solveFullbodyIKLoopFast(self.robot,
                                          constraints,
                                          jlim_avoid_weight_old,
                                          dq_weight_all,
                                          20,
                                          1e-6,
                                          d_level)
        if debug:
            for cntr, const in enumerate(constraints):
                const.debuglevel = 1
                if const.checkConvergence():
                    print('constraint %d (%s) : converged'%(cntr, const))
                else:
                    print('constraint %d (%s) : NOT converged'%(cntr, const))

        return loop

    def inverse_kinematics(self, coords, limb = 'rarm', weight = [1,1,1, 1,1,1], debug = False):
        pos = coords.toPosition()
        return inverse_kinematics_cnoid(pos, limb=limb, weight=weight, debug=debug)

    def move_centroid_on_foot_cnoid(self, p = 0.5, debug = False):
        mid_pos = self.foot_mid_coords(p)
        #mid_trans = iu.Position_translation(mid_pos)
        mid_trans = mid_pos.pos

        constraints = IK.Constraints()

        rl_constraint = IK.PositionConstraint()
        rl_constraint.A_link = self.rleg_tip_link
        rl_constraint.A_localpos = self.rleg_tip_to_eef
        #constraint->B_link() = nullptr;
        rl_constraint.B_localpos = self.rleg_end_effector().toPosition()
        constraints.push_back(rl_constraint)

        ll_constraint = IK.PositionConstraint()
        ll_constraint.A_link = self.lleg_tip_link
        ll_constraint.A_localpos = self.lleg_tip_to_eef
        #constraint->B_link() = nullptr;
        ll_constraint.B_localpos = self.lleg_end_effector().toPosition()
        constraints.push_back(ll_constraint)

        com_constraint = IK.COMConstraint()
        com_constraint.A_robot = self.robot
        com_constraint.B_localp = mid_trans
        w = com_constraint.weight
        w[2] = 0.0
        com_constraint.weight = w
        constraints.push_back(com_constraint)

        jlim_avoid_weight_old = np.zeros(6 + self.robot.getNumJoints())
        ##dq_weight_all = np.ones(6 + self.robot.getNumJoints())
        dq_weight_all = np.array( (1,1,0, 0,0,0) + self.leg_mask() )

        d_level = 0
        if debug:
            d_level = 1
            for const in constraints:
                const.debuglevel = 1

        loop = IK.solveFullbodyIKLoopFast(self.robot,
                                          constraints,
                                          jlim_avoid_weight_old,
                                          dq_weight_all,
                                          20,
                                          1e-6,
                                          d_level)
        if debug:
            for cntr, const in enumerate(constraints):
                const.debuglevel = 1
                if const.checkConvergence():
                    print('constraint %d (%s) : converged'%(cntr, const))
                else:
                    print('constraint %d (%s) : NOT converged'%(cntr, const))

        return loop

    def move_centroid_on_foot_qp(self, p = 0.5, debug = False):
        pass

    def move_centroid_on_foot(self, p = 0.5, debug = False):
        return self.move_centroid_on_foot_cnoid(p = p, debug = debug)

    def fullbody_inverse_kinematics_cnoid(self):
        pass
    def fullbody_inverse_kinematics_qp(self):
        pass
    def fullbody_inverse_kinematics(self):
        return self.fullbody_inverse_kinematics_cnoid()

def merge_mask(tp1, tp2):
    return tuple([x or y for (x, y) in zip(tp1, tp2)])
def invert_mask(tp1):
    return tuple([0 if x else 1 for x in tp1])
