# Metodología del Proyecto
## Sistema de Información de Equidad Educativa

### Objetivo General

Demostrar competencias en **Gobernanza de Datos** mediante un análisis completo
de equidad educativa en el sistema penitenciario chileno, desde extracción de datos públicos
hasta análisis comparativo y visualización profesional.

### Objetivos Específicos

1. **Arquitectura de Datos**: Diseñar modelo relacional 3NF con tablas dimensionales y de hechos
2. **Procesamiento de Datos**: Validar, limpiar y normalizar datos de múltiples fuentes
3. **Procesos ETL**: Implementar pipeline completo de extracción, transformación y carga
4. **Análisis Comparativo**: Calcular 5 indicadores clave de equidad educativa
5. **Gobernanza de Datos**: Documentar completamente metodología, síntesis y validaciones

### Fases del Proyecto

#### Fase 1: Extracción y Validación de Datos Públicos

**Fuentes**:
- Gendarmería de Chile: Datos demográficos agregados (Portal datos.gob.cl)
- MINEDUC: Estadísticas de matrícula pública (Portal datos.gob.cl)

**Validaciones ejecutadas**:
- Estructura de datos (filas, columnas)
- Tipos de datos (numéricos, texto, fechas)
- Datos faltantes (% por columna)
- Registros duplicados (por ID)
- Rangos de valores (mín, máx)
- Cobertura geográfica

**Salidas**: `output/01_validation_report.txt`

#### Fase 2: Generación de Datos Sintéticos

**Justificación**:
Gendarmería publica datos agregados pero NO detalles de programas educativos por participante individual.
Se generó síntesis basada en 8 años de experiencia etnográfica en educación penitenciaria.

**Metodología de síntesis**:
- **Población**: N=5,000 personas (reproducible, seed=42)
- **Participación**: 35% (1,750 instancias de programas)
- **Variables**: Edad, género, estado civil, hijos, nivel educativo
- **Programas**: 5 tipos (Básica, Media, Técnica, Alfabetización)
- **Estados**: Completado (60%), En Curso (25%), Abandonado (15%)

**Validaciones**:
- Coherencia interna (edad > 18, hijos correlacionan con edad)
- Realismo (parámetros basados en observación 8 años)
- Reproducibilidad (seed=42)
- Documentación completa en `SYNTHETIC_DATA_GENERATION_METHODOLOGY.md`

**Salidas**:
- `data/synthetic/poblacion_penitenciaria.csv`
- `data/synthetic/participacion_educativa.csv`
- `SYNTHETIC_DATA_GENERATION_METHODOLOGY.md`

#### Fase 3: Normalización y Carga en PostgreSQL

**Modelo de Datos** (3NF):
- 3 tablas dimensionales (dim_establecimientos, dim_poblacion, dim_educacion)
- 2 tablas de hechos (fact_participacion_educativa, fact_matricula_publica)

**Transformaciones**:
- Desnormalización de datos sintéticos en dimensiones
- Generación de 10 establecimientos penitenciarios ficticios
- Asignación de FK para integridad referencial
- Creación de índices para optimización

**Validaciones**:
- Conteo de registros cargados
- Detección de violaciones de integridad referencial
- Verificación de constraints

**Salidas**:
- Base de datos PostgreSQL `equidad_educativa`
- `output/03_load_report.txt`

#### Fase 4: Análisis Comparativo

**5 Indicadores Clave**:

1. **Tasa de Acceso**: 35% de población accede a educación
2. **Brecha de Género**: Diferencias M/F en participación
3. **Brecha de Edad**: Variación según grupos etarios
4. **Efectos de Interacción**: Género + Edad combinados
5. **Completitud**: 60% completa, 15% abandona

**Análisis Estadístico**:
- Prueba Chi-squared para significancia
- Distribuciones por estado de participación
- Estadísticas descriptivas (media, mediana, cuartiles)

**Salidas**:
- 5 CSVs analíticos (genero, edad, interaccion, completitud, horas)
- `output/04_analysis_report.txt`

#### Fase 5: Visualización y Reporte HTML

**Gráficos**:
1. Tasa de acceso general (barras)
2. Brecha de género (barras comparativas)
3. Brecha de edad (barras agrupadas)
4. Efectos de interacción (barras agrupadas)
5. Distribución de completitud (pastel)
6. Horas asistidas por estado (barras horizontales)

**Reporte HTML**:
- Presentación profesional interactiva
- Narrativa interpretativa para cada indicador
- Recomendaciones de política pública
- Nota metodológica sobre síntesis

**Salidas**: `output/reporte_equidad_educativa.html`

#### Fase 6: Documentación y QA

**Documentación**:
- README.md (guía de uso)
- DATA_DICTIONARY.md (definición de variables)
- METHODOLOGY.md (este documento)
- VALIDATION_LOG.md (log de validaciones)

**QA (Quality Assurance)**:
- Verificación de archivos
- Validación de datos
- Checklist de integridad
- Reporte final

**Salidas**:
- Archivos MD de documentación
- `output/06_qa_report.txt`
- `.gitignore`

### Competencias Demostradas

#### 1. Arquitectura de Datos
- ✓ Modelo relacional 3NF con 5 tablas
- ✓ Tablas dimensionales y de hechos
- ✓ Claves primarias y extranjeras
- ✓ Índices para optimización
- ✓ Documentación de schema

#### 2. Procesamiento de Datos
- ✓ Validación de calidad de datos
- ✓ Detección de anomalías
- ✓ Limpieza y normalización
- ✓ Transformación a formatos estándar
- ✓ Estadísticas descriptivas

#### 3. Procesos ETL
- ✓ Extracción de múltiples fuentes
- ✓ Transformación con reglas explícitas
- ✓ Carga en base de datos relacional
- ✓ Documentación de transformaciones
- ✓ Reproducibilidad con seeds

#### 4. Gobernanza de Datos
- ✓ Control de calidad completo
- ✓ Trazabilidad de datos
- ✓ Documentación exhaustiva
- ✓ Validación estadística
- ✓ Transparencia en síntesis

#### 5. Base de Datos
- ✓ Creación de esquema
- ✓ Relaciones y constraints
- ✓ Integridad referencial
- ✓ Optimización con índices
- ✓ Mantenimiento y documentación

### Herramientas Utilizadas

- **Python 3.14.7**: Scripting principal
- **PostgreSQL 18**: Base de datos relacional
- **Pandas**: Procesamiento de datos
- **Matplotlib/Seaborn**: Visualizaciones
- **Scipy**: Pruebas estadísticas (Chi-squared)
- **Git**: Control de versiones
- **HTML/CSS**: Reporte interactivo

### Limitaciones Reconocidas

1. **Datos Sintéticos**: NO son datos reales. Solo para demostración técnica.
2. **Muestra Pequeña**: 5,000 personas (población real es ~40,000)
3. **Variables Limitadas**: No incluye tipo de delito, duración de condena
4. **Un Contexto**: Simplificado como un solo contexto penitenciario
5. **Correlaciones**: Algunas variables son independientes (podrían correlacionar)

### Validez y Generalización

Este análisis demuestra **competencias técnicas en gobernanza de datos**.

Para inferencias sobre política pública real se requeriría:
- Acceso a datos administrativos reales de Gendarmería
- Aprobación ética e institucional
- Análisis cualitativo complementario
- Diálogo con stakeholders (educadores, internos, autoridades)

### Reproducibilidad

Todo el proyecto es reproducible:
- **Seed fija**: 42 (genera exactamente los mismos datos sintéticos)
- **Scripts documentados**: Comentarios en cada fase
- **Versiones pinned**: Dependencias específicas
- **Git control**: Historial completo de cambios

Cualquiera puede clonar el repo y reproducir exactamente este análisis ejecutando:
```bash
for i in {1..6}; do python scripts/0${i}_*.py; done
```

---

**Autor**: Camila Ignacia González Silva
**Contexto**: Portfolio de Data Governance
**Generado**: {datetime.now().strftime('%d de %B de %Y')}
