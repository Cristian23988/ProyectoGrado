-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-11-2022 a las 16:10:46
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `musicp`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad`
--

CREATE TABLE `actividad` (
  `id` int(11) NOT NULL,
  `id_sesion` int(11) NOT NULL,
  `id_tipo_actividad` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `descripcion_actividad` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `actividad`
--

INSERT INTO `actividad` (`id`, `id_sesion`, `id_tipo_actividad`, `id_materia`, `id_profesor`, `descripcion_actividad`) VALUES
(15, 7, 3, 1, 2, '1. EL PENTAGRAMA\r\nRepresentado por cinco líneas y cuatro espacios.'),
(16, 7, 3, 1, 2, '2. LAS CLAVES MUSICALES\r\nRepresentados por signos que definen el orden de las notas que se encuentran en el pentagrama.\r\n'),
(17, 7, 3, 1, 2, '2.1 UBICACIÓN DE LAS CLAVES EN EL PENTAGRAMA'),
(18, 7, 3, 1, 2, '2.2 PUNTO DE ORIGEN DE LAS CLAVES MUSICALES.'),
(19, 7, 3, 1, 2, '3. LAS NOTAS MUSICALES\r\nRepresentadas por medio de unos signos que se escriben en las líneas y espacios del pentagrama. Cada nota representa un sonido musical.\r\n'),
(20, 7, 3, 1, 2, '3.1 LINEAS ADICIONALES\r\nSon pequeñas líneas que se colocan en parte inferior o superior del pentagrama.\r\n'),
(21, 8, 3, 1, 2, '1. Las figuras musicales son siete catalogadas desde mayor a menor duración.'),
(22, 8, 3, 1, 2, '1.2 Valor de duración de cada figura musical y su silencio que equivale a la misma duración de la figura.'),
(23, 10, 3, 1, 2, 'Es la unidad de tiempo en que se divide una frase u obra musical.\r\n\r\n1.	LINEAS DIVISORIAS\r\nSe representa por medio de una línea para separar cada compa en el pentagrama.\r\n'),
(24, 10, 3, 1, 2, '1.2	DOBLE BARRA\r\nSon dos líneas una más aguda y la otra más gruesa que indican el final de una obra.\r\n'),
(25, 10, 3, 1, 2, '2.	TIEMPOS Y PARTES DEL COMPAS\r\nCada compa está dividido en periodos de tiempo de igual duración llamados “Pulsos” estos se representan por medio de números fraccionarios.\r\n'),
(26, 10, 3, 1, 2, '3.	ALTERACIONES\r\nLas alteraciones son símbolos musicales que modifican el sonido de una nota musical.\r\n'),
(29, 7, 4, 1, 2, 'Realizar Examen teorico'),
(30, 11, 2, 1, 2, 'PRACTICA\r\n\r\nSolfeo 1'),
(32, 8, 4, 1, 2, 'Realizar examen teorico'),
(33, 11, 1, 1, 2, 'Realizar Solfeo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_materia`
--

CREATE TABLE `estudiante_materia` (
  `id` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `estudiante_materia`
--

INSERT INTO `estudiante_materia` (`id`, `id_estudiante`, `id_materia`) VALUES
(1, 12, 1),
(2, 13, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_nota_clase`
--

CREATE TABLE `estudiante_nota_clase` (
  `id` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_actividad` int(11) NOT NULL,
  `puntaje` varchar(30) NOT NULL,
  `intentos` int(11) NOT NULL,
  `id_evidencia` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `estudiante_nota_clase`
--

INSERT INTO `estudiante_nota_clase` (`id`, `id_estudiante`, `id_actividad`, `puntaje`, `intentos`, `id_evidencia`) VALUES
(28, 12, 33, '92%', 1, 37),
(30, 12, 30, '17%', 1, 38),
(31, 12, 30, '4%', 1, 39),
(32, 12, 30, '98%', 1, 40),
(33, 12, 30, '31%', 1, 41),
(34, 12, 30, '31%', 1, 42),
(35, 12, 30, '97%', 1, 43);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evidencia_estudiante`
--

CREATE TABLE `evidencia_estudiante` (
  `id` int(11) NOT NULL,
  `ruta` varchar(100) NOT NULL,
  `id_estudiante` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `evidencia_estudiante`
--

INSERT INTO `evidencia_estudiante` (`id`, `ruta`, `id_estudiante`) VALUES
(32, 'src/audio/audio_de_estudiante/voz_solfeo.wav', 12),
(33, 'src/audio/audio_de_estudiante/voz_solfeo0.wav', 12),
(34, 'src/audio/audio_de_estudiante/voz_solfeo1.wav', 12),
(35, 'src/audio/audio_de_estudiante/voz_solfeo2.wav', 12),
(36, 'src/audio/audio_de_estudiante/voz_solfeo3.wav', 12),
(37, 'src/audio/audio_de_estudiante/voz_solfeo4.wav', 12),
(38, 'src/audio/audio_de_estudiante/voz_solfeo5.wav', 12),
(39, 'src/audio/audio_de_estudiante/voz_solfeo6.wav', 12),
(40, 'src/audio/audio_de_estudiante/voz_solfeo7.wav', 12),
(41, 'src/audio/audio_de_estudiante/voz_solfeo8.wav', 12),
(42, 'src/audio/audio_de_estudiante/voz_solfeo9.wav', 12),
(43, 'src/audio/audio_de_estudiante/voz_solfeo10.wav', 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examen_multiple`
--

CREATE TABLE `examen_multiple` (
  `id` int(11) NOT NULL,
  `id_actividad` int(11) NOT NULL,
  `texto_descripcion` text NOT NULL,
  `ruta_imagen_descripcion` varchar(60) NOT NULL,
  `id_sesion` int(11) NOT NULL,
  `id_tipo_material` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `examen_multiple`
--

INSERT INTO `examen_multiple` (`id`, `id_actividad`, `texto_descripcion`, `ruta_imagen_descripcion`, `id_sesion`, `id_tipo_material`) VALUES
(8, 29, 'TAREAS 1\r\nRepresentadas por medio de unos signos que se escriben en las líneas y espacios del pentagrama. Cada nota representa un sonido musical.\r\n\r\nSeleccione la opción que coincide con la nota que está en color ROJO y la clave musical del pentagrama.', 'src/image_preguntas/pregunta1.png', 7, 1),
(9, 32, 'Seleccione la opción con el tiempo correspondiente a la figura musical y el silencio de la figura.', 'src/image_preguntas/pregunta2.png', 8, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materia`
--

CREATE TABLE `materia` (
  `id` int(11) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `descripcion` varchar(60) NOT NULL,
  `id_profesor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `materia`
--

INSERT INTO `materia` (`id`, `titulo`, `descripcion`, `id_profesor`) VALUES
(1, 'Clase1', 'Teoria, practica y solfeo', 2),
(3, 'Clase2', 'Solfeo', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `material`
--

CREATE TABLE `material` (
  `id` int(11) NOT NULL,
  `id_tipo_material` int(11) NOT NULL,
  `ruta` varchar(100) NOT NULL,
  `id_sesion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_actividad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `material`
--

INSERT INTO `material` (`id`, `id_tipo_material`, `ruta`, `id_sesion`, `id_usuario`, `id_actividad`) VALUES
(94, 1, 'src/material_actividad/archivo_actividad_1_imagen_4.png', 7, 2, 18),
(95, 1, 'src/material_actividad/archivo_actividad_1_imagen_5.png', 7, 2, 19),
(96, 1, 'src/material_actividad/archivo_actividad_1_imagen_6.png', 7, 2, 20),
(97, 1, 'src/material_actividad/archivo_actividad_1_imagen_2.png', 7, 2, 16),
(98, 1, 'src/material_actividad/archivo_actividad_1_imagen_1.png', 7, 2, 15),
(99, 1, 'src/material_actividad/archivo_actividad_1_imagen_3.png', 7, 2, 17),
(100, 1, 'src/material_actividad/archivo_actividad_2_imagen_1.png', 8, 2, 21),
(101, 1, 'src/material_actividad/archivo_actividad_2_imagen_2.png', 8, 2, 22),
(102, 1, 'src/material_actividad/archivo_actividad_3_imagen_1.png', 10, 2, 23),
(103, 1, 'src/material_actividad/archivo_actividad_3_imagen_2.png', 10, 2, 24),
(104, 1, 'src/material_actividad/archivo_actividad_3_imagen_3.png', 10, 2, 25),
(105, 1, 'src/material_actividad/archivo_actividad_3_imagen_4.png', 10, 2, 26),
(123, 3, 'src/audio/audio_de_profesor/audio_profesor.wav', 11, 2, 33),
(124, 3, 'src/audio/audio_de_profesor/audio_profesor0.wav', 11, 2, 30);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nota_quiz`
--

CREATE TABLE `nota_quiz` (
  `id` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_actividad` int(11) NOT NULL,
  `puntaje` varchar(11) NOT NULL,
  `id_sesion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `nota_quiz`
--

INSERT INTO `nota_quiz` (`id`, `id_estudiante`, `id_actividad`, `puntaje`, `id_sesion`) VALUES
(1, 12, 15, '3.0', 7),
(2, 13, 15, '3.0', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas`
--

CREATE TABLE `respuestas` (
  `id` int(11) NOT NULL,
  `respuesta` text NOT NULL,
  `id_examen` int(11) NOT NULL,
  `rta` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `respuestas`
--

INSERT INTO `respuestas` (`id`, `respuesta`, `id_examen`, `rta`) VALUES
(7, 'Nota Si y Clave Fa', 8, 0),
(8, 'Nota Sol y Clave Sol', 8, 1),
(9, 'Nota Fa y Clave Sol', 8, 0),
(10, 'Nota Re y Clave Fa', 8, 0),
(11, '1/8 Tiempo', 9, 1),
(12, '1/16', 9, 0),
(13, '1 Tiempo', 9, 0),
(14, '1/2 Tiempo', 9, 0),
(15, '4 Tiempos', 9, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id_rol` int(11) NOT NULL,
  `rol` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `rol`) VALUES
(1, 'Administrador'),
(2, 'Profesor'),
(3, 'Estudiante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesion`
--

CREATE TABLE `sesion` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `corte` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `sesion`
--

INSERT INTO `sesion` (`id`, `title`, `id_materia`, `corte`) VALUES
(7, 'ESCRITURA MUSICAL', 1, 1),
(8, 'FIGURAS MUSICALES', 1, 1),
(10, 'EL COMPAS', 1, 1),
(11, 'SOLFEO', 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_actividad`
--

CREATE TABLE `tipo_actividad` (
  `id` int(11) NOT NULL,
  `descripcion_actividad` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `tipo_actividad`
--

INSERT INTO `tipo_actividad` (`id`, `descripcion_actividad`) VALUES
(1, 'Quiz_Solfeo'),
(2, 'Practica'),
(3, 'Teoria'),
(4, 'Quiz_Teorico');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_archivo`
--

CREATE TABLE `tipo_archivo` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `tipo_archivo`
--

INSERT INTO `tipo_archivo` (`id`, `descripcion`) VALUES
(1, 'Imagen'),
(2, 'PDF'),
(3, 'Audio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_Usuario` int(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `rol` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_Usuario`, `username`, `password`, `rol`) VALUES
(2, 'profesor', '1234', 2),
(12, 'Cristian', '1234', 3),
(13, 'Manuel', '1234', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_sesion` (`id_sesion`),
  ADD KEY `id_tipo_actividad` (`id_tipo_actividad`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `estudiante_materia`
--
ALTER TABLE `estudiante_materia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `estudiante_nota_clase`
--
ALTER TABLE `estudiante_nota_clase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_actividad` (`id_actividad`),
  ADD KEY `id_evidencia` (`id_evidencia`);

--
-- Indices de la tabla `evidencia_estudiante`
--
ALTER TABLE `evidencia_estudiante`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `examen_multiple`
--
ALTER TABLE `examen_multiple`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_actividad` (`id_actividad`),
  ADD KEY `id_sesion` (`id_sesion`),
  ADD KEY `id_tipo_material` (`id_tipo_material`);

--
-- Indices de la tabla `materia`
--
ALTER TABLE `materia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_profesor` (`id_profesor`);

--
-- Indices de la tabla `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_tipo_material` (`id_tipo_material`),
  ADD KEY `id_sesion` (`id_sesion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_actividad` (`id_actividad`);

--
-- Indices de la tabla `nota_quiz`
--
ALTER TABLE `nota_quiz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_actividad` (`id_actividad`),
  ADD KEY `id_sesion` (`id_sesion`);

--
-- Indices de la tabla `respuestas`
--
ALTER TABLE `respuestas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_examen` (`id_examen`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `sesion`
--
ALTER TABLE `sesion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `tipo_actividad`
--
ALTER TABLE `tipo_actividad`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_archivo`
--
ALTER TABLE `tipo_archivo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_Usuario`),
  ADD KEY `rol` (`rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividad`
--
ALTER TABLE `actividad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `estudiante_nota_clase`
--
ALTER TABLE `estudiante_nota_clase`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `evidencia_estudiante`
--
ALTER TABLE `evidencia_estudiante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT de la tabla `examen_multiple`
--
ALTER TABLE `examen_multiple`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `materia`
--
ALTER TABLE `materia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `material`
--
ALTER TABLE `material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=125;

--
-- AUTO_INCREMENT de la tabla `nota_quiz`
--
ALTER TABLE `nota_quiz`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `respuestas`
--
ALTER TABLE `respuestas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `sesion`
--
ALTER TABLE `sesion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tipo_actividad`
--
ALTER TABLE `tipo_actividad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `tipo_archivo`
--
ALTER TABLE `tipo_archivo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_Usuario` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD CONSTRAINT `actividad_ibfk_2` FOREIGN KEY (`id_tipo_actividad`) REFERENCES `tipo_actividad` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `actividad_ibfk_4` FOREIGN KEY (`id_sesion`) REFERENCES `sesion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `actividad_ibfk_5` FOREIGN KEY (`id_profesor`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `actividad_ibfk_6` FOREIGN KEY (`id_materia`) REFERENCES `materia` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `estudiante_materia`
--
ALTER TABLE `estudiante_materia`
  ADD CONSTRAINT `estudiante_materia_ibfk_1` FOREIGN KEY (`id_materia`) REFERENCES `materia` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `estudiante_materia_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `estudiante_nota_clase`
--
ALTER TABLE `estudiante_nota_clase`
  ADD CONSTRAINT `estudiante_nota_clase_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `estudiante_nota_clase_ibfk_2` FOREIGN KEY (`id_actividad`) REFERENCES `actividad` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `estudiante_nota_clase_ibfk_3` FOREIGN KEY (`id_evidencia`) REFERENCES `evidencia_estudiante` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `evidencia_estudiante`
--
ALTER TABLE `evidencia_estudiante`
  ADD CONSTRAINT `evidencia_estudiante_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `examen_multiple`
--
ALTER TABLE `examen_multiple`
  ADD CONSTRAINT `examen_multiple_ibfk_1` FOREIGN KEY (`id_actividad`) REFERENCES `actividad` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `examen_multiple_ibfk_2` FOREIGN KEY (`id_sesion`) REFERENCES `sesion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `examen_multiple_ibfk_3` FOREIGN KEY (`id_tipo_material`) REFERENCES `tipo_archivo` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `materia`
--
ALTER TABLE `materia`
  ADD CONSTRAINT `materia_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `material`
--
ALTER TABLE `material`
  ADD CONSTRAINT `material_ibfk_1` FOREIGN KEY (`id_tipo_material`) REFERENCES `tipo_archivo` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `material_ibfk_2` FOREIGN KEY (`id_sesion`) REFERENCES `sesion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `material_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `material_ibfk_4` FOREIGN KEY (`id_actividad`) REFERENCES `actividad` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `nota_quiz`
--
ALTER TABLE `nota_quiz`
  ADD CONSTRAINT `nota_quiz_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `usuario` (`id_Usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `nota_quiz_ibfk_2` FOREIGN KEY (`id_sesion`) REFERENCES `sesion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `nota_quiz_ibfk_3` FOREIGN KEY (`id_actividad`) REFERENCES `actividad` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `respuestas`
--
ALTER TABLE `respuestas`
  ADD CONSTRAINT `respuestas_ibfk_1` FOREIGN KEY (`id_examen`) REFERENCES `examen_multiple` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `sesion`
--
ALTER TABLE `sesion`
  ADD CONSTRAINT `sesion_ibfk_1` FOREIGN KEY (`id_materia`) REFERENCES `materia` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`rol`) REFERENCES `rol` (`id_rol`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
