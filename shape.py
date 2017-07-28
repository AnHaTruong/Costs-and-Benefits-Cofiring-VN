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
    """Abstract base class for a geometric shape.

    Let's keep it simple, since all fits in one file:
    Child classes should define init, str, area, first_moment_of_area and shrink.
    """

    def area(self):
        pass

    def first_moment_of_area(self):
        pass

    def shrink(self, factor):
        pass


class Disk(Shape):
    """A disk is the area inside a circle."""

    def __init__(self, radius):
        assert radius >= 0 * m
        self.radius = radius

    def __str__(self):
        return "Disk with radius " + str(self.radius) + ", area " + str(self.area())

    def area(self):
        return pi * self.radius**2

    def first_moment_of_area(self):
        """Return first momement with respect to the center."""
        return 2 * pi * self.radius**3 / 3

    def shrink(self, factor):
        """Return a new homotetic disk, changing the area by factor."""
        assert factor >= 0
        return Disk(self.radius * sqrt(factor))

    def outer_radius(self):
        return self.radius


class Annulus(Shape):
    """An annulus is the area between two concentric disks, a ring in common language."""

    def __init__(self, r, R):
        assert R >= r >= 0 * m
        self.r = r
        self.R = R

    def __str__(self):
        return ("Annulus with inner radius " + str(self.r)
                + ", outer radius " + str(self.R)
                + ", area " + str(self.area())
                )

    def area(self):
        return pi * (self.R**2 - self.r**2)

    def first_moment_of_area(self):
        """Return first moment with respect to the centroid."""
        return 2 * pi * (self.R**3 - self.r**3) / 3

    def shrink(self, factor):
        """Return a new Annulus, with same inner radius and total area scaled by factor."""
        assert factor >= 0
        new_R = sqrt(self.r**2 + factor * (self.R**2 - self.r**2))
        return Annulus(self.r, new_R)

    def outer_radius(self):
        return self.R


class Semiannulus(Annulus):
    """A semiannulus is half an annulus."""

    def __init__(self, r, R):
        Annulus.__init__(self, r, R)

    def __str__(self):
        return "Semiannulus. Half of the " + Annulus.__str__(self)

    def area(self):
        return Annulus.area(self) / 2

    def first_moment_of_area(self):
        return Annulus.first_moment_of_area(self) / 2

    def shrink(self, factor):
        """Return a new Semiannulus, with same inner radius and total area scaled by factor."""
        assert factor >= 0
        new_R = sqrt(self.r**2 + factor * (self.R**2 - self.r**2))
        return Semiannulus(self.r, new_R)
