"""
FASE 3: NORMALIZACIÓN Y CARGA EN POSTGRESQL
Sistema de Información de Equidad Educativa

Este script:
1. Lee CSVs sintéticos de Phase 2
2. Normaliza a 3NF
3. Conecta a PostgreSQL
4. Crea tablas dimensionales y de hechos
5. Carga datos con integridad referencial
6. Genera reporte de carga
"""

import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import sql, Error
import os
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("FASE 3: NORMALIZACIÓN Y CARGA EN POSTGRESQL")
print("=" * 70)

# ============================================================================
# PASO 1: CONFIGURAR CONEXIÓN POSTGRESQL
# ============================================================================

print("\n1. CONECTANDO A POSTGRESQL...")
print("-" * 70)

# Credenciales
host = 'localhost'
port = 5432
user = 'postgres'
password = '7788'
database = 'equidad_educativa'

try:
    # Conectar al servidor (sin especificar BD para crearla después)
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database='postgres'  # Conectar a BD por defecto
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print(f"   ✓ Conectado a PostgreSQL {host}:{port}")

    # Crear base de datos si no existe
    try:
        cursor.execute(f"CREATE DATABASE {database}")
        print(f"   ✓ Base de datos '{database}' creada")
    except Error as e:
        if 'already exists' in str(e):
            print(f"   ⚠ Base de datos '{database}' ya existe")
        else:
            raise

    cursor.close()
    conn.close()

except Error as e:
    print(f"   ✗ ERROR: No se pudo conectar a PostgreSQL")
    print(f"      {e}")
    exit(1)

# Conectar a la BD específica
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    print(f"   ✓ Conectado a base de datos '{database}'")
except Error as e:
    print(f"   ✗ ERROR: No se pudo conectar a la BD {database}")
    print(f"      {e}")
    exit(1)

# ============================================================================
# PASO 2: LEER DATOS SINTÉTICOS
# ============================================================================

print("\n2. LEYENDO DATOS SINTÉTICOS...")
print("-" * 70)

try:
    df_poblacion = pd.read_csv('data/synthetic/poblacion_penitenciaria.csv')
    print(f"   ✓ Población: {len(df_poblacion)} registros")
except FileNotFoundError:
    print("   ✗ ERROR: No encontré poblacion_penitenciaria.csv")
    exit(1)

try:
    df_participacion = pd.read_csv('data/synthetic/participacion_educativa.csv')
    print(f"   ✓ Participación: {len(df_participacion)} registros")
except FileNotFoundError:
    print("   ✗ ERROR: No encontré participacion_educativa.csv")
    exit(1)

# ============================================================================
# PASO 3: CREAR TABLAS DIMENSIONALES Y DE HECHOS
# ============================================================================

print("\n3. CREANDO ESTRUCTURA DE TABLAS...")
print("-" * 70)

# Eliminar tablas previas si existen (para reiniciar limpio)
try:
    cursor.execute("DROP TABLE IF EXISTS fact_participacion_educativa CASCADE")
    cursor.execute("DROP TABLE IF EXISTS dim_educacion CASCADE")
    cursor.execute("DROP TABLE IF EXISTS dim_poblacion CASCADE")
    cursor.execute("DROP TABLE IF EXISTS dim_establecimientos CASCADE")
    cursor.execute("DROP TABLE IF EXISTS fact_matricula_publica CASCADE")
    conn.commit()
    print("   ✓ Tablas previas eliminadas")
except Error as e:
    print(f"   ⚠ No se pudieron eliminar tablas previas: {e}")

# Crear dim_establecimientos
sql_create_establecimientos = """
CREATE TABLE dim_establecimientos (
    id_establecimiento SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(100),
    capacidad INTEGER,
    ubicacion VARCHAR(255),
    fecha_registro DATE DEFAULT CURRENT_DATE
);
"""
cursor.execute(sql_create_establecimientos)
print("   ✓ Tabla dim_establecimientos creada")

# Crear dim_poblacion
sql_create_poblacion = """
CREATE TABLE dim_poblacion (
    id_poblacion SERIAL PRIMARY KEY,
    edad INTEGER,
    genero VARCHAR(20),
    estado_civil VARCHAR(20),
    tiene_hijos BOOLEAN,
    num_hijos INTEGER,
    nivel_educativo_ingreso VARCHAR(50),
    contexto VARCHAR(50),
    fecha_registro DATE
);
"""
cursor.execute(sql_create_poblacion)
print("   ✓ Tabla dim_poblacion creada")

# Crear dim_educacion
sql_create_educacion = """
CREATE TABLE dim_educacion (
    id_educacion SERIAL PRIMARY KEY,
    nombre_programa VARCHAR(255) NOT NULL,
    tipo_programa VARCHAR(100),
    duracion_meses_estandar INTEGER
);
"""
cursor.execute(sql_create_educacion)
print("   ✓ Tabla dim_educacion creada")

# Crear fact_participacion_educativa
sql_create_participacion = """
CREATE TABLE fact_participacion_educativa (
    id_participacion SERIAL PRIMARY KEY,
    id_poblacion INTEGER NOT NULL REFERENCES dim_poblacion(id_poblacion),
    id_establecimiento INTEGER NOT NULL REFERENCES dim_establecimientos(id_establecimiento),
    id_educacion INTEGER NOT NULL REFERENCES dim_educacion(id_educacion),
    fecha_inicio DATE NOT NULL,
    fecha_termino DATE NOT NULL,
    estado_participacion VARCHAR(50),
    horas_asistidas INTEGER,
    promedio_calificacion DECIMAL(3,1),
    certificado_obtenido BOOLEAN,
    fecha_registro DATE DEFAULT CURRENT_DATE
);
"""
cursor.execute(sql_create_participacion)
print("   ✓ Tabla fact_participacion_educativa creada")

# Crear fact_matricula_publica
sql_create_matricula = """
CREATE TABLE fact_matricula_publica (
    id_matricula SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    matricula_general INTEGER,
    matricula_especial INTEGER,
    tasa_cobertura DECIMAL(5,2),
    fecha_registro DATE DEFAULT CURRENT_DATE
);
"""
cursor.execute(sql_create_matricula)
print("   ✓ Tabla fact_matricula_publica creada")

conn.commit()

# ============================================================================
# PASO 4: CARGAR DIMENSIONES
# ============================================================================

print("\n4. CARGANDO DIMENSIONES...")
print("-" * 70)

# Cargar dim_establecimientos (generar 10 establecimientos)
establecimientos = [
    ('CP Masculino Santiago', 'Penitenciario', 500, 'Santiago'),
    ('CP Femenino San Joaquín', 'Penitenciario', 300, 'Santiago'),
    ('CP Sur Temuco', 'Penitenciario', 400, 'Araucanía'),
    ('CP Centro Valparaíso', 'Penitenciario', 350, 'Valparaíso'),
    ('CP Occidente Quillota', 'Penitenciario', 280, 'Valparaíso'),
    ('CP Sur Concepción', 'Penitenciario', 450, 'Bíobío'),
    ('CP Centro Curicó', 'Penitenciario', 320, 'Maule'),
    ('CP Norte Iquique', 'Penitenciario', 290, 'Tarapacá'),
    ('CP Centro La Serena', 'Penitenciario', 310, 'Coquimbo'),
    ('CP Sur Punta Arenas', 'Penitenciario', 200, 'Magallanes'),
]

for nombre, tipo, capacidad, ubicacion in establecimientos:
    cursor.execute(
        "INSERT INTO dim_establecimientos (nombre, tipo, capacidad, ubicacion) VALUES (%s, %s, %s, %s)",
        (nombre, tipo, capacidad, ubicacion)
    )
conn.commit()
print(f"   ✓ {len(establecimientos)} establecimientos cargados")

# Cargar dim_poblacion (desde df_poblacion)
for _, row in df_poblacion.iterrows():
    cursor.execute(
        """INSERT INTO dim_poblacion
           (edad, genero, estado_civil, tiene_hijos, num_hijos, nivel_educativo_ingreso, contexto, fecha_registro)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            int(row['edad']),
            row['genero'],
            row['estado_civil'],
            bool(row['tiene_hijos']),
            int(row['num_hijos']),
            row['nivel_educativo_ingreso'],
            row['contexto'],
            row['fecha_registro']
        )
    )
conn.commit()
print(f"   ✓ {len(df_poblacion)} registros de población cargados")

# Cargar dim_educacion (5 programas)
programas = [
    ('Educación Básica para Adultos', 'Educación Básica', 12),
    ('Nivelación Educativa Media', 'Educación Media', 12),
    ('Capacitación Técnica - Electricidad', 'Técnica', 6),
    ('Capacitación Técnica - Cocina', 'Técnica', 6),
    ('Taller de Alfabetización', 'Alfabetización', 6),
]

for nombre, tipo, duracion in programas:
    cursor.execute(
        "INSERT INTO dim_educacion (nombre_programa, tipo_programa, duracion_meses_estandar) VALUES (%s, %s, %s)",
        (nombre, tipo, duracion)
    )
conn.commit()
print(f"   ✓ {len(programas)} programas educativos cargados")

# ============================================================================
# PASO 5: CARGAR TABLA DE HECHOS
# ============================================================================

print("\n5. CARGANDO TABLA DE HECHOS...")
print("-" * 70)

# Cargar fact_participacion_educativa
for _, row in df_participacion.iterrows():
    cursor.execute(
        """INSERT INTO fact_participacion_educativa
           (id_poblacion, id_establecimiento, id_educacion, fecha_inicio, fecha_termino,
            estado_participacion, horas_asistidas, promedio_calificacion, certificado_obtenido, fecha_registro)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            int(row['id_persona']),
            int(row['id_establecimiento']),
            int(row['id_educacion']),
            row['fecha_inicio'],
            row['fecha_termino'],
            row['estado_participacion'],
            int(row['horas_asistidas']),
            row['promedio_calificacion'] if pd.notna(row['promedio_calificacion']) else None,
            bool(row['certificado_obtenido']),
            row['fecha_registro']
        )
    )
conn.commit()
print(f"   ✓ {len(df_participacion)} registros de participación cargados")

# ============================================================================
# PASO 6: CREAR ÍNDICES
# ============================================================================

print("\n6. CREANDO ÍNDICES...")
print("-" * 70)

indices = [
    "CREATE INDEX idx_poblacion_genero ON dim_poblacion(genero)",
    "CREATE INDEX idx_poblacion_edad ON dim_poblacion(edad)",
    "CREATE INDEX idx_participacion_estado ON fact_participacion_educativa(estado_participacion)",
    "CREATE INDEX idx_participacion_fecha ON fact_participacion_educativa(fecha_inicio, fecha_termino)",
    "CREATE INDEX idx_participacion_poblacion ON fact_participacion_educativa(id_poblacion)",
]

for idx_sql in indices:
    try:
        cursor.execute(idx_sql)
    except Error as e:
        print(f"   ⚠ Error creando índice: {e}")

conn.commit()
print(f"   ✓ {len(indices)} índices creados")

# ============================================================================
# PASO 7: VALIDAR INTEGRIDAD
# ============================================================================

print("\n7. VALIDANDO INTEGRIDAD...")
print("-" * 70)

# Contar registros
cursor.execute("SELECT COUNT(*) FROM dim_establecimientos")
n_establecimientos = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM dim_poblacion")
n_poblacion = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM dim_educacion")
n_educacion = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM fact_participacion_educativa")
n_participacion = cursor.fetchone()[0]

print(f"   ✓ dim_establecimientos: {n_establecimientos} registros")
print(f"   ✓ dim_poblacion: {n_poblacion} registros")
print(f"   ✓ dim_educacion: {n_educacion} registros")
print(f"   ✓ fact_participacion_educativa: {n_participacion} registros")

# Validar integridad referencial
cursor.execute("""
    SELECT COUNT(*) FROM fact_participacion_educativa fpe
    WHERE NOT EXISTS (SELECT 1 FROM dim_poblacion dp WHERE dp.id_poblacion = fpe.id_poblacion)
""")
fk_violations_poblacion = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) FROM fact_participacion_educativa fpe
    WHERE NOT EXISTS (SELECT 1 FROM dim_establecimientos de WHERE de.id_establecimiento = fpe.id_establecimiento)
""")
fk_violations_estab = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) FROM fact_participacion_educativa fpe
    WHERE NOT EXISTS (SELECT 1 FROM dim_educacion de WHERE de.id_educacion = fpe.id_educacion)
""")
fk_violations_educ = cursor.fetchone()[0]

print(f"   ✓ Violaciones de FK (poblacion): {fk_violations_poblacion}")
print(f"   ✓ Violaciones de FK (establecimientos): {fk_violations_estab}")
print(f"   ✓ Violaciones de FK (educacion): {fk_violations_educ}")

if fk_violations_poblacion + fk_violations_estab + fk_violations_educ == 0:
    print("   ✓ INTEGRIDAD REFERENCIAL VALIDADA")
else:
    print("   ✗ PROBLEMAS DE INTEGRIDAD DETECTADOS")

# ============================================================================
# PASO 8: GENERAR REPORTE
# ============================================================================

print("\n8. GENERANDO REPORTE...")
print("-" * 70)

reporte = f"""# REPORTE DE CARGA - FASE 3
## Normalización y Carga en PostgreSQL

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Proyecto:** Sistema de Información de Equidad Educativa
**Base de Datos:** {database}

---

## Resumen de Carga

### Tablas Dimensionales
- **dim_establecimientos**: {n_establecimientos} registros
- **dim_poblacion**: {n_poblacion} registros
- **dim_educacion**: {n_educacion} registros

### Tabla de Hechos
- **fact_participacion_educativa**: {n_participacion} registros

---

## Validación de Integridad Referencial

✓ FK violations (poblacion): {fk_violations_poblacion}
✓ FK violations (establecimientos): {fk_violations_estab}
✓ FK violations (educacion): {fk_violations_educ}

**Estado General:** {'EXITOSA' if fk_violations_poblacion + fk_violations_estab + fk_violations_educ == 0 else 'CON PROBLEMAS'}

---

## Índices Creados

- idx_poblacion_genero
- idx_poblacion_edad
- idx_participacion_estado
- idx_participacion_fecha
- idx_participacion_poblacion

---

## Próximos Pasos

1. Ejecutar análisis comparativo (Fase 4: 04_comparative_analysis.py)
2. Generar visualizaciones (Fase 5: 05_generate_report.py)
3. Documentar y validar (Fase 6)

"""

# Guardar reporte
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

with open('output/03_load_report.txt', 'w', encoding='utf-8') as f:
    f.write(reporte)

print(f"   ✓ Reporte guardado en: output/03_load_report.txt")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

cursor.close()
conn.close()

print("\n" + "=" * 70)
print("✓ FASE 3 COMPLETADA EXITOSAMENTE")
print("=" * 70)

print(f"\nBase de Datos: {database}")
print(f"\nRegistros Cargados:")
print(f"  • dim_establecimientos: {n_establecimientos}")
print(f"  • dim_poblacion: {n_poblacion}")
print(f"  • dim_educacion: {n_educacion}")
print(f"  • fact_participacion_educativa: {n_participacion}")

print(f"\nIntegridad Referencial: {'VALIDADA ✓' if fk_violations_poblacion + fk_violations_estab + fk_violations_educ == 0 else 'CON PROBLEMAS ✗'}")

print("\n🎯 PRÓXIMO PASO: Ejecutar Fase 4")
print("   python scripts/04_comparative_analysis.py")
