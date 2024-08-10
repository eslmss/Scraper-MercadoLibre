-- crea la base de datos donde irán los datos scrapeados de MercadoLibre
CREATE DATABASE PythonScrapedData;

-- Usa la base de datos recién creada
--USE PythonScrapedData;

---- Crea la tabla Productos
--CREATE TABLE Productos (
--    ProductID INT IDENTITY(1,1) PRIMARY KEY,
--    Nombre VARCHAR(100) NOT NULL,
--    Precio DECIMAL(10,2) NOT NULL,
--    URL VARCHAR(255) NOT NULL
--);

--SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Productos]')

--DROP TABLE Productos

--SELECT * FROM Productos

--TRUNCATE TABLE Productos