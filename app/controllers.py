from flask import Blueprint, jsonify, request


def crud_blueprint(name, url_prefix, service):
    bp = Blueprint(name, __name__, url_prefix=url_prefix)

    @bp.get("")
    def list_items():
        return jsonify([i.to_dict() for i in service.list()])

    @bp.get("/<int:item_id>")
    def get_item(item_id):
        return jsonify(service.get(item_id).to_dict())

    @bp.post("")
    def create_item():
        return jsonify(service.create(request.get_json(silent=True)).to_dict()), 201

    @bp.put("/<int:item_id>")
    def update_item(item_id):
        return jsonify(service.update(item_id, request.get_json(silent=True)).to_dict())

    @bp.delete("/<int:item_id>")
    def delete_item(item_id):
        service.delete(item_id)
        return "", 204

    return bp
