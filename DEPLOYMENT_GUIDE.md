# 📦 Guía de Despliegue - Streamlit Cloud & GitHub

## 🎯 Objetivo
Desplegar la aplicación Streamlit en Streamlit Cloud con repositorio en GitHub para que sea accesible públicamente.

---

## 📋 REQUISITOS PREVIOS

### 1. Cuentas Necesarias
- ✅ Cuenta GitHub (https://github.com)
- ✅ Cuenta Streamlit Cloud (https://streamlit.io/cloud)
- ✅ Git instalado localmente

### 2. Archivos Requeridos (✅ YA CREADOS)

```
tennis-ao26_with_csv_export/
├── tennis_app.py                 # 🎾 Aplicación Streamlit principal
├── requirements.txt              # 📦 Dependencias Python
├── data_for_streamlit.csv        # 📊 Datos de prueba
├── metrics_summary.json          # 📈 Métricas del modelo
├── .gitignore                    # 🚫 Archivos a ignorar en Git
├── README.md                     # 📖 Documentación del proyecto
├── Proy_4ta_Visualizacion_Interactiva_BarrancoJuan.ipynb  # 📓 Notebook con visualizaciones
└── .streamlit/
    └── config.toml               # ⚙️ Configuración de Streamlit (crear)
```

---

## 🚀 PASO 1: CREAR REPOSITORIO EN GITHUB

### 1.1 Inicializar Git Localmente

```bash
# Navegar al directorio del proyecto
cd /Users/juanignaciobarrancobastan/Documents/cienciaDeDatos/tennis-ao26_with_csv_export

# Inicializar repositorio
git init

# Agregar todos los archivos (excepto los en .gitignore)
git add .

# Primer commit
git commit -m "Initial commit: Tennis Match Duration Predictor - 4ta Entrega"
```

### 1.2 Crear Repositorio en GitHub

1. Ir a https://github.com/new
2. **Nombre del repositorio:** `tennis-ao26-streamlit`
3. **Descripción:** "Tennis Match Duration Prediction - Interactive Streamlit App (4th Delivery)"
4. **Visibilidad:** Public
5. **NO** inicializar con README (ya lo tenemos)
6. Click en "Create repository"

### 1.3 Conectar Repositorio Local con GitHub

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/tennis-ao26-streamlit.git

# Renombrar rama principal a main (si es necesario)
git branch -M main

# Hacer push inicial
git push -u origin main
```

> **Nota:** Reemplazar `TU_USUARIO` con tu nombre de usuario de GitHub

---

## 🔧 PASO 2: CONFIGURAR ARCHIVO DE CONFIGURACIÓN STREAMLIT

### 2.1 Crear directorio `.streamlit`

```bash
mkdir -p .streamlit
touch .streamlit/config.toml
```

### 2.2 Contenido de `.streamlit/config.toml`

```toml
# Config para Streamlit Cloud
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"

[server]
port = 8501
headless = true
runOnSave = true
maxUploadSize = 200
```

---

## 🌐 PASO 3: DESPLEGAR EN STREAMLIT CLOUD

### 3.1 Acceder a Streamlit Cloud

1. Ir a https://share.streamlit.io/
2. Click en "New app"

### 3.2 Configurar la Aplicación

**Campos a completar:**

| Campo | Valor |
|-------|-------|
| **GitHub repository** | `https://github.com/TU_USUARIO/tennis-ao26-streamlit` |
| **Branch** | `main` |
| **Main file path** | `tennis_app.py` |
| **App URL** | (Auto-generada) |

### 3.3 Configuración Avanzada (Opcional)

1. Click en "Advanced settings"
2. **Secrets:** Si la app requiere variables de ambiente:

```toml
[secrets]
db_password = "tu_contraseña"
api_key = "tu_api_key"
```

3. **Python version:** 3.11
4. Click en "Deploy"

### 3.4 Monitoreo de Despliegue

- ✅ Verde: Despliegue exitoso
- 🟡 Amarillo: En proceso
- 🔴 Rojo: Error en despliegue

Verificar logs en caso de error.

---

## ✅ PASO 4: VALIDAR LA APLICACIÓN

### 4.1 Acceso a la App

```
URL pública: https://share.streamlit.io/TU_USUARIO/tennis-ao26-streamlit
```

### 4.2 Testing Funcional

**Pruebas a realizar:**

- [ ] **Dashboard Principal**
  - ✅ Métricas se cargan correctamente
  - ✅ Gráficos de predicciones vs realidad funcionan
  - ✅ Distribución de errores se visualiza

- [ ] **Exploración Interactiva**
  - ✅ Filtros funcionan correctamente
  - ✅ Gráficos Altair responden a la selección
  - ✅ Estadísticas se actualizan con filtros

- [ ] **Predictor Interactivo**
  - ✅ Inputs aceptan valores correctamente
  - ✅ Botón "Predecir" genera predicción
  - ✅ Medidor gauge se visualiza correctamente
  - ✅ Explicación de factores aparece

- [ ] **Análisis Avanzado**
  - ✅ Q-Q plot de residuos se carga
  - ✅ Feature importance se muestra
  - ✅ Matriz de confusión se visualiza
  - ✅ Insights se listan correctamente

### 4.3 Performance

```bash
# Tiempo de carga esperado: < 5 segundos (primera vez)
# Tiempo de actualizacion: < 2 segundos (filtros/predicciones)
```

---

## 📝 PASO 5: ACTUALIZAR DOCUMENTACIÓN

### 5.1 README.md (actualizar con link de Streamlit)

```markdown
## 🌐 Acceso a la Aplicación

La aplicación está disponible en:
👉 **[Tennis Match Duration Predictor en Streamlit Cloud](https://share.streamlit.io/TU_USUARIO/tennis-ao26-streamlit)**

### Instrucciones de Uso

1. **Dashboard Principal:** Revisa métricas y performance general
2. **Exploración Interactiva:** Filtra datos y explora patrones
3. **Predictor:** Ingresa características de un partido para predicción
4. **Análisis Avanzado:** Analiza residuos e importancia de features
```

### 5.2 Requirements.txt (Verificar dependencias)

```bash
# Instalar localmente para verificar
pip install -r requirements.txt

# Listar versiones exactas
pip freeze > requirements_exact.txt
```

---

## 🔄 PASO 6: ACTUALIZAR LA APLICACIÓN

### 6.1 Flujo de Actualización

```bash
# 1. Hacer cambios locales en tennis_app.py

# 2. Probar localmente
streamlit run tennis_app.py

# 3. Hacer commit
git add .
git commit -m "Descripción del cambio: [feature/fix/improvement]"

# 4. Push a GitHub
git push origin main

# 5. Streamlit Cloud se actualiza automáticamente (2-3 minutos)
```

### 6.2 Actualizar Datos o Modelos

```bash
# Si actualizas data_for_streamlit.csv o metrics_summary.json
git add data_for_streamlit.csv metrics_summary.json
git commit -m "Update training data and metrics"
git push origin main

# La app se recargará automáticamente
```

---

## 🐛 TROUBLESHOOTING

### Problema: "ModuleNotFoundError"

**Solución:**
```bash
# 1. Verificar requirements.txt en root
# 2. Asegurar que todas las dependencias estén listadas
# 3. Push a GitHub
git add requirements.txt
git commit -m "Fix: Update requirements"
git push origin main
```

### Problema: "FileNotFoundError: data_for_streamlit.csv"

**Solución:**
```bash
# 1. Asegurar archivo está en root del repositorio
# 2. Verificar nombre exacto (case-sensitive)
# 3. Hacer push
git add data_for_streamlit.csv
git push origin main
```

### Problema: App tarda más de 10 segundos en cargar

**Optimizaciones:**
```python
# Usar @st.cache_data para datos estáticos
@st.cache_data
def load_data():
    return pd.read_csv('data_for_streamlit.csv')

# Usar @st.cache_resource para objetos pesados
@st.cache_resource
def load_model():
    return pickle.load(open('model.pkl', 'rb'))
```

### Problema: App se reinicia constantemente

**Soluciones:**
1. Revisar logs en Streamlit Cloud
2. Verificar that no hay inputs sin valores por defecto
3. Revisar `requirements.txt` por versiones incompatibles

---

## 📊 MONITOREO Y MANTENIMIENTO

### Checks Periódicos

```markdown
- [ ] Cada semana: Verificar que la app sigue cargando
- [ ] Cada mes: Revisar logs de errores en Streamlit Cloud
- [ ] Antes de presentación: Hacer prueba completa funcional
```

### Actualizar Versiones de Dependencias

```bash
# Verificar actualizaciones disponibles
pip list --outdated

# Actualizar dependencias de forma segura
pip install --upgrade streamlit altair plotly scikit-learn
pip freeze > requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

---

## 🎬 PARA LA PRESENTACIÓN ORAL (12/11 y 19/11)

### Demostración en Vivo

**Preparación:**
1. ✅ Verificar conexión a internet
2. ✅ Tener URL lista: `https://share.streamlit.io/TU_USUARIO/tennis-ao26-streamlit`
3. ✅ Hacer prueba de funcionamiento 1 hora antes
4. ✅ Tener PowerPoint con explicación de cada sección

**Demostración:**
1. **Dashboard (1 min):**
   - Mostrar métricas principales
   - Explicar predicciones vs realidad

2. **Exploración (1.5 min):**
   - Aplicar filtros
   - Mostrar interactividad con Altair
   - Resaltar insights

3. **Predictor (1 min):**
   - Ingresar ejemplo de partido real
   - Mostrar predicción
   - Explicar factores

4. **Análisis Avanzado (1 min):**
   - Mostrar análisis de residuos
   - Destacar feature importance
   - Interpretar matriz de confusión

**Total: ~4-5 minutos de demostración en vivo**

---

## 📞 SOPORTE

Para problemas con Streamlit Cloud:
- 📖 Documentación: https://docs.streamlit.io/
- 🆘 Comunidad: https://discuss.streamlit.io/
- 🐛 Issues: https://github.com/streamlit/streamlit/issues

---

## 🎉 ¡LISTO PARA DESPLEGAR!

Todos los archivos necesarios están creados. Solo falta:

1. ✅ Crear repositorio en GitHub
2. ✅ Hacer push inicial
3. ✅ Conectar con Streamlit Cloud
4. ✅ Validar funcionamiento
5. ✅ Preparar para presentación

**Estado:** 🟢 LISTO PARA PRODUCCIÓN

---

**Última actualización:** 4 de Noviembre de 2025
**Autor:** Juan Ignacio Barranco Bastan
**Proyecto:** Tennis Match Duration Prediction - 4ta Entrega
