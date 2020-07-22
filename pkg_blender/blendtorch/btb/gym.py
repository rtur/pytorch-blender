import bpy
import zmq

from .animation import AnimationController
from .constants import DEFAULT_TIMEOUTMS


class AgentContext:
    def __init__(self, env):
        self.env = env
        self.reset()

    def reset(self):
        self.time = 0
        self.episode = 1
        self.action = None
        self.reward = None
        self.obs = None
        self.done = False

    def __repr__(self):
        return f'AgentContext(action={self.action}, reward={self.reward}, obs={self.obs}, done={self.done}, time={self.time}, episode={self.episode}>'

    def __str__(self):
        return self.__repr__()
    

class BaseEnv:
    '''Environment base class, based on the model of OpenAI Gym.'''

    def __init__(self, agent, frame_range=None, use_animation=True, offline_render=True):
        self.events = AnimationController()
        self.events.pre_frame.add(self._pre_frame)
        self.events.pre_animation.add(self._pre_animation)
        self.events.post_frame.add(self._post_frame)
        self.agent = agent
        self.agent_context = AgentContext(self)
        self.frame_range = frame_range
        self.events.play(
            self.frame_range, 
            num_episodes=-1, 
            use_animation=use_animation, 
            offline_render=offline_render)

    def _pre_frame(self):
        if self.events.frameid > self.frame_range[0]:
            self.agent_context.time = self.events.frameid
            action = self.agent(self.agent_context)
            if action == None:
                self._restart()
            else:
                self._env_prepare_step(action, self.agent_context)
                self.agent_context.action = action
            
    def _pre_animation(self):        
        self._env_reset(self.agent_context)

    def _post_frame(self):        
        self._env_post_step(self.agent_context)

    def _restart(self):
        self.events.rewind()

    def _env_reset(self, ctx):
        eps = ctx.episode
        ctx.reset()
        ctx.episode = eps + 1
        
    def _env_prepare_step(self, action, ctx):
        raise NotImplementedError()

    def _env_post_step(self, ctx):
        raise NotImplementedError()
        
class RemoteControlledAgent:
    STATE_REQ = 0
    STATE_REP = 1

    def __init__(self, address, timeoutms=DEFAULT_TIMEOUTMS):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.bind(address)
        self.state = RemoteControlledAgent.STATE_REQ
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.timeoutms = timeoutms

    def __call__(self, ctx):
        if self.state == RemoteControlledAgent.STATE_REP:
            self.socket.send_pyobj((ctx.obs, ctx.reward, ctx.done))
            self.state = RemoteControlledAgent.STATE_REQ

        socks = dict(self.poller.poll(self.timeoutms))
        assert self.socket in socks, 'No response within timeout interval.'
        
        cmd, action = self.socket.recv_pyobj()
        assert cmd in ['reset', 'step']
        self.state = RemoteControlledAgent.STATE_REP

        if cmd == 'reset':
            action = None
            if ctx.action is None:
                # Already reset
                action = self.__call__(ctx)        
        return action
        

