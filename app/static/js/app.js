// app/static/js/app.js - JavaScript Moderno y Mejorado

document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const ingredientesForm = document.getElementById('ingredientesForm');
    const ingredientesInput = document.getElementById('ingredientesInput');
    const agregarIngredienteBtn = document.getElementById('agregarIngrediente');
    const ingredientesSeleccionados = document.getElementById('ingredientesSeleccionados');
    
    const preferenciasForm = document.getElementById('preferenciasForm');
    const alergiasInput = document.getElementById('alergiasInput');
    const agregarAlergiaBtn = document.getElementById('agregarAlergia');
    const alergiasSeleccionadas = document.getElementById('alergiasSeleccionadas');
    
    const consultaForm = document.getElementById('consultaForm');
    const consultaInput = document.getElementById('consultaInput');
    const resultadosContainer = document.getElementById('resultadosContainer');
    
    const recetaModal = document.getElementById('recetaModal');
    const recetaModalLabel = document.getElementById('recetaModalLabel');
    const recetaModalBody = document.getElementById('recetaModalBody');
    const descargarPdfBtn = document.getElementById('descargarPdfBtn');
    
    // Arrays para almacenar selecciones
    let ingredientes = [];
    let alergias = [];
    let recetaActualId = null;
    
    // Configuración de animaciones
    const animationConfig = {
        duration: 300,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    };
    
    // === UTILIDADES ===
    
    // Función para mostrar notificaciones toast mejoradas
    function mostrarToast(mensaje, tipo = 'info') {
        const toastElement = document.getElementById('liveToast');
        const toastBody = toastElement.querySelector('.toast-body');
        const toastHeader = toastElement.querySelector('.toast-header');
        
        // Configurar icono y color según el tipo
        const iconos = {
            success: 'bi-check-circle-fill text-success',
            error: 'bi-exclamation-triangle-fill text-danger',
            warning: 'bi-exclamation-circle-fill text-warning',
            info: 'bi-info-circle-fill text-info'
        };
        
        const icono = toastHeader.querySelector('i');
        icono.className = `bi ${iconos[tipo]} me-2`;
        
        toastBody.innerHTML = mensaje;
        
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
    
    // Función para crear elementos con animación
    function crearElementoAnimado(html, tipo = 'fadeIn') {
        const temp = document.createElement('div');
        temp.innerHTML = html;
        const elemento = temp.firstElementChild;
        elemento.style.opacity = '0';
        elemento.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            elemento.style.transition = `all ${animationConfig.duration}ms ${animationConfig.easing}`;
            elemento.style.opacity = '1';
            elemento.style.transform = 'translateY(0)';
        }, 10);
        
        return elemento;
    }
    
    // Función para limpiar el container de ingredientes
    function limpiarContainerIngredientes() {
        if (ingredientes.length === 0) {
            ingredientesSeleccionados.innerHTML = `
                <div class="text-muted text-center py-3">
                    <i class="bi bi-inbox fs-1 d-block mb-2 opacity-50"></i>
                    <small>Los ingredientes aparecerán aquí...</small>
                </div>
            `;
        }
    }
    
    // === MANEJO DE INGREDIENTES ===
    
    function agregarIngrediente() {
        const ingrediente = ingredientesInput.value.trim();
        
        if (!ingrediente) {
            mostrarToast('Por favor ingresa un ingrediente', 'warning');
            return;
        }
        
        if (ingredientes.includes(ingrediente.toLowerCase())) {
            mostrarToast('Este ingrediente ya está agregado', 'warning');
            ingredientesInput.value = '';
            return;
        }
        
        ingredientes.push(ingrediente.toLowerCase());
        
        // Limpiar el container si es el primer ingrediente
        if (ingredientes.length === 1) {
            ingredientesSeleccionados.innerHTML = '';
        }
        
        // Crear badge animado
        const badgeHtml = `
            <span class="badge bg-primary me-2 mb-2 d-inline-flex align-items-center position-relative badge-ingrediente">
                <i class="bi bi-check2 me-1"></i>
                ${ingrediente}
                <button class="btn-close btn-close-white ms-2" style="font-size: 0.7rem;" data-ingrediente="${ingrediente}">
                </button>
            </span>
        `;
        
        const badge = crearElementoAnimado(badgeHtml);
        
        // Agregar event listener para eliminar
        const closeBtn = badge.querySelector('.btn-close');
        closeBtn.addEventListener('click', function() {
            const ingredienteAEliminar = this.getAttribute('data-ingrediente');
            eliminarIngrediente(ingredienteAEliminar, badge);
        });
        
        ingredientesSeleccionados.appendChild(badge);
        ingredientesInput.value = '';
        
        mostrarToast(`${ingrediente} agregado correctamente`, 'success');
        
        // Efecto de pulso en el botón de búsqueda
        const submitBtn = ingredientesForm.querySelector('button[type="submit"]');
        submitBtn.classList.add('animate__animated', 'animate__pulse');
        setTimeout(() => {
            submitBtn.classList.remove('animate__animated', 'animate__pulse');
        }, 1000);
    }
    
    function eliminarIngrediente(ingrediente, elemento) {
        // Animación de salida
        elemento.style.transition = `all ${animationConfig.duration}ms ${animationConfig.easing}`;
        elemento.style.opacity = '0';
        elemento.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            ingredientes = ingredientes.filter(i => i !== ingrediente.toLowerCase());
            elemento.remove();
            limpiarContainerIngredientes();
            mostrarToast(`${ingrediente} eliminado`, 'info');
        }, animationConfig.duration);
    }
    
    // === MANEJO DE ALERGIAS ===
    
    function agregarAlergia() {
        const alergia = alergiasInput.value.trim();
        
        if (!alergia) {
            mostrarToast('Por favor ingresa una alergia', 'warning');
            return;
        }
        
        if (alergias.includes(alergia.toLowerCase())) {
            mostrarToast('Esta alergia ya está agregada', 'warning');
            alergiasInput.value = '';
            return;
        }
        
        alergias.push(alergia.toLowerCase());
        
        const badgeHtml = `
            <span class="badge bg-danger me-2 mb-2 d-inline-flex align-items-center badge-alergia">
                <i class="bi bi-exclamation-triangle me-1"></i>
                ${alergia}
                <button class="btn-close btn-close-white ms-2" style="font-size: 0.7rem;" data-alergia="${alergia}">
                </button>
            </span>
        `;
        
        const badge = crearElementoAnimado(badgeHtml);
        
        const closeBtn = badge.querySelector('.btn-close');
        closeBtn.addEventListener('click', function() {
            const alergiaAEliminar = this.getAttribute('data-alergia');
            eliminarAlergia(alergiaAEliminar, badge);
        });
        
        alergiasSeleccionadas.appendChild(badge);
        alergiasInput.value = '';
        
        mostrarToast(`Alergia a ${alergia} registrada`, 'success');
    }
    
    function eliminarAlergia(alergia, elemento) {
        elemento.style.transition = `all ${animationConfig.duration}ms ${animationConfig.easing}`;
        elemento.style.opacity = '0';
        elemento.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            alergias = alergias.filter(a => a !== alergia.toLowerCase());
            elemento.remove();
            mostrarToast(`Alergia a ${alergia} eliminada`, 'info');
        }, animationConfig.duration);
    }
    
    // === LOADING STATES MEJORADOS ===
    
    function mostrarCargando(container, mensaje) {
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="d-flex justify-content-center mb-4">
                    <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                </div>
                <h5 class="text-primary mb-3">
                    <i class="bi bi-robot me-2"></i>
                    ${mensaje}
                </h5>
                <div class="progress mb-3" style="height: 6px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                         style="width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    </div>
                </div>
                <small class="text-muted">
                    <i class="bi bi-cpu me-1"></i>
                    Procesando con algoritmos de IA avanzados...
                </small>
            </div>
        `;
    }
    
    // === BÚSQUEDA POR INGREDIENTES MEJORADA ===
    
    async function buscarRecetasPorIngredientes() {
        if (ingredientes.length === 0) {
            mostrarToast('Por favor, agrega al menos un ingrediente', 'warning');
            
            // Efecto de shake en el input
            ingredientesInput.classList.add('animate__animated', 'animate__shakeX');
            setTimeout(() => {
                ingredientesInput.classList.remove('animate__animated', 'animate__shakeX');
                ingredientesInput.focus();
            }, 1000);
            return;
        }
        
        try {
            mostrarCargando(resultadosContainer, 'Analizando tus ingredientes...');
            
            const response = await fetch('/api/recomendaciones/por-ingredientes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ingredientes: ingredientes,
                    max_resultados: 5
                }),
            });
            
            const responseText = await response.text();
            console.log('Respuesta del servidor:', responseText);
            
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es válida', 'danger');
                return;
            }
            
            if (data.success && data.data.length > 0) {
                mostrarResultados(data.data, data.metodo_usado);
                mostrarToast(`¡Encontré ${data.data.length} recetas perfectas para ti!`, 'success');
            } else {
                mostrarMensajeVacio('ingredientes');
                mostrarToast('No encontré recetas con esos ingredientes. ¡Intenta con otros!', 'info');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Error de conexión. Por favor, intenta de nuevo.', 'danger');
            mostrarToast('Error de conexión', 'error');
        }
    }
    
    // === BÚSQUEDA POR CONSULTA MEJORADA ===
    
    async function buscarRecetasPorConsulta() {
        const consulta = consultaInput.value.trim();
        
        if (!consulta) {
            mostrarToast('Por favor, escribe una consulta', 'warning');
            consultaInput.focus();
            return;
        }
        
        try {
            mostrarCargando(resultadosContainer, 'Procesando tu consulta con IA...');
            
            const response = await fetch('/api/recomendaciones/consulta', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    consulta: consulta,
                    max_resultados: 5
                }),
            });
            
            const responseText = await response.text();
            console.log('Respuesta del servidor:', responseText);
            
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es válida', 'danger');
                return;
            }
            
            if (data.success && data.data.recomendaciones.length > 0) {
                let analisisHTML = '';
                
                if (data.data.analisis) {
                    analisisHTML = generarAnalisisHTML(data.data.analisis);
                }
                
                mostrarResultados(data.data.recomendaciones, data.metodo_usado, analisisHTML);
                mostrarToast('¡Consulta procesada exitosamente!', 'success');
            } else {
                mostrarMensajeVacio('consulta');
                mostrarToast('No encontré recetas para tu consulta. ¡Intenta con otros términos!', 'info');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Error al procesar tu consulta. Intenta de nuevo.', 'danger');
            mostrarToast('Error al procesar consulta', 'error');
        }
    }
    
    // === GENERACIÓN DE ANÁLISIS HTML ===
    
    function generarAnalisisHTML(analisis) {
        let html = `
            <div class="alert alert-info border-0 mb-4" style="background: linear-gradient(135deg, rgba(168, 237, 234, 0.2), rgba(254, 214, 227, 0.2));">
                <div class="d-flex align-items-center mb-3">
                    <i class="bi bi-brain fs-4 me-3 text-info"></i>
                    <h5 class="mb-0">Análisis de IA completado</h5>
                </div>
                <div class="row g-3">
        `;
        
        if (analisis.ingredientes && analisis.ingredientes.length > 0) {
            html += `
                <div class="col-md-6">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                        <strong>Ingredientes detectados:</strong>
                    </div>
                    <div class="d-flex flex-wrap gap-1">
                        ${analisis.ingredientes.map(ing => 
                            `<span class="badge bg-success">${ing}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }
        
        if (analisis.restricciones && analisis.restricciones.length > 0) {
            html += `
                <div class="col-md-6">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-shield-check text-warning me-2"></i>
                        <strong>Restricciones detectadas:</strong>
                    </div>
                    <div class="d-flex flex-wrap gap-1">
                        ${analisis.restricciones.map(rest => 
                            `<span class="badge bg-warning text-dark">${rest}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }
        
        if (analisis.alergias && analisis.alergias.length > 0) {
            html += `
                <div class="col-md-12">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-exclamation-triangle text-danger me-2"></i>
                        <strong>Alergias detectadas:</strong>
                    </div>
                    <div class="d-flex flex-wrap gap-1">
                        ${analisis.alergias.map(alergia => 
                            `<span class="badge bg-danger">${alergia}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
        
        return html;
    }
    
    // === MOSTRAR RESULTADOS MEJORADO ===
    
    function mostrarResultados(recetas, metodoUsado = 'IA', contenidoAdicional = '') {
        let html = contenidoAdicional;
        
        // Header de resultados mejorado
        html += `
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h4 class="mb-1">
                        <i class="bi bi-stars text-primary me-2"></i>
                        Recetas Recomendadas
                    </h4>
                    <small class="text-muted">
                        <i class="bi bi-cpu me-1"></i>
                        Generadas por ${metodoUsado} • ${recetas.length} resultado(s)
                    </small>
                </div>
                <div class="d-flex gap-2">
                    ${getAlgorithmBadges(recetas)}
                </div>
            </div>
        `;
        
        // Grid de recetas
        html += '<div class="row g-4">';
        
        recetas.forEach((receta, index) => {
            html += generarTarjetaReceta(receta, index);
        });
        
        html += '</div>';
        
        // Botones de acción
        html += `
            <div class="row g-2 mt-4">
                <div class="col-md-6">
                    <button class="btn btn-success btn-lg w-100" onclick="descargarPDFMultiple()">
                        <i class="bi bi-file-earmark-pdf me-2"></i>
                        Descargar todas en PDF
                    </button>
                </div>
                <div class="col-md-6">
                    <button class="btn btn-info btn-lg w-100" onclick="reentrenarSistema()">
                        <i class="bi bi-arrow-clockwise me-2"></i>
                        Reentrenar IA
                    </button>
                </div>
            </div>
            
            <div class="alert alert-light border-0 mt-4">
                <div class="d-flex align-items-center">
                    <i class="bi bi-lightbulb text-warning me-3"></i>
                    <div>
                        <strong>Sistema Inteligente:</strong> 
                        Estas recomendaciones fueron generadas usando múltiples algoritmos de IA 
                        que analizan ingredientes, preferencias y patrones culinarios.
                    </div>
                </div>
            </div>
        `;
        
        resultadosContainer.innerHTML = html;
        
        // Animar las tarjetas
        const tarjetas = resultadosContainer.querySelectorAll('.recipe-card');
        tarjetas.forEach((tarjeta, index) => {
            setTimeout(() => {
                tarjeta.classList.add('animate__animated', 'animate__fadeInUp');
            }, index * 100);
        });
    }
    
    // === GENERAR BADGES DE ALGORITMOS ===
    
    function getAlgorithmBadges(recetas) {
        const algoritmos = new Set();
        
        recetas.forEach(receta => {
            if (receta.metodos_usados) {
                receta.metodos_usados.forEach(metodo => algoritmos.add(metodo));
            }
        });
        
        const badges = Array.from(algoritmos).map(algoritmo => {
            const config = {
                'contenido_texto': { icon: 'bi-file-text', text: 'TF-IDF', class: 'bg-primary' },
                'contenido_receta': { icon: 'bi-arrow-repeat', text: 'Similitud', class: 'bg-info' },
                'kmeans': { icon: 'bi-diagram-3', text: 'K-means', class: 'bg-success' },
                'random_forest': { icon: 'bi-tree', text: 'R. Forest', class: 'bg-warning text-dark' }
            };
            
            const conf = config[algoritmo] || { icon: 'bi-cpu', text: algoritmo, class: 'bg-secondary' };
            
            return `
                <span class="badge ${conf.class} px-3 py-2">
                    <i class="${conf.icon} me-1"></i>
                    ${conf.text}
                </span>
            `;
        }).join('');
        
        return badges;
    }
    
    // === GENERAR TARJETA DE RECETA ===
    
    function generarTarjetaReceta(receta, index) {
        const ingredientesFaltantes = receta.ingredientes_faltantes && receta.ingredientes_faltantes.length > 0 
            ? `
                <div class="mt-2">
                    <small class="text-danger">
                        <i class="bi bi-exclamation-circle me-1"></i>
                        <strong>Te faltan:</strong> ${receta.ingredientes_faltantes.slice(0, 3).join(', ')}
                        ${receta.ingredientes_faltantes.length > 3 ? '...' : ''}
                    </small>
                </div>
            ` : '';
        
        const metodosInfo = receta.metodos_usados && receta.metodos_usados.length > 0 
            ? `
                <div class="mt-2">
                    <small class="text-info">
                        <i class="bi bi-cpu me-1"></i>
                        ${receta.metodos_usados.map(m => getMethodName(m)).join(' • ')}
                    </small>
                </div>
            ` : '';
        
        const scoreInfo = receta.score_recomendacion 
            ? `
                <div class="mt-2">
                    <div class="d-flex align-items-center">
                        <small class="text-success me-2">
                            <i class="bi bi-star-fill me-1"></i>
                            Compatibilidad:
                        </small>
                        <div class="progress flex-grow-1" style="height: 4px;">
                            <div class="progress-bar bg-success" 
                                 style="width: ${Math.round(receta.score_recomendacion * 100)}%">
                            </div>
                        </div>
                        <small class="text-success ms-2">${Math.round(receta.score_recomendacion * 100)}%</small>
                    </div>
                </div>
            ` : '';
        
        const featuredClass = index === 0 ? 'featured-recipe border-primary' : '';
        const featuredBadge = index === 0 ? '<span class="badge bg-primary position-absolute top-0 start-0 m-2"><i class="bi bi-star-fill me-1"></i>Top</span>' : '';
        
        return `
            <div class="col-md-6 mb-4">
                <div class="card h-100 recipe-card ${featuredClass}" style="opacity: 0;">
                    ${featuredBadge}
                    <div class="card-header ${index === 0 ? 'bg-primary text-white' : 'bg-light'}">
                        <h5 class="card-title mb-0 d-flex align-items-center">
                            <i class="bi bi-bookmark-heart me-2"></i>
                            ${receta.nombre}
                        </h5>
                    </div>
                    ${receta.imagen_url ? `
                        <div class="position-relative overflow-hidden">
                            <img src="/static/${receta.imagen_url}" class="card-img-top" alt="${receta.nombre}" style="height: 200px; object-fit: cover;">
                            <div class="position-absolute top-0 end-0 m-2">
                                <span class="badge bg-dark bg-opacity-75">
                                    <i class="bi bi-clock me-1"></i>${receta.tiempo_preparacion}min
                                </span>
                            </div>
                        </div>
                    ` : ''}
                    <div class="card-body">
                        <p class="card-text text-muted mb-3">
                            ${receta.descripcion ? receta.descripcion.substring(0, 120) + '...' : 'Deliciosa receta para disfrutar'}
                        </p>
                        
                        <div class="row g-2 mb-3 text-center">
                            <div class="col-4">
                                <div class="bg-light rounded p-2">
                                    <i class="bi bi-clock text-primary d-block"></i>
                                    <small class="fw-bold">${receta.tiempo_preparacion || 'N/A'}</small>
                                    <small class="d-block text-muted">min</small>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="bg-light rounded p-2">
                                    <i class="bi bi-people text-success d-block"></i>
                                    <small class="fw-bold">${receta.porciones || 'N/A'}</small>
                                    <small class="d-block text-muted">porciones</small>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="bg-light rounded p-2">
                                    <i class="bi bi-star text-warning d-block"></i>
                                    <small class="fw-bold">${receta.dificultad || 'Media'}</small>
                                    <small class="d-block text-muted">dificultad</small>
                                </div>
                            </div>
                        </div>
                        
                        ${receta.calorias ? `
                            <div class="nutrition-summary bg-light rounded p-2 mb-3">
                                <div class="row g-1 text-center">
                                    <div class="col-3">
                                        <small class="fw-bold text-danger">${receta.calorias}</small>
                                        <small class="d-block text-muted">kcal</small>
                                    </div>
                                    <div class="col-3">
                                        <small class="fw-bold text-primary">${receta.proteinas || 0}g</small>
                                        <small class="d-block text-muted">prot</small>
                                    </div>
                                    <div class="col-3">
                                        <small class="fw-bold text-warning">${receta.carbohidratos || 0}g</small>
                                        <small class="d-block text-muted">carb</small>
                                    </div>
                                    <div class="col-3">
                                        <small class="fw-bold text-info">${receta.grasas || 0}g</small>
                                        <small class="d-block text-muted">gras</small>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                        
                        ${metodosInfo}
                        ${scoreInfo}
                        ${ingredientesFaltantes}
                    </div>
                    <div class="card-footer bg-transparent">
                        <button class="btn btn-primary w-100" onclick="verReceta(${receta.id})">
                            <i class="bi bi-eye me-2"></i>
                            Ver Detalles Completos
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    function getMethodName(metodo) {
        const nombres = {
            'contenido_texto': 'Análisis de Texto',
            'contenido_receta': 'Similitud',
            'kmeans': 'K-means',
            'random_forest': 'Random Forest'
        };
        return nombres[metodo] || metodo;
    }
    
    // === MENSAJES DE ESTADO ===
    
    function mostrarMensaje(mensaje, tipo) {
        const alertClass = {
            success: 'alert-success',
            danger: 'alert-danger',
            warning: 'alert-warning',
            info: 'alert-info'
        };
        
        resultadosContainer.innerHTML = `
            <div class="alert ${alertClass[tipo]} border-0" role="alert">
                <div class="d-flex align-items-center">
                    <i class="bi bi-info-circle-fill me-3"></i>
                    <div>${mensaje}</div>
                </div>
            </div>
        `;
    }
    
    function mostrarMensajeVacio(tipo) {
        const mensajes = {
            ingredientes: {
                icon: 'bi-basket2',
                titulo: 'No se encontraron recetas',
                mensaje: 'Intenta agregando más ingredientes o usa términos diferentes',
                sugerencia: 'Sugerencia: Usa ingredientes comunes como pollo, tomate, cebolla...'
            },
            consulta: {
                icon: 'bi-chat-dots',
                titulo: 'No hay resultados',
                mensaje: 'Tu consulta no coincide con ninguna receta disponible',
                sugerencia: 'Sugerencia: Intenta ser más específico o usa términos culinarios comunes'
            }
        };
        
        const config = mensajes[tipo];
        
        resultadosContainer.innerHTML = `
            <div class="text-center py-5">
                <div class="mb-4">
                    <i class="bi ${config.icon} display-1 text-muted opacity-25"></i>
                </div>
                <h5 class="text-muted mb-3">${config.titulo}</h5>
                <p class="text-muted mb-4">${config.mensaje}</p>
                <div class="alert alert-light border-0">
                    <i class="bi bi-lightbulb text-warning me-2"></i>
                    ${config.sugerencia}
                </div>
                <button class="btn btn-outline-primary" onclick="location.reload()">
                    <i class="bi bi-arrow-clockwise me-2"></i>
                    Intentar de nuevo
                </button>
            </div>
        `;
    }
    
    // === GUARDAR PREFERENCIAS MEJORADO ===
    
    async function guardarPreferencias() {
        try {
            const restricciones = [];
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {
                restricciones.push(checkbox.value);
            });
            
            mostrarCargando(resultadosContainer, 'Guardando tus preferencias...');
            
            const response = await fetch('/api/recomendaciones/preferencias', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    restricciones: restricciones,
                    alergias: alergias
                }),
            });
            
            const responseText = await response.text();
            let data;
            
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                mostrarMensaje('Error: Respuesta del servidor no válida', 'danger');
                return;
            }
            
            if (data.success) {
                mostrarMensaje(
                    data.message || 'Preferencias guardadas correctamente. Las recomendaciones ahora serán personalizadas según tus necesidades.',
                    'success'
                );
                mostrarToast('Preferencias guardadas exitosamente', 'success');
            } else {
                mostrarMensaje(data.error || 'No se pudieron guardar las preferencias.', 'warning');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Error de conexión al guardar preferencias', 'danger');
            mostrarToast('Error de conexión', 'error');
        }
    }
    
    // === FUNCIONES GLOBALES ===
    
    window.verReceta = async function(id) {
        try {
            recetaModalLabel.textContent = "Cargando detalles...";
            recetaModalBody.innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-primary mb-3" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="text-muted">Preparando la receta...</p>
                </div>
            `;
            
            recetaActualId = id;
            
            const modalInstance = new bootstrap.Modal(recetaModal);
            modalInstance.show();
            
            const response = await fetch(`/api/recetas/${id}`);
            const responseText = await response.text();
            
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                recetaModalBody.innerHTML = '<div class="alert alert-danger">Error al cargar la receta</div>';
                return;
            }
            
            if (data.success) {
                const receta = data.data;
                recetaModalLabel.textContent = receta.nombre;
                recetaModalBody.innerHTML = generarContenidoReceta(receta);
                
                mostrarToast('Receta cargada correctamente', 'success');
            } else {
                recetaModalBody.innerHTML = '<div class="alert alert-danger">Error al cargar los detalles de la receta.</div>';
            }
        } catch (error) {
            console.error('Error:', error);
            recetaModalBody.innerHTML = '<div class="alert alert-danger">Error de conexión. Intenta de nuevo.</div>';
        }
    }
    
    function generarContenidoReceta(receta) {
        return `
            <div class="container-fluid p-4">
                <div class="row">
                    ${receta.imagen_url ? `
                        <div class="col-md-4 mb-4">
                            <img src="/static/${receta.imagen_url}" class="img-fluid rounded shadow" alt="${receta.nombre}">
                        </div>
                    ` : ''}
                    
                    <div class="col-md-${receta.imagen_url ? '8' : '12'} mb-4">
                        ${receta.descripcion ? `<p class="lead">${receta.descripcion}</p>` : ''}
                        
                        <div class="row g-3 mb-4">
                            <div class="col-md-3 text-center">
                                <div class="bg-primary text-white rounded p-3">
                                    <i class="bi bi-clock fs-3 d-block mb-2"></i>
                                    <div class="fw-bold">${receta.tiempo_preparacion}</div>
                                    <small>minutos</small>
                                </div>
                            </div>
                            <div class="col-md-3 text-center">
                                <div class="bg-success text-white rounded p-3">
                                    <i class="bi bi-people fs-3 d-block mb-2"></i>
                                    <div class="fw-bold">${receta.porciones}</div>
                                    <small>porciones</small>
                                </div>
                            </div>
                            <div class="col-md-3 text-center">
                                <div class="bg-warning text-dark rounded p-3">
                                    <i class="bi bi-star fs-3 d-block mb-2"></i>
                                    <div class="fw-bold">${receta.dificultad || 'Media'}</div>
                                    <small>dificultad</small>
                                </div>
                            </div>
                            <div class="col-md-3 text-center">
                                <div class="bg-info text-white rounded p-3">
                                    <i class="bi bi-tag fs-3 d-block mb-2"></i>
                                    <div class="fw-bold">${receta.categoria || 'General'}</div>
                                    <small>categoría</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <div class="card h-100">
                            <div class="card-header bg-warning text-dark">
                                <h5 class="card-title mb-0">
                                    <i class="bi bi-basket2-fill me-2"></i>
                                    Ingredientes
                                </h5>
                            </div>
                            <div class="card-body">
                                <div class="list-group list-group-flush">
                                    ${receta.ingredientes.map(ri => `
                                        <div class="list-group-item d-flex justify-content-between align-items-center border-0">
                                            <span>
                                                <i class="bi bi-check2 text-success me-2"></i>
                                                ${ri.nombre}${ri.es_opcional ? ' <small class="text-muted">(opcional)</small>' : ''}
                                            </span>
                                            <span class="badge bg-light text-dark">
                                                ${ri.cantidad || ''} ${ri.unidad || ''}
                                            </span>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                        <div class="card h-100">
                            <div class="card-header bg-success text-white">
                                <h5 class="card-title mb-0">
                                    <i class="bi bi-bar-chart-fill me-2"></i>
                                    Información Nutricional
                                </h5>
                            </div>
                            <div class="card-body">
                                <div class="row g-3">
                                    <div class="col-6">
                                        <div class="text-center p-2 bg-light rounded">
                                            <div class="fw-bold text-danger fs-5">${receta.calorias || 0}</div>
                                            <small class="text-muted">Calorías</small>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="text-center p-2 bg-light rounded">
                                            <div class="fw-bold text-primary fs-5">${receta.proteinas || 0}g</div>
                                            <small class="text-muted">Proteínas</small>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="text-center p-2 bg-light rounded">
                                            <div class="fw-bold text-warning fs-5">${receta.carbohidratos || 0}g</div>
                                            <small class="text-muted">Carbohidratos</small>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="text-center p-2 bg-light rounded">
                                            <div class="fw-bold text-info fs-5">${receta.grasas || 0}g</div>
                                            <small class="text-muted">Grasas</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h5 class="card-title mb-0">
                            <i class="bi bi-list-ol me-2"></i>
                            Preparación
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            ${receta.pasos.map((paso, index) => `
                                <div class="col-12 mb-3">
                                    <div class="d-flex align-items-start">
                                        <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" 
                                             style="min-width: 40px; height: 40px; font-weight: bold;">
                                            ${paso.numero}
                                        </div>
                                        <div class="flex-grow-1">
                                            <p class="mb-0">${paso.descripcion}</p>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    window.descargarPDF = function() {
        if (recetaActualId) {
            window.location.href = `/api/recetas/${recetaActualId}/pdf`;
            mostrarToast('Descargando PDF...', 'info');
        }
    }
    
    window.descargarPDFMultiple = function() {
        const recetasIds = Array.from(document.querySelectorAll('.recipe-card'))
            .map(card => {
                const btn = card.querySelector('button[onclick^="verReceta"]');
                return btn ? parseInt(btn.getAttribute('onclick').match(/\d+/)[0]) : null;
            })
            .filter(id => id !== null);
        
        if (recetasIds.length > 0) {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/api/recomendaciones/pdf';
            form.target = '_blank';
            
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'recetas_ids';
            input.value = JSON.stringify(recetasIds);
            form.appendChild(input);
            
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
            
            mostrarToast(`Generando PDF con ${recetasIds.length} recetas...`, 'info');
        }
    }
    
    window.reentrenarSistema = async function() {
        try {
            mostrarCargando(resultadosContainer, 'Reentrenando sistema de IA...');
            
            const response = await fetch('/api/recomendaciones/entrenar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                mostrarMensaje('🎉 Sistema de IA reentrenado correctamente. Las próximas recomendaciones serán aún más precisas!', 'success');
                mostrarToast('IA reentrenada exitosamente', 'success');
            } else {
                mostrarMensaje('❌ Error al reentrenar el sistema: ' + (data.error || 'Error desconocido'), 'warning');
                mostrarToast('Error al reentrenar', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('❌ Error de conexión al reentrenar el sistema', 'danger');
            mostrarToast('Error de conexión', 'error');
        }
    }
    
    // === EVENT LISTENERS ===
    
    if (agregarIngredienteBtn) {
        agregarIngredienteBtn.addEventListener('click', agregarIngrediente);
    }
    
    if (ingredientesInput) {
        ingredientesInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                agregarIngrediente();
            }
        });
        
        // Autocompletado simple
        ingredientesInput.addEventListener('input', function() {
            // Aquí se podría implementar autocompletado
        });
    }
    
    if (agregarAlergiaBtn) {
        agregarAlergiaBtn.addEventListener('click', agregarAlergia);
    }
    
    if (alergiasInput) {
        alergiasInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                agregarAlergia();
            }
        });
    }
    
    if (ingredientesForm) {
        ingredientesForm.addEventListener('submit', function(e) {
            e.preventDefault();
            buscarRecetasPorIngredientes();
        });
    }
    
    if (consultaForm) {
        consultaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            buscarRecetasPorConsulta();
        });
    }
    
    if (preferenciasForm) {
        preferenciasForm.addEventListener('submit', function(e) {
            e.preventDefault();
            guardarPreferencias();
        });
    }
    
    if (descargarPdfBtn) {
        descargarPdfBtn.addEventListener('click', descargarPDF);
    }
    
    // === INICIALIZACIÓN ===
    
    // Limpiar containers al iniciar
    limpiarContainerIngredientes();
    
    // Mostrar mensaje de bienvenida
    setTimeout(() => {
        mostrarToast('¡Bienvenido al Chef Virtual IA! 🤖👨‍🍳', 'info');
    }, 1000);
    
    console.log('🤖 Chef Virtual IA - Sistema cargado correctamente');
    console.log('🧠 Algoritmos disponibles: TF-IDF, K-means, Random Forest');
});