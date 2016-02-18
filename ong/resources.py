# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import OngDocument

ong_blueprint = Blueprint('ong', __name__)
api = Api(ong_blueprint)


@api.resource('/ong/', '/ong/<string:id>')
class OngResource(Resource):

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args(strict=True)
        limit = args.get('limit')
        if limit is not None:
            ongs = OngDocument.objects[:limit]
            return [ong.to_dict() for ong in ongs]
        elif id is not None:
            ong = OngDocument.objects.get_or_404(id=id)
            return ong.to_dict()

        abort(400, message="You must provide limit or id")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args(strict=True)

        name = args.get('name')
        description = args.get("description", None)

        if name is None:
            abort(400, message="You must provide name")

        ong = OngDocument(name=name, description=description).save()
        return ong.to_dict(), 201

    def delete(self, id=None):
        if id is not None:
            ong_document = OngDocument.objects.get_or_404(id=id)
            ong_document.delete()
            return None, 204
        abort(400, message="You must provide an id")

    def put(self, id=None):
        if id is None:
            abort(400, message="You must provide an id")

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args(strict=True)

        name = args.get("name")
        description = args.get("description")
        ong_document = OngDocument.objects.get_or_404(id=id)

        ong_document.name = name
        ong_document.description = description
        ong_document.save()

        return ong_document.to_dict(), 201
