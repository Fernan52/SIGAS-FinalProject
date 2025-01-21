from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada
ventas = []

# Endpoint para obtener todas las ventas
@app.route('/ventas', methods=['GET'])
def obtener_ventas():
    return jsonify(ventas), 200

# Endpoint para agregar una nueva venta
@app.route('/ventas', methods=['POST'])
def agregar_venta():
    datos = request.get_json()
    nueva_venta = {
        "id": len(ventas) + 1,
        "producto": datos.get("producto"),
        "cantidad": datos.get("cantidad"),
        "total": datos.get("total")
    }
    ventas.append(nueva_venta)
    return jsonify(nueva_venta), 201

# Endpoint para obtener una venta específica
@app.route('/ventas/<int:id>', methods=['GET'])
def obtener_venta(id):
    venta = next((v for v in ventas if v["id"] == id), None)
    if venta is None:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(venta), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
