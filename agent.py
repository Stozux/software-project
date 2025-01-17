from utils.ssl.Navigation import Navigation
from rsoccer_gym.Entities import Robot
from utils.Point import Point
from utils.ssl.base_agent import BaseAgent

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)


    def step(self, my_agents: dict[int, BaseAgent] ,self_robot : Robot, 
             opponents: dict[int, Robot] = dict(), 
             teammates: dict[int, Robot] = dict(), 
             targets: list[Point] = [], 
             keep_targets=False) -> Robot:

        self.reset()
        self.pos = Point(self_robot.x, self_robot.y)
        self.vel = Point(self_robot.v_x, self_robot.v_y)
        self.body_angle = self_robot.theta

        if len(targets) > 0:
            self.targets = targets.copy()
        elif len(self.targets) == 0 or not keep_targets:
            self.targets = []
            
        self.robot = self_robot
        self.opponents = opponents.copy()
        self.teammates = teammates.copy()



        self.decision(my_agents)
        self.post_decision()

        return Robot( id=self.id, yellow=self.yellow,
                      v_x=self.next_vel.x, v_y=self.next_vel.y, v_theta=self.angle_vel)
    

    def decision(self, my_agents: dict[int, BaseAgent]):
        if len(self.targets) == 0:
            return
        if len(my_agents) == 0:
            return
        
        for targ in self.targets:
            keys = list(my_agents.keys())
            vetordisini = Point(targ.x, targ.y) - my_agents[keys[0]].pos
            disini = vetordisini.length()
            agentkey = 0
            for key in keys:
                vetornova = Point(targ.x, targ.y) - my_agents[keys[key]].pos
                novadis = vetornova.length()
                if novadis < disini:
                    disini = novadis
                    agentkey = key

            if agentkey == self.id:
                target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, targ)
                self.set_vel(target_velocity)
                self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
