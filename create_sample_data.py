import json
import pandas as pd
import numpy as np

def create_sample_data():
    """Crear datos de ejemplo para la aplicación Streamlit"""
    np.random.seed(42)
    n_samples = 500
    
    # Generar datos realistas
    surfaces = ['Hard', 'Clay', 'Grass']
    levels = ['G', 'M', 'A', 'C']
    rounds = ['1st Round', '2nd Round', '3rd Round', 'QF', 'SF', 'F']
    
    df = pd.DataFrame({
        'duracion_real': np.random.gamma(2, 60),  # Distribución más realista
        'superficie': np.random.choice(surfaces, n_samples, p=[0.6, 0.3, 0.1]),
        'nivel_torneo': np.random.choice(levels, n_samples, p=[0.1, 0.2, 0.5, 0.2]),
        'ronda': np.random.choice(rounds, n_samples),
        'mejor_de': np.random.choice([3, 5], n_samples, p=[0.8, 0.2]),
        'rank_diff': np.random.exponential(20),
        'is_grand_slam': np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
    })
    
    # Ajustar duración según características
    df.loc[df['superficie'] == 'Clay', 'duracion_real'] *= 1.15
    df.loc[df['superficie'] == 'Grass', 'duracion_real'] *= 0.9
    df.loc[df['nivel_torneo'] == 'G', 'duracion_real'] *= 1.2
    df.loc[df['mejor_de'] == 5, 'duracion_real'] += 40
    df.loc[df['rank_diff'] < 10, 'duracion_real'] *= 1.1
    
    # Crear predicciones realistas (con ruido)
    df['duracion_predicha'] = df['duracion_real'] + np.random.normal(0, 15, n_samples)
    df['duracion_predicha'] = np.maximum(df['duracion_predicha'], 60)  # Mínimo 60 min
    
    # Crear categorías
    def categorize_duration(duration):
        if duration < 100:
            return 'CORTO'
        elif duration < 150:
            return 'MEDIO'
        else:
            return 'LARGO'
    
    df['categoria_real'] = df['duracion_real'].apply(categorize_duration)
    df['categoria_predicha'] = df['duracion_predicha'].apply(categorize_duration)
    
    # Añadir algo de error a las categorías predichas
    wrong_predictions = np.random.choice(df.index, size=int(0.3 * len(df)), replace=False)
    categories = ['CORTO', 'MEDIO', 'LARGO']
    for idx in wrong_predictions:
        current_cat = df.loc[idx, 'categoria_predicha']
        other_cats = [c for c in categories if c != current_cat]
        df.loc[idx, 'categoria_predicha'] = np.random.choice(other_cats)
    
    # Redondear valores
    df['duracion_real'] = df['duracion_real'].round(1)
    df['duracion_predicha'] = df['duracion_predicha'].round(1)
    df['rank_diff'] = df['rank_diff'].round(0).astype(int)
    
    return df

def create_metrics():
    """Crear métricas de ejemplo"""
    df = create_sample_data()
    
    # Calcular métricas reales
    rmse = np.sqrt(np.mean((df['duracion_real'] - df['duracion_predicha'])**2))
    r2 = 1 - (np.sum((df['duracion_real'] - df['duracion_predicha'])**2) / 
              np.sum((df['duracion_real'] - df['duracion_real'].mean())**2))
    accuracy = (df['categoria_real'] == df['categoria_predicha']).mean()
    mae = np.mean(np.abs(df['duracion_real'] - df['duracion_predicha']))
    
    return {
        'rmse': float(rmse),
        'r2': float(r2),
        'accuracy': float(accuracy),
        'mae': float(mae),
        'total_matches': len(df)
    }

if __name__ == "__main__":
    # Crear y guardar datos de ejemplo
    df = create_sample_data()
    metrics = create_metrics()
    
    # Guardar archivos
    df.to_csv('data_for_streamlit.csv', index=False)
    
    with open('metrics_summary.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("✅ Datos de ejemplo creados:")
    print(f"   - data_for_streamlit.csv ({len(df)} registros)")
    print(f"   - metrics_summary.json")
    print(f"   - RMSE: {metrics['rmse']:.2f} min")
    print(f"   - R²: {metrics['r2']:.4f}")
    print(f"   - Accuracy: {metrics['accuracy']:.4f}")
    print("\n📊 Primeras filas del dataset:")
    print(df.head())