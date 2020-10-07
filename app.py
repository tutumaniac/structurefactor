from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
import pickledb
import lib
import uuid

db = pickledb.load('test.db', False)
db.dcreate('crystals')

app = Flask(__name__)
CORS(app)
api = Api(app)

data = api.namespace('data', description='Data stuff')

@data.route('/crystals')
class Crystals(Resource):
    def get(self):
        crystals = db.dgetall('crystals') 
        return [{'crystal_id':key, 'name':crystals[key].name} for key in crystals], 200

    def post(self):
        id = str(uuid.uuid4())
        crystal = lib.Crystal.fromDict(api.payload)
        db.dadd(
            'crystals',
            (id, crystal)
        )
        return {'id': id}, 201

@data.route('/crystals/<string:crystal_id>')
class Crystal(Resource):
    def get(self, crystal_id):
        crystal = db.dget('crystals', crystal_id)
        return crystal.toDict(), 200

    def put(self, crystal_id):
        crystal = lib.Crystal.fromDict(api.payload)
        db.dadd(
            'crystals',
            (crystal_id, crystal)
        )
        return '', 200

    def delete(self, crystal_id):
        db.dpop(
            'crystals',
            crystal_id
        )
        return '', 204


@data.route('/crystals/<string:crystal_id>/structurefactor')
class Structurefactor(Resource):
    def get(self, crystal_id):
        return {'hello':'world'}

# @data.route('/crystals/<int:crystal_id>/basis')
# class Basis(Resource):
#     def get(self, id):
#         return {'hello':'world'}

# @data.route('/crystals/<int:crystal_id>/basis/atoms')
# class Atoms(Resource):
#     def get(self, id):
#         return {'hello':'world'}

# @data.route('/crystals/<int:crystal_id>/basis/atoms/<int:atom_id>')
# class Atom(Resource):
#     def get(self, id):
#         return {'hello':'world'}

# @data.route('/crystals/<int:crystal_id>/basis/bonds')
# class Bonds(Resource):
#     def get(self, id):
#         return {'hello':'world'}

# @data.route('/crystals/<int:crystal_id>/basis/bonds/<int:bond_id>')
# class Bond(Resource):
#     def get(self, id):
#         return {'hello':'world'}

# @data.route('/crystals/<int:crystal_id>/crystalclass')
# class Crystalclass(Resource):
#     def get(self, id):
#         return {'hello':'world'}

if __name__ == '__main__':
    app.run(debug=True)