from flask import jsonify


def http_500(e):
    return jsonify({"error": e, "status": 500}), 500

def http_400(e):
    return jsonify({"error": e, "status": 400}), 400

def http_400(e):
    return jsonify({"error": e, "status": 400}), 400


def http_404(e):
    return jsonify({"error": e, "status": 404}), 404


def http_401(e):
    return jsonify({"error": e, "status": 401}), 401


def http_200(m):
    return jsonify({"data": m, "status": 200}), 200
