const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
require('dotenv').config();

const app = express();

// Rutas de proxy
app.use('/ventas', createProxyMiddleware({ target: 'http://localhost:5000', changeOrigin: true }));
app.use('/empleados', createProxyMiddleware({ target: 'http://localhost:8080', changeOrigin: true }));
app.use('/notificaciones', createProxyMiddleware({ target: 'http://localhost:8081', changeOrigin: true }));

app.listen(process.env.PORT || 3000, () => {
    console.log('API Gateway corriendo en el puerto 3000');
});
