import pika
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada
ventas = []

# Función para enviar mensajes a RabbitMQ
def enviar_mensaje(mensaje):
    try:
        # Establecer conexión con RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        
        # Asegurarse de que la cola 'ventas' exista
        channel.queue_declare(queue='ventas')

        # Convertir el mensaje a formato JSON para enviarlo correctamente
        mensaje_json = json.dumps(mensaje)
        
        # Publicar el mensaje en la cola 'ventas'
        channel.basic_publish(exchange='', routing_key='ventas', body=mensaje_json)
        print(f"Mensaje enviado: {mensaje_json}")
        
        # Cerrar la conexión
        connection.close()
    except Exception as e:
        print(f"Error al enviar mensaje a RabbitMQ: {e}")

# Endpoint para obtener todas las ventas
@app.route('/ventas', methods=['GET'])
def obtener_ventas():
    return jsonify(ventas), 200

# Endpoint para agregar una nueva venta
@app.route('/ventas', methods=['POST'])
def agregar_venta():
    # Obtener los datos de la venta desde el cuerpo de la solicitud
    datos = request.get_json()
    
    # Crear la nueva venta
    nueva_venta = {
        "id": len(ventas) + 1,
        "producto": datos.get("producto"),
        "cantidad": datos.get("cantidad"),
        "total": datos.get("total")
    }
    
    # Agregar la venta a la base de datos simulada
    ventas.append(nueva_venta)

    # Convertir la venta a formato JSON y enviarla a RabbitMQ
    enviar_mensaje(nueva_venta)

    # Retornar la nueva venta como respuesta
    return jsonify(nueva_venta), 201

# Endpoint para obtener una venta específica por su ID
@app.route('/ventas/<int:id>', methods=['GET'])
def obtener_venta(id):
    # Buscar la venta por ID
    venta = next((v for v in ventas if v["id"] == id), None)
    
    # Si no se encuentra la venta, retornar un error 404
    if venta is None:
        return jsonify({"error": "Venta no encontrada"}), 404
    
    # Retornar la venta encontrada
    return jsonify(venta), 200

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en todas las interfaces de red en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
