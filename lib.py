import numpy as np
import json
import os

class Atom():
    
    def __init__(self, name, element, x, y, z, occupation):
        self.name = name
        self.element = element
        self.x = x
        self.y = y
        self.z = z
        self.occupation = occupation

    def toDict(self):
        return {
            'name': self.name,
            'element': self.element,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'occupation': self.occupation
        }

    @classmethod
    def fromDict(cls, atom_dict):
        return cls(**atom_dict)
        

class Crystalclass():
    
    def __init__(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def toDict(self):
        return {
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma,
        }

    @classmethod
    def fromDict(cls, crystalclass_dict):
        return cls(**crystalclass_dict)


class Bond():
    
    def __init__(self, name, atom1, atom2):
        self.name = name
        self.atom1 = atom1
        self.atom2 = atom2

    def toDict(self):
        return {
            'name': self.name,
            'atom1': self.atom1.name,
            'atom2': self.atom2.name,
        }


class Basis():
    
    def __init__(self, name, atoms, bonds, crystalclass):
        self.name = name
        self.atoms = atoms
        self.bonds = bonds
        self.crystalclass = crystalclass

    def toDict(self):
        return {
            'name': self.name,
            'crystalclass': self.crystalclass.toDict(),
            'atoms': [atom.toDict() for atom in self.atoms],
            'bonds': [bond.toDict() for bond in self.bonds]
        }

    @classmethod
    def fromDict(cls, basis_dict):

        name = basis_dict['name']
        atoms = {atom_dict['name']:Atom.fromDict(atom_dict) for atom_dict in basis_dict['atoms']}
        crystalclass = Crystalclass.fromDict(basis_dict['crystalclass'])
        bonds = [Bond( name = bond['name'] , atom1 = atoms[bond['atom1']], atom2 = atoms[bond['atom2']] ) for bond in basis_dict['bonds']]

        return cls(
            name=name,
            atoms=list(atoms.values()),
            bonds=bonds,
            crystalclass=crystalclass
        )
        

class Crystal():
    
    def __init__(self, name, rotation, bulk, surface):
        self.name = name
        self.rotation = rotation
        self.bulk = bulk
        self.surface = surface

    def toDict(self):
        return {
            'name': self.name,
            'rotation': self.rotation,
            'bulk': self.bulk.toDict(),
            'surface': self.surface.toDict()
        }

    @classmethod
    def fromDict(cls, crystal_dict):

        bulk = Basis.fromDict(crystal_dict['bulk'])
        surface = Basis.fromDict(crystal_dict['surface'])

        return cls(
            name=crystal_dict['name'],
            rotation=crystal_dict['rotation'],
            bulk=bulk,
            surface=surface
        )
        

if __name__ == '__main__':
    
    atom_dict = dict(
        name='He1',
        element='He',
        x = 0,
        y = 0,
        z = 0,
        occupation = 0
    )

    atom = Atom.fromDict(atom_dict)

    crystalclass_dict = dict(
        a = 1,
        b = 1,
        c = 1,
        alpha = 90,
        beta = 90,
        gamma = 90
    )

    crystalclass = Crystalclass.fromDict(crystalclass_dict)

    fp = os.path.join( os.path.dirname(__file__), 'basis_test.json' )
    with open( fp, 'r') as file:
        basis_dict = json.load(file)

    basis = Basis.fromDict(basis_dict)

    fp = os.path.join( os.path.dirname(__file__), 'crystal_test.json' )
    with open( fp, 'r') as file:
        crystal_dict = json.load(file)

    crystal = Crystal.fromDict(crystal_dict)
    print(crystal)

    fp = os.path.join( os.path.dirname(__file__), 'crystal_new_test.json' )
    crystal_dict_new = crystal.toDict()
    with open( fp, 'w') as file:
        json.dump(crystal_dict_new, file)