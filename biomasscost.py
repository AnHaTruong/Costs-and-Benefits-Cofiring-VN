# Economic of co-firing in two power plants in Vietnam
#
# Biomass cost
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Calculate the unit price of biomass for co-firing as delivered to the plant
    Unit price include fix price and transportation cost
"""

import math
from units import km, zero_km
from natu.math import sqrt
from parameters import MongDuong1, NinhBinh
from strawdata import MongDuong1_straw_density1, MongDuong1_straw_density2
from strawdata import NinhBinh_straw_density

from biomassrequired import biomass_required
from parameters import transport_tariff, tortuosity_factor
from parameters import biomass_fix_cost, biomass_ratio

#
# import math, sympy
#   simplify(integrate(integrate(x, (x, r, R)),(t, 0, pi)) )
#
# The transport activity (t km) is the order one moment
#   tortuosity * simplify(integrate(integrate(x * x, (x, r, R)),(t, 0, pi)) )
#   tortuosity * (R**3 - r**3) / 3


def radius_of_disk(area):
    return sqrt(area / math.pi)


def area_semi_annulus(R, r):
    return math.pi * (R**2 - r**2) / 2


def area_required(Q, D):
    """area needed to provide Q ton of straw when straw density within this area is D (t/ha)
    """
#    assert D > 0 * t / ha
#    assert Q >= 0 * t / y
    return Q / D


def collection_area(plant):
    """
    Biomass is collected from two semi annulus centered on the plant.
    The surface of a semi annulus is  pi * (R**2 - r**2) / 2

    Ninh Binh case: collection area is a disk
    both semi annulus have zero smaller radius, identical larger radius,
    and the same biomass density

    Mong Duong 1 case: collection area is a half disk
    1st semi annulus has zero smaller radius, larger radius = distance from plant to Quang Ninh province border
    2nd semi annulus has smaller radius = larger radius of 1st semi annulus
    1st and 2nd semi annulus have different straw density
    straw density of 1st semi annulus is the straw density of Quang Ninh provice
    straw density of 2nd semi annulus is the average of straw density in adjacent provinces
    """
    if plant == MongDuong1:
        R1 = 50*km  # Large radius of semi annulus 1
        r1 = 0*km   # Small radius of semi annulus 1
        area1 = area_semi_annulus(R1, r1)
        Q = biomass_required(MongDuong1) - area1 * MongDuong1_straw_density1
        area2 = area_required(Q, MongDuong1_straw_density2)
        return area1 + area2

    if plant == NinhBinh:
        return area_required(biomass_required(NinhBinh), NinhBinh_straw_density)


def collection_radius(plant):
    if plant == MongDuong1:
        r1 = 0 * km
        R1 = 50 * km
        r2 = R1
        area1 = area_semi_annulus(R1, r1)

        if biomass_ratio == 0:
            return zero_km
        else:
#        we need to calculate the large radius of 2nd semi annulus.
            area2 = collection_area(MongDuong1) - area1
            radius = sqrt(area2/math.pi*2 + r2**2)
            radius.display_unit = 'km'
            return radius

    if plant == NinhBinh:
        radius = radius_of_disk(collection_area(NinhBinh))
        radius.display_unit = 'km'
        return radius


def transport_tkm(R, r, D, tau):
    """ Transportation activity (in t.km) for biomass collected from a
    collection area of a semi annulus to the center
    R is the large radius
    r is the small radius
    D is the biomass density
    tau is the tortuosity factor
    total_transport_cost = integrate(integrate(x**2 dx dt)) * D * tau
    with x[r, R], t[0, pi]
    """
    return D * tau * math.pi * (R**3 - r**3)/3


# Use an intermediate function "transportation activity" in t km (reused to compute emissions)
# Dig the 5 whys - the units should have prevented error on degree
def bm_transport_tkm(plant):
    """
    Total straw transportation activity of each plant
    """

    if plant == MongDuong1:
        r1 = 0 * km
        R1 = 50 * km
        r2 = R1
        cost_area1 = transport_tkm(R1,
                                   r1,
                                   MongDuong1_straw_density1,
                                   tortuosity_factor
                                   )
        cost_area2 = transport_tkm(collection_radius(MongDuong1),
                                   r2,
                                   MongDuong1_straw_density2,
                                   tortuosity_factor
                                   )
        return cost_area1 + cost_area2

    if plant == NinhBinh:
        return transport_tkm(collection_radius(NinhBinh),
                             0*km,
                             NinhBinh_straw_density,
                             tortuosity_factor
                             )


def bm_transportation_cost(plant):
    """
    Total transportation cost of straw in 1 year is transportation
    activity multiplied by transportation tariff (USD/t/km)
    """
    cost = bm_transport_tkm(plant) * transport_tariff
    cost.display_unit = 'USD/y'
    return cost


def bm_unit_cost(plant):
    cost = bm_transportation_cost(plant) / biomass_required(plant) + biomass_fix_cost
    cost.display_unit = 'USD/t'
    return cost

if __name__ == "__main__":
    import doctest
    doctest.testmod()
