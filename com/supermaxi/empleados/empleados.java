package com.supermaxi.empleados;

public class empleados {
    private int id;
    private String nombre;
    private String puesto;

    // Constructor
    public empleados(int id, String nombre, String puesto) {
        this.id = id;
        this.nombre = nombre;
        this.puesto = puesto;
    }

    // Getters y Setters
    public int getId() { 
        return id; 
    }

    public void setId(int id) { 
        this.id = id; 
    }

    public String getNombre() { 
        return nombre; 
    }

    public void setNombre(String nombre) { 
        this.nombre = nombre; 
    }

    public String getPuesto() { 
        return puesto; 
    }

    public void setPuesto(String puesto) { 
        this.puesto = puesto; 
    }

    // Método toString para representar el empleado en formato de texto
    @Override
    public String toString() {
        return "Empleado [id=" + id + ", nombre=" + nombre + ", puesto=" + puesto + "]";
    }

    // Método para actualizar los detalles del empleado
    public void actualizarEmpleado(String nuevoNombre, String nuevoPuesto) {
        this.nombre = nuevoNombre;
        this.puesto = nuevoPuesto;
    }
}
