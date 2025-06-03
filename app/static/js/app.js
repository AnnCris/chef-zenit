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
    
    // Array para almacenar los ingredientes y alergias seleccionados
    let ingredientes = [];
    let alergias = [];
    let recetaActualId = null;
    
    // Función para agregar un ingrediente a la lista
    function agregarIngrediente() {
        const ingrediente = ingredientesInput.value.trim();
        
        if (ingrediente && !ingredientes.includes(ingrediente)) {
            ingredientes.push(ingrediente);
            
            // Crear badge para el ingrediente
            const badge = document.createElement('span');
            badge.className = 'badge bg-primary me-1 mb-1';
            badge.textContent = ingrediente;
            
            // Agregar botón para eliminar
            const closeBtn = document.createElement('button');
            closeBtn.className = 'btn-close btn-close-white ms-1';
            closeBtn.setAttribute('aria-label', 'Eliminar');
            closeBtn.style.fontSize = '0.5rem';
            closeBtn.addEventListener('click', function() {
                ingredientesSeleccionados.removeChild(badge);
                ingredientes = ingredientes.filter(i => i !== ingrediente);
            });
            
            badge.appendChild(closeBtn);
            ingredientesSeleccionados.appendChild(badge);
            
            ingredientesInput.value = '';
        }
    }
    
    // Función para agregar una alergia a la lista
    function agregarAlergia() {
        const alergia = alergiasInput.value.trim();
        
        if (alergia && !alergias.includes(alergia)) {
            alergias.push(alergia);
            
            // Crear badge para la alergia
            const badge = document.createElement('span');
            badge.className = 'badge bg-danger me-1 mb-1';
            badge.textContent = alergia;
            
            // Agregar botón para eliminar
            const closeBtn = document.createElement('button');
            closeBtn.className = 'btn-close btn-close-white ms-1';
            closeBtn.setAttribute('aria-label', 'Eliminar');
            closeBtn.style.fontSize = '0.5rem';
            closeBtn.addEventListener('click', function() {
                alergiasSeleccionadas.removeChild(badge);
                alergias = alergias.filter(a => a !== alergia);
            });
            
            badge.appendChild(closeBtn);
            alergiasSeleccionadas.appendChild(badge);
            
            alergiasInput.value = '';
        }
    }
    
    // Función para buscar recetas por ingredientes
    async function buscarRecetasPorIngredientes() {
        if (ingredientes.length === 0) {
            mostrarMensaje('Por favor, agrega al menos un ingrediente.', 'warning');
            return;
        }
        
        try {
            // Mostrar indicador de carga
            resultadosContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div><p class="mt-2">Buscando recetas...</p></div>';
            
            // Realizar petición a la API
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
            
            console.log('Respuesta de la API:', response.status);
            
            // Obtener texto de la respuesta para diagnóstico
            const responseText = await response.text();
            console.log('Respuesta del servidor (texto):', responseText);
            
            // Intentar parsear como JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es un JSON válido. Verifica los logs para más detalles.', 'danger');
                return;
            }
            
            console.log('Datos de la API:', data);
            
            if (data.success && data.data.length > 0) {
                mostrarResultados(data.data);
            } else {
                if (data.error) {
                    mostrarMensaje(`Error: ${data.error}`, 'danger');
                } else {
                    mostrarMensaje('No se encontraron recetas con esos ingredientes. ¡Intenta agregar más ingredientes o prueba con otros diferentes!', 'info');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Ocurrió un error al buscar recetas. Por favor, intenta de nuevo más tarde.', 'danger');
        }
    }
    
    // Función para buscar recetas por consulta
    async function buscarRecetasPorConsulta() {
        const consulta = consultaInput.value.trim();
        
        if (!consulta) {
            mostrarMensaje('Por favor, escribe una consulta.', 'warning');
            return;
        }
        
        try {
            // Mostrar indicador de carga
            resultadosContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div><p class="mt-2">Analizando tu consulta...</p></div>';
            
            // Realizar petición a la API
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
            
            if (!response.ok) {
                throw new Error('Error en la petición');
            }
            
            // Obtener texto de la respuesta para diagnóstico
            const responseText = await response.text();
            console.log('Respuesta del servidor (texto):', responseText);
            
            // Intentar parsear como JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es un JSON válido. Verifica los logs para más detalles.', 'danger');
                return;
            }
            
            if (data.success && data.data.recomendaciones.length > 0) {
                // Mostrar información de análisis
                let analisisHTML = `<div class="alert alert-info">
                    <h5>He analizado tu consulta:</h5>`;
                    
                if (data.data.analisis.ingredientes.length > 0) {
                    analisisHTML += `<p><strong>Ingredientes detectados:</strong> ${data.data.analisis.ingredientes.join(', ')}</p>`;
                }
                
                if (data.data.analisis.restricciones.length > 0) {
                    analisisHTML += `<p><strong>Restricciones dietéticas:</strong> ${data.data.analisis.restricciones.join(', ')}</p>`;
                }
                
                if (data.data.analisis.alergias.length > 0) {
                    analisisHTML += `<p><strong>Alergias detectadas:</strong> ${data.data.analisis.alergias.join(', ')}</p>`;
                }
                
                analisisHTML += `</div>`;
                
                // Mostrar resultados con el análisis
                mostrarResultados(data.data.recomendaciones, analisisHTML);
            } else {
                mostrarMensaje('No encontré recetas que coincidan con tu consulta. Por favor, intenta ser más específico o usa términos diferentes.', 'info');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo más tarde.', 'danger');
        }
    }
    
    // Función para guardar preferencias
    async function guardarPreferencias() {
        try {
            // Obtener restricciones dietéticas seleccionadas
            const restricciones = [];
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {
                restricciones.push(checkbox.value);
            });
            
            console.log("Restricciones seleccionadas:", restricciones);
            console.log("Alergias seleccionadas:", alergias);
            
            // Mostrar indicador de carga
            resultadosContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Guardando...</span></div><p class="mt-2">Guardando preferencias...</p></div>';
            
            // Realizar petición a la API
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
            
            // Obtener texto de la respuesta para diagnóstico
            const responseText = await response.text();
            console.log('Respuesta del servidor (texto):', responseText);
            
            // Intentar parsear como JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es un JSON válido. Verifica los logs para más detalles.', 'danger');
                return;
            }
            
            if (data.success) {
                mostrarMensaje(data.message || 'Preferencias guardadas correctamente. A partir de ahora, las recomendaciones tendrán en cuenta tus preferencias y restricciones.', 'success');
            } else {
                mostrarMensaje(data.error || 'No se pudieron guardar las preferencias.', 'warning');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Ocurrió un error al guardar las preferencias. Por favor, intenta de nuevo más tarde.', 'danger');
        }
    }
    
    // Función para mostrar un mensaje en el contenedor de resultados
    function mostrarMensaje(mensaje, tipo) {
        resultadosContainer.innerHTML = `
            <div class="alert alert-${tipo}" role="alert">
                ${mensaje}
            </div>
        `;
    }
    
    // Función para mostrar los resultados de las recetas
    function mostrarResultados(recetas, contenidoAdicional = '') {
        let html = contenidoAdicional;
        
        html += `
            <h4 class="mb-3">Recetas Recomendadas</h4>
            <div class="row">
        `;
        
        recetas.forEach(receta => {
            let ingredientesFaltantes = '';
            if (receta.ingredientes_faltantes && receta.ingredientes_faltantes.length > 0) {
                ingredientesFaltantes = `
                    <div class="mt-2">
                        <small class="text-danger">
                            <strong>Te faltan:</strong> ${receta.ingredientes_faltantes.join(', ')}
                        </small>
                    </div>
                `;
            }
            
            html += `
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">${receta.nombre}</h5>
                        </div>
                        ${receta.imagen_url ? `<img src="/static/${receta.imagen_url}" class="card-img-top" alt="${receta.nombre}">` : ''}
                        <div class="card-body">
                            <p class="card-text">${receta.descripcion ? receta.descripcion.substring(0, 100) + '...' : 'Sin descripción'}</p>
                            
                            <div class="d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-clock"></i> ${receta.tiempo_preparacion} min</span>
                                <span><i class="bi bi-person"></i> ${receta.porciones} porciones</span>
                                <span><i class="bi bi-star"></i> ${receta.dificultad || 'Media'}</span>
                            </div>
                            ${ingredientesFaltantes}
                        </div>
                        <div class="card-footer">
                            <button class="btn btn-outline-primary w-100" onclick="verReceta(${receta.id})">Ver Detalles</button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `
            </div>
            <div class="d-grid gap-2 mt-3">
                <button class="btn btn-success" onclick="descargarPDFMultiple()">Descargar todas las recetas en PDF</button>
            </div>
        `;
        
        resultadosContainer.innerHTML = html;
    }
    
    // Función para ver detalles de una receta
    window.verReceta = async function(id) {
        try {
            // Mostrar modal con indicador de carga
            recetaModalLabel.textContent = "Cargando detalles...";
            recetaModalBody.innerHTML = '<div class="text-center py-5"><div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
            
            // Guardar el ID de la receta actual
            recetaActualId = id;
            
            // Mostrar el modal
            const modalInstance = new bootstrap.Modal(recetaModal);
            modalInstance.show();
            
            // Realizar petición a la API
            const response = await fetch(`/api/recetas/${id}`);
            
            if (!response.ok) {
                throw new Error('Error en la petición');
            }
            
            // Obtener texto de la respuesta para diagnóstico
            const responseText = await response.text();
            console.log('Respuesta del servidor (texto):', responseText);
            
            // Intentar parsear como JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es un JSON válido. Verifica los logs para más detalles.', 'danger');
                return;
            }
            
            if (data.success) {
                const receta = data.data;
                
                // Actualizar título del modal
                recetaModalLabel.textContent = receta.nombre;
                
                // Construir contenido HTML
                let html = `
                    <div class="row">
                        ${receta.imagen_url ? `
                            <div class="col-md-4 mb-3">
                                <img src="/static/${receta.imagen_url}" class="img-fluid rounded" alt="${receta.nombre}">
                            </div>
                        ` : ''}
                        
                        <div class="col-md-${receta.imagen_url ? '8' : '12'} mb-3">
                            ${receta.descripcion ? `<p>${receta.descripcion}</p>` : ''}
                            
                            <div class="d-flex justify-content-between mb-3">
                                <div class="text-center">
                                    <i class="bi bi-clock fs-3"></i>
                                    <p class="mb-0">${receta.tiempo_preparacion} min</p>
                                    <small class="text-muted">Tiempo</small>
                                </div>
                                <div class="text-center">
                                    <i class="bi bi-person fs-3"></i>
                                    <p class="mb-0">${receta.porciones}</p>
                                    <small class="text-muted">Porciones</small>
                                </div>
                                <div class="text-center">
                                    <i class="bi bi-star fs-3"></i>
                                    <p class="mb-0">${receta.dificultad || 'Media'}</p>
                                    <small class="text-muted">Dificultad</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-header bg-warning">
                                    <h5 class="card-title mb-0">Ingredientes</h5>
                                </div>
                                <div class="card-body">
                                    <ul class="list-group list-group-flush">
                `;
                
                // Agregar ingredientes
                receta.ingredientes.forEach(ri => {
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            ${ri.nombre}${ri.es_opcional ? ' <small class="text-muted">(opcional)</small>' : ''}
                            <span>${ri.cantidad} ${ri.unidad || ''}</span>
                        </li>
                    `;
                });
                
                html += `
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-header bg-success text-white">
                                    <h5 class="card-title mb-0">Información Nutricional</h5>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-6 mb-2">
                                            <p class="mb-0"><strong>Calorías:</strong> ${receta.calorias || 0} kcal</p>
                                        </div>
                                        <div class="col-6 mb-2">
                                            <p class="mb-0"><strong>Proteínas:</strong> ${receta.proteinas || 0} g</p>
                                        </div>
                                        <div class="col-6 mb-2">
                                            <p class="mb-0"><strong>Carbohidratos:</strong> ${receta.carbohidratos || 0} g</p>
                                        </div>
                                        <div class="col-6 mb-2">
                                            <p class="mb-0"><strong>Grasas:</strong> ${receta.grasas || 0} g</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card mb-3">
                        <div class="card-header bg-info">
                            <h5 class="card-title mb-0">Preparación</h5>
                        </div>
                        <div class="card-body">
                            <ol class="list-group list-group-numbered">
                `;
                
                // Agregar pasos de preparación
                receta.pasos.forEach(paso => {
                    html += `<li class="list-group-item">${paso.descripcion}</li>`;
                });
                
                html += `
                            </ol>
                        </div>
                    </div>
                `;
                
                // Actualizar contenido del modal
                recetaModalBody.innerHTML = html;
            } else {
                recetaModalBody.innerHTML = `<div class="alert alert-danger">Error al cargar los detalles de la receta.</div>`;
            }
        } catch (error) {
            console.error('Error:', error);
            recetaModalBody.innerHTML = `<div class="alert alert-danger">Ocurrió un error al cargar los detalles. Por favor, intenta de nuevo más tarde.</div>`;
        }
    }
    
    // Función para descargar PDF de la receta actual
    window.descargarPDF = function() {
        if (recetaActualId) {
            window.location.href = `/api/recetas/${recetaActualId}/pdf`;
        }
    }
    
    // Función para descargar PDF de múltiples recetas
    window.descargarPDFMultiple = function() {
        // Obtener todos los IDs de recetas mostradas
        const recetasIds = Array.from(document.querySelectorAll('.card-footer button'))
            .map(btn => parseInt(btn.getAttribute('onclick').match(/\d+/)[0]));
        
        if (recetasIds.length > 0) {
            // Crear un formulario oculto para hacer la solicitud POST
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/api/recomendaciones/pdf';
            form.target = '_blank';
            
            // Agregar campo para los IDs de recetas
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'recetas_ids';
            input.value = JSON.stringify(recetasIds);
            form.appendChild(input);
            
            // Agregar formulario al documento y enviarlo
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
        }
    }
    
    // Event listeners
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
        descargarPdfBtn.addEventListener('click', function() {
            descargarPDF();
        });
    }
});