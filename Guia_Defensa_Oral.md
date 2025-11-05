# 🎯 Guía para Defensa Oral - Proyecto de Tenis (3ra Entrega)

## 📊 Análisis de Resultados - Explicación Simple

Basado en tu ejecución exitosa en Kaggle, aquí está todo lo que necesitas saber para defender tu proyecto:

---

## 1. ¿QUÉ HICISTE? (El Objetivo)

**Pregunta típica:** "¿De qué trata tu proyecto?"

**Tu respuesta:**
> "Mi proyecto predice cuánto tiempo va a durar un partido de tenis, usando solo información que se conoce ANTES de que empiece el partido. Por ejemplo: quiénes juegan, en qué superficie, en qué ronda, etc."

**¿Por qué cambiaste el objetivo original?**
> "Originalmente queríamos predecir quién ganaría el torneo, pero el profesor nos dijo que no era viable porque no teníamos datos de torneos completos, solo de partidos individuales. Entonces, basándonos en nuestro EDA (análisis exploratorio), vimos que había mucha variación en la duración de los partidos y era algo predecible."

---

## 2. ¿CON QUÉ DATOS TRABAJASTE?

**Datos iniciales:**
- 5,861 partidos totales en el dataset
- 29 variables disponibles

**Datos utilizables para modelado:**
- 5,418 partidos (después de limpiar)
- **¿Por qué menos?** Eliminamos partidos sin información de duración o con duración inválida (≤ 0 minutos)

**Variables que USASTE (features pre-partido):**
- **Del torneo:** nivel, superficie, ronda, best_of (a 3 o 5 sets)
- **De los jugadores:** ranking, edad, mano dominante, altura

**Variables que NO USASTE (para evitar "trampa"):**
- Estadísticas del partido (aces, dobles faltas, etc.) → solo se conocen DESPUÉS
- Nombres de jugadores → para evitar "memorizar" jugadores específicos

---

## 3. ¿QUÉ DESCUBRISTE SOBRE LA DURACIÓN?

**Estadísticas clave de la variable objetivo (`minutes`):**

| Medida | Valor | Significado |
|--------|-------|-------------|
| **Promedio** | 119 minutos | ~2 horas por partido |
| **Mediana** | 112 minutos | La mitad dura menos de 2h |
| **Mínimo** | 43 minutos | Partidos muy rápidos |
| **Máximo** | 345 minutos | Partidos épicos de ~6 horas |
| **Desviación** | 42 minutos | Gran variabilidad |

**Observaciones importantes:**
- **Asimetría = 1.03:** Hay partidos muy largos que son "outliers" (casos raros)
- **Distribución:** La mayoría de partidos duran entre 87 y 143 minutos

**¿Qué significa esto?**
> "La duración varía mucho. Hay partidos cortos de 1 hora y otros maratónicos de 6 horas. Esto hace que predecir con exactitud sea un desafío."

---

## 4. ¿CÓMO DIVIDISTE LOS DATOS?

**División:**
- **Entrenamiento (Train):** 80% → 4,334 partidos
- **Prueba (Test):** 20% → 1,084 partidos

**¿Por qué esta división?**
> "El 80% lo usamos para que el modelo aprenda patrones, y el 20% lo dejamos para evaluar qué tan bien funciona con datos que nunca vio."

**Estratificación por `best_of`:**
- Mantuviste la proporción de partidos a 3 sets (~83.6%) y a 5 sets (~16.4%) en ambos conjuntos
- **¿Por qué?** Porque los partidos a 5 sets duran MUCHO más, y querías que ambos conjuntos sean representativos

---

## 5. ¿QUÉ MODELOS PROBASTE?

### Requisito: Probar al menos 3 modelos diferentes ✅

#### **Modelo 1: Ridge Regression** (Regresión Lineal con Regularización)
- **Qué hace:** Busca relaciones lineales entre variables
- **Ventaja:** Simple, rápido, interpretable
- **Desventaja:** No captura relaciones complejas

#### **Modelo 2: Random Forest** (Bosque de Árboles de Decisión)
- **Qué hace:** Crea muchos árboles y promedia sus predicciones
- **Ventaja:** Captura relaciones no lineales, robusto
- **Desventaja:** Puede "memorizar" el entrenamiento

#### **Modelo 3: Gradient Boosting** (Árboles Secuenciales)
- **Qué hace:** Crea árboles uno tras otro, corrigiendo errores previos
- **Ventaja:** Muy preciso, state-of-the-art
- **Desventaja:** Más lento, requiere ajuste fino

---

## 6. ¿QUÉ RESULTADOS OBTUVISTE?

### Comparación de los 3 modelos (ANTES de optimizar):

| Modelo | RMSE Test | R² Test | Diagnóstico |
|--------|-----------|---------|-------------|
| **Ridge** | 35.84 min | 0.2614 | ⚠️ Underfitting |
| **Random Forest** | 36.79 min | 0.2217 | ⚠️ Overfitting severo |
| **Gradient Boosting** | **35.80 min** | **0.2631** | ✅ Mejor balance |

### **Explicación de las métricas:**

#### **RMSE (Root Mean Squared Error) = 35.80 minutos**
> "En promedio, mis predicciones se equivocan por 36 minutos. Si un partido dura 120 minutos, podría predecir entre 84 y 156 minutos."

#### **MAE (Mean Absolute Error) = 29.30 minutos**
> "El error típico es de 29 minutos. Es un poco mejor que RMSE porque no penaliza tanto los errores grandes."

#### **R² (Coeficiente de Determinación) = 0.2631**
> "Mi modelo explica el 26.3% de la variación en la duración de los partidos."

**¿Es bueno o malo 26%?**
> "Para este tipo de problema, es razonable pero no excelente. Significa que hay muchos factores que afectan la duración que no tenemos en los datos (como el estado físico del día, estrategia, clima, etc.)."

---

## 7. ¿POR QUÉ ELEGISTE GRADIENT BOOSTING?

**Criterio de selección:**
- Menor RMSE en test (35.80 min vs 35.84 de Ridge y 36.79 de Random Forest)
- Mejor R² en test (26.31%)
- **Balance entre train y test:** No sobreajusta tanto como Random Forest

**Problemas detectados en los otros:**
- **Ridge:** Underfitting (R² test = 26%) → demasiado simple
- **Random Forest:** Overfitting brutal (R² train = 89.5% pero test = 22.2%) → memorizó el entrenamiento

---

## 8. ¿QUÉ ES EL PIPELINE Y POR QUÉ LO USASTE?

**Pipeline = Tubería de procesamiento automático**

**¿Qué hace tu pipeline?**
1. **Identifica** qué variables son numéricas y cuáles categóricas
2. **Imputa** valores faltantes:
   - Numéricas → usa la mediana
   - Categóricas → rellena con "missing"
3. **Escala** variables numéricas (StandardScaler)
4. **Codifica** variables categóricas (One-Hot Encoding)
5. **Entrena** el modelo

**¿Por qué es importante?**
> "El pipeline evita 'data leakage' (trampa de datos). Todo el preprocesamiento se aprende SOLO con los datos de entrenamiento, no con los de test. Esto simula el mundo real."

**Ejemplo práctico:**
> "Si escalo el ranking usando toda la data, el modelo 've' información del test. Con el pipeline, calculo la media y desviación solo del train, y luego aplico esa transformación al test."

---

## 9. ¿QUÉ ES GRIDSEARCHCV Y PARA QUÉ LO USASTE?

**GridSearchCV = Búsqueda exhaustiva de los mejores hiperparámetros**

**¿Qué probaste?**
```
- n_estimators: [50, 100, 200]    → cantidad de árboles
- learning_rate: [0.01, 0.1, 0.2] → qué tan rápido aprende
- max_depth: [3, 5, 7]            → profundidad de árboles
```

**Total:** 3 × 3 × 3 = 27 combinaciones

**Validación cruzada 5-fold:**
> "Cada combinación se probó 5 veces con diferentes divisiones de datos. Total: 135 entrenamientos (27 × 5)."

**Resultado:**
- **Mejor configuración encontrada:**
  - `n_estimators = 50`
  - `learning_rate = 0.1`
  - `max_depth = 3`

**¿Mejoró el modelo?**
- RMSE bajó de 35.80 a **35.69 minutos** (mejora de 0.3%)
- R² subió de 0.2631 a **0.2676**

> "La mejora es modesta, pero confirma que los hiperparámetros están bien ajustados."

---

## 10. DIAGNÓSTICO: ¿HAY OVERFITTING O UNDERFITTING?

### Resultados del modelo optimizado:

| Conjunto | RMSE | R² |
|----------|------|-----|
| **Train** | 33.67 min | 0.3511 |
| **Test** | 35.69 min | 0.2676 |
| **Diferencia** | 2.02 min | 0.0835 |

### **Diagnóstico: ⚠️ LEVE UNDERFITTING**

**¿Qué significa?**
> "El modelo no está capturando todos los patrones relevantes. Tanto en train como en test, el R² es bajo (~35% y ~27%)."

**¿Por qué NO es overfitting?**
> "Porque la diferencia entre train y test es pequeña (8.35% en R²). Si hubiera overfitting, el train sería mucho mejor que el test."

**¿Qué se podría hacer?**
- Agregar más features (ej: historial de enfrentamientos previos)
- Crear interacciones entre variables (ej: ranking × superficie)
- Probar modelos más complejos (XGBoost, LightGBM)

---

## 11. ¿QUÉ VARIABLES SON MÁS IMPORTANTES?

### Top 5 features más influyentes:

| Ranking | Feature | Importancia | Significado |
|---------|---------|-------------|-------------|
| 1 | **tourney_level_G** | 77.4% | Si es Grand Slam o no |
| 2 | **loser_rank** | 6.7% | Ranking del perdedor |
| 3 | **winner_rank** | 5.1% | Ranking del ganador |
| 4 | **winner_age** | 2.6% | Edad del ganador |
| 5 | **loser_ht** | 1.9% | Altura del perdedor |

**Interpretación:**

### **1. Grand Slam domina (77%)**
> "La variable más importante con MUCHA diferencia es si el partido es de Grand Slam. Estos partidos son a 5 sets y duran significativamente más."

### **2. Rankings importan (12% combinado)**
> "El ranking de ambos jugadores afecta. Jugadores de menor ranking (números más altos) tienden a jugar partidos más largos porque están más igualados."

### **3. Edad y altura tienen influencia menor**
> "Jugadores más viejos o más altos pueden tener estilos de juego que afectan la duración, pero es un efecto pequeño."

### **4. Superficie aparece pero poco**
> "Grass (pasto) tiene algo de importancia (1.1%), pero mucho menos de lo esperado. Esto puede deberse a que está correlacionado con `tourney_level`."

---

## 12. ¿CÓMO SE VEN LAS PREDICCIONES?

### Análisis de errores:

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Media de errores** | 0.57 min | ✅ Casi cero (no hay sesgo) |
| **Desviación estándar** | 35.70 min | ⚠️ Alta variabilidad |

**¿Qué significa esto?**
> "El modelo no está sesgado (no predice sistemáticamente más o menos tiempo). Pero la variabilidad es alta, lo que confirma que hay mucha incertidumbre en las predicciones."

---

## 13. PREGUNTAS FRECUENTES EN LA DEFENSA ORAL

### **P1: ¿Por qué cambiaste el objetivo del proyecto?**
**R:** "El objetivo original (predecir campeón) no era viable porque no teníamos datos de torneos completos. El profesor nos orientó a usar el EDA para encontrar un objetivo factible, y la duración de partidos mostró patrones interesantes y es un problema relevante."

---

### **P2: ¿Por qué el R² es tan bajo (26%)?**
**R:** "La duración de un partido depende de muchos factores que no tenemos en los datos:
- Estado físico del día
- Estrategia de juego
- Condiciones climáticas
- Momentum psicológico
- Lesiones durante el partido

Con solo información pre-partido, explicar el 26% es razonable. Hay mucho 'ruido' inherente al deporte."

---

### **P3: ¿Qué es data leakage y cómo lo evitaste?**
**R:** "Data leakage es cuando el modelo 've' información del futuro que no debería conocer. Lo evité:
1. Excluyendo estadísticas del partido (aces, etc.)
2. Usando pipeline para que el preprocesamiento se ajuste solo con train
3. No usando nombres de jugadores (para evitar memorizar jugadores específicos)"

---

### **P4: ¿Por qué Gradient Boosting y no Random Forest?**
**R:** "Random Forest tuvo overfitting severo (R² train 89% vs test 22%). Gradient Boosting tiene mejor balance y menor RMSE en test. Ridge era demasiado simple (underfitting)."

---

### **P5: ¿Qué mejorarías en el futuro?**
**R:** "Tres cosas principales:
1. **Ingeniería de features:** agregar historial H2H (head-to-head), racha de victorias, diferencia absoluta de ranking
2. **Modelos avanzados:** probar XGBoost, LightGBM, o stacking de modelos
3. **Datos externos:** clima, estado de forma reciente, superficie específica del torneo"

---

### **P6: ¿Cómo validaste que el modelo funciona bien?**
**R:** "Usé tres estrategias:
1. **División train/test 80/20** con estratificación por best_of
2. **Validación cruzada 5-fold** durante GridSearchCV (135 entrenamientos)
3. **Comparación de múltiples métricas:** RMSE, MAE, R² (no solo una)"

---

### **P7: ¿Qué aprendiste del proyecto?**
**R:** "Tres lecciones clave:
1. El EDA es fundamental para definir un objetivo realista
2. El preprocesamiento correcto (pipeline) es tan importante como el modelo
3. No siempre se logran R² altos, y eso está bien si el problema es inherentemente ruidoso"

---

## 14. PUNTOS FUERTES DE TU TRABAJO (Para destacar)

✅ **Cambio de objetivo justificado** con base en EDA y feedback
✅ **Evitaste data leakage** correctamente
✅ **Pipeline profesional** siguiendo mejores prácticas
✅ **Comparaste 3 modelos** con métricas múltiples
✅ **Validación cruzada** y GridSearchCV aplicados correctamente
✅ **Diagnóstico de overfitting/underfitting** realizado
✅ **Interpretabilidad** mediante feature importance
✅ **Documentación clara** con markdown y visualizaciones

---

## 15. GLOSARIO RÁPIDO (Por si te preguntan)

| Término | Explicación simple |
|---------|-------------------|
| **RMSE** | Error promedio en minutos (penaliza errores grandes) |
| **MAE** | Error promedio absoluto (más robusto) |
| **R²** | % de varianza explicada (0-1, mayor mejor) |
| **Overfitting** | Memoriza el train, falla en test |
| **Underfitting** | Demasiado simple, no captura patrones |
| **Pipeline** | Tubería automática de preprocesamiento |
| **GridSearchCV** | Búsqueda de mejores hiperparámetros |
| **Stratify** | Mantener proporciones en train/test |
| **One-Hot Encoding** | Convertir categorías a números binarios |
| **StandardScaler** | Escalar variables a media 0 y desv 1 |
| **Feature importance** | Qué variables son más influyentes |
| **Cross-validation** | Dividir train en K partes para validar |

---

## 16. FRASE DE CIERRE (Para tu presentación)

> "Este proyecto demuestra que, aunque la duración de partidos de tenis tiene alta variabilidad e incertidumbre, es posible construir un modelo predictivo razonable usando solo información pre-partido. El modelo Gradient Boosting optimizado logra un error promedio de 36 minutos (26% de varianza explicada), lo cual es valioso para planificación de torneos y broadcasting. El trabajo futuro se enfoca en ingeniería de features más sofisticadas y modelos ensamblados."

---

## 📚 Tiempo de ejecución en Kaggle

- **Total:** ~74 segundos
- **Más lento:** GridSearchCV (52 segundos) → esperado, son 135 entrenamientos
- **Preparación datos:** <1 segundo
- **Entrenamiento modelos base:** ~2 segundos
- **Visualizaciones:** ~1 segundo cada una

> "El notebook es eficiente y reproducible en cualquier entorno."

---

## ✅ CHECKLIST PARA LA DEFENSA

Antes de presentar, asegúrate de poder explicar:
- [ ] ¿Por qué cambiaste el objetivo?
- [ ] ¿Qué variables usaste y cuáles NO usaste?
- [ ] ¿Cómo dividiste los datos y por qué?
- [ ] ¿Qué hace el pipeline?
- [ ] ¿Por qué elegiste Gradient Boosting?
- [ ] ¿Qué significan RMSE, MAE y R²?
- [ ] ¿Hay overfitting o underfitting?
- [ ] ¿Cuál es la variable más importante?
- [ ] ¿Qué mejorarías en el futuro?

---

## Respuestas rápidas para la defensa

### ¿Por qué cambiaste el objetivo?
El objetivo original (predecir el campeón) no era viable porque solo teníamos datos de partidos individuales, no de torneos completos. El profesor sugirió buscar un objetivo factible y, tras el EDA, la duración de los partidos resultó ser relevante y predecible.

### ¿Qué variables usaste y cuáles NO usaste?
Usé solo variables conocidas antes del partido: nivel del torneo, superficie, ronda, best_of, ranking, edad, mano y altura de ambos jugadores. No usé estadísticas del partido ni nombres de jugadores para evitar data leakage.

### ¿Cómo dividiste los datos y por qué?
Dividí el dataset en 80% para entrenamiento y 20% para test, manteniendo la proporción de partidos a 3 y 5 sets (estratificación por best_of). Así el modelo aprende y se evalúa de forma realista.

### ¿Qué hace el pipeline?
Automatiza el preprocesamiento: identifica tipos de variables, imputa valores faltantes, escala numéricas, codifica categóricas y entrena el modelo, todo sin mezclar información de test y train.

### ¿Por qué elegiste Gradient Boosting?
Fue el modelo con mejor balance entre error y capacidad de generalización. Random Forest sobreajustó y Ridge era demasiado simple. Gradient Boosting tuvo el menor RMSE y mejor R² en test.

### ¿Qué significan RMSE, MAE y R²?
- RMSE: error promedio en minutos (penaliza errores grandes)
- MAE: error promedio absoluto (más robusto)
- R²: porcentaje de varianza explicada por el modelo (0-1, mayor es mejor)

### ¿Hay overfitting o underfitting?
Hay leve underfitting: el modelo no captura todos los patrones, pero la diferencia entre train y test es pequeña. Es preferible a un modelo que sobreajuste.

### ¿Cuál es la variable más importante?
Si el partido es Grand Slam (tourney_level_G), porque estos partidos son a 5 sets y duran mucho más. También influyen los rankings de los jugadores.

### ¿Qué mejorarías en el futuro?
Agregar más features (historial de enfrentamientos, rachas, clima), probar modelos más avanzados (XGBoost, LightGBM) y usar datos externos para enriquecer el modelo.

---

**¡Éxito en tu defensa! 🎓🎾**
