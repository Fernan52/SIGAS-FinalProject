const express = require('express');
const mongoose = require('mongoose');
const app = express();

app.use(express.json());

// Configuración de la base de datos
const MONGO_URI = 'mongodb://localhost:27017/sigas';
let useMongoDB = true; // Indicador para decidir entre MongoDB o datos en memoria

mongoose.connect(MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => {
    console.log('Conexión exitosa a MongoDB');
  })
  .catch((err) => {
    console.error('Error al conectar a la base de datos:', err);
    console.log('Usando datos en memoria como respaldo.');
    useMongoDB = false;
  });

// Esquema y modelo para MongoDB
const InventarioSchema = new mongoose.Schema({
  producto: String,
  cantidad: Number,
});
const Inventario = mongoose.model('Inventario', InventarioSchema);

// Simulando inventarios en memoria
let inventariosMemoria = [
  { id: 1, producto: 'Arroz', cantidad: 100 },
  { id: 2, producto: 'Azúcar', cantidad: 50 },
];

// Endpoint para obtener inventarios
app.get('/inventarios', async (req, res) => {
  if (useMongoDB) {
    try {
      const inventarios = await Inventario.find();
      res.json(inventarios);
    } catch (err) {
      res.status(500).json({ message: 'Error al obtener inventarios desde MongoDB' });
    }
  } else {
    res.json(inventariosMemoria);
  }
});

// Endpoint para agregar un producto al inventario
app.post('/inventarios', async (req, res) => {
  const { producto, cantidad } = req.body;

  if (useMongoDB) {
    const nuevoInventario = new Inventario({ producto, cantidad });
    try {
      await nuevoInventario.save();
      res.status(201).json(nuevoInventario);
    } catch (err) {
      res.status(500).json({ message: 'Error al agregar al inventario en MongoDB' });
    }
  } else {
    const nuevoProducto = { id: inventariosMemoria.length + 1, producto, cantidad };
    inventariosMemoria.push(nuevoProducto);
    res.status(201).json(nuevoProducto);
  }
});

// Iniciar el servidor
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Microservicio de Inventarios corriendo en el puerto ${PORT}`);
});
