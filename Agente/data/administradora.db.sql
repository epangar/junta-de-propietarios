BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Apartamento" (
	"id_apto"	INTEGER,
	"id_edificio"	INTEGER,
	"cuota_mes"	REAL,
	"derrama"	REAL,
	"deuda"	REAL,
	"estado"	TEXT,
	"propietario"	TEXT,
	"telefono"	TEXT,
	"email"	TEXT,
	"id_usuario"	INTEGER,
	PRIMARY KEY("id_apto" AUTOINCREMENT),
	FOREIGN KEY("id_edificio") REFERENCES "Edificio"("id_edificio"),
	FOREIGN KEY("id_usuario") REFERENCES "Usuario"("id_usuario")
);
CREATE TABLE IF NOT EXISTS "Balance_general" (
	"id_balance"	INTEGER,
	"resultado"	REAL,
	"fecha"	DATE,
	"gastos"	REAL,
	"ingresos"	REAL,
	PRIMARY KEY("id_balance" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Contactos" (
	"id_contacto"	INTEGER,
	"persona_contacto"	TEXT,
	"lugar"	TEXT,
	"telefono"	TEXT,
	"email"	TEXT,
	"horario"	TEXT,
	"id_usuario"	INTEGER,
	PRIMARY KEY("id_contacto" AUTOINCREMENT),
	FOREIGN KEY("id_usuario") REFERENCES "Usuario"("id_usuario")
);
CREATE TABLE IF NOT EXISTS "Edificio" (
	"id_edificio"	INTEGER,
	"direccion"	TEXT NOT NULL,
	"nombre"	TEXT NOT NULL,
	"id_contacto"	INTEGER,
	"id_balance"	INTEGER,
	PRIMARY KEY("id_edificio" AUTOINCREMENT),
	FOREIGN KEY("id_balance") REFERENCES "Balance_general"("id_balance"),
	FOREIGN KEY("id_contacto") REFERENCES "Contactos"("id_contacto")
);
CREATE TABLE IF NOT EXISTS "Gasto_apartamento" (
	"id_gasto_apto"	INTEGER,
	"id_edificio"	INTEGER,
	"id_apto"	INTEGER,
	"concepto"	TEXT,
	"monto"	REAL,
	"fecha"	DATE,
	PRIMARY KEY("id_gasto_apto" AUTOINCREMENT),
	FOREIGN KEY("id_apto") REFERENCES "Apartamento"("id_apto"),
	FOREIGN KEY("id_edificio") REFERENCES "Edificio"("id_edificio")
);
CREATE TABLE IF NOT EXISTS "Junta_Propietario" (
	"id_Junta_Propietario"	INTEGER,
	"Horario"	TEXT,
	"Ubicacion"	TEXT,
	"id_usuario"	INTEGER NOT NULL,
	PRIMARY KEY("id_Junta_Propietario" AUTOINCREMENT),
	FOREIGN KEY("id_usuario") REFERENCES "Usuario"("id_usuario") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Usuario" (
	"id_usuario"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"rol"	TEXT NOT NULL CHECK("rol" IN ('admin', 'junta', 'propietario')),
	"fecha_creacion"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"fecha_modificacion"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"activo"	INTEGER DEFAULT 1,
	PRIMARY KEY("id_usuario" AUTOINCREMENT)
);

CREATE INDEX IF NOT EXISTS "idx_email" ON "Usuario" (
	"email"
);
CREATE INDEX IF NOT EXISTS "idx_rol" ON "Usuario" (
	"rol"
);
CREATE INDEX IF NOT EXISTS "idx_username" ON "Usuario" (
	"username"
);
COMMIT;
