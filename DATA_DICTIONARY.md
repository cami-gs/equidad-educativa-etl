# Diccionario de Datos
## Sistema de Información de Equidad Educativa

### dim_establecimientos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_establecimiento | INT (PK) | Identificador único de establecimiento penitenciario |
| nombre | VARCHAR(255) | Nombre del establecimiento |
| tipo | VARCHAR(100) | Tipo (ej: Penitenciario) |
| capacidad | INT | Capacidad total de internos |
| ubicacion | VARCHAR(255) | Región/ubicación geográfica |
| fecha_registro | DATE | Fecha de registro en BD |

### dim_poblacion
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_poblacion | INT (PK) | Identificador único de persona |
| edad | INT | Edad en años (rango 18-95) |
| genero | VARCHAR(20) | Masculino o Femenino |
| estado_civil | VARCHAR(20) | Soltero, Casado, Divorciado, Viudo |
| tiene_hijos | BOOLEAN | Si tiene hijos (70% mujeres, 50% hombres) |
| num_hijos | INT | Número de hijos si tiene |
| nivel_educativo_ingreso | VARCHAR(50) | Nivel al momento de entrada |
| contexto | VARCHAR(50) | Contexto (Penitenciario) |
| fecha_registro | DATE | Fecha de registro en BD |

**Notas**:
- Edad distribuida Normal(μ=38, σ=12)
- Género: 70% M, 30% F (proporción real sistema chileno)
- Nivel educativo: 5% sin escolaridad, 30% primaria, 50% secundaria, 10% técnico, 5% superior

### dim_educacion
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_educacion | INT (PK) | Identificador único de programa |
| nombre_programa | VARCHAR(255) | Nombre del programa educativo |
| tipo_programa | VARCHAR(100) | Tipo: Básica, Media, Técnica, Alfabetización |
| duracion_meses_estandar | INT | Duración estándar en meses |

**Programas disponibles**:
1. Educación Básica para Adultos (12 meses)
2. Nivelación Educativa Media (12 meses)
3. Capacitación Técnica - Electricidad (6 meses)
4. Capacitación Técnica - Cocina (6 meses)
5. Taller de Alfabetización (6 meses)

### fact_participacion_educativa
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_participacion | INT (PK) | Identificador único de participación |
| id_poblacion | INT (FK) | Referencia a dim_poblacion |
| id_establecimiento | INT (FK) | Referencia a dim_establecimientos |
| id_educacion | INT (FK) | Referencia a dim_educacion |
| fecha_inicio | DATE | Fecha de inicio del programa |
| fecha_termino | DATE | Fecha de término o abandono |
| estado_participacion | VARCHAR(50) | Completado, En Curso, Abandonado |
| horas_asistidas | INT | Total de horas asistidas (~40 horas/mes) |
| promedio_calificacion | DECIMAL(3,1) | Calificación promedio (4.0-7.0, escala chilena) |
| certificado_obtenido | BOOLEAN | Si obtuvo certificado (solo si completó) |
| fecha_registro | DATE | Fecha de registro en BD |

**Notas**:
- 35% de población participa (1,750 de 5,000)
- Duraciones: 20% 6m, 40% 12m, 25% 18m, 15% 24m
- Estados: 60% Completado, 25% En Curso, 15% Abandonado
- Horas: 95-100% si Completado, 30-70% si En Curso, 10-50% si Abandonado

### fact_matricula_publica
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_matricula | INT (PK) | Identificador único |
| fecha | DATE | Fecha de registro |
| matricula_general | INT | Matrícula sector general |
| matricula_especial | INT | Matrícula sector especial |
| tasa_cobertura | DECIMAL(5,2) | Tasa de cobertura (%) |
| fecha_registro | DATE | Fecha de registro en BD |

**Notas**: Para futuras comparaciones con datos MINEDUC públicos

---

## Variables Clave para Análisis

### Indicador 1: Tasa de Acceso
```sql
COUNT(DISTINCT fpe.id_poblacion) / COUNT(*) FROM dim_poblacion * 100
```
**Resultado esperado**: 35%

### Indicador 2: Brecha de Género
```sql
SELECT genero,
       COUNT(DISTINCT fpe.id_poblacion) / COUNT(DISTINCT dp.id_poblacion) * 100 as tasa
FROM dim_poblacion dp
LEFT JOIN fact_participacion_educativa fpe ON dp.id_poblacion = fpe.id_poblacion
GROUP BY genero
```
**Resultado esperado**: Diferencia estadísticamente significativa

### Indicador 3: Brecha de Edad
```sql
SELECT CASE
       WHEN edad < 25 THEN '18-24'
       WHEN edad < 35 THEN '25-34'
       ...
       END as grupo_edad,
       COUNT(DISTINCT fpe.id_poblacion) / COUNT(DISTINCT dp.id_poblacion) * 100 as tasa
```

### Indicador 4: Efectos de Interacción
Combina género + grupo de edad en análisis desagregado

### Indicador 5: Completitud
```sql
SELECT estado_participacion,
       COUNT(*) as cantidad,
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as pct
FROM fact_participacion_educativa
GROUP BY estado_participacion
```
**Resultado esperado**: 60% Completado, 25% En Curso, 15% Abandonado

---

**Generado**: {datetime.now().strftime('%d de %B de %Y')}
