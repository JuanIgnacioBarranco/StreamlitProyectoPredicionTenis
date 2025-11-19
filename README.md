# 🎾 Predictor de Duración de Partidos de Tenis - VERSIÓN FINAL ✅

**Estado: LISTO PARA EXAMEN FINAL**

Aplicación web interactiva para la predicción de duración de partidos de tenis utilizando Machine Learning. 

⚠️ **IMPORTANTE**: La versión funcional y corregida está en `version_final_corregida/tennis_app_final.py`

## 🏆 Entrega Final - Versión Corregida y Optimizada

### 🎯 Objetivo
Desarrollar un sistema completo de predicción de duración de partidos de tenis con interfaz web educativa y académicamente apropiada.

### ✅ Mejoras y Correcciones Implementadas

- **🔧 Errores Corregidos**: Solucionados todos los KeyError de métricas (rmse_regression, accuracy_classification)
- **🚫 Funcionalidad Removida**: Eliminada sección inapropiada de "Predictor de Partidos Futuros" que predecía ganadores
- **📚 Contenido Educativo**: Agregadas explicaciones de terminología de tenis para audiencia no especializada
- **🎨 Formato Académico**: Limpieza de emojis innecesarios y estilo apropiado para evaluación
- **📝 Notas Explicativas**: Aclaraciones para valores "None" en niveles de torneo
- **🎯 Enfoque Clarificado**: Aplicación centrada exclusivamente en predicción de duración

### 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web
- **Altair**: Visualizaciones interactivas con gramática de gráficos
- **Plotly**: Gráficos interactivos adicionales
- **Scikit-learn**: Modelos de Machine Learning
- **Pandas & Numpy**: Manipulación de datos

### 📁 Estructura del Proyecto - Versión Final

```bash
tennis-ao26_with_csv_export/
├── version_final_corregida/               # 🎯 VERSIÓN FUNCIONAL PARA EXAMEN
│   ├── tennis_app_final.py               # ✅ Aplicación Streamlit corregida y funcional
│   ├── matches_cleaned.csv               # Dataset principal
│   ├── metrics_summary_real.json         # Métricas del modelo corregidas
│   ├── requirements.txt                  # Dependencias específicas
│   └── README.md                         # Documentación de la versión final
├── tennis_app_mejorada.py                # Versión con API en tiempo real
├── README_MEJORADO.md                    # Documentación completa actualizada
├── requirements_mejorados.txt            # Dependencias completas
├── Proy_3ra_Modelado_Mejorado_BarrancoJuan.ipynb  # Modelado final
├── Proy_4ta_Visualizacion_Interactiva_BarrancoJuan.ipynb  # Visualizaciones
└── entrega2proy_EDA/                     # Análisis exploratorio original
    └── matches_cleaned.csv
```

### 🚀 Instalación y Ejecución

#### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd tennis-ao26_with_csv_export
```

#### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 3. Ejecutar el notebook de visualizaciones (opcional)
```bash
jupyter notebook Proy_4ta_Visualizacion_Interactiva_BarrancoJuan.ipynb
```

#### 4. Ejecutar la aplicación Streamlit (Versión Final)
```bash
# Versión corregida y funcional para el examen
cd version_final_corregida
streamlit run tennis_app_final.py

# O versión con funcionalidades adicionales
streamlit run tennis_app_mejorada.py
```

### 📊 Funcionalidades de la Aplicación

#### 1. Dashboard Principal
- Métricas clave del modelo (RMSE, R², Accuracy)
- Scatter plot de predicciones vs realidad
- Distribución de errores
- Performance por segmento

#### 2. Exploración Interactiva
- Filtros dinámicos por superficie, nivel de torneo y duración
- Visualizaciones interactivas con Altair
- Estadísticas en tiempo real de los datos filtrados

#### 3. Predictor de Partidos
- Interfaz para ingresar características del partido
- Predicción instantánea de duración y categoría
- Explicación de factores que influyen en la predicción
- Ejemplos predefinidos

#### 4. Análisis Avanzado
- Q-Q plot de residuos
- Análisis de residuos vs valores predichos
- Importancia de features
- Matriz de confusión para clasificación

### 🎨 Principios de Visualización Aplicados

#### Gramática de Gráficos
- **Expresividad**: Cada visualización comunica información específica sin ambigüedad
- **Comparabilidad**: Escalas y referencias permiten comparación directa entre elementos
- **Interactividad**: Selecciones, filtros y tooltips facilitan la exploración
- **Adaptabilidad**: Visualizaciones responsive que se adaptan a diferentes variables

#### Ejemplos Implementados
1. **Scatter Plot Interactivo**: Predicciones vs realidad con selección por superficie
2. **Heatmap Dinámico**: Performance por superficie y nivel de torneo
3. **Dashboard Multi-Panel**: Comparativa de modelos con múltiples métricas

### 📈 Resultados del Modelo (Versión Final Corregida)

- **RMSE**: 34.93 minutos (modelo de regresión)
- **R²**: 0.307 (30.7% de varianza explicada)
- **Accuracy (Clasificación)**: 47.0%
- **MAE**: 28.26 minutos

### 🔍 Estado del Proyecto para Examen Final

#### ✅ Problemas Resueltos
1. **Error de métricas**: Corregidos KeyError para 'rmse' y 'accuracy' → ahora usa 'rmse_regression' y 'accuracy_classification'
2. **Funcionalidad inapropiada**: Removida completamente la sección de "Predicción de Ganadores" 
3. **Formato académico**: Eliminados emojis excesivos y estilo informal
4. **Contenido educativo**: Agregadas explicaciones de terminología de tenis
5. **Claridad de datos**: Notas explicativas para valores "None" en tournament levels

#### 🎯 Versión Recomendada para Evaluación
**Archivo principal**: `version_final_corregida/tennis_app_final.py`
- ✅ Sin errores de ejecución
- ✅ Formato académico apropiado  
- ✅ Funcionalidades educativas para no conocedores de tenis
- ✅ Enfoque exclusivo en predicción de duración (no ganadores)

### 🔍 Insights Principales

1. **Grand Slams** son la característica más importante (35% de importancia)
2. **Superficie Clay** tiende a generar partidos más largos y predecibles
3. **Diferencia de ranking < 20** indica partidos equilibrados que duran más
4. **Finales y Semifinales** tienen mayor duración promedio
5. **Grass** tiene la mayor variabilidad en duración

### 🌐 Despliegue en Streamlit Cloud

La aplicación está disponible en:
👉 **[Tennis Match Duration Predictor - Streamlit Cloud](https://share.streamlit.io/TU_USUARIO/tennis-ao26-streamlit)**

Para desplegar en Streamlit Cloud:

1. Subir el código a GitHub: `https://github.com/TU_USUARIO/tennis-ao26-streamlit`
2. Conectar el repositorio en [share.streamlit.io](https://share.streamlit.io)
3. Especificar `tennis_app.py` como archivo principal
4. Rama: `main`
5. La aplicación se desplegará automáticamente en ~2-3 minutos

**Ver:** `DEPLOYMENT_GUIDE.md` para instrucciones detalladas de despliegue.

### 👥 Presentación Oral (12/11 y 19/11)

La aplicación está diseñada para ser demostrada en vivo durante la presentación oral, mostrando:

- Cómo se visualizan los resultados
- Interacción del usuario con el modelo
- Exploración de datos en tiempo real
- Interpretación de predicciones

### 📚 Archivos Relacionados

- `Proy_3ra_Modelado_Mejorado_BarrancoJuan.ipynb`: Notebook con el modelado completo
- `ANALISIS_LOGS_EJECUCION_KAGGLE_PROFUNDO.md`: Análisis detallado de la ejecución
- `Guia_Defensa_Oral.md`: Guía para la presentación oral

### 👨‍💻 Autor

**Juan Ignacio Barranco Bastan**  
Ciencia de Datos  
Noviembre 2025

---

## 📁 Estructura Original del Proyecto

- `entrega2proy_EDA/`: Contiene el análisis exploratorio de datos (EDA)
- `dags/`: DAGs de Apache Airflow para procesamiento de datos
- `include/sql/`: Scripts SQL para creación de esquemas y carga de datos
- `logs/`: Logs de ejecución de Airflow
- `figs/`: Figuras y gráficos generados

## Archivos principales previos

- `Proy_2da_EDA_BarrancoJuan.ipynb`: Notebook principal con el EDA
- `Proy_3ra_Modelado_BarrancoJuan.ipynb`: Notebook de modelado predictivo
- `docker-compose.yml`: Configuración para servicios con Docker
- `consultasValidacionPrimerEntregaCDD.pgsql`: Consultas de validación SQL

### Configuración original (ETL/Airflow)

#### Requerimientos

- Docker y Docker Compose instalados.
- Mínimo 4GB RAM libre.
- Conexión a internet para descargar datasets.

#### Configuración

1. Crear archivo `.env` con credenciales de Postgres:
   - POSTGRES_USER=tennis
   - POSTGRES_PASSWORD=tennis
   - POSTGRES_DB=tennisdb

2. Levantar el stack:
   - docker compose up airflow-init
   - docker compose up -d
   - Acceder a Airflow en <http://localhost:8080>.
   - Usuario inicial: admin / admin.

*Esta aplicación es parte de la Cuarta Entrega del proyecto de predicción de duración de partidos de tenis.*
