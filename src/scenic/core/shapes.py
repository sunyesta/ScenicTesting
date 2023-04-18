""" Module containing the Shape class and its subclasses, which represent shapes of Objects"""

from abc import ABC, abstractmethod

import trimesh
from trimesh.transformations import translation_matrix, quaternion_matrix, concatenate_matrices
import numpy

from scenic.core.distributions import (distributionFunction, distributionMethod, Samplable,
                                       needsSampling, toDistribution)
from scenic.core.vectors import Orientation
from scenic.core.utils import cached_property

###################################################################################################
# Abstract Classes and Utilities
###################################################################################################

class Shape(Samplable, ABC):
    """ An abstract base class for Scenic shapes.

    Represents physical shape in Scenic. Does not represent position or orientation,
    which is all handled by the region class. Does contain dimension information, which
    is used as a default value by any Object with this shape and can be overwritten.

    Args:
        dimensions: The raw (before scaling) dimensions of the shape. If dimensions
          and scale are both specified the dimensions are first set by dimensions, and then
          scaled by scale.
        scale: Scales all the dimensions of the shape by a multiplicative factor.
          If dimensions and scale are both specified the dimensions are first set by dimensions,
          and then scaled by scale.
    """
    def __init__(self, dimensions, scale):
        # Report dimensions and scale as samplable
        dimensions = toDistribution(dimensions)
        super().__init__([dimensions, scale])

        # Store values
        self.raw_dimensions = dimensions
        self.scale = scale
        self.dimensions = tuple(dim * self.scale for dim in self.raw_dimensions)
        self.width = self.dimensions[0]
        self.length = self.dimensions[1]
        self.height = self.dimensions[2]

    @cached_property
    def containsCenter(self):
        """Whether or not this object contains its central point"""
        pq = trimesh.proximity.ProximityQuery(self.mesh)
        region_distance = pq.signed_distance([(0,0,0)])[0]

        return region_distance > 0

    @property
    @abstractmethod
    def mesh(self):
        pass

###################################################################################################
# 3D Shape Classes
###################################################################################################

class MeshShape(Shape):
    """ A Shape subclass defined by a Trimesh object.

    Args:
        mesh: A trimesh.Trimesh mesh object.
        dimensions: The raw (before scaling) dimensions of the shape. If dimensions
          and scale are both specified the dimensions are first set by dimensions, and then
          scaled by scale.
        scale: Scales all the dimensions of the shape by a multiplicative factor.
          If dimensions and scale are both specified the dimensions are first set by dimensions,
          and then scaled by scale.
        initial_rotation: A 3-tuple containing the yaw, pitch, and roll respectively to apply when loading
          the mesh. Note the initial_rotation must be fixed.
    """
    def __init__(self, mesh, dimensions=None, scale=1, initial_rotation=None):
        # Ensure the mesh is watertight so volume is well defined
        if not mesh.is_watertight:
            raise ValueError("A MeshShape cannot be defined with a mesh that does not have a well defined volume.")

        # Copy mesh and center vertices around origin
        self._mesh = mesh.copy()
        self._mesh.vertices -= self._mesh.bounding_box.center_mass

        # If dimensions are not specified, infer them.
        if dimensions is None:
            dimensions = list(self._mesh.extents)

        # If rotation is provided, apply rotation
        if initial_rotation is not None:
            if needsSampling(initial_rotation):
                raise ValueError("Shape initial_rotation parameter must be fixed." +
                    "If you want to orient an Object randomly, you should change the Object's rotation.")

            rotation = Orientation.fromEuler(*initial_rotation)
            rotation_matrix = quaternion_matrix((rotation.w, rotation.x, rotation.y, rotation.z))
            self._mesh.apply_transform(rotation_matrix)

        # Scale mesh to unit size
        scale_vals = self._mesh.extents / numpy.array([1,1,1])
        scale_matrix = numpy.eye(4)
        scale_matrix[:3, :3] /= scale_vals
        self._mesh.apply_transform(scale_matrix)

        # Report samplables
        super().__init__(dimensions, scale)

    @property
    def mesh(self):
        return self._mesh

    @classmethod
    def fromFile(cls, path, type, dimensions=None, scale=1, initial_rotation=None):
        with open(path, "r") as mesh_file:
            mesh = trimesh.load(mesh_file, file_type=type)

        return cls(mesh, dimensions=dimensions, scale=scale, initial_rotation=initial_rotation)

    def sampleGiven(self, values):
        return MeshShape(self.mesh, values[self.raw_dimensions], values[self.scale])

class BoxShape(MeshShape):
    def __init__(self, dimensions=(1,1,1), scale=1):
        # Report samplables
        super().__init__(trimesh.creation.box((1,1,1)), dimensions, scale)

class CylinderShape(MeshShape):
    def __init__(self, dimensions=(1,1,1), scale=1, sections=24):
        # Report samplables
        super().__init__(trimesh.creation.cylinder(radius=0.5, height=1, sections=sections), dimensions, scale)
        self.sections=sections
    
    def sampleGiven(self, values):
        return CylinderShape(values[self.raw_dimensions], values[self.scale], sections=self.sections)

class ConeShape(MeshShape):
    def __init__(self, dimensions=(1,1,1), scale=1):
        # Report samplables
        super().__init__(trimesh.creation.cone(radius=0.5, height=1), dimensions, scale)

class SpheroidShape(MeshShape):
    def __init__(self, dimensions=(1,1,1), scale=1):
        # Report samplables
        super().__init__(trimesh.creation.icosphere(radius=1), dimensions, scale)