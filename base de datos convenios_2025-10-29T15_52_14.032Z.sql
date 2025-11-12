CREATE OR REPLACE TABLE `municipios` (
	`id_municipio` INTEGER,
	`municipio` VARCHAR(255) NOT NULL,
	PRIMARY KEY(`id_municipio`)
);

CREATE OR REPLACE TABLE `instituciones` (
	`nit_institucion` INTEGER,
	`nombre` VARCHAR(255),
	`direccion` VARCHAR(255),
	`id_municipio` INTEGER,
	`cant_convenios` TINYINT,
	PRIMARY KEY(`nit_institucion`)
);

CREATE OR REPLACE TABLE `homologacion` (
	`id_homologacion` INTEGER,
	`nit_institucion` INTEGER,
	`nombre_programa_sena` VARCHAR(255),
	`cod_programa_sena` VARCHAR(255),
	`version` TINYINT,
	`titulo` VARCHAR(255),
	`programa_ies` VARCHAR(255),
	`nivel_ programa` VARCHAR(255),
	`snies` SMALLINT,
	`creditos_homologados` TINYINT,
	`creditos_totales` TINYINT,
	`creditos_pendientes` TINYINT,
	`modalidad` VARCHAR(255),
	`semestres` VARCHAR(255),
	`regional` VARCHAR(255),
	`enlace` VARCHAR(255),
	PRIMARY KEY(`id_homologacion`)
);

CREATE OR REPLACE TABLE `convenios` (
	`num_proceso` VARCHAR(255),
	`anio` TINYINT,
	`nit_institucion` INTEGER,
	`enlace_convenio` VARCHAR(255),
	`enlace_secop` VARCHAR(255),
	`fecha_inicio` DATETIME,
	`fecha_fin` DATETIME,
	`vigencia` VARCHAR(255),
	PRIMARY KEY(`num_proceso`)
);

CREATE OR REPLACE TABLE `grupos` (
	`ficha` VARCHAR(255) UNSIGNED NOT NULL UNIQUE,
	`cod_programa` MEDIUMINT UNSIGNED,
	`cod_centro` SMALLINT UNSIGNED,
	`modalidad` VARCHAR(50),
	`jornada` VARCHAR(30),
	`etapa_ficha` VARCHAR(30),
	`estado_curso` VARCHAR(30),
	`fecha_inicio` DATE,
	`fecha_fin` DATE,
	`cod_municipio` CHAR(5),
	`cod_estrategia` CHAR(5),
	`nombre_responsable` VARCHAR(80),
	`cupo_asignado` SMALLINT UNSIGNED,
	`num_aprendices_fem` SMALLINT UNSIGNED,
	`num_aprendices_mas` SMALLINT UNSIGNED,
	`num_aprendices_nobin` SMALLINT UNSIGNED,
	`num_aprendices_matriculados` SMALLINT UNSIGNED,
	`num_aprendices_activos` SMALLINT UNSIGNED,
	`tipo_doc_empresa` CHAR(3),
	`num_doc_empresa` VARCHAR(20),
	`nombre_empresa` VARCHAR(80),
	PRIMARY KEY(`ficha`)
);

CREATE OR REPLACE TABLE `egresados` (
	`documento` VARCHAR(255),
	`ficha` VARCHAR(255) UNIQUE,
	`Convenio_media_tecnica` BOOLEAN,
	`fecha_certificacion` DATE,
	`estado_certificado` VARCHAR(255),
	`tipo_documento` VARCHAR(255),
	`nombre_egresado` VARCHAR(255),
	`lugar_recidencia` VARCHAR(255),
	`correo` VARCHAR(255),
	`tel_principal` VARCHAR(255),
	`tel_alterno` VARCHAR(255),
	PRIMARY KEY(`documento`)
);

CREATE OR REPLACE TABLE `egresado_convenio` (
	`documento` VARCHAR(255) NOT NULL UNIQUE,
	`num_proceso` VARCHAR(255),
	PRIMARY KEY(`documento`)
);

ALTER TABLE `instituciones`
ADD FOREIGN KEY(`id_municipio`) REFERENCES `municipios`(`id_municipio`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `homologacion`
ADD FOREIGN KEY(`nit_institucion`) REFERENCES `instituciones`(`nit_institucion`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `convenios`
ADD FOREIGN KEY(`nit_institucion`) REFERENCES `instituciones`(`nit_institucion`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `grupos`
ADD FOREIGN KEY(`ficha`) REFERENCES `egresados`(`ficha`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `convenios`
ADD FOREIGN KEY(`num_proceso`) REFERENCES `egresado_convenio`(`num_proceso`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `egresados`
ADD FOREIGN KEY(`documento`) REFERENCES `egresado_convenio`(`documento`)
ON UPDATE NO ACTION ON DELETE NO ACTION;