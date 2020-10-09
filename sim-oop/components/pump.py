
"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

    class Pump

                   ┌───────┐
                   │       │
    oNode        ← ┼───────┼← iNode
    (No.j)         │       │  (No.i)
                   └───────┘  
 
  json object example:
     {
            "name": "Feedwater Pump1",
            "type": "PUMP",
            "ef": 1.00,
            "iNode":i,
            "oNode":j
        }

  Last updated: 2018.05.08
  Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from seuif97 import ps2h
from .node import *


class Pump():

    energy = "workRequired"
    devtype = "PUMP"

    def __init__(self, dictDev, nodes):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.iNode = nodes[dictDev['iNode']]
        self.oNode = nodes[dictDev['oNode']]
        self.ef = dictDev['ef']

    def state(self):
        """
        calc oNode of the pump 
        """
        sout_s = self.iNode.s
        hout_s = ps2h(self.oNode.p, sout_s)
        self.oNode.h = self.iNode.h + (hout_s - self.iNode.h)/self.ef
        self.oNode.ph()

    def balance(self):
        """  mass and energy balance the pump    """
        # mass balance
        if self.iNode.fdot is not None:
            self.oNode.fdot = self.iNode.fdot
        elif self.oNode.fdot is not None:
            self.iNode.fdot = self.oNode.fdot

        # energy
        self.workRequired = self.iNode.fdot * (self.oNode.h - self.iNode.h)

    def sm_energy(self):
        self.WRequired = self.iNode.mdot * \
            (self.oNode.h - self.iNode.h)/(3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()

        result += '\nworkRequired(kJ/kg): \t{:>.2f}'.format(self.workRequired)
        result += '\nWRequired(MW): \t{:>.2f}'.format(self.WRequired)
        return result
