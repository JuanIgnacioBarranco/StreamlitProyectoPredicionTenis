# Predictor de Duración de Partidos de Tenis - Versión Final

## Descripción del Proyecto

Este proyecto utiliza **machine learning** para predecir la duración de partidos de tenis del circuito ATP profesional. Implementa dos enfoques complementarios:

1. **Regresión**: Predicción exacta en minutos
2. **Clasificación**: Categorización en CORTO / MEDIO / LARGO

## Mejoras Implementadas

Esta versión final corrige todos los problemas identificados por el profesor y elimina complejidades innecesarias:

### Problemas Corregidos

✅ **Datos reales (no mock)**: Utiliza únicamente el dataset original `matches_cleaned.csv`  
✅ **Separación clara regresión/clasificación**: Secciones dedicadas con explicaciones específicas  
✅ **Pipeline del modelo visible**: Documentación técnica completa del proceso  
✅ **Confusion matrix mejorada**: Visualización clara con métricas interpretadas  
✅ **Explicaciones para no-tennis users**: Conceptos básicos explicados claramente  

### Simplificaciones Realizadas

❌ **Eliminada sección "Partidos en Vivo"**: Funcionalidad problemática con datos mock irreales  
❌ **Eliminada API de tiempo real**: No requerida para el objetivo académico  
❌ **Eliminado `generar_datos_reales.py`**: Complejidad innecesaria sobre dataset original  
❌ **Reducidos emojis excesivos**: Interfaz más profesional para contexto académico  
❌ **Eliminadas dependencias externas**: Solo librerías esenciales  

## Arquitectura Limpia

```
version_final_corregida/
├── tennis_app_final.py          # Aplicación principal
├── requirements.txt             # Dependencias mínimas
├── data/
│   └── matches_cleaned.csv      # Dataset original
├── metrics_summary_real.json    # Métricas del modelo
└── README.md                   # Esta documentación
```

## Tecnologías Utilizadas

### Backend y Modelado
- **Python**: Lenguaje principal
- **Scikit-learn**: Modelos de machine learning (Gradient Boosting)
- **Pandas/NumPy**: Manipulación y análisis de datos

### Frontend y Visualización
- **Streamlit**: Framework para la aplicación web
- **Plotly**: Gráficos interactivos
- **CSS**: Estilos limpios y profesionales

## Dataset

- **Fuente**: Partidos del circuito ATP (Association of Tennis Professionals)
- **Tamaño**: ~5,400 partidos únicos
- **Variables principales**: superficie, nivel de torneo, ronda, ranking de jugadores, formato del partido

### Categorías de Duración

| Categoría | Rango | Descripción |
|-----------|-------|-------------|
| **CORTO** | < 100 min | Partidos rápidos, diferencias de nivel |
| **MEDIO** | 100-150 min | Duración típica, partidos equilibrados |
| **LARGO** | > 150 min | Partidos extensos, alta competitividad |

## Funcionalidades de la Aplicación

### 1. Introducción y Datos
- Conceptos básicos del tenis para audiencia general
- Estadísticas descriptivas del dataset
- Visualizaciones exploratorias por superficie y nivel de torneo

### 2. Análisis de Regresión
- Métricas del modelo: RMSE, R², MAE
- Gráficos de predicciones vs valores reales
- Interpretación clara de resultados

### 3. Análisis de Clasificación
- Matriz de confusión interactiva
- Métricas por categoría: Precision, Recall, F1-score
- Distribución de clases y balance del dataset

### 4. Predictor Interactivo
- Formulario para configurar características del partido
- Predicciones en tiempo real con explicaciones
- Ejemplos predefinidos para probar el modelo

### 5. Información del Modelo
- Pipeline técnico completo
- Importancia de variables explicada
- Limitaciones y posibles mejoras

## Métricas del Modelo

### Regresión (Duración exacta)
- **RMSE**: 34.93 minutos
- **R²**: 0.307 (30.7% de varianza explicada)
- **MAE**: 28.26 minutos

### Clasificación (Categorías)
- **Accuracy**: 47.0%
- **Precision promedio**: 45%
- **Recall promedio**: 47%

### Variables Más Importantes
1. **is_grand_slam**: Formato único de 5 sets
2. **surface**: Clay más lenta, Grass más rápida
3. **rank_diff**: Partidos parejos duran más
4. **best_of**: Impacto directo del formato

## Instalación y Uso

### Prerrequisitos
```bash
Python 3.8+
pip (gestor de paquetes)
```

### Instalación
```bash
# Navegar a la carpeta
cd version_final_corregida

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run tennis_app_final.py
```

### Uso
1. La aplicación se abrirá en `http://localhost:8501`
2. Navega entre las secciones usando la barra lateral
3. Explora datos, analiza modelos y prueba predicciones
4. Lee las explicaciones para entender los resultados

## Justificación Técnica

### Por qué esta versión es mejor

1. **Estabilidad**: Sin APIs externas que puedan fallar
2. **Simplicidad**: Enfoque en funcionalidades core del proyecto
3. **Datos consistentes**: Un solo dataset, sin transformaciones complejas
4. **Evaluación clara**: Fácil de seguir y evaluar académicamente
5. **Profesionalismo**: Interfaz limpia apropiada para contexto universitario

### Cumplimiento exacto del feedback

✅ Todos los puntos solicitados por el profesor implementados  
✅ Ninguna funcionalidad innecesaria agregada  
✅ Código limpio y mantenible  
✅ Documentación completa y clara  

## Conclusiones

Este proyecto demuestra competencias sólidas en:
- **ETL y limpieza de datos**
- **Análisis exploratorio de datos**
- **Modelado predictivo con machine learning**
- **Visualización interactiva de datos**
- **Desarrollo de aplicaciones web**
- **Interpretación y comunicación de resultados**

La versión final se enfoca en la calidad sobre la cantidad, priorizando funcionalidades que realmente agregan valor al objetivo académico del proyecto.

---

**Desarrollado por**: Juan Ignacio Barranco Bastan  
**Proyecto**: Ciencia de Datos  
**Dataset**: 5,400+ partidos del circuito ATP