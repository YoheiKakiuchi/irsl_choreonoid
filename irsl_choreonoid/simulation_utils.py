import irsl_choreonoid.cnoid_base as ib
import cnoid.BodyPlugin as BodyPlugin
import cnoid.Body as cbody
from .control_utils import PDController
from .control_utils import BodySequencer
import cnoid.IRSLUtil as IU
import math

## generatesettings of body
def generatePDParameters(body, dt=0.001, P='normal', D='normal', I='normal', updateRotorInertia=False, **kwargs):
    res = {}
    kk=0.05
    if P == 'hard':
        kk=0.5
    elif P == 'soft':
        kk=0.0005
    kd=0.5
    if D == 'hard':
        kd=2.0
    elif D == 'soft':
        kd=0.1
    kI=1.0
    if I == 'hard':
        kI=0.1
    elif I == 'soft':
        kI=10
    ##
    for idx in range(body.numJoints):
        j = body.joint(idx)
        ax = j.jointAxis
        lk_mass, lk_c, lk_I = ru.mergedMassPropertyOfAllDescendants(j)
        joint_m = np.linalg.norm(np.cross(ax, lk_c)) + np.dot(ax, lk_I @ ax)
        K = 2*kk*joint_m/dt/dt
        D = K * kd * ( 10 ** (math.log10(joint_m/5)/4 - 1.5) )
        if updateRotorInertia:
            I = kI * joint_m
            j.setEquivalentRotorInertia(I)
        res[j.jointName] = {'K': K, 'D': D}
    ##
    return res

class SimulationEnvironment(object):
    def __init__(self, robotName, simulator=None, addSimulator=True, fixed=True, world=None):
        """
        """
        self.robot_name = robotName
        if simulator is None:
            res = ib.findItemsByClass( BodyPlugin.SimulatorItem )
            if len(res) == 0:
                if addSimulator:
                    simulator = ib.addSimulator(world=world)
                else:
                    raise Exception('No simulator found')
            else:
                simulator = res[0]
        ## checkRobotName
        self.sim = simulator
        self.sim.setRealtimeSyncMode(3) ## manual-mode
        #self.dt = sim.worldTimeStep
        self.controller = None
        self.sequencer = None
        self._world  = None
        if fixed:
            self.setFixed()

    @property
    def world(self):
        if self._world is None:
            itm = self.sim.parentItem
            if type(item) is BodyPlugin.WorldItem:
                ## simulation should be under worldItem
                self._world = item
        return self._world

    @property
    def bodies(self):
        return ib.findItemsByClass(BodyPlugin.BodyItem, root=self.world)

    @property
    def bodyNames(self):
        return [ bd.name for bd in self.bodies ]

    @property
    def simulationBodies(self):
        return [ self.sim.findSimulationBody(bd.name) for bd in self.bodies ]

    def simulationBody(self, name=None):
        if name is None:
            return self.sim.findSimulationBody(self.robot_name)
        else:
            return self.sim.findSimulationBody(name)

    def setFixed():
        res = ib.findItemsByName(self.robot_name, root=self.world)
        for r in res:
            r.body.rootLink.setJointType(cbody.Link.FixedJoint)

    def start(self, addCountroller=True, addSequencer=True, controllerSettings=None, P=10000, D=200, generatePDsettings=False, **kwargs):
        """
        """
        self.sim.startSimulation()
        sim_body = self.sim.findSimulationBody(self.robot_name)
        if sim_body is None:
            self.sim.stopSimulation()
            raise Exception('No body found : {}'.format(self.robot_name))
        self.body = sim_body.body()
        self.controller = None
        self.sequencer = None
        if generatePDsettings:
            controllerSettings=generatePDParameters(self.body, P=P, D=D, **kwargs)
        if addCountroller:
            self.controller = PDController(self.body, dt=sim.worldTimeStep, P=P, D=D, settings=controllerSettings)
        if addSequencer:
            self.sequencer = BodySequencer(self.body, dt=sim.worldTimeStep)

    def storeInitialState(self):
        """
        """
        for bd in self.bodies:
            bd.storeInitialState()

    def isRunning(self):
        """
        """
        return self.sim.isRunning()

    def stop(self):
        """
        """
        self.sim.stopSimulation()

    def restart(self):
        """
        """
        pass

    def sendAngleVector(self, angle_vector, tm=1.0, **kwargs):
        """
        """
        if self.sequencer is not None:
            self.sequencer.pushNextAngle(angle_vector, tm)

    def sendAngleVectorSequence(self, angle_vector_list, tm_list, **kwargs):
        """
        """
        if self.sequencer is not None:
            self.sequencer.pushNextAngles(angle_vector_list, tm_list)

    def run(self, sec, update=33, stop=False, callback=None, **kwargs):
        """
        """
        if not self.sim.isRunning():
            self.start(**kwargs)
        for i in range(math.floor(sec*1000)):
            if not self.sim.isRunning():
                break
            ##
            if self.sequencer is not None:
                self.sequencer.setNextTarget()
            if self.controller is not None:
                self.controller.control()
            ##
            if update is not None:
                if i % update == 0:
                    self.sim.tickRequest()
                    IU.processEvent()
                    while self.sim.tickRequested():
                        IU.usleep(1)
                else:
                    self.sim.tickRequest(True)
            else:
                self.sim.tickRequest(True)
            if callback is not None:
                callback(self.body)
        if stop:
            self.sim.stopSimulation()
