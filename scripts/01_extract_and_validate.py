import pandas as pd
import numpy as np
import os
from pathlib import Path

print("=" * 70)
print("FASE 1: EXTRACCIÓN Y VALIDACIÓN DE DATOS PÚBLICOS")
print("=" * 70)

# PASO 1: CARGAR DATOS
print("\n1. CARGANDO DATOS PÚBLICOS...")
print("-" * 70)

# Cargar Gendarmería
print("   Cargando datos de Gendarmería...")
try:
    df_gendarmeria = pd.read_csv('data/raw/gendarmeria_poblacion_2025.csv', encoding='utf-8')
    print(f"   ✓ Gendarmería: {len(df_gendarmeria)} registros")
except FileNotFoundError:
    print("   ✗ ERROR: No encontré gendarmeria_poblacion_2025.csv")
    exit(1)

# Cargar MINEDUC
print("   Cargando datos de MINEDUC...")
try:
    df_mineduc = pd.read_csv('data/raw/mineduc_matricula_2025.csv', encoding='utf-8', sep=';')
except Exception as e1:
    try:
        df_mineduc = pd.read_csv('data/raw/mineduc_matricula_2025.csv', encoding='utf-8', sep=',', skiprows=2)
    except Exception as e2:
        try:
            df_mineduc = pd.read_csv('data/raw/mineduc_matricula_2025.csv', encoding='latin-1')
        except Exception as e3:
            print(f"   ✗ ERROR: No puedo cargar MINEDUC. Errores: {e1}, {e2}, {e3}")
            exit(1)

# PASO 2: VALIDACIONES
print("\n2. EJECUTANDO VALIDACIONES...")
print("-" * 70)

print(f"   ✓ Gendarmería: {df_gendarmeria.shape[0]} filas, {df_gendarmeria.shape[1]} columnas")
print(f"   ✓ MINEDUC: {df_mineduc.shape[0]} filas, {df_mineduc.shape[1]} columnas")

# Datos faltantes
missing_gen = (df_gendarmeria.isnull().sum().sum() / (df_gendarmeria.shape[0] * df_gendarmeria.shape[1]) * 100)
missing_min = (df_mineduc.isnull().sum().sum() / (df_mineduc.shape[0] * df_mineduc.shape[1]) * 100)

print(f"   ✓ Gendarmería - Datos faltantes: {missing_gen:.2f}%")
print(f"   ✓ MINEDUC - Datos faltantes: {missing_min:.2f}%")

# PASO 3: CREAR REPORTE
print("\n3. GENERANDO REPORTE...")
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

reporte = f"""# REPORTE DE VALIDACIÓN - FASE 1

**Gendarmería**: {len(df_gendarmeria):,} registros, {len(df_gendarmeria.columns)} columnas
**MINEDUC**: {len(df_mineduc):,} registros, {len(df_mineduc.columns)} columnas

✓ FASE 1 COMPLETADA EXITOSAMENTE

Próximos pasos:
1. Ejecutar Fase 2: Generación de dataset sintético
"""

with open('output/01_validation_report.txt', 'w', encoding='utf-8') as f:
    f.write(reporte)

print(f"   ✓ Reporte guardado en: output/01_validation_report.txt")

print("\n" + "=" * 70)
print("✓ FASE 1 COMPLETADA EXITOSAMENTE")
print("=" * 70)