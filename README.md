# 🎓 Sistema de Información de Equidad Educativa

**Análisis Comparativo de Acceso Educativo en Contextos Penitenciarios Chilenos**

## Descripción General

Este proyecto demuestra competencias en **Gobernanza de Datos** a través de un análisis completo
de equidad educativa en el sistema penitenciario chileno. Integra:

- ✅ **Extracción de Datos Públicos** (Gendarmería, MINEDUC)
- ✅ **Generación de Datos Sintéticos** (metodología documentada)
- ✅ **Normalización 3NF** (modelo relacional)
- ✅ **Carga en PostgreSQL** (integridad referencial)
- ✅ **Análisis Comparativo** (5 indicadores clave)
- ✅ **Visualización Profesional** (reporte HTML interactivo)
- ✅ **Documentación Completa** (trazabilidad y reproducibilidad)

## Estructura del Proyecto

```
equidad_educativa/
├── data/
│   ├── raw/                          # Datos públicos descargados
│   │   ├── gendarmeria_poblacion_2025.csv
│   │   └── mineduc_matricula_2025.csv
│   └── synthetic/                    # Datos sintéticos generados
│       ├── poblacion_penitenciaria.csv
│       └── participacion_educativa.csv
├── scripts/
│   ├── 01_extract_and_validate.py    # Fase 1: Extracción y validación
│   ├── 02_generate_synthetic_data.py # Fase 2: Generación de síntesis
│   ├── 03_normalize_and_load.py      # Fase 3: Normalización y carga
│   ├── 04_comparative_analysis.py    # Fase 4: Análisis comparativo
│   ├── 05_generate_report.py         # Fase 5: Visualizaciones
│   └── 06_documentation_and_qa.py    # Fase 6: Documentación y QA
├── output/
│   ├── 01_validation_report.txt      # Reporte de validación
│   ├── 03_load_report.txt            # Reporte de carga
│   ├── 04_analysis_report.txt        # Reporte de análisis
│   ├── reporte_equidad_educativa.html # Reporte visual interactivo
│   ├── analisis_*.csv                # CSVs analíticos
│   └── [documentación]               # Archivos MD de documentación
├── README.md                          # Este archivo
├── DATA_DICTIONARY.md                 # Diccionario de datos
├── METHODOLOGY.md                     # Metodología del proyecto
├── SYNTHETIC_DATA_GENERATION_METHODOLOGY.md  # Síntesis documentada
└── .gitignore
```

## 5 Indicadores Clave de Equidad

| # | Indicador | Pregunta | Valor |
|---|-----------|----------|-------|
| 1 | Tasa de Acceso | ¿Qué % participa en educación? | 35% |
| 2 | Brecha de Género | ¿Hay diferencias M/F? | Sí, significativa |
| 3 | Brecha de Edad | ¿La edad influye? | Sí, relevante |
| 4 | Interacción | ¿Se combinan género y edad? | Sí, compleja |
| 5 | Completitud | ¿Cuántos completan programas? | 60% |

## Uso del Proyecto

### Requisitos Previos
- Python 3.8+
- PostgreSQL 18+
- Conda (Anaconda)

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/cami-gs/equidad_educativa.git
cd equidad_educativa

# 2. Crear ambiente conda
conda create -n proyecto python=3.14.7
conda activate proyecto

# 3. Instalar dependencias
conda install pandas numpy psycopg2 scipy matplotlib seaborn

# 4. Descargar datos públicos
# Descargar manualmente desde https://datos.gob.cl:
# - gendarmeria_poblacion_2025.csv → data/raw/
# - mineduc_matricula_2025.csv → data/raw/
```

### Ejecutar Pipeline Completo

```bash
# Fase 1: Extracción y validación
python scripts/01_extract_and_validate.py

# Fase 2: Generación de datos sintéticos
python scripts/02_generate_synthetic_data.py

# Fase 3: Normalización y carga en PostgreSQL
python scripts/03_normalize_and_load.py

# Fase 4: Análisis comparativo
python scripts/04_comparative_analysis.py

# Fase 5: Visualizaciones y reporte HTML
python scripts/05_generate_report.py

# Fase 6: Documentación y QA
python scripts/06_documentation_and_qa.py
```

### Visualizar Resultados

Abre en navegador:
```
output/reporte_equidad_educativa.html
```

## Competencias Demostradas

### 1. Arquitectura de Datos ✓
- Modelo relacional 3NF (5 tablas)
- Fact-dimension schema
- Integridad referencial (FKs)
- Índices para optimización

### 2. Procesamiento de Datos ✓
- Validación de calidad (datos faltantes, duplicados)
- Limpieza y normalización
- Transformación ETL
- Estadísticas descriptivas

### 3. Procesos ETL ✓
- Extracción de múltiples fuentes
- Transformación a 3NF
- Carga en PostgreSQL
- Documentación de síntesis

### 4. Gobernanza de Datos ✓
- Control de calidad
- Trazabilidad completa
- Documentación exhaustiva
- Reproducibilidad (seed=42)
- Validación estadística

### 5. Base de Datos ✓
- Creación de esquema
- Relaciones y constraints
- Índices para consultas
- Backup y documentación

## Metodología

### Datos Sintéticos
Este proyecto utiliza **datos sintéticos** basados en:
- 8 años de experiencia en educación penitenciaria
- Observación etnográfica en CP Femenino San Joaquín (2017-2025)
- Normativas de Gendarmería de Chile
- Especificaciones MINEDUC

**NO son datos reales**, pero son realistas en estructura y parámetros.
Se utilizan expresamente como ejercicio de gobernanza de datos y documentación.

Ver: `SYNTHETIC_DATA_GENERATION_METHODOLOGY.md` para detalles completos.

## Hallazgos Clave

1. **Acceso Limitado**: 35% de participación refleja restricciones de capacidad
2. **Brechas Reales**: Género y edad son factores diferenciadores estadísticamente significativos
3. **Alta Efectividad**: 60% de completitud indica que programas funcionan cuando se accede
4. **Inequidad Interseccional**: Algunos subgrupos están más marginados que otros

## Recomendaciones

1. Ampliar capacidad de infraestructura educativa penitenciaria
2. Diseñar políticas diferenciadas según género y edad
3. Focalizar en subgrupos marginados
4. Implementar sistema de información continuo de indicadores

## Licencia y Responsabilidad

Este proyecto es un **portfolio de demostración** de competencias en gobernanza de datos.

Los datos sintéticos están explícitamente identificados como tales.
NO deben usarse para inferencias sobre población real o política pública sin aclaraciones explícitas.

Responsable: Camila Ignacia González Silva

## Contacto y Consultas

- **Email**: cami.pinha.sa@gmail.com
- **Contexto**: Portfolio para postulación a posición de Data Governance
  en Subsecretaría de Educación Parvularia, Departamento de Estudios y Estadísticas

---

**Generado**: {datetime.now().strftime('%d de %B de %Y')}

Para más detalles, ver archivos de documentación:
- `DATA_DICTIONARY.md` - Definición de variables
- `METHODOLOGY.md` - Metodología completa
- `output/04_analysis_report.txt` - Resultados analíticos
