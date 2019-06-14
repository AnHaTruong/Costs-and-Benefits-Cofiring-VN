# -*- coding: utf-8 -*-
# Economic of co-firing in two power plants in Vietnam
#
# Basic geometric shapes
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Define geometric shapes: Disk, Annulus (ring), Semiannulus (half a ring)."""

from natu.math import sqrt, pi
from natu.units import m


class Shape:
    """Abstract base class for a geometric shape.

    Virtual methods: area, first_moment_of_area, shrink, max_radius.
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

    def max_radius(self):
        return self.radius


class Annulus(Shape):
    """An annulus is the area between two concentric disks, a ring in common language."""

    def __init__(self, inner_radius, outer_radius):
        assert outer_radius >= inner_radius >= 0 * m
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

    def __str__(self):
        return ("Annulus with inner radius " + str(self.inner_radius)
                + ", outer radius " + str(self.outer_radius)
                + ", area " + str(self.area())
                )

    def area(self):
        return pi * (self.outer_radius**2 - self.inner_radius**2)

    def first_moment_of_area(self):
        """Return first moment with respect to the centroid."""
        return 2 * pi * (self.outer_radius**3 - self.inner_radius**3) / 3

    def shrink(self, factor):
        """Return a new Annulus, with same inner radius and total area scaled by factor.

        >>> a = Annulus(1 * m, 30 * m)
        >>> print(a)
        Annulus with inner radius 1 m, outer radius 30 m, area 2824.29 m2
        >>> print(a.shrink(0.5))
        Annulus with inner radius 1 m, outer radius 21.225 m, area 1412.15 m(2)
        """
        assert factor >= 0
        new_outer_radius = sqrt(
            self.inner_radius**2 + factor * (self.outer_radius**2 - self.inner_radius**2))
        return Annulus(self.inner_radius, new_outer_radius)

    def max_radius(self):
        return self.outer_radius


class Semiannulus(Annulus):
    """A semiannulus is half an annulus."""

    def __init__(self, inner_radius, outer_radius):
        Annulus.__init__(self, inner_radius, outer_radius)

    def __str__(self):
        return "Semiannulus. Half of the " + Annulus.__str__(self)

    def area(self):
        return Annulus.area(self) / 2

    def first_moment_of_area(self):
        return Annulus.first_moment_of_area(self) / 2

    def shrink(self, factor):
        """Return a new Semiannulus, with same inner radius and total area scaled by factor."""
        assert factor >= 0
        new_outer_radius = sqrt(
            self.inner_radius**2 + factor * (self.outer_radius**2 - self.inner_radius**2))
        return Semiannulus(self.inner_radius, new_outer_radius)
