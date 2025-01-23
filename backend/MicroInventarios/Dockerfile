# Usar la imagen base oficial de Node.js
FROM node:16-alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo package.json y package-lock.json (si existe)
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto de los archivos del proyecto
COPY . .

# Exponer el puerto en el que la aplicación va a correr
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["node", "inventarios.js"]
