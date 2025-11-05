# 🔍 ANÁLISIS EN PROFUNDIDAD - LOGS DE EJECUCIÓN EN KAGGLE
## Proyecto de Tenis - Tercera Entrega Mejorada v2.0

**Fecha de Análisis:** 4 de Noviembre de 2025  
**Tiempo Total de Ejecución:** ~32 segundos  
**Estado:** ✅ EXITOSO

---

## PARTE 1: ESTADO GENERAL Y VERSIONES

### ✅ Librerías Instaladas Correctamente

```
Python: 3.11.13 | OS: Linux 6.6.56+
pandas: 2.2.3 | numpy: 1.26.4
sklearn: 1.2.2 | xgboost: 2.0.3 | lightgbm: 4.6.0
```

**Análisis:**
- Python 3.11.13: Versión estable y moderna ✅
- XGBoost 2.0.3: Versión actual ✅
- LightGBM 4.6.0: Versión actual ✅
- sklearn 1.2.2: Versión compatible ✅

**Conclusión:** Ambiente correctamente configurado para machine learning.

---

## PARTE 2: PREPARACIÓN DE DATOS

### 📊 Dataset Cargado

```
5,861 partidos totales
29 variables
```

**Análisis:**
- Dataset completo sin errores de carga
- Se muestra correctamente: match_id, tourney_name, surface, tourney_level, round, minutes, rankings

### Limpieza de Datos

```
Dataset para modelado: 5,418 partidos (443 registros removidos)
Valores faltantes: 51
```

**Análisis:**
- Se eliminaron ~7.5% de datos (443 de 5861)
- La razón: partidos sin duración o duración inválida (<= 0)
- Pérdida aceptable (esperada en datasets deportivos)
- Valida correctamente

### 📈 Variable Objetivo (minutes)

```
count: 5,418
mean: 119.1 minutos (~2 horas)
std: 41.8 minutos (alta variabilidad)
min: 43 minutos
25%: 87 minutos (Q1)
50%: 112 minutos (mediana)
75%: 143 minutos (Q3)
max: 345 minutos (~5.75 horas)
```

**Análisis Detallado:**

1. **Media vs Mediana (119 vs 112):**
   - Diferencia pequeña (7 minutos) → distribución relativamente simétrica
   - Indica que no hay sesgo fuerte hacia duraciones extremas

2. **Rango (43-345 minutos):**
   - Ratio max/min = 8x
   - Variación ENORME en duraciones
   - Explica por qué el R² no puede ser muy alto (hay demasiado "ruido" inherente)

3. **Desviación estándar (42 minutos):**
   - ~35% de la media
   - Muy alta variabilidad relativa
   - Hace que la predicción exacta sea extremadamente difícil

4. **Distribución de cuartiles:**
   - Q1-Q3 = 56 minutos (rango intercuartílico)
   - La mayoría de partidos duran entre 87 y 143 minutos
   - Pero hay outliers en ambos lados

**Conclusión:** La variable objetivo es altamente variable, lo que justifica el R² "bajo" (~26%). No es un problema del modelo, sino de la naturaleza del deporte.

---

## PARTE 3: INGENIERÍA DE FEATURES (NUEVO)

### ✅ 7 Features Derivadas Creadas

```
✅ rank_diff: Diferencia absoluta de ranking
✅ rank_avg: Promedio de ranking
✅ age_diff: Diferencia de edad
✅ ht_diff: Diferencia de altura
✅ is_grand_slam: Flag de Grand Slam
✅ same_hand: Si los jugadores tienen la misma mano dominante
✅ fast_surface: Flag de superficie rápida (Grass/Hard vs Clay)
```

**Ejemplo del dataset con features derivadas:**

| rank_diff | rank_avg | age_diff | is_grand_slam | same_hand | minutes |
|-----------|----------|----------|---------------|-----------|---------|
| 7 | 12.5 | 1.6 | 0 | 1 | 135 |
| 1 | 9.5 | 0.7 | 0 | 1 | 104 |
| 226 | 132.0 | 1.0 | 0 | 1 | 79 |
| 12 | 10.0 | 2.4 | 0 | 1 | 155 |
| 780 | 413.0 | 2.5 | 0 | 1 | 62 |

**Análisis:**

1. **rank_diff (7 a 780):**
   - Rango enorme: desde partidos parejos (top 10 vs top 10) hasta desbalanceados (top 10 vs 400+)
   - Relación esperada: partidos más parejos → duran más
   - Feature IMPORTANTE

2. **rank_avg (9.5 a 413):**
   - Identifica si es un partido "estrella" (bajo) o "cualificaciones" (alto)
   - Correlaciona con la duración: mejores jugadores → partidos más competitivos → duran más

3. **age_diff, ht_diff:**
   - Pueden influir en estilo de juego
   - Rangos pequeños pero significativos

4. **is_grand_slam (0 o 1):**
   - Flag binario muy importante
   - Logs posteriores confirman: es la feature MÁS importante (77% en v1.0)
   - Grand Slams = partidos a 5 sets = duran MUCHO más

5. **same_hand (0 o 1):**
   - Efecto en el rally y duración
   - Feature nueva que v1.0 no tenía

6. **fast_surface (0 o 1):**
   - Superficie rápida → puntos más cortos
   - Debería correlacionar negativamente con duración

**Conclusión:** Ingeniería de features bien pensada y relevante. Estas features DEBEN mejorar la capacidad predictiva del modelo.

### Total de Features Finales

```
12 originales + 7 derivadas = 19 features totales
14 numéricas + 5 categóricas
```

✅ Aumento del 58% en features (de 12 a 19)

---

## PARTE 4: DIVISIÓN TRAIN/TEST

```
Train: 4,334 partidos (80%)
Test: 1,084 partidos (20%)

Proporción best_of en train:
  3 sets: 83.62%
  5 sets: 16.38%

Proporción best_of en test:
  3 sets: 83.58%
  5 sets: 16.42%
```

**Análisis:**

1. **Proporción perfectamente mantenida:**
   - Train 3-sets: 83.62% vs Test 3-sets: 83.58% → Diferencia: 0.04% ✅
   - Train 5-sets: 16.38% vs Test 5-sets: 16.42% → Diferencia: 0.04% ✅

2. **Estratificación exitosa:**
   - La estratificación por `best_of` garantiza que ambos conjuntos sean representativos
   - Crucial porque 5-sets duran significativamente más

3. **Tamaño de split:**
   - 80/20 es estándar y correcto
   - 1,084 partidos en test = suficiente para validación robusta

**Conclusión:** División realizada perfectamente. No hay data leakage potencial.

---

## PARTE 5: MODELOS DE REGRESIÓN - ANÁLISIS DETALLADO

### 📊 Resultados Comparativos

| Modelo | Train RMSE | Test RMSE | Train R² | Test R² | Diferencia R² |
|--------|------------|-----------|----------|---------|---------------|
| **GradientBoosting** | 32.50 | 35.84 | 0.3953 | 0.2613 | 0.1340 |
| Ridge | 35.06 | 35.85 | 0.2963 | 0.2608 | 0.0355 |
| RandomForest | 13.51 | 36.75 | 0.8955 | 0.2234 | 0.6721 |
| LightGBM | 25.58 | 36.76 | 0.6253 | 0.2229 | 0.4024 |
| XGBoost | 13.30 | 39.08 | 0.8987 | 0.1217 | 0.7770 |

### 🏆 GANADOR: GradientBoosting (Test RMSE: 35.84 minutos)

---

### ANÁLISIS MODELO POR MODELO

#### 1. **GradientBoosting** ✅ (MEJOR)

**Métricas:**
- Train RMSE: 32.50 | Test RMSE: 35.84 (diferencia: 3.34 min)
- Train R²: 0.3953 | Test R²: 0.2613 (diferencia: 0.1340)

**Análisis Detallado:**

✅ **Pros:**
- MEJOR Test RMSE (35.84 min)
- Segunda mejor Test R²
- **Balance perfecto:** diferencia Train-Test de solo 0.1340 en R²
- Esto significa: NO hay overfitting severo
- RMSE casi idéntico en train y test → generaliza bien

✅ **Interpretación del RMSE (35.84 minutos):**
- Error promedio: ±35.84 minutos
- Si un partido dura 120 min, el modelo predice entre 84 y 156 minutos
- Error porcentual: 35.84 / 119.1 = 30% (aceptable para este dominio)

🟡 **Cómo evita overfitting:**
- Regularización incluida (shrinkage/learning_rate)
- Los árboles son poco profundos (max_depth=3 según v1.0)
- Aprendizaje gradual limita memorización

**Conclusión:** Este es el modelo CORRECTO para este problema. Balance perfecto.

---

#### 2. **Ridge** (CERCANO, MÁS SIMPLE)

**Métricas:**
- Train RMSE: 35.06 | Test RMSE: 35.85 (diferencia: 0.79 min ¡LA MÁS PEQUEÑA!)
- Train R²: 0.2963 | Test R²: 0.2608 (diferencia: 0.0355)

**Análisis Detallado:**

✅ **Pros:**
- CASI idéntico al GradientBoosting en test
- Mejor generalizador (diferencia Train-Test más pequeña)
- MÁS SIMPLE (interpretable)
- Más rápido de entrenar

❌ **Contras:**
- RMSE apenas 0.01 minutos peor que GradientBoosting
- Pero asume linealidad (relaciones rectas entre variables)

**Conclusión:** Estadísticamente casi indistinguible de GradientBoosting. Podrías usar Ridge si necesitas simplicidad/velocidad.

---

#### 3. **RandomForest** (⚠️ OVERFITTING SEVERO)

**Métricas:**
- Train RMSE: 13.51 | Test RMSE: 36.75 (diferencia: 23.24 min ¡MUY GRANDE!)
- Train R²: 0.8955 | Test R²: 0.2234 (diferencia: 0.6721 ¡ENORME!)

**Análisis Detallado:**

❌ **PROBLEMA CRÍTICO:**
- Train RMSE de 13.51 vs Test de 36.75 = MEMORIZA datos de entrenamiento
- Train R² de 89.55% vs Test de 22.34% = Diferencia de 67.21 puntos porcentuales ¡¡¡
- Esto es **OVERFITTING SEVERO**

🔍 **¿Por qué ocurre?**
- Random Forest sin restricciones tiende a sobreajustarse
- Con 100 árboles y max_depth sin límite, crea particiones muy específicas para datos de entrenamiento
- Falla miserablemente en datos nuevos

⚠️ **Evidencia en los logs:**
- El modelo PARECE excelente en entrenamiento (R²=89.55%)
- Pero en test es MEDIOCRE (R²=22.34%, peor que Ridge)

**Conclusión:** Este modelo NO es confiable. Está "memorizando". Nunca lo usarías en producción.

---

#### 4. **LightGBM** (ALTERNATIVA, MODERADAMENTE BIEN)

**Métricas:**
- Train RMSE: 25.58 | Test RMSE: 36.76 (diferencia: 11.18 min)
- Train R²: 0.6253 | Test R²: 0.2229 (diferencia: 0.4024)

**Análisis Detallado:**

✅ **Pros:**
- Más rápido que Gradient Boosting
- Eficiente en memoria
- Test RMSE razonable

❌ **Contras:**
- Test RMSE ligeramente peor que GradientBoosting (36.76 vs 35.84)
- Diferencia Train-Test más grande (11.18 min) → algo de overfitting
- Diferencia R² grande (0.4024) → más overfitting que GradientBoosting

**Conclusión:** Buena alternativa si necesitas velocidad, pero sacrificas un poco de precisión.

---

#### 5. **XGBoost** (❌ PEOR CASO DE OVERFITTING)

**Métricas:**
- Train RMSE: 13.30 | Test RMSE: 39.08 (diferencia: 25.78 min ¡ENORME!)
- Train R²: 0.8987 | Test R²: 0.1217 (diferencia: 0.7770 ¡¡¡CATASTRÓFICO!!!)

**Análisis Detallado:**

❌ **ALERTA ROJA:**
- Este es el PEOR modelo
- Test RMSE: 39.08 minutos (el PEOR de todos)
- Test R²: 0.1217 (el PEOR, apenas explica 12% de varianza)
- Diferencia Train-Test: 0.7770 en R² = **OVERFITTING EXTREMO**

🔍 **¿Por qué falla XGBoost?**
- Probablemente necesita más tuning de hiperparámetros
- Sin regularización apropiada, XGBoost puede ser más propenso a overfitting que GB
- Los hiperparámetros por defecto no son óptimos para este dataset

⚠️ **Cómo se vería:**
- Train: El modelo se ajusta casi perfectamente (R²=89.87%)
- Test: Falla completamente (R²=12.17%)

**Conclusión:** XGBoost necesitaría ajuste fino de hiperparámetros. Con los defaults, es inútil.

---

### 🎯 RANKING FINAL DE REGRESIÓN

1. **🥇 GradientBoosting:** RMSE 35.84, R² 0.2613, Balance excelente
2. **🥈 Ridge:** RMSE 35.85, R² 0.2608, Casi idéntico, más simple
3. **🥉 LightGBM:** RMSE 36.76, R² 0.2229, Más rápido pero menos preciso
4. ❌ RandomForest: RMSE 36.75, R² 0.2234, Overfitting severo
5. ❌❌ XGBoost: RMSE 39.08, R² 0.1217, Overfitting catastrófico

---

## PARTE 6: CLASIFICACIÓN (NUEVO)

### 📊 Distribución de Clases

```
CORTO (<100 min):    2,160 partidos (39.9%)
MEDIO (100-150 min): 2,146 partidos (39.6%)
LARGO (>150 min):    1,112 partidos (20.5%)
```

**Análisis:**

1. **Balance de clases:**
   - CORTO y MEDIO: casi iguales (39.9% vs 39.6%) → bien balanceado
   - LARGO: 20.5% → minoritario pero no extremo
   - No hay desbalance severo que cause problemas

2. **Razón CORTO:MEDIO:**
   - Casi 1:1, lo que es ideal para clasificación
   - Facilita que el modelo aprenda ambas clases bien

3. **Minoría LARGO:**
   - 20.5% es suficiente (no es 1% o 5%)
   - El modelo puede aprender patrones

**Conclusión:** Distribución razonable para clasificación.

---

### 📈 Resultados de Clasificadores

| Modelo | Train Accuracy | Test Accuracy | F1 (weighted) | Diferencia |
|--------|----------------|---------------|---------------|------------|
| **GradientBoostingClassifier** | 0.6241 | 0.4862 | 0.4775 | 0.1379 |
| LogisticRegression | 0.5145 | 0.4788 | 0.4660 | 0.0357 |
| RandomForestClassifier | 1.0000 | 0.4539 | 0.4462 | 0.5461 |

### 🏆 GANADOR: GradientBoostingClassifier (Test Accuracy: 48.62%)

---

### ANÁLISIS CLASIFICADOR POR CLASIFICADOR

#### 1. **GradientBoostingClassifier** ✅ (MEJOR)

**Métricas:**
- Train Accuracy: 62.41%
- Test Accuracy: 48.62%
- F1 (weighted): 0.4775
- Diferencia: 13.79%

**Análisis:**

✅ **Pros:**
- Mejor Test Accuracy (48.62%)
- Mejor F1 weighted (0.4775)
- Diferencia Train-Test razonable (13.79%)

🟡 **Análisis Detallado:**

**¿Por qué 48.62% parece bajo?**
- Base aleatoria: 33% (si elijes al azar entre 3 clases)
- 48.62% es +47% mejor que aleatorio ✅
- Pero parece bajo porque nos acostumbramos a "accuracy" en problemas binarios (50% = aleatorio para 2 clases, pero aquí es 33%)

**F1 (weighted) = 0.4775:**
- Promedia las F1-scores ponderadas por la cantidad de cada clase
- 0.4775 en una escala 0-1 es razonable
- Indica que el modelo balancea precisión y recall

🟡 **¿Por qué no es superior?**
- La tarea es inherentemente difícil: 3 categorías similares
- Las categorías se solapan (ej: un partido a 95 minutos está en CORTO/MEDIO fronterizo)
- El modelo tiene que aprender límites borrosos

**Conclusión:** Buen desempeño. Mejor que alternativas.

---

#### 2. **LogisticRegression**

**Métricas:**
- Train Accuracy: 51.45%
- Test Accuracy: 47.88%
- F1 (weighted): 0.4660
- Diferencia: 3.57%

**Análisis:**

✅ **Pros:**
- Excelente generalización (diferencia Train-Test: 3.57%)
- CASI NO overfitting
- Muy simple (interpretable)

❌ **Contras:**
- Test Accuracy ligeramente peor (47.88% vs 48.62%)
- Asume frontera lineal entre clases (poco realista)

**Conclusión:** Alternativa simple, pero GradientBoosting es mejor.

---

#### 3. **RandomForestClassifier** (❌ OVERFITTING)

**Métricas:**
- Train Accuracy: 100% (ALERTA)
- Test Accuracy: 45.39%
- F1 (weighted): 0.4462
- Diferencia: 54.61% (¡¡¡)

**Análisis:**

❌ **PROBLEMA CRÍTICO:**
- Train Accuracy de 100% es IMPOSIBLE = está memorizando perfectamente el entrenamiento
- Pero test de 45.39% = falla miserablemente en datos nuevos
- Diferencia de 54.61% es ENORME

🔴 **Alerta Roja:**
- Este modelo NO es confiable
- Está "viendo el futuro" en training pero completamente ciego en test

**Conclusión:** NUNCA usar este modelo. Está completamente sobreajustado.

---

## PARTE 7: ANÁLISIS DE ERRORES POR SEGMENTO (NUEVO - MUY IMPORTANTE)

### 1️⃣ ERROR POR TIPO DE TORNEO

```
Torneo  | Error Promedio | Error Máximo | Partidos
--------|----------------|--------------|----------
F       | 20.96 min      | 53.74 min    | 12
G       | 38.50 min      | 100.24 min   | 168
D       | 27.16 min      | 70.07 min    | 35
M       | 30.47 min      | 126.91 min   | 307
A       | 26.50 min      | 103.33 min   | 562
```

**Análisis Detallado:**

🟢 **Mejor desempeño: Torneos F (Finales)**
- Error: 20.96 minutos
- Muestra: Solo 12 partidos (poco representativo)
- Posible razón: Finales tienen estructura predecible

🔴 **Peor desempeño: Torneos G (Grand Slams)**
- Error: 38.50 minutos
- Muestra: 168 partidos (representativo)
- Posible razón: 
  - Grand Slams = partidos a 5 sets
  - Son MUCHO más variables en duración
  - Pueden ir de 2 horas a 5+ horas
  - El modelo lucha con esta variabilidad

**Conclusión:** El modelo tiene dificultades con Grand Slams. Esto sugiere que necesitaría:
- Modelos especializados por tipo de torneo
- O más data de Grand Slams
- O features adicionales que capturen mejor la competitividad

---

### 2️⃣ ERROR POR SUPERFICIE

```
Superficie | Error Promedio | Error Máximo | Partidos
-----------|----------------|--------------|----------
Grass      | 28.04 min      | 91.30 min    | 135
Hard       | 29.11 min      | 104.82 min   | 625
Clay       | 30.67 min      | 126.91 min   | 324
```

**Análisis Detallado:**

✅ **Mejor: Grass (Pasto)**
- Error: 28.04 minutos (el MEJOR entre superficies)
- Razón probable: Grass es superficie MÁS RÁPIDA
  - Puntos más cortos
  - Partidos más predecibles en duración
  - Menos variabilidad
- Máximo 91 minutos (los partidos en grass son inherentemente cortos)

🟡 **Medio: Hard**
- Error: 29.11 minutos
- Es la mayoría de torneos (625 partidos)
- Variabilidad media

🔴 **Peor: Clay (Arcilla)**
- Error: 30.67 minutos (el PEOR entre superficies)
- Razón probable: Clay es superficie MÁS LENTA
  - Puntos más largos (más amortiguación)
  - Mayor variabilidad en duración
  - Jugadores adaptan estrategia a la superficie
  - Los rallies pueden ser muy largos (30+ toques)
- Máximo 126.91 minutos (mucho más que Grass)

**Conclusión:** El modelo es mejor en superficies "rápidas" y peor en "lentas". Esto es lógico: superficies lentas tienen más variabilidad inherente.

---

### 3️⃣ ERROR POR RONDA (TOP 5)

```
Ronda | Error Promedio | Error Máximo | Partidos
------|----------------|--------------|----------
R128  | 36.17 min      | 126.91 min   | 154
R64   | 30.90 min      | 109.44 min   | 190
R32   | 29.34 min      | 98.25 min    | 331
SF    | 27.73 min      | 103.33 min   | 54
R16   | 26.71 min      | 80.90 min    | 175
```

**Análisis Detallado:**

🔴 **Peor: Ronda 128 (Primera ronda)**
- Error: 36.17 minutos
- Razón: Jugadores muy desigualados
  - Favorito vs (casi) cualquiera
  - Varía MUCHO: puede ser 45 min o 3+ horas
  - Es IMPREDECIBLE (¿Le lluvere el match? ¿Se retira?)
  - Máximo 126.91 minutos (partidos sorpresa)

✅ **Mejor: Ronda 16**
- Error: 26.71 minutos
- Razón: Jugadores más parejos
  - Semifinales/Cuartos generalmente tienen competencia cerrada
  - Duración más predecible (ambos luchan por ganar)
  - Máximo 80.90 minutos (más consistente)

**Conclusión:** El modelo es mejor en rondas posteriores (Cuartos, Semis, Finals) porque los partidos son más "parejos" = duración más predecible. En primeras rondas hay mucha variabilidad.

---

### 4️⃣ PARTIDOS EXTREMOS (> 300 minutos)

```
No hay partidos > 300 minutos en el test set
```

**Análisis:**

- En el dataset de entrenamiento había 1 máximo de 345 minutos
- No aparece en test (mala suerte estadística o era única)
- Esto es BUENO: no tenemos que analizar un caso edge raro

---

### 5️⃣ PARTIDOS CORTOS (< 90 minutos)

```
Total: 305 partidos
Error promedio: 34.56 minutos
Error máximo: 103.33 minutos
```

**Análisis:**

❌ **PROBLEMA DETECTADO:**
- Partidos cortos (<90 min) tienen error de 34.56 minutos
- Esto es ENORME: error relativo de 34.56/85 = 41% (tomando 85 como duración promedio)
- Máximo error: 103.33 minutos (un partido de 90 se predice como 193 minutos ¡¡¡)

🔍 **¿Por qué ocurre?**
- El modelo tiende a predecir hacia el PROMEDIO (119 minutos)
- Un partido de 60 minutos es "anómalo" (alguien se retira, gana fácilmente)
- El modelo no tiene suficiente información pre-partido para saber esto
- Sería necesario: información de retiros, forma actual del jugador, etc.

**Conclusión:** El modelo es DÉBIL para partidos cortos. Necesitaría features adicionales.

---

### 6️⃣ PARTIDOS PROMEDIO (90-150 minutos)

```
Total: 544 partidos
Error promedio: 19.01 minutos
Error máximo: 82.53 minutos
```

**Análisis:**

✅ **EXCELENTE DESEMPEÑO:**
- Error promedio: 19.01 minutos (el MEJOR de todos los segmentos)
- Error relativo: 19.01/120 = 15.8% (muy aceptable)
- Máximo: 82.53 minutos (controlado)

🎯 **¿Por qué es tan bueno aquí?**
- Estos son partidos "típicos"
- La mayoría de entrenamientos ocurre en este rango
- El modelo aprendió bien estos patrones
- No hay tantos "anómalo" (retiros, sorpresas)

**Conclusión:** El modelo es CONFIABLE para su rango de operación óptimo (90-150 minutos).

---

## PARTE 8: RESUMEN COMPARATIVO REGRESIÓN VS CLASIFICACIÓN

### 📊 Regresión

```
Mejor modelo: GradientBoosting
Test RMSE: 35.84 minutos
Test MAE: 29.44 minutos
Test R²: 0.2613
```

**Interpretación:**
- Error promedio: 35.84 minutos (~30% de la media)
- Predice la duración EXACTA
- Útil para: logística, broadcasting, planificación

---

### 📊 Clasificación

```
Mejor modelo: GradientBoostingClassifier
Test Accuracy: 48.62%
F1 (weighted): 0.4775
```

**Interpretación:**
- Predice la CATEGORÍA (Corto/Medio/Largo)
- 48.62% es +47% mejor que aleatorio (33%)
- Útil para: decisiones rápidas, clasificación en tiempo real

---

## PARTE 9: HALLAZGOS PRINCIPALES

### ✅ 1. MEJORA CON INGENIERÍA DE FEATURES

```
7 nuevas features derivadas creadas y probadas
```

**Evidencia:**
- Las features nuevas (rank_diff, rank_avg, etc.) son interpretables
- Capturan relaciones importantes (diferencia de ranking → competitividad)
- Aunque el R² final no sea mucho mayor (es fundamental del problema), estos features son MORE RELEVANT

---

### ✅ 2. NUEVOS MODELOS PROBADOS

**XGBoost:** ❌ Falla con defaults, necesitaría ajuste
**LightGBM:** 🟡 Funciona bien, alternativa viable
**Clasificación:** ✅ Complementa la regresión

---

### ✅ 3. ANÁLISIS DE ERRORES REVELA INSIGHTS CRÍTICOS

1. **Grand Slams son impredecibles** (+38.50 min error)
2. **Clay es más variable** que otras superficies
3. **Primeras rondas son caóticas** (variabilidad alta)
4. **Rondas posteriores son predecibles** (jugadores parejos)
5. **Partidos cortos son anomalías** (error alto)
6. **Rango 90-150 min es óptimo** (error bajo: 19 min)

---

### ✅ 4. MODELOS CONFIABLES

- ✅ **GradientBoosting (Regresión):** Confiable, balance excelente
- ✅ **GradientBoostingClassifier:** Buen clasificador
- ❌ **RandomForest/XGBoost:** Demasiado overfitting

---

## PARTE 10: RECOMENDACIONES BASADAS EN EVIDENCIA

### 1. **Para Predicción Exacta (Regresión)**
- Usar: **GradientBoosting**
- Esperar: ±36 minutos de error
- Mejor uso: Partidos 90-150 minutos
- Evitar: Grand Slams, primeras rondas, partidos cortos

### 2. **Para Categorización Rápida (Clasificación)**
- Usar: **GradientBoostingClassifier**
- Esperar: 48.62% accuracy
- Útil: Decisiones rápidas sin necesidad de duración exacta

### 3. **Próximos Pasos para Mejora**
- Agregar datos de retiros/lesiones
- Incluir forma reciente del jugador
- H2H (historial de enfrentamientos)
- Crear modelos especializados por Grand Slam vs otros
- Aumentar data de primeras rondas

### 4. **Casos de Uso Recomendados**
✅ Broadcasting: "El partido durará ~120 minutos ±36"
✅ Logística: "Reservar slot de 160 minutos"
✅ Apuestas: "Predicción de categoría: MEDIO (50% confianza)"
✅ Análisis: "Este Grand Slam tendrá error esperado de 38.50 min"

---

## CONCLUSIÓN GENERAL

### ✅ ÉXITO

El notebook v2.0 ejecutó exitosamente:
- ✅ Ingeniería de 7 features nuevas
- ✅ 5 modelos de regresión entrenados
- ✅ 3 modelos de clasificación entrenados
- ✅ Análisis profundo de errores por segmento
- ✅ Insights accionables extraídos

### 📊 HALLAZGO CLAVE

**El R² de 26% NO es un fracaso del modelo, sino una REALIDAD de los datos:**
- Partidos de tenis tienen variabilidad inherente (43-345 min = 8x rango)
- Muchos factores NO medibles (clima, forma actual, psicología)
- El modelo CAPTURA lo captureable correctamente
- En partidos estándar (90-150 min), el error es solo 19 minutos (15.8%)

### 🎯 VEREDICTO

**Proyecto EXITOSO y LISTO para presentación/defensa**

Demostraste:
1. Entendimiento profundo del problema
2. Ingeniería de features relevante
3. Comparación de múltiples modelos
4. Diagnóstico de overfitting/underfitting
5. Análisis de errores por segmento
6. Clasificación como alternativa
7. Recomendaciones basadas en evidencia

---

**Análisis Completado:** 4 de Noviembre de 2025
