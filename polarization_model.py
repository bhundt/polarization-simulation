from functools import partial
import math
import numpy as np
import agentpy as ap

class Person(ap.Agent):
    """ a Person which has a polarization """

    def setup(self):
        self.polarization = 0.0
        #self.initial_polarization = self.polarization
        #self.group = 0
        pass

    def _move_to(self, partner_pol):
        move_amount = (partner_pol - self.polarization) * self.model.p.R
        self.polarization = self.polarization + move_amount
        self._enforce_polarization_bounds()
    
    def _move_away(self, partner_pol):
        move_amount = (self.polarization - partner_pol) * self.model.p.R
        self.polarization = self.polarization + move_amount
        self._enforce_polarization_bounds()

    def _enforce_polarization_bounds(self):
        if self.polarization > 1.0:
            self.polarization = 1.0
        if self.polarization < 0.0:
            self.polarization = 0.0


    def update_polarization(self):
        # # we model self interest as the tendency to move to ones initial starting point
        # if self.model.nprandom.random() <= self.model.p.P:
        #     self._move_to(self.initial_polarization)

        # pick a random agent
        partner = self.model.agents.random().to_list()[0]
        partner_dist = np.abs( self.polarization - partner.polarization)
        
        # # with a certain prob. we will just be repulsed by a member of the opposite group regardless of distance; similiarily we will be attracted by a member of our own group
        # if (self.model.nprandom.random() <= self.model.p.A) and (self.group != 0):
        #     if (self.group == partner.group):
        #         self._move_to(partner.polarization)
        #     if (self.group != partner.group):
        #         self._move_away(partner.polarization) 

        # check whether we can interact, interaction prob is ~ (1/2)^(d/E)
        interaction_prob = math.pow(1/2, partner_dist / self.model.p.E)
        if self.model.nprandom.random() <= interaction_prob:
            # if we are within tolerance range we move closer (attraction), else we are repulsed
            if partner_dist <= self.model.p.T:
                self._move_to(partner.polarization)
            else:
                self._move_away(partner.polarization)


class PolarizationModel(ap.Model):

    """ A model simulating the evolution of polarization in society """
    def setup(self):
        # init agents
        self.agents = ap.AgentList(self, self.p.agents, Person)

        # init polarization change
        for agent in self.agents:
            agent.polarization = self.nprandom.normal(loc=0.5, scale= 0.2)
            #agent.initial_polarization = agent.polarization
            #agent.group = self.random.choice([-1, 0, 1])

    def step(self):
        self.agents.update_polarization()

    def update(self):
        self.record('Mean', np.mean(np.array(self.agents.polarization)))
        self.record('Std', np.std(np.array(self.agents.polarization)))
        self.record('Var', np.var(np.array(self.agents.polarization)))
        
        hist_values, bins = np.histogram(np.array([pol for pol in self.agents.polarization]), bins=25)
        self.record('Hist', hist_values)
        self.record('Bins', bins)

    def end(self):
        pass