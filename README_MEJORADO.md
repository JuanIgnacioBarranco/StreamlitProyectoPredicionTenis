# 🎾 Predictor de Duración de Partidos de Tenis

## 📋 Descripción del Proyecto

Este proyecto utiliza **machine learning** para predecir la duración de partidos de tenis del circuito ATP profesional. Implementa dos enfoques complementarios:

1. **Regresión**: Predicción exacta en minutos
2. **Clasificación**: Categorización en CORTO / MEDIO / LARGO

## 🎯 Objetivos

- **Principal**: Desarrollar modelos predictivos precisos para la duración de partidos
- **Secundario**: Crear una aplicación web interactiva para explorar datos y hacer predicciones
- **Educativo**: Demostrar el pipeline completo de ciencia de datos desde ETL hasta deployment

## 📊 Dataset

- **Fuente**: Partidos del circuito ATP (Association of Tennis Professionals)
- **Tamaño**: ~5,400 partidos únicos
- **Período**: Datos históricos del circuito profesional
- **Variables principales**: superficie, nivel de torneo, ronda, ranking de jugadores, formato del partido

### Categorías de Duración (Clasificación)

| Categoría | Rango | Descripción |
|-----------|-------|-------------|
| **CORTO** | < 100 min | Partidos rápidos, diferencias de nivel |
| **MEDIO** | 100-150 min | Duración típica, partidos equilibrados |
| **LARGO** | > 150 min | Partidos extensos, alta competitividad |

*Justificación de umbrales*: Basados en análisis estadístico del dataset (~33° y 67° percentiles)

## 🔧 Tecnologías Utilizadas

### Backend y Modelado
- **Python**: Lenguaje principal
- **Scikit-learn**: Modelos de machine learning (Gradient Boosting)
- **Pandas/NumPy**: Manipulación y análisis de datos

### Frontend y Visualización
- **Streamlit**: Framework para la aplicación web
- **Plotly**: Gráficos interactivos avanzados
- **CSS**: Estilos personalizados

### Deployment
- **Streamlit Cloud**: Hosting de la aplicación
- **GitHub**: Control de versiones y CI/CD

## 🏗️ Arquitectura del Proyecto

```
tennis-ao26_with_csv_export/
├── 📊 Datos
│   ├── entrega2proy_EDA/matches_cleaned.csv      # Dataset original limpio
│   ├── data_for_streamlit_real.csv               # Datos de test del modelo
│   └── metrics_summary_real.json                 # Métricas de rendimiento
├── 🧠 Modelos y Scripts
│   ├── Proy_3ra_Modelado_Mejorado_BarrancoJuan.ipynb  # Entrenamiento
│   ├── generar_datos_reales.py                   # Pipeline de datos
│   └── tennis_app_mejorada.py                    # Aplicación principal
├── 📚 Documentación
│   ├── README.md                                 # Este archivo
│   ├── DEPLOYMENT_GUIDE.md                      # Guía de despliegue
│   └── requirements_mejorados.txt               # Dependencias
```

## 🎯 Modelos Implementados

### 1. Modelo de Regresión
- **Algoritmo**: Gradient Boosting Regressor
- **Objetivo**: Predicir duración exacta en minutos
- **Métricas**:
  - RMSE: 34.93 minutos
  - R²: 0.307 (30.7% de varianza explicada)
  - MAE: 28.26 minutos

### 2. Modelo de Clasificación
- **Algoritmo**: Gradient Boosting Classifier
- **Objetivo**: Clasificar en categorías CORTO/MEDIO/LARGO
- **Métricas**:
  - Accuracy: 47.0%
  - Precision macro: 45%
  - Recall macro: 47%

### Variables de Entrada (Features)
1. **surface**: Superficie (Hard/Clay/Grass)
2. **tourney_level**: Nivel del torneo (G/M/A/C)
3. **round**: Ronda del torneo (1st Round, QF, SF, F, etc.)
4. **best_of**: Formato del partido (3 o 5 sets)
5. **rank_diff**: Diferencia de ranking entre jugadores
6. **rank_avg**: Ranking promedio de ambos jugadores
7. **is_grand_slam**: Booleano si es Grand Slam

## 🖥️ Aplicación Web

La aplicación Streamlit incluye **7 secciones principales**:

### 1. 🏠 Introducción y Datos
- Explicaciones sobre conceptos básicos del tenis
- Estadísticas descriptivas del dataset
- Visualizaciones exploratorias

### 2. 📊 Análisis de Regresión
- Rendimiento detallado del modelo de regresión
- Gráficos de predicciones vs valores reales
- Análisis de residuos y distribución de errores
- Métricas interpretadas para audiencia no técnica

### 3. 🎯 Análisis de Clasificación
- Matriz de confusión interactiva
- Reporte de clasificación completo
- Análisis de distribución de categorías
- Interpretación de resultados

### 4. 🔮 Predictor Interactivo
- Formulario para ingreso de características del partido
- Predicciones en tiempo real (regresión + clasificación)
- Ejemplos predefinidos para probar el modelo
- Explicaciones contextuales de cada predicción

### 5. 🔴 Partidos en Vivo *(NUEVO)*
- Monitoreo en tiempo real de partidos en curso
- Visualización de marcadores actuales
- Predicciones de duración final estimada
- Información de torneos y superficies

### 6. 📅 Partidos Futuros *(NUEVO)*
- Lista de próximos partidos con predicciones automáticas
- Filtros por tipo de torneo y fecha
- Rankings y cuotas de apuestas
- Análisis estadístico de partidos programados
- Visualizaciones interactivas de distribuciones

### 7. ⚙️ Información del Modelo
- Pipeline completo de desarrollo
- Importancia de características  
- Limitaciones y futuras mejoras
- Documentación técnica

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
Python 3.8+
pip (gestor de paquetes)
```

### Instalación Local
```bash
# Clonar el repositorio
git clone https://github.com/JuanIgnacioBarranco/StreamlitProyectoPredicionTenis.git
cd tennis-ao26_with_csv_export

# Instalar dependencias
pip install -r requirements_mejorados.txt

# Ejecutar aplicación
streamlit run tennis_app_mejorada.py
```

### Uso en Streamlit Cloud
1. Visita: [URL de la aplicación]
2. Navega entre las secciones usando la barra lateral
3. Interactúa con filtros y controles para explorar datos
4. Usa el predictor para hacer predicciones personalizadas

## 🔴 Funcionalidades de API en Tiempo Real *(NUEVO)*

### Integración con APIs Externas
- **Tennis Data API**: Datos oficiales del circuito ATP
- **Sports Open API**: Información de partidos y resultados
- **Sistema de Fallback**: Datos mock realistas cuando las APIs fallan

### Funcionalidades Implementadas

#### 🔴 Partidos en Vivo
- Monitoreo en tiempo real de partidos en curso
- Visualización de marcadores actuales por set
- Predicción de duración final estimada basada en progreso
- Información contextual (torneo, superficie, jugadores)

#### 📅 Partidos Futuros  
- Lista de próximos partidos con predicciones automáticas
- Filtros configurables por tipo de torneo y fecha (hasta 14 días)
- Rankings actuales y cuotas de apuestas integradas
- Análisis estadístico con visualizaciones interactivas:
  - Distribución de duraciones predichas
  - Partidos por superficie y categoría
  - Métricas agregadas por tipo de torneo

### Características Técnicas
- **Manejo robusto de errores** con múltiples APIs de respaldo
- **Predicciones automáticas** para cada partido obtenido
- **Actualización en tiempo real** con indicadores de estado
- **Interface intuitiva** con métricas visuales y colores semánticos

### Impacto del Proyecto
Esta implementación eleva significativamente el valor del proyecto al proporcionar:
- ✅ **Funcionalidad profesional** de predicciones en tiempo real
- ✅ **Integración con datos en vivo** del circuito ATP
- ✅ **Experiencia de usuario completa** para seguimiento de torneos
- ✅ **Valor comercial tangible** para apostadores y aficionados

## 📈 Resultados y Insights

### Factores Más Importantes
1. **is_grand_slam** (30-35%): Factor más determinante
2. **surface** (20-25%): Clay más lento, Grass más rápido
3. **rank_diff** (15-18%): Partidos parejos duran más
4. **best_of** (10-12%): Formato directo de impacto

### Insights del Dominio
- **Grand Slams**: Partidos significativamente más largos
- **Superficie Clay**: +15 min promedio vs otras superficies
- **Partidos parejos** (rank_diff < 20): +20 min de duración
- **Finales**: +15 min vs primeras rondas por mayor tensión

### Limitaciones Identificadas
- No considera condiciones climáticas
- Ausencia de histórico entre jugadores (H2H)
- No incluye estilos de juego específicos
- Dataset limitado a circuito masculino ATP

## 🔧 Posibles Mejoras

### Técnicas
- **Algoritmos avanzados**: XGBoost, Neural Networks
- **Feature engineering**: Velocidad de saque, winners/errors
- **Ensemble methods**: Combinación de múltiples modelos

### Datos
- **Expansión**: Incluir circuito WTA femenino
- **Contexto**: Condiciones meteorológicas, estado físico
- **Tiempo real**: Predicciones durante el partido

### Producto
- **API REST**: Para integración con otras aplicaciones
- **Mobile app**: Versión optimizada para móviles
- **Notificaciones**: Alertas para partidos de interés

## 👨‍💻 Autor

**Juan Ignacio Barranco Bastan**
- Proyecto de Ciencia de Datos
- Universidad/Institución: [Nombre]
- Fecha: Noviembre 2025

## 📄 Licencia

Este proyecto es de uso académico y educativo.

## 🙏 Agradecimientos

- Datos del circuito ATP
- Comunidad de Streamlit
- Librerías open-source utilizadas

---

*Para más información técnica, consulta la documentación en la aplicación web o los notebooks de análisis.*