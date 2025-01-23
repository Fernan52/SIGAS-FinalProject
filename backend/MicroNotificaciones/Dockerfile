# Usar una imagen base oficial de Go
FROM golang:1.23-alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias (si las tienes)
RUN go mod tidy

# Exponer el puerto en el que la aplicación va a correr
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["go", "run", "notificaciones.go"]
