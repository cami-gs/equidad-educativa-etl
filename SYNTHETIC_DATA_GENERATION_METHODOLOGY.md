# METODOLOGÍA DE GENERACIÓN DE DATOS SINTÉTICOS

## Justificación

Gendarmería de Chile publica datos demográficos agregados en sus Compendios Estadísticos,
pero **no publica detalles de programas educativos específicos por participante individual**.

Esta síntesis se basa en:
- **8 años de facilitación de educación** en CP Femenino San Joaquín (2017-2025)
- Marco de la Subdirección de Reinserción Social de Gendarmería de Chile
- Normativas de educación en contextos carcelarios

---

## Variables Sintéticas Generadas

### 1. POBLACIÓN PENITENCIARIA (N=5,000)

**Edad**
- Distribución: Normal(μ=38, σ=12), rango [18-95]
- **Justificación**: La edad promedio de población penitenciaria chilena es ~38 años
- **Fuente**: Observación etnográfica 2017-2025

**Género**
- Distribución: 70% Masculino, 30% Femenino
- **Justificación**: Proporción real del sistema penitenciario chileno
- **Relevancia**: CP Femenino San Joaquín representa ~30% de población adulta privada de libertad

**Estado Civil**
- Distribución: 60% Soltero, 25% Casado, 10% Divorciado, 5% Viudo
- **Justificación**: Según datos desagregados de Gendarmería
- **Observación**: Alta tasa de soltería en contexto carcelario

**Tiene Hijos**
- Distribución diferenciada por género:
  - Mujeres: 70% tienen hijos
  - Hombres: 50% tienen hijos
- **Justificación**: Basado en características de género observadas en San Joaquín
- **Contexto**: Madres privadas de libertad tienen responsabilidades de cuidado

**Número de Hijos**
- Distribución: Poisson(λ=2) si tiene
- **Promedio**: ~2 hijos cuando presente
- **Observación**: Correlaciona con edad

**Nivel Educativo al Ingreso**
- Distribución: 5% Sin escolaridad, 30% Primaria, 50% Secundaria, 10% Técnico, 5% Superior
- **Justificación**: Especificación de MINEDUC para población penitenciaria

---

### 2. PARTICIPACIÓN EN PROGRAMAS EDUCATIVOS

**Tasa de Participación**: 35%
- **Justificación**: Capacidad limitada de establecimientos (~35-40% de población puede participar)
- **Observación**: Limitado por infraestructura, educadores, materiales

**Programas Disponibles**
1. Educación Básica para Adultos
2. Nivelación Educativa Media
3. Capacitación Técnica - Electricidad
4. Capacitación Técnica - Cocina
5. Taller de Alfabetización

**Fecha de Inicio**
- Uniforme en últimos 5 años (2020-2025)
- Refleja continuidad de programas en el tiempo

**Duración del Programa**
- Opciones: 6, 12, 18 o 24 meses
- Distribución: 20%, 40%, 25%, 15% respectivamente
- **Justificación**: Programas de educación penitenciaria suelen durar 6-24 meses

**Estado de Participación**
- Completado: 60%
- En Curso: 25%
- Abandonado: 15%
- **Justificación**: Tasas realistas de completitud en educación penitenciaria

**Horas Asistidas**
- Base: ~40 horas/mes
- Si Completado: 95-100% de horas esperadas
- Si En Curso: 30-70% de horas esperadas
- Si Abandonado: 10-50% de horas esperadas

**Calificación Promedio**
- Rango: 4.0 a 7.0 (escala chilena)
- Solo si: Completado o En Curso
- Abandono: Sin calificación registrada

**Certificado Obtenido**
- Solo si completó el programa
- Refleja formalidad de reconocimiento

---

## Reproducibilidad

**Seed**: 42
- Establece aleatoriedad controlada
- Permite que cualquiera reproduzca exactamente estos datos

**Código**: Disponible en `scripts/02_generate_synthetic_data.py`

---

## Validación de Síntesis

**Coherencia interna**: Estructura lógica (edad > 18, hijos correlacionan con edad)
**Realismo**: Parámetros basados en observación de 8 años en contexto carcelario
**Documentación**: Cada decisión justificada y rastreable
**Transparencia**: Síntesis explícitamente identificada como tal

---

## Limitaciones Reconocidas

1. **No incluye**: Tipo de delito, duración de condena, reincidencia
   - *Razón*: No disponible en datos públicos de Gendarmería

2. **Simplificación**: Un solo contexto penitenciario (no desagrega por establecimiento específico)
   - *Razón*: Proteger confidencialidad de CP Femenino San Joaquín

3. **Correlaciones**: Algunas variables son independientes (podrían correlacionar con edad/género)
   - *Razón*: Falta de datos públicos para calibrar correlaciones

---

## Uso Apropiado de Esta Síntesis

**Apropiado para**:
- Portfolio técnico de gobernanza de datos
- Demostración de pipelines ETL
- Desarrollo de dashboards y análisis
- Propósitos educativos

**NO apropiado para**:
- Inferencias sobre población penitenciaria real
- Políticas públicas
- Estudios académicos (sin aclaración explícita de síntesis)

---

**Responsabilidad**: Esta síntesis fue generada por [Camila Ignacia González Silva]
como parte de un portfolio de gobernanza de datos. Está explícitamente identificada
como síntesis basada en experiencia etnográfica, no como datos reales.
