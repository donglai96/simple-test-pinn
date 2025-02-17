'''
Author: Donglai Ma
Date: 2021-01-06 18:40:23
LastEditTime: 2021-01-06 19:16:41
LastEditors: Donglai Ma
Description: A generator for multi dipole field
FilePath: \simple-test-pinn\dfield_generator.py
A test work for PINN work
'''

import numpy as np


def B(r, theta, alpha, B0):
    """
    Dipole field
    Args:
        r: radius
        theta: theta in polar coordinate
        alpha: Deviation of magnetic pole from axis
        B0: The strength of magnetic pole at r = 1

    Returns: Br, Btheta

    """
    fac = B0 * (1 / r) ** 3
    return -2 * fac * np.cos(theta + alpha), -fac * np.sin(theta + alpha)


class DipoleMoment(object):

    def __init__(self, name, position, alpha, B0,outputinfo = True):
        """

        Args:
            name: number of this B field
            position: The original coordinate
            alpha: Deviation of magnetic pole from axis
            B0: The strength of magnetic pole at r = 1
        """
        self.name = name
        self.position = position
        self.alpha = alpha
        self.B0 = B0
        if outputinfo:
            print("This is No. {} field ".format(self.name))
            print("The initial position is :", position)
            print("The angle is :", alpha)
            print("The constant(strength) of this dipole field is:", B0)

        self.bfield = None

    def get_field(self, x, y):
        """Get the field from position x and y 


        Args:
            x (array): x
            y (array): y

        Returns:
            Bx, By: two array of magnetic field

        """
        x_, y_ = x-self.position[0], y - self.position[1]
        r, theta = np.hypot(x_, y_), np.arctan2(y_, x_)
        Br, Btheta = B(r, theta,self.alpha, self.B0)
        c, s = np.cos(np.pi / 2 + theta), np.sin(np.pi / 2 + theta)
        Bx = -Btheta * s + Br * c
        By = Btheta * c + Br * s
        return Bx, By


def get_field_t(t):
    a = np.sin(t)
    k,m,n,i = 50,50,5,60

    x0 = -1000
    y0 = 0
    theta0 = -30.6
    s0 = 62


    x = x0 + k*a
    y = y0
    theta = theta0 + n*a
    s = s0 + i*a

    polar1 = DipoleMoment(name = 1, position = [500,0],
                             alpha= np.radians(9.6),
                             B0 = 5,outputinfo=False)

    polar2 = DipoleMoment(name = 2, position = [x,y],
                             alpha= np.radians(theta),
                             B0 = s,outputinfo=False)



    nx, ny = 500, 500
    XMAX, YMAX = 500, 500
    xx = np.linspace(-XMAX, XMAX, nx)
    yy = np.linspace(-YMAX, YMAX, ny)
    X, Y = np.meshgrid(xx, yy)
    Bx_1, By_1 = polar1.get_field(X,Y)


    Bx_2, By_2 = polar2.get_field(X,Y)
    Bx, By = Bx_1 + Bx_2, By_1 + By_2
    return Bx, By