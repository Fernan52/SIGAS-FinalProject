# Usar la imagen oficial de MongoDB
FROM mongo:6.0

# Establecer las variables de entorno necesarias para inicializar la base de datos
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=rootpassword
ENV MONGO_INITDB_DATABASE=inventarios

# Exponer el puerto 27017 de MongoDB
EXPOSE 27017

# Configurar el punto de entrada predeterminado
CMD ["mongod"]
