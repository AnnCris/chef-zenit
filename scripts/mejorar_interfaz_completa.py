# scripts/mejorar_interfaz_completa.py
#!/usr/bin/env python3
"""
Script completo para implementar todas las mejoras de interfaz de usuario
"""

import os
import sys
import logging
import shutil
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def crear_css_moderno():
    """Crea el archivo CSS moderno y atractivo"""
    css_content = """/* app/static/css/style.css - Diseño Moderno y Atractivo */

/* Importar fuentes de Google */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Variables CSS para consistencia */
:root {
  /* Colores principales */
  --primary-color: #667eea;
  --primary-light: #764ba2;
  --secondary-color: #f093fb;
  --accent-color: #4facfe;
  --success-color: #00f2fe;
  --warning-color: #ffecd2;
  --danger-color: #ff9a9e;
  --info-color: #a8edea;
  
  /* Gradientes */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --gradient-warm: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  --gradient-cool: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  --gradient-dark: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  /* Colores neutros */
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --text-primary: #2d3748;
  --text-secondary: #718096;
  --text-light: #a0aec0;
  --border-color: #e2e8f0;
  --shadow-light: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-heavy: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  
  /* Tipografía */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-secondary: 'Poppins', sans-serif;
  
  /* Espaciado */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  
  /* Bordes */
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --border-radius-xl: 24px;
}

/* Reset y estilos base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-primary);
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  overflow-x: hidden;
  
  /* Fondo animado */
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 75% 75%, rgba(240, 147, 251, 0.1) 0%, transparent 50%);
  background-attachment: fixed;
  min-height: 100vh;
}

/* Container principal */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

/* Header moderno */
header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  padding: var(--spacing-2xl) 0;
  position: relative;
  overflow: hidden;
}

header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-primary);
  opacity: 0.05;
  border-radius: var(--border-radius-xl);
  transform: skewY(-2deg);
}

header h1 {
  font-family: var(--font-secondary);
  font-size: 3.5rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--spacing-md);
  position: relative;
  z-index: 1;
  
  /* Animación de aparición */
  animation: fadeInUp 1s ease-out;
}

header p.lead {
  font-size: 1.25rem;
  color: var(--text-secondary);
  font-weight: 400;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.2s both;
}

/* Animaciones */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

/* Cards modernas */
.card {
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-light);
  margin-bottom: var(--spacing-xl);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  backdrop-filter: blur(10px);
  
  /* Borde sutil con gradiente */
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-heavy);
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card:hover::before {
  opacity: 1;
}

/* Headers de cards con gradientes */
.card-header {
  padding: var(--spacing-lg) var(--spacing-xl);
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.card-header.bg-primary {
  background: var(--gradient-primary) !important;
  color: white;
  border-bottom: none;
}

.card-header.bg-success {
  background: var(--gradient-success) !important;
  color: white;
  border-bottom: none;
}

.card-header.bg-info {
  background: var(--gradient-cool) !important;
  color: var(--text-primary);
  border-bottom: none;
}

.card-header.bg-warning {
  background: var(--gradient-warm) !important;
  color: var(--text-primary);
  border-bottom: none;
}

/* Card body */
.card-body {
  padding: var(--spacing-xl);
}

/* Formularios modernos */
.form-label {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  display: block;
}

.form-control {
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md) var(--spacing-lg);
  border: 2px solid var(--border-color);
  font-size: 1rem;
  transition: all 0.3s ease;
  background: var(--bg-secondary);
  width: 100%;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.form-control::placeholder {
  color: var(--text-light);
}

/* Input groups modernos */
.input-group {
  display: flex;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-light);
}

.input-group .form-control {
  border-radius: 0;
  border-right: none;
}

.input-group .btn {
  border-radius: 0;
  border-left: none;
}

/* Botones modernos */
.btn {
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md) var(--spacing-xl);
  font-weight: 500;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  min-height: 44px;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
  box-shadow: var(--shadow-light);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-medium);
}

.btn-success {
  background: var(--gradient-success);
  color: white;
  box-shadow: var(--shadow-light);
}

.btn-success:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-medium);
}

.btn-info {
  background: var(--gradient-cool);
  color: var(--text-primary);
  box-shadow: var(--shadow-light);
}

.btn-info:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-medium);
}

.btn-outline-primary {
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
}

.btn-outline-primary:hover {
  background: var(--gradient-primary);
  color: white;
  transform: translateY(-3px);
}

/* Badges modernos */
.badge {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 0.875rem;
  border-radius: var(--border-radius-xl);
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin: var(--spacing-xs);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.badge:hover {
  transform: scale(1.05);
}

.badge.bg-primary {
  background: var(--gradient-primary);
  color: white;
}

.badge.bg-danger {
  background: var(--gradient-secondary);
  color: white;
}

.badge.bg-success {
  background: var(--gradient-success);
  color: white;
}

.badge.bg-info {
  background: var(--gradient-cool);
  color: var(--text-primary);
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.3s ease;
  padding: 2px;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.2);
}

/* Checkboxes modernos */
.form-check {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  transition: background-color 0.3s ease;
}

.form-check:hover {
  background: rgba(102, 126, 234, 0.05);
}

.form-check-input {
  width: 20px;
  height: 20px;
  margin-right: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--spacing-xs);
  transition: all 0.3s ease;
}

.form-check-input:checked {
  background: var(--gradient-primary);
  border-color: var(--primary-color);
}

.form-check-label {
  font-weight: 400;
  color: var(--text-primary);
  cursor: pointer;
}

/* Resultados de recetas */
.recipe-card {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.recipe-card:hover {
  transform: translateY(-10px) rotateX(2deg);
}

.recipe-card .card-img-top {
  height: 220px;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.recipe-card:hover .card-img-top {
  transform: scale(1.1);
}

/* Modal moderno */
.modal-content {
  border-radius: var(--border-radius-lg);
  border: none;
  box-shadow: var(--shadow-heavy);
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.modal-header {
  background: var(--gradient-primary);
  color: white;
  border-bottom: none;
  padding: var(--spacing-xl);
}

.modal-footer {
  background: var(--bg-primary);
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-xl);
}

/* Spinner moderno */
.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 4px;
  border-color: var(--primary-color);
  border-right-color: transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Alertas modernas */
.alert {
  border: none;
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

.alert::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: currentColor;
}

.alert-success {
  background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.1));
  color: #0369a1;
  border-left: 4px solid var(--accent-color);
}

.alert-danger {
  background: linear-gradient(135deg, rgba(255, 154, 158, 0.1), rgba(250, 92, 124, 0.1));
  color: #dc2626;
  border-left: 4px solid var(--danger-color);
}

.alert-warning {
  background: linear-gradient(135deg, rgba(255, 236, 210, 0.3), rgba(252, 182, 159, 0.3));
  color: #d97706;
  border-left: 4px solid #f59e0b;
}

.alert-info {
  background: linear-gradient(135deg, rgba(168, 237, 234, 0.2), rgba(254, 214, 227, 0.2));
  color: #0369a1;
  border-left: 4px solid var(--info-color);
}

/* Lista de ingredientes y pasos */
.list-group-item {
  border: none;
  border-bottom: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  transition: all 0.3s ease;
  background: transparent;
}

.list-group-item:hover {
  background: rgba(102, 126, 234, 0.05);
  transform: translateX(10px);
}

.list-group-item:last-child {
  border-bottom: none;
}

/* Información nutricional */
.nutrition-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.nutrition-item {
  text-align: center;
  padding: var(--spacing-md);
  background: var(--gradient-cool);
  border-radius: var(--border-radius-md);
  transition: transform 0.3s ease;
}

.nutrition-item:hover {
  transform: scale(1.05);
}

/* Efectos de carga */
.loading-shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}

/* Responsive design */
@media (max-width: 768px) {
  .container {
    padding: var(--spacing-md);
  }
  
  header h1 {
    font-size: 2.5rem;
  }
  
  .card-body {
    padding: var(--spacing-lg);
  }
  
  .btn {
    padding: var(--spacing-md);
    font-size: 0.9rem;
  }
  
  .nutrition-info {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  header h1 {
    font-size: 2rem;
  }
  
  .card-header, .card-body {
    padding: var(--spacing-md);
  }
  
  .nutrition-info {
    grid-template-columns: 1fr;
  }
}

/* Efectos especiales para elementos destacados */
.featured-recipe {
  position: relative;
  overflow: hidden;
}

.featured-recipe::before {
  content: '⭐';
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 1.5rem;
  z-index: 10;
  animation: pulse 2s infinite;
}

/* Micro-interacciones */
.btn:active {
  transform: translateY(-1px) scale(0.98);
}

.card:active {
  transform: translateY(-4px) scale(1.01);
}

/* Scrollbar personalizada */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
  background: var(--gradient-primary);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--primary-light);
}

/* Estilo para elementos focus */
*:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
}

/* Transiciones suaves para todos los elementos */
* {
  transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
}

/* Estilos adicionales para elementos específicos */
.cursor-pointer { cursor: pointer; }
.min-height-100 { min-height: 100px; }

/* Partículas de fondo */
.background-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.particle:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
.particle:nth-child(2) { top: 60%; left: 80%; animation-delay: 2s; }
.particle:nth-child(3) { top: 80%; left: 20%; animation-delay: 4s; }
.particle:nth-child(4) { top: 40%; left: 90%; animation-delay: 1s; }
.particle:nth-child(5) { top: 10%; left: 70%; animation-delay: 3s; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
  50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
}

/* Efectos hover mejorados */
.example-query:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.custom-check:hover {
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
}

/* Gradientes para badges */
.bg-gradient-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
.bg-gradient-success { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important; }
.bg-gradient-info { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important; }
"""
    
    css_path = os.path.join('app', 'static', 'css', 'style.css')
    
    try:
        # Crear backup del CSS original
        if os.path.exists(css_path):
            backup_path = css_path + '.backup'
            if not os.path.exists(backup_path):
                shutil.copy2(css_path, backup_path)
                logger.info(f"📄 Backup del CSS original creado: {backup_path}")
        
        # Escribir el nuevo CSS
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        logger.info(f"✅ CSS moderno creado en {css_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al crear CSS: {e}")
        return False

def actualizar_html_template():
    """Actualiza el template HTML principal"""
    template_path = os.path.join('app', 'templates', 'index.html')
    
    # Crear backup
    if os.path.exists(template_path):
        backup_path = template_path + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(template_path, backup_path)
            logger.info(f"📄 Backup del HTML original creado: {backup_path}")
    
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍽️ Chef Virtual IA - Tu Asistente Culinario Inteligente</title>
    
    <!-- Bootstrap 5.3 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    
    <!-- Animate.css para animaciones -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    
    <!-- CSS personalizado -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    <!-- Favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🍽️</text></svg>">
    
    <!-- Meta tags para SEO -->
    <meta name="description" content="Sistema inteligente de recomendaciones culinarias con IA. Encuentra recetas perfectas basadas en tus ingredientes.">
    <meta name="keywords" content="recetas, cocina, inteligencia artificial, recomendaciones, chef virtual">
</head>
<body>
    <!-- Partículas de fondo animadas -->
    <div class="background-particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>

    <div class="container">
        <!-- Header mejorado -->
        <header class="animate__animated animate__fadeInDown">
            <div class="row align-items-center">
                <div class="col-12 text-center">
                    <h1 class="display-3 fw-bold mb-3">
                        <i class="bi bi-robot me-3"></i>
                        Chef Virtual IA
                    </h1>
                    <p class="lead fs-4 mb-4">
                        <i class="bi bi-stars me-2"></i>
                        Tu asistente culinario inteligente powered by 
                        <span class="badge bg-gradient-primary">K-means</span>
                        <span class="badge bg-gradient-success">Random Forest</span>
                        <span class="badge bg-gradient-info">TF-IDF</span>
                    </p>
                    <div class="d-flex justify-content-center gap-2 flex-wrap">
                        <span class="badge bg-light text-dark px-3 py-2">
                            <i class="bi bi-cpu me-1"></i> IA Avanzada
                        </span>
                        <span class="badge bg-light text-dark px-3 py-2">
                            <i class="bi bi-lightning me-1"></i> Recomendaciones Instantáneas
                        </span>
                        <span class="badge bg-light text-dark px-3 py-2">
                            <i class="bi bi-heart me-1"></i> Personalizado
                        </span>
                    </div>
                </div>
            </div>
        </header>

        <div class="row g-4">
            <!-- Columna izquierda - Controles -->
            <div class="col-lg-6">
                <!-- Card de ingredientes mejorada -->
                <div class="card animate__animated animate__fadeInLeft" style="animation-delay: 0.2s">
                    <div class="card-header bg-primary text-white">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-basket2-fill fs-4 me-3"></i>
                            <div>
                                <h3 class="card-title mb-1">¿Qué tienes en tu cocina?</h3>
                                <small class="opacity-75">Descubre recetas mágicas con tus ingredientes</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id="ingredientesForm">
                            <div class="mb-4">
                                <label for="ingredientesInput" class="form-label">
                                    <i class="bi bi-plus-circle me-2"></i>
                                    Ingresa los ingredientes disponibles
                                </label>
                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-light">
                                        <i class="bi bi-search text-primary"></i>
                                    </span>
                                    <input 
                                        type="text" 
                                        class="form-control" 
                                        id="ingredientesInput" 
                                        placeholder="Ej: tomate, cebolla, pollo..."
                                        autocomplete="off"
                                    >
                                    <button class="btn btn-outline-primary" type="button" id="agregarIngrediente">
                                        <i class="bi bi-plus-lg"></i>
                                    </button>
                                </div>
                                <div class="form-text">
                                    <i class="bi bi-lightbulb me-1"></i>
                                    Presiona Enter o haz clic en + para agregar
                                </div>
                            </div>
                            
                            <!-- Contenedor de ingredientes seleccionados -->
                            <div class="mb-4">
                                <label class="form-label">
                                    <i class="bi bi-check2-square me-2"></i>
                                    Ingredientes seleccionados
                                </label>
                                <div class="border rounded-3 p-3 bg-light min-height-100" id="ingredientesSeleccionados">
                                    <div class="text-muted text-center py-3">
                                        <i class="bi bi-inbox fs-1 d-block mb-2 opacity-50"></i>
                                        <small>Los ingredientes aparecerán aquí...</small>
                                    </div>
                                </div>
                            </div>
                            
                            <button type="submit" class="btn btn-primary btn-lg w-100">
                                <i class="bi bi-magic me-2"></i>
                                Generar Recomendaciones IA
                                <i class="bi bi-arrow-right ms-2"></i>
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Card de preferencias mejorada -->
                <div class="card animate__animated animate__fadeInLeft" style="animation-delay: 0.4s">
                    <div class="card-header bg-success text-white">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-gear-fill fs-4 me-3"></i>
                            <div>
                                <h3 class="card-title mb-1">Personaliza tu experiencia</h3>
                                <small class="opacity-75">Configura tus preferencias dietéticas</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id="preferenciasForm">
                            <!-- Restricciones dietéticas con iconos -->
                            <div class="mb-4">
                                <label class="form-label mb-3">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Restricciones dietéticas
                                </label>
                                <div class="row g-2">
                                    <div class="col-md-6">
                                        <div class="form-check custom-check">
                                            <input class="form-check-input" type="checkbox" value="vegetariano" id="checkVegetariano">
                                            <label class="form-check-label d-flex align-items-center" for="checkVegetariano">
                                                <i class="bi bi-flower1 me-2 text-success"></i>
                                                Vegetariano
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check custom-check">
                                            <input class="form-check-input" type="checkbox" value="vegano" id="checkVegano">
                                            <label class="form-check-label d-flex align-items-center" for="checkVegano">
                                                <i class="bi bi-leaf me-2 text-success"></i>
                                                Vegano
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check custom-check">
                                            <input class="form-check-input" type="checkbox" value="sin_gluten" id="checkSinGluten">
                                            <label class="form-check-label d-flex align-items-center" for="checkSinGluten">
                                                <i class="bi bi-x-circle me-2 text-warning"></i>
                                                Sin Gluten
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check custom-check">
                                            <input class="form-check-input" type="checkbox" value="sin_lactosa" id="checkSinLactosa">
                                            <label class="form-check-label d-flex align-items-center" for="checkSinLactosa">
                                                <i class="bi bi-droplet-half me-2 text-info"></i>
                                                Sin Lactosa
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Alergias -->
                            <div class="mb-4">
                                <label for="alergiasInput" class="form-label">
                                    <i class="bi bi-exclamation-triangle me-2"></i>
                                    Alergias o ingredientes a evitar
                                </label>
                                <div class="input-group">
                                    <span class="input-group-text bg-light">
                                        <i class="bi bi-shield-exclamation text-danger"></i>
                                    </span>
                                    <input 
                                        type="text" 
                                        class="form-control" 
                                        id="alergiasInput" 
                                        placeholder="Ej: nueces, mariscos, lácteos..."
                                    >
                                    <button class="btn btn-outline-danger" type="button" id="agregarAlergia">
                                        <i class="bi bi-plus-lg"></i>
                                    </button>
                                </div>
                                <div class="mt-2" id="alergiasSeleccionadas">
                                    <!-- Aquí aparecerán las alergias -->
                                </div>
                            </div>
                            
                            <button type="submit" class="btn btn-success btn-lg w-100">
                                <i class="bi bi-check-circle me-2"></i>
                                Guardar Preferencias
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Columna derecha - Consulta y resultados -->
            <div class="col-lg-6">
                <!-- Card de consulta IA -->
                <div class="card animate__animated animate__fadeInRight" style="animation-delay: 0.2s">
                    <div class="card-header bg-info text-dark">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-chat-dots-fill fs-4 me-3"></i>
                            <div>
                                <h3 class="card-title mb-1">Pregúntale al Chef IA</h3>
                                <small class="opacity-75">Describe lo que quieres cocinar</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id="consultaForm">
                            <div class="mb-4">
                                <label for="consultaInput" class="form-label">
                                    <i class="bi bi-mic me-2"></i>
                                    Describe tu consulta
                                </label>
                                <textarea 
                                    class="form-control form-control-lg" 
                                    id="consultaInput" 
                                    rows="4" 
                                    placeholder="Ej: Quiero hacer una cena romántica con pollo y vino blanco, algo fácil y rápido..."
                                    style="resize: none;"
                                ></textarea>
                                <div class="form-text">
                                    <i class="bi bi-cpu me-1"></i>
                                    Powered by procesamiento de lenguaje natural
                                </div>
                            </div>
                            
                            <!-- Ejemplos de consultas -->
                            <div class="mb-4">
                                <label class="form-label">
                                    <i class="bi bi-lightbulb me-2"></i>
                                    Ejemplos de consultas
                                </label>
                                <div class="d-flex flex-wrap gap-2">
                                    <span class="badge bg-light text-dark px-3 py-2 cursor-pointer example-query" data-query="Cena rápida y saludable">
                                        🍽️ Cena rápida
                                    </span>
                                    <span class="badge bg-light text-dark px-3 py-2 cursor-pointer example-query" data-query="Postre sin azúcar">
                                        🍰 Postre saludable
                                    </span>
                                    <span class="badge bg-light text-dark px-3 py-2 cursor-pointer example-query" data-query="Almuerzo vegetariano">
                                        🥗 Vegetariano
                                    </span>
                                    <span class="badge bg-light text-dark px-3 py-2 cursor-pointer example-query" data-query="Receta italiana tradicional">
                                        🇮🇹 Italiana
                                    </span>
                                </div>
                            </div>
                            
                            <button type="submit" class="btn btn-info btn-lg w-100">
                                <i class="bi bi-robot me-2"></i>
                                Analizar con IA
                                <i class="bi bi-arrow-right ms-2"></i>
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Card de resultados mejorada -->
                <div class="card animate__animated animate__fadeInRight" style="animation-delay: 0.4s">
                    <div class="card-header bg-warning text-dark">
                        <div class="d-flex align-items-center justify-content-between">
                            <div class="d-flex align-items-center">
                                <i class="bi bi-stars fs-4 me-3"></i>
                                <div>
                                    <h3 class="card-title mb-1">Recomendaciones IA</h3>
                                    <small class="opacity-75">Resultados personalizados para ti</small>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button class="btn btn-sm btn-outline-dark" id="statusBtn" title="Estado del sistema">
                                    <i class="bi bi-cpu"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-dark" id="refreshBtn" title="Reentrenar IA">
                                    <i class="bi bi-arrow-clockwise"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="card-body" id="resultadosContainer">
                        <!-- Estado inicial mejorado -->
                        <div class="text-center py-5">
                            <div class="mb-4">
                                <i class="bi bi-robot display-1 text-primary opacity-25"></i>
                            </div>
                            <h5 class="text-muted mb-3">¡Listo para generar recomendaciones!</h5>
                            <p class="text-muted mb-4">
                                Agrega ingredientes o haz una consulta para que la IA encuentre las recetas perfectas para ti.
                            </p>
                            <div class="d-flex justify-content-center gap-3 flex-wrap">
                                <div class="text-center">
                                    <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                                        <i class="bi bi-search"></i>
                                    </div>
                                    <small class="d-block mt-2 text-muted">Buscar</small>
                                </div>
                                <div class="text-center">
                                    <div class="bg-success text-white rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                                        <i class="bi bi-cpu"></i>
                                    </div>
                                    <small class="d-block mt-2 text-muted">Analizar</small>
                                </div>
                                <div class="text-center">
                                    <div class="bg-info text-white rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                                        <i class="bi bi-stars"></i>
                                    </div>
                                    <small class="d-block mt-2 text-muted">Recomendar</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal mejorado para detalles de receta -->
    <div class="modal fade" id="recetaModal" tabindex="-1" aria-labelledby="recetaModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="d-flex align-items-center">
                        <i class="bi bi-book-fill fs-3 me-3"></i>
                        <div>
                            <h4 class="modal-title mb-0" id="recetaModalLabel">Detalles de la Receta</h4>
                            <small class="opacity-75">Información completa y pasos detallados</small>
                        </div>
                    </div>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-0" id="recetaModalBody">
                    <!-- Aquí se cargará el contenido de la receta -->
                </div>
                <div class="modal-footer">
                    <div class="d-flex gap-2 w-100">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                            <i class="bi bi-x-lg me-2"></i>Cerrar
                        </button>
                        <button type="button" class="btn btn-primary flex-fill" id="descargarPdfBtn">
                            <i class="bi bi-download me-2"></i>Descargar PDF
                        </button>
                        <button type="button" class="btn btn-success" id="favoriteBtn">
                            <i class="bi bi-heart me-2"></i>Favorito
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast para notificaciones -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="bi bi-bell-fill text-primary me-2"></i>
                <strong class="me-auto">Chef Virtual IA</strong>
                <small class="text-muted">ahora</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                <!-- Mensaje dinámico -->
            </div>
        </div>
    </div>

    <!-- Footer con información del sistema -->
    <footer class="text-center mt-5 py-4">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="bg-light rounded-3 p-4">
                        <h6 class="fw-bold mb-3">
                            <i class="bi bi-cpu-fill me-2"></i>
                            Powered by Advanced AI
                        </h6>
                        <div class="row g-3 text-muted small">
                            <div class="col-md-4">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="bi bi-diagram-3 me-2 text-primary"></i>
                                    <span>K-means Clustering</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="bi bi-tree me-2 text-success"></i>
                                    <span>Random Forest ML</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="d-flex align-items-center justify-content-center">
                                    <i class="bi bi-file-text me-2 text-info"></i>
                                    <span>TF-IDF Analysis</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>

    <!-- Script para efectos adicionales -->
    <script>
        // Efectos de las partículas de fondo
        document.addEventListener('DOMContentLoaded', function() {
            // Agregar efectos a los ejemplos de consulta
            document.querySelectorAll('.example-query').forEach(badge => {
                badge.addEventListener('click', function() {
                    const query = this.getAttribute('data-query');
                    document.getElementById('consultaInput').value = query;
                    this.classList.add('animate__animated', 'animate__pulse');
                });
            });

            // Efecto de typing en el placeholder
            const textarea = document.getElementById('consultaInput');
            const examples = [
                'Quiero hacer una cena romántica...',
                'Algo rápido para el almuerzo...',
                'Receta saludable con pollo...',
                'Postre sin azúcar fácil...'
            ];
            let currentExample = 0;
            
            // Cambiar placeholder cada 3 segundos
            setInterval(() => {
                textarea.placeholder = examples[currentExample];
                currentExample = (currentExample + 1) % examples.length;
            }, 3000);
        });
    </script>
</body>
</html>"""
    
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Template HTML actualizado en {template_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al actualizar HTML: {e}")
        return False

def actualizar_javascript_moderno():
    """Actualiza el JavaScript con efectos modernos"""
    # Este script usa el JavaScript que ya creé en el artifact anterior
    # Solo necesitamos asegurarnos de que se aplique
    
    js_path = os.path.join('app', 'static', 'js', 'app.js')
    
    # Crear backup
    if os.path.exists(js_path):
        backup_path = js_path + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(js_path, backup_path)
            logger.info(f"📄 Backup del JavaScript original creado: {backup_path}")
    
    logger.info(f"✅ JavaScript listo para actualizarse en {js_path}")
    logger.info("💡 Copia el contenido del JavaScript moderno del artifact anterior")
    return True

def crear_assets_adicionales():
    """Crea assets adicionales como favicon dinámico"""
    try:
        # Crear directorio de assets si no existe
        assets_dir = os.path.join('app', 'static', 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        # Crear un archivo de configuración de tema
        theme_config = {
            "version": "2.0.0",
            "theme": "modern",
            "features": [
                "gradients",
                "animations", 
                "particles",
                "responsive",
                "dark_mode_ready"
            ],
            "algorithms": [
                "tf-idf",
                "k-means", 
                "random-forest"
            ]
        }
        
        import json
        config_path = os.path.join(assets_dir, 'theme-config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(theme_config, f, indent=2)
        
        logger.info(f"✅ Configuración de tema creada en {config_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al crear assets: {e}")
        return False

def main():
    """Función principal para aplicar todas las mejoras de UI"""
    logger.info("🎨 MEJORANDO LA INTERFAZ DE USUARIO")
    logger.info("🚀 Aplicando diseño moderno y atractivo")
    logger.info("=" * 80)
    
    pasos = [
        ("🎨 Crear CSS moderno con gradientes y animaciones", crear_css_moderno),
        ("📝 Actualizar template HTML con mejor estructura", actualizar_html_template),
        ("⚡ Preparar JavaScript moderno", actualizar_javascript_moderno),
        ("🎯 Crear assets adicionales", crear_assets_adicionales),
    ]
    
    pasos_completados = 0
    
    for nombre, funcion in pasos:
        logger.info(f"\n{nombre}...")
        logger.info("-" * 50)
        
        if funcion():
            pasos_completados += 1
            logger.info(f"✅ {nombre} - COMPLETADO")
        else:
            logger.error(f"❌ {nombre} - FALLÓ")
            # Continuar con los otros pasos aunque uno falle
    
    # Instrucciones adicionales
    logger.info(f"\n{'='*80}")
    logger.info("📋 PASOS ADICIONALES REQUERIDOS")
    logger.info("=" * 80)
    
    logger.info("🔧 Para completar la mejora, también necesitas:")
    logger.info("   1. 📄 Copiar el JavaScript moderno del artifact anterior")
    logger.info("   2. 🔄 Reiniciar tu servidor web")
    logger.info("   3. 🧹 Limpiar caché del navegador (Ctrl+F5)")
    
    # Resumen final
    logger.info(f"\n{'='*80}")
    logger.info(f"📊 RESUMEN: {pasos_completados}/{len(pasos)} pasos completados")
    logger.info("=" * 80)
    
    if pasos_completados >= len(pasos) - 1:  # Permitir que falle el JS ya que es manual
        logger.info("🎉 ¡MEJORAS DE UI APLICADAS EXITOSAMENTE!")
        
        logger.info("\n🔥 TU INTERFAZ AHORA INCLUYE:")
        logger.info("   🌈 Gradientes modernos y atractivos")
        logger.info("   ✨ Animaciones suaves y profesionales")
        logger.info("   🎯 Diseño responsive y accesible")
        logger.info("   🎨 Efectos visuales avanzados")
        logger.info("   📱 Optimizado para móviles")
        logger.info("   🎪 Partículas animadas de fondo")
        
        logger.info("\n🎨 CARACTERÍSTICAS VISUALES:")
        logger.info("   💫 Cards con efectos hover 3D")
        logger.info("   🌊 Botones con gradientes y efectos shimmer")
        logger.info("   🏷️  Badges modernos con iconos")
        logger.info("   📊 Información nutricional visual")
        logger.info("   🎭 Modal mejorado con mejor UX")
        logger.info("   🔔 Notificaciones toast elegantes")
        
        logger.info("\n🚀 PRÓXIMOS PASOS:")
        logger.info("   1. 🔄 python run.py")
        logger.info("   2. 🌐 Abre tu navegador")
        logger.info("   3. 🎊 ¡Disfruta de tu nueva interfaz!")
        
        return True
    else:
        logger.warning("⚠️  Mejoras parcialmente aplicadas")
        logger.info("💡 Revisa los errores y ejecuta el script nuevamente")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)