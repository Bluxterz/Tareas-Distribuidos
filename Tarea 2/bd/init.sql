-- init.sql

-- Crear la base de datos
CREATE DATABASE proyecto;

-- Conéctate a la base de datos
\c proyecto;

-- Crear una tabla para almacenar la información de los usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    correo VARCHAR(255),
    usuario VARCHAR(255),
    contraseña VARCHAR(255)
);
