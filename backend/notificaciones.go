package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/streadway/amqp"
)

type Notificacion struct {
	ID      int    `json:"id"`
	Mensaje string `json:"mensaje"`
}

var notificaciones []Notificacion

// Función para obtener las notificaciones
func obtenerNotificaciones(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(notificaciones)
}

// Función para agregar una nueva notificación
func agregarNotificacion(w http.ResponseWriter, r *http.Request) {
	var nueva Notificacion
	err := json.NewDecoder(r.Body).Decode(&nueva)
	if err != nil {
		http.Error(w, "Datos inválidos", http.StatusBadRequest)
		return
	}
	nueva.ID = len(notificaciones) + 1
	notificaciones = append(notificaciones, nueva)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(nueva)
}

// Función para consumir mensajes desde RabbitMQ
func consumirMensajesRabbitMQ() {
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		log.Fatalf("Error al conectar con RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Error al abrir canal: %s", err)
	}
	defer ch.Close()

	// Consumir mensajes de la cola "ventas"
	msgs, err := ch.Consume(
		"ventas", // Nombre de la cola
		"",
		true,  // auto ack
		false, // exclusivity
		false, // no local
		false, // no wait
		nil,   // no arguments
	)
	if err != nil {
		log.Fatalf("Error al consumir mensajes: %s", err)
	}

	// Canal para esperar los mensajes
	forever := make(chan bool)

	// Goroutine para procesar los mensajes recibidos
	go func() {
		for d := range msgs {
			log.Printf("Mensaje recibido: %s", d.Body)

			// Crear una notificación a partir del mensaje recibido
			notificacion := Notificacion{
				ID:      len(notificaciones) + 1,
				Mensaje: string(d.Body),
			}

			// Agregar la notificación a la lista
			notificaciones = append(notificaciones, notificacion)
			log.Printf("Notificación agregada: %v", notificacion)
		}
	}()

	log.Printf("Esperando mensajes...")

	// Bloquear el proceso para que siga recibiendo mensajes
	<-forever
}

func main() {
	// Configurar rutas del servidor HTTP para manejar notificaciones
	http.HandleFunc("/notificaciones", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			obtenerNotificaciones(w, r)
		case http.MethodPost:
			agregarNotificacion(w, r)
		default:
			http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
		}
	})

	// Iniciar el servidor HTTP en una goroutine
	go func() {
		fmt.Println("Servidor de notificaciones ejecutándose en http://localhost:8080")
		log.Fatal(http.ListenAndServe(":8080", nil))
	}()

	// Iniciar la función para consumir mensajes de RabbitMQ
	consumirMensajesRabbitMQ()
}
