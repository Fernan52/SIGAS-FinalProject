# Usar una imagen base de OpenJDK
FROM openjdk:17-jdk-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo JAR al contenedor
COPY target/MicroEmpleados-1.0-SNAPSHOT.jar /app/empleados.jar
# (Si usas Gradle, usa build/libs en lugar de target/empleados.jar)

# Exponer el puerto en el que se ejecuta la aplicación (por defecto, Spring Boot usa el puerto 8080)
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["java", "-jar", "/app/empleados.jar"]
