# -*- coding: utf-8 -*-
# Economic of co-firing in two power plants in Vietnam
#
# Basic geometric shapes
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
from natu.math import sqrt, pi
from natu.units import m

class Shape:
    pass


class Disk(Shape):
    def __init__(self, radius):
        assert radius >= 0 * m
        self.radius = radius

    def area(self):
        return pi * self.radius**2

    def first_moment_of_area(self):
        """With respect to the center"""
        return 2 * pi * self.radius**3 / 3

    def shrink(self, factor):
        """Shrink or extend the area by a given factor"""
        assert factor >= 0
        return Disk(self.radius * sqrt(factor))


class Annulus(Shape):
    """An annulus is the area between two concentric disks"""
    def __init__(self, r, R):
        assert R >= r >= 0 * m
        self.r = r
        self.R = R

    def area(self):
        return pi * (self.R**2 - self.r**2)

    def first_moment_of_area(self):
        """With respect to the centroid"""
        return 2 * pi * (self.R**3 - self.r**3) / 3

    def shrink(self, factor):
        """Shrink or extend the area by a given factor, keeping the inner radius constant"""
        assert factor >= 0
        new_R = sqrt(self.r**2 + factor * (self.R**2 - self.r**2))
        return Annulus(self.r, new_R)


class Semi_Annulus(Annulus):
    def __init__(self, r, R):
        super().__init__(r, R)

    def area(self):
        return super().area() / 2

    def first_moment_of_area(self):
        return super().first_moment_of_area() / 2

    def shrink(self, factor):
        """Shrink or extend the area by a given factor, keeping the inner radius constant"""
        assert factor >= 0
        new_R = sqrt(self.r**2 + factor * (self.R**2 - self.r**2))
        return Semi_Annulus(self.r, new_R)
