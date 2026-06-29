                document.getElementById('pulse_sp_link').addEventListener('input', async function() {
                    const url = this.value;
                    if (!url.includes('spotify.com') && !url.includes('apple.com')) return;
                    if (url.length < 20) return; // Prevent triggering on partial pastes
                    
                    document.getElementById('pulse_loading').style.display = 'block';
                    try {
                        const response = await fetch('/api/fetch_meta', {
                            method: 'POST',
                            credentials: 'same-origin',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ url: url })
                        });
                        const data = await response.json();
                        if (data.title) document.getElementById('pulse_short_desc').value = data.title;
                        if (data.band) document.getElementById('pulse_title').value = data.band;
                    } catch (e) {
                        console.error('Error:', e);
                    } finally {
                        document.getElementById('pulse_loading').style.display = 'none';
                    }
                });
            
        // User Management scripts
        function editUser(id, nombre, username, email, role) {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-pen"></i> Editar Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/edit/' + id;
            document.getElementById('user_nombre').value = nombre;
            document.getElementById('user_username').value = username;
            document.getElementById('user_email').value = email;
            document.getElementById('user_role').value = role;
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Actualizar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'inline-block';
            
            form.scrollIntoView({ behavior: 'smooth' });
        }

                function toggleUserStatus(id) {
            fetch('/admin/users/toggle/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(!data.success) {
                    alert('Error al actualizar el estado del usuario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error de conexión');
            });
        }

        function cancelUserEdit() {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Añadir Nuevo Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/add';
            form.reset();
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'none';
        }

                function updateSingleSetting(key, value) {
                    const formData = new FormData();
                    formData.append('key', key);
                    formData.append('value', value);
                    fetch('/admin/update_single_setting', {
                        method: 'POST',
                        body: formData
                    }).then(res => res.json()).then(data => {
                        if(data.success) {
                            console.log('Setting updated');
                        }
                    });
                }
            
        // User Management scripts
        function editUser(id, nombre, username, email, role) {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-pen"></i> Editar Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/edit/' + id;
            document.getElementById('user_nombre').value = nombre;
            document.getElementById('user_username').value = username;
            document.getElementById('user_email').value = email;
            document.getElementById('user_role').value = role;
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Actualizar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'inline-block';
            
            form.scrollIntoView({ behavior: 'smooth' });
        }

                function toggleUserStatus(id) {
            fetch('/admin/users/toggle/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(!data.success) {
                    alert('Error al actualizar el estado del usuario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error de conexión');
            });
        }

        function cancelUserEdit() {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Añadir Nuevo Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/add';
            form.reset();
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'none';
        }

            document.addEventListener('DOMContentLoaded', function() {
                const rawData = {{ analytics_data | tojson | safe if analytics_data else '[]' }};
                
                // Procesar datos para gráficas
                const scrollCounts = { '0%':0, '25%':0, '50%':0, '75%':0, '100%':0 };
                let totalTime = 0;
                let timeCount = 0;
                const newReturn = { 'Nuevos': 0, 'Recurrentes': 0 };
                const devices = { 'Desktop': 0, 'Mobile': 0 };
                const referrers = {};
                const countries = {};

                // Map time on page over time for line chart (last 20 sessions)
                const timeHistory = [];
                const timeLabels = [];

                if (rawData && rawData.length > 0) {
                    rawData.forEach(row => {
                    // Scroll
                    if (row.scroll_depth >= 100) scrollCounts['100%']++;
                    else if (row.scroll_depth >= 75) scrollCounts['75%']++;
                    else if (row.scroll_depth >= 50) scrollCounts['50%']++;
                    else if (row.scroll_depth >= 25) scrollCounts['25%']++;
                    else scrollCounts['0%']++;

                    // Time
                    if (row.time_on_page > 0) {
                        totalTime += row.time_on_page;
                        timeCount++;
                        if (timeHistory.length < 20) {
                            timeHistory.unshift(row.time_on_page);
                            timeLabels.unshift(row.created_at.substring(5,16));
                        }
                    }

                    // Users
                    if (row.is_new_user) newReturn['Nuevos']++;
                    else newReturn['Recurrentes']++;

                    // Devices
                    if (row.device_type === 'mobile') devices['Mobile']++;
                    else devices['Desktop']++;

                    // Referrer
                    let ref = row.referrer || 'Directo';
                    try {
                        if (ref.startsWith('http')) {
                            let url = new URL(ref);
                            ref = url.hostname.replace('www.','');
                        }
                    } catch(e) {}
                    referrers[ref] = (referrers[ref] || 0) + 1;

                    // Countries
                    let country = row.country || 'Desconocido';
                    countries[country] = (countries[country] || 0) + 1;
                });
                }

                // Chart defaults
                Chart.defaults.color = '#888';
                Chart.defaults.font.family = 'Inter, sans-serif';

                // Time Chart
                new Chart(document.getElementById('timeChart'), {
                    type: 'line',
                    data: {
                        labels: timeLabels,
                        datasets: [{
                            label: 'Segundos',
                            data: timeHistory,
                            borderColor: '#cca85b',
                            backgroundColor: 'rgba(204, 168, 91, 0.2)',
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: { maintainAspectRatio: false }
                });

                // Scroll Chart
                new Chart(document.getElementById('scrollChart'), {
                    type: 'bar',
                    data: {
                        labels: Object.keys(scrollCounts),
                        datasets: [{
                            label: 'Sesiones',
                            data: Object.values(scrollCounts),
                            backgroundColor: '#cca85b'
                        }]
                    },
                    options: { maintainAspectRatio: false }
                });

                // Users Chart
                new Chart(document.getElementById('usersChart'), {
                    type: 'doughnut',
                    data: {
                        labels: Object.keys(newReturn),
                        datasets: [{
                            data: Object.values(newReturn),
                            backgroundColor: ['#cca85b', '#333'],
                            borderWidth: 0
                        }]
                    },
                    options: { maintainAspectRatio: false }
                });

                // Devices Chart
                new Chart(document.getElementById('devicesChart'), {
                    type: 'pie',
                    data: {
                        labels: Object.keys(devices),
                        datasets: [{
                            data: Object.values(devices),
                            backgroundColor: ['#555', '#cca85b'],
                            borderWidth: 0
                        }]
                    },
                    options: { maintainAspectRatio: false }
                });

                // Referrer Chart
                const sortedRefs = Object.entries(referrers).sort((a,b) => b[1]-a[1]).slice(0,5);
                new Chart(document.getElementById('referrerChart'), {
                    type: 'bar',
                    data: {
                        labels: sortedRefs.map(x => x[0]),
                        datasets: [{
                            label: 'Visitas',
                            data: sortedRefs.map(x => x[1]),
                            backgroundColor: '#444'
                        }]
                    },
                    options: { indexAxis: 'y', maintainAspectRatio: false }
                });

                // Countries Chart
                const sortedCountries = Object.entries(countries).sort((a,b) => b[1]-a[1]).slice(0,5);
                new Chart(document.getElementById('countriesChart'), {
                    type: 'bar',
                    data: {
                        labels: sortedCountries.map(x => x[0]),
                        datasets: [{
                            label: 'Visitas',
                            data: sortedCountries.map(x => x[1]),
                            backgroundColor: '#cca85b'
                        }]
                    },
                    options: { indexAxis: 'y', maintainAspectRatio: false }
                });
            });
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
    localStorage.setItem('activeAdminTab', tabName);
}

document.addEventListener('DOMContentLoaded', function() {
    // Check if there is an alert that says "Es necesario validar"
    const alerts = document.querySelectorAll('.alert');
    let shouldOpenPreview = false;
    alerts.forEach(alert => {
        if (alert.textContent.includes('Es necesario validar')) {
            shouldOpenPreview = true;
        }
    });

    if (shouldOpenPreview) {
        // Auto-open preview tab
        const previewBtn = document.querySelector('button[onclick*="tab-preview"]');
        if (previewBtn) {
            openTab({currentTarget: previewBtn}, 'tab-preview');
        }
    } else {
        // Default tab behavior
        const savedTab = localStorage.getItem('activeAdminTab');
        if (savedTab) {
            const savedBtn = document.querySelector(`button[onclick*="${savedTab}"]`);
            if (savedBtn) {
                openTab({currentTarget: savedBtn}, savedTab);
            } else {
                const firstBtn = document.querySelector('.tab-btn');
                if (firstBtn) openTab({currentTarget: firstBtn}, 'tab-crear');
            }
        } else {
            const firstBtn = document.querySelector('.tab-btn');
            if (firstBtn && !document.querySelector('.tab-btn.active')) {
                openTab({currentTarget: firstBtn}, 'tab-crear');
            }
        }
    }

    // Auto-fill pub_date with current OS date/time
    const pubDateInput = document.querySelector('input[name="pub_date"]');
    if (pubDateInput && !pubDateInput.value) {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        pubDateInput.value = now.toISOString().slice(0, 16);
    }
});

function editRecord(btn) {
    var id = btn.getAttribute('data-id');
    
    // Switch to "Crear" tab automatically when editing
    var firstBtn = document.querySelector(".tab-btn[onclick*='tab-crear']");
    if(firstBtn) openTab({currentTarget: firstBtn}, 'tab-crear');
    
    document.getElementById('form-title').innerHTML = '<i class="fa-solid fa-pen-nib"></i> Editar Registro #' + id;
    document.getElementById('main-form').action = '/admin/edit/' + id;
    document.getElementById('submit-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Cambios';
    document.getElementById('cancel-btn').style.display = 'block';
    
    document.querySelector('#main-form select[name="section"]').value = btn.getAttribute('data-section') || '';
    document.querySelector('#main-form input[name="pub_date"]').value = btn.getAttribute('data-pub') || '';
    document.querySelector('#main-form input[name="title"]').value = btn.getAttribute('data-title') || '';
    
    // Handle author properly (don't set to empty if it's missing, keep what's there or use a fallback)
    var authorData = btn.getAttribute('data-author');
    if (authorData && authorData !== 'None' && authorData.trim() !== '') {
        document.querySelector('#main-form input[name="author"]').value = authorData;
    }
    
    document.querySelector('#main-form input[name="short_desc"]').value = btn.getAttribute('data-short') || '';
    document.querySelector('#main-form textarea[name="full_desc"]').value = btn.getAttribute('data-full') || '';
    document.querySelector('#main-form input[name="yt_link"]').value = btn.getAttribute('data-yt') || '';
    document.querySelector('#main-form input[name="sp_link"]').value = btn.getAttribute('data-sp') || '';
    document.querySelector('#main-form input[name="ap_link"]').value = btn.getAttribute('data-ap') || '';
    
    document.getElementById('image-input').required = false;
    document.getElementById('image-hint').style.display = 'inline';
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
    syncAllVisualsToEditors();
}

function cancelEdit() {
    document.getElementById('form-title').innerHTML = '<i class="fa-solid fa-pen-nib"></i> Crear Nuevo Registro';
    document.getElementById('main-form').action = '/admin/dashboard';
    document.getElementById('submit-btn').innerHTML = '<i class="fa-solid fa-bolt"></i> Actualizar Web y Generar Redes Sociales';
    document.getElementById('cancel-btn').style.display = 'none';
    
    document.getElementById('image-input').required = true;
    document.getElementById('image-hint').style.display = 'none';
    document.getElementById('main-form').reset();
    document.querySelector('input[name="image"]').required = true;
    syncAllVisualsToEditors();
}

function editBandaRecord(btn) {
    var id = btn.getAttribute('data-id');
    
    // Switch to "Banda" tab automatically when editing
    var bandBtn = document.querySelector(".tab-btn[onclick*='tab-banda']");
    if(bandBtn) openTab({currentTarget: bandBtn}, 'tab-banda');
    
    document.getElementById('form-banda-title').innerHTML = '<i class="fa-solid fa-pen-nib"></i> Editar Banda #' + id;
    document.getElementById('banda-form').action = '/admin/banda/edit/' + id;
    document.getElementById('banda-submit-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Cambios';
    document.getElementById('banda-cancel-btn').style.display = 'block';
    
    document.querySelector('#banda-form input[name="nombre"]').value = btn.getAttribute('data-nombre') || '';
    document.querySelector('#banda-form input[name="fecha_inicio"]').value = btn.getAttribute('data-fechainicio') || '';
    document.querySelector('#banda-form input[name="fecha_fin"]').value = btn.getAttribute('data-fechafin') || '';
    document.querySelector('#banda-form input[name="pais"]').value = btn.getAttribute('data-pais') || '';
    document.querySelector('#banda-form input[name="ciudad"]').value = btn.getAttribute('data-ciudad') || '';
    document.querySelector('#banda-form textarea[name="bio_corta"]').value = btn.getAttribute('data-biocorta') || '';
    document.querySelector('#banda-form input[name="ano_formacion"]').value = btn.getAttribute('data-ano') || '';
    document.querySelector('#banda-form input[name="line_up"]').value = btn.getAttribute('data-lineup') || '';
    document.querySelector('#banda-form input[name="ig_link"]').value = btn.getAttribute('data-ig') || '';
    document.querySelector('#banda-form input[name="fb_link"]').value = btn.getAttribute('data-fb') || '';
    document.querySelector('#banda-form input[name="tk_link"]').value = btn.getAttribute('data-tk') || '';
    document.querySelector('#banda-form input[name="sp_link"]').value = btn.getAttribute('data-sp') || '';
    document.querySelector('#banda-form input[name="ap_link"]').value = btn.getAttribute('data-ap') || '';
    document.querySelector('#banda-form input[name="yt_link"]').value = btn.getAttribute('data-yt') || '';
    
    document.querySelector('#banda-form input[name="titulo_resena"]').value = btn.getAttribute('data-titulores') || '';
    document.querySelector('#banda-form textarea[name="texto_resena"]').value = btn.getAttribute('data-textores') || '';
    
    document.querySelector('#banda-form textarea[name="discografia"]').value = btn.getAttribute('data-disco') || '';
    document.querySelector('#banda-form input[name="ultimo_lanzamiento_titulo"]').value = btn.getAttribute('data-ulttit') || '';
    
    var ultTipo = btn.getAttribute('data-ulttipo');
    if (ultTipo) document.querySelector('#banda-form select[name="ultimo_lanzamiento_tipo"]').value = ultTipo;
    
    document.querySelector('#banda-form input[name="ultimo_lanzamiento_sp_link"]').value = btn.getAttribute('data-ultsp') || '';
    document.querySelector('#banda-form input[name="ultimo_lanzamiento_ap_link"]').value = btn.getAttribute('data-ultap') || '';
    
    document.querySelector('#banda-form input[name="img_video_path"]').required = false;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
    syncAllVisualsToEditors();
}

function cancelBandaEdit() {
    document.getElementById('form-banda-title').innerHTML = '<i class="fa-solid fa-star"></i> Configurar Banda de la Semana';
    document.getElementById('banda-form').action = '/admin/banda';
    document.getElementById('banda-submit-btn').innerHTML = '<i class="fa-solid fa-plus"></i> Agregar Banda de la Semana';
    document.getElementById('banda-cancel-btn').style.display = 'none';
    
    document.getElementById('banda-form').reset();
    document.querySelector('#banda-form input[name="img_video_path"]').required = true;
}

function toggleEventoStatus(id) {
    fetch('/admin/eventos/toggle/' + id, { method: 'POST' })
    .then(r => r.json())
    .then(data => {
        if (!data.success) {
            alert('Error al cambiar el estado del evento');
            location.reload();
        }
    })
    .catch(err => {
        console.error(err);
        alert('Error de conexión');
    });
}

function editEventoRecord(btn) {
    var id = btn.getAttribute('data-id');
    
    var eventosBtn = document.querySelector(".tab-btn[onclick*='tab-eventos']");
    if(eventosBtn) openTab({currentTarget: eventosBtn}, 'tab-eventos');
    
    document.getElementById('form-eventos-title').innerHTML = '<i class="fa-solid fa-pen-nib"></i> Editar Evento #' + id;
    document.getElementById('eventos-form').action = '/admin/eventos/edit/' + id;
    document.getElementById('eventos-submit-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Cambios';
    document.getElementById('eventos-cancel-btn').style.display = 'block';
    
    document.querySelector('#eventos-form input[name="titulo_articulo"]').value = btn.getAttribute('data-titulo') || '';
    document.querySelector('#eventos-form input[name="nombre_evento"]').value = btn.getAttribute('data-nombre') || '';
    document.querySelector('#eventos-form input[name="fecha_inicio_pub"]').value = btn.getAttribute('data-fechainiciopub') || '';
    document.querySelector('#eventos-form input[name="fecha_fin_pub"]').value = btn.getAttribute('data-fechafinpub') || '';
    document.querySelector('#eventos-form input[name="fecha_evento"]').value = btn.getAttribute('data-fechaevento') || '';
    document.querySelector('#eventos-form input[name="promotor"]').value = btn.getAttribute('data-promotor') || '';
    document.querySelector('#eventos-form input[name="pais"]').value = btn.getAttribute('data-pais') || '';
    document.querySelector('#eventos-form input[name="ciudad"]').value = btn.getAttribute('data-ciudad') || '';
    document.querySelector('#eventos-form textarea[name="bio_corta"]').value = btn.getAttribute('data-biocorta') || '';
    document.querySelector('#eventos-form textarea[name="texto_articulo"]').value = btn.getAttribute('data-texto') || '';
    document.querySelector('#eventos-form input[name="ig_link"]').value = btn.getAttribute('data-ig') || '';
    document.querySelector('#eventos-form input[name="fb_link"]').value = btn.getAttribute('data-fb') || '';
    
    document.querySelector('#eventos-form input[name="img_video_path"]').required = false;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
    syncAllVisualsToEditors();
}

function cancelEventoEdit() {
    document.getElementById('form-eventos-title').innerHTML = '<i class="fa-solid fa-calendar-star"></i> Gestión Eventos Destacados';
    document.getElementById('eventos-form').action = '/admin/eventos';
    document.getElementById('eventos-submit-btn').innerHTML = '<i class="fa-solid fa-plus"></i> Agregar Evento de la Semana';
    document.getElementById('eventos-cancel-btn').style.display = 'none';
    
    document.getElementById('eventos-form').reset();
    document.querySelector('#eventos-form input[name="img_video_path"]').required = true;
}

function setPreviewMode(mode) {
    const container = document.getElementById('preview-container');
    document.getElementById('btn-desktop').style.borderColor = '#555';
    document.getElementById('btn-ios').style.borderColor = '#555';
    document.getElementById('btn-android').style.borderColor = '#555';
    
    if (mode === 'desktop') {
        container.style.width = '100%';
        container.style.height = '700px';
        document.getElementById('btn-desktop').style.borderColor = 'var(--accent-color)';
    } else if (mode === 'ios') {
        container.style.width = '390px'; // iPhone size
        container.style.height = '844px';
        document.getElementById('btn-ios').style.borderColor = 'var(--accent-color)';
    } else if (mode === 'android') {
        container.style.width = '412px'; // Android size
        container.style.height = '915px';
        document.getElementById('btn-android').style.borderColor = 'var(--accent-color)';
    }
}

function confirmGoLive() {
    if (confirm("⚠️ ¿Estás seguro de continuar y publicar los cambios en vivo para todo el público?\n\n(Aceptar = Sí, Publicar | Cancelar = Seguir editando)")) {
        alert("✅ ¡Cambios publicados exitosamente! Tu sitio está en vivo.");
    }
}

        // User Management scripts
        function editUser(id, nombre, username, email, role) {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-pen"></i> Editar Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/edit/' + id;
            document.getElementById('user_nombre').value = nombre;
            document.getElementById('user_username').value = username;
            document.getElementById('user_email').value = email;
            document.getElementById('user_role').value = role;
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Actualizar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'inline-block';
            
            form.scrollIntoView({ behavior: 'smooth' });
        }

                function toggleUserStatus(id) {
            fetch('/admin/users/toggle/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(!data.success) {
                    alert('Error al actualizar el estado del usuario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error de conexión');
            });
        }

        function cancelUserEdit() {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Añadir Nuevo Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/add';
            form.reset();
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'none';
        }

function toggleBandaStatus(id) {
    fetch(`/admin/toggle_banda/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if(!data.success) {
            alert('Error al actualizar el estado de la banda');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error de conexión');
    });
}

const dict = {
    'Crear/Editar Registro': 'Create/Edit Record',
    'Sincronización Automática': 'Auto Sync',
    'Gestión Noticiero': 'News Mgmt',
    'Gestión Reseñas': 'Reviews Mgmt',
    'Metal Pulse': 'Metal Pulse',
    'Crear Nuevo Registro': 'Create New Record',
    'Llena este formulario para actualizar la web y generar automáticamente tus copys e imágenes para redes sociales.': 'Fill out this form to update the web and automatically generate your copy and images for social media.',
    'Sección de la Página': 'Page Section',
    'Fecha de Publicación': 'Publish Date',
    'Título del Registro': 'Record Title',
    'Descripción Corta (Para tarjetas y listados)': 'Short Description (Cards & Lists)',
    'Descripción Completa (Para modal/cuerpo de la noticia)': 'Full Description (Modal/Body)',
    'Imagen de Portada': 'Cover Image',
    'Link YouTube (Opcional)': 'YouTube Link (Optional)',
    'Link Spotify (Opcional)': 'Spotify Link (Optional)',
    'Link Apple Podcast (Opcional)': 'Apple Podcast Link (Optional)',
    'Autor / Crew': 'Author / Crew',
    'Actualizar Web y Generar Redes Sociales': 'Update Web & Generate Socials',
    'Cancelar': 'Cancel',
    'Importa automáticamente desde Apple, Spotify, YouTube o Google Sheets.': 'Import automatically from Apple, Spotify, YouTube or Google Sheets.',
    'La Galería Nocturna': 'La Galería Nocturna',
    'Busca nuevos episodios en YouTube para La Galería': 'Search for new episodes on YouTube for La Galería',
    'Actualizar Galería': 'Update Galería',
    'Busca nuevos episodios en Apple Podcast y Spotify': 'Search for new episodes on Apple Podcast and Spotify',
    'Actualizar Metal Pulse': 'Update Metal Pulse',
    'Busca nuevas entrevistas en tu lista de YouTube': 'Search for new interviews in your YouTube playlist',
    'Actualizar Entrevistas': 'Update Interviews',
    'Agenda Metalera': 'Metal Agenda',
    'Lee los nuevos eventos confirmados desde tu Google Sheet': 'Read newly confirmed events from your Google Sheet',
    'Actualizar Agenda': 'Update Agenda',
    'El Noticiero Nocturno': 'El Noticiero Nocturno',
    'Registros manuales de esta sección.': 'Manual records for this section.',
    'Reseñas de Conciertos': 'Concert Reviews',
    'Gestión Metal Pulse': 'Metal Pulse Mgmt',
    'Agrega recomendaciones de canciones y álbumes para la sección Metal Pulse (Top 10).': 'Add song and album recommendations for the Metal Pulse section (Top 10).',
    'Nombre de la Banda': 'Band Name',
    'Nombre de la Canción / Álbum': 'Song / Album Name',
    'Link de Spotify': 'Spotify Link',
    'Agregar Track': 'Add Track',
    'Tracks Actuales': 'Current Tracks',
    'Acciones': 'Actions',
    'Banda': 'Band',
    'Canción / Álbum': 'Song / Album',
    'Editar': 'Edit',
    'Eliminar': 'Delete',
    'Título': 'Title',
    'Fecha': 'Date',
    'Ej. ¡Nuevo Box Set de Metallica!': 'Ex. New Metallica Box Set!',
    'Resumen de 1-2 líneas...': '1-2 line summary...',
    'Toda la información del evento, noticia o episodio...': 'All info for the event, news or episode...',
    'Ej. Nekrogoblikon': 'Ex. Nekrogoblikon',
    'Ej. The Boiling Sea': 'Ex. The Boiling Sea',
    'Salir': 'Logout',
    'Metal Pulse Tracks': 'Metal Pulse Tracks',
    'Vista Previa': 'Preview',
    'Vista Previa del Sitio': 'Site Preview',
    'Verifica los cambios en diferentes pantallas antes de liberar.': 'Verify changes on different screens before releasing.',
    'Computadora': 'Desktop',
    'Go Live (Publicar)': 'Go Live (Publish)'
};

const reverseDict = {};
for (const [es, en] of Object.entries(dict)) {
    reverseDict[en] = es;
}

let currentLang = 'es';

function setLanguage(lang) {
    if (lang === currentLang) return;
    const targetDict = lang === 'en' ? dict : reverseDict;
    
    // Update text nodes
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while (node = walker.nextNode()) {
        let trimmed = node.nodeValue.trim();
        if (targetDict[trimmed]) {
            node.nodeValue = node.nodeValue.replace(trimmed, targetDict[trimmed]);
        }
    }

    // Update placeholders
    const inputs = document.querySelectorAll('input[placeholder], textarea[placeholder]');
    inputs.forEach(input => {
        let trimmed = input.placeholder.trim();
        if (targetDict[trimmed]) {
            input.placeholder = targetDict[trimmed];
        }
    });
    
    // Update select options
    const options = document.querySelectorAll('option');
    options.forEach(opt => {
        let trimmed = opt.textContent.trim();
        if (targetDict[trimmed]) {
            opt.textContent = targetDict[trimmed];
            opt.value = lang === 'en' ? reverseDict[targetDict[trimmed]] : targetDict[trimmed]; // ensure value stays ES so DB works! Wait! 
            // Actually, keep value identical so backend doesn't break, only change textContent!
            opt.value = opt.value; // Keep original DB value
        }
    });

    currentLang = lang;
    
    // Update button styles
    document.getElementById('btn-es').style.borderColor = lang === 'es' ? 'var(--accent-color)' : '#555';
    document.getElementById('btn-en').style.borderColor = lang === 'en' ? 'var(--accent-color)' : '#555';
}

        // User Management scripts
        function editUser(id, nombre, username, email, role) {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-pen"></i> Editar Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/edit/' + id;
            document.getElementById('user_nombre').value = nombre;
            document.getElementById('user_username').value = username;
            document.getElementById('user_email').value = email;
            document.getElementById('user_role').value = role;
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Actualizar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'inline-block';
            
            form.scrollIntoView({ behavior: 'smooth' });
        }

                function toggleUserStatus(id) {
            fetch('/admin/users/toggle/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(!data.success) {
                    alert('Error al actualizar el estado del usuario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error de conexión');
            });
        }

        function cancelUserEdit() {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Añadir Nuevo Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/add';
            form.reset();
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'none';
        }



let savedEditorRange = null;
let lastActiveEditor = null;

document.addEventListener('selectionchange', () => {
    const selection = window.getSelection();
    if (selection.rangeCount > 0 && selection.anchorNode) {
        let node = selection.anchorNode;
        if (node.nodeType === 3) node = node.parentNode; // Si es un nodo de texto, obtener el elemento padre
        
        if (node && node.closest) {
            const editor = node.closest('.rich-editor');
            if (editor) {
                savedEditorRange = selection.getRangeAt(0).cloneRange();
                lastActiveEditor = editor;
            }
        }
    }
});

function formatVisual(event, action, value=null) {
    event.preventDefault(); // Keep focus on editor by preventing default click behavior
    const btn = event.currentTarget;
    const container = btn.closest('.visual-editor-container');
    const editor = container.querySelector('.rich-editor');
    
    // Force focus
    if (document.activeElement !== editor) {
        editor.focus();
    }
    
    let currentRange = null;
    const selection = window.getSelection();
    
    if (selection.rangeCount > 0 && !selection.isCollapsed) {
        currentRange = selection.getRangeAt(0);
    } else if (savedEditorRange && lastActiveEditor === editor) {
        // Restore if lost
        selection.removeAllRanges();
        selection.addRange(savedEditorRange);
        currentRange = savedEditorRange;
    }
    
    if (action === 'bold') {
        if (currentRange && !currentRange.collapsed) {
            const b = document.createElement('b');
            b.appendChild(currentRange.extractContents());
            currentRange.insertNode(b);
        } else {
            document.execCommand('bold', false, null);
        }
    } else if (action === 'foreColor') {
        if (currentRange && !currentRange.collapsed) {
            const span = document.createElement('span');
            span.style.color = value;
            span.appendChild(currentRange.extractContents());
            currentRange.insertNode(span);
        } else {
            document.execCommand('styleWithCSS', false, true);
            document.execCommand('foreColor', false, value);
        }
    } else {
        document.execCommand(action, false, null);
    }
    
    // Clear selection so the user sees the format change
    selection.removeAllRanges();
    syncEditor(editor);
}

// Ensure paste keeps plain text with proper newlines
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.rich-editor').forEach(editor => {
        editor.addEventListener('paste', (e) => {
            e.preventDefault();
            const text = (e.originalEvent || e).clipboardData.getData('text/plain');
            const html = text.split('\n\n').map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
            document.execCommand('insertHTML', false, html);
        });
    });
});

function syncEditor(editorDiv) {
    const container = editorDiv.closest('.visual-editor-container');
    const textarea = container.querySelector('textarea');
    textarea.value = editorDiv.innerHTML;
}


function syncAllEditorsToTextareas() {
    document.querySelectorAll('.visual-editor-container').forEach(container => {
        const textarea = container.querySelector('textarea');
        const editor = container.querySelector('.rich-editor');
        if(textarea && editor) {
            textarea.value = editor.innerHTML;
        }
    });
}

function syncAllVisualsToEditors() {
    // Also use setTimeout to ensure browser has updated textarea.value before we sync
    setTimeout(() => {
        document.querySelectorAll('.visual-editor-container').forEach(container => {
            const textarea = container.querySelector('textarea');
            const editor = container.querySelector('.rich-editor');
            if(textarea && editor) {
                editor.innerHTML = textarea.value;
            }
        });
    }, 100);
}

function addHistoryYear() {
    const container = document.getElementById('history-container');
    const newYearStr = prompt("Ingrese el año que desea agregar (ej. 2027):");
    if(!newYearStr) return;
    
    // Validar que sea número (opcional, pero buena práctica)
    const newYear = parseInt(newYearStr, 10);
    if(isNaN(newYear)) {
        alert("Por favor ingrese un año válido.");
        return;
    }
    
    // Check if it already exists to avoid duplicates
    if(document.querySelector(`input[name="team_history_${newYear}"]`)) {
        alert("Ese año ya existe en la lista.");
        return;
    }

    const html = `
    <div class="history-item" style="background: #222; padding: 15px; border-radius: 6px; border: 1px solid #444; display: flex; gap: 15px; align-items: flex-start; margin-top: 15px;">
        <div style="flex: 0 0 100px;">
            <label style="font-size: 0.8rem; color: #aaa;">Año</label>
            <input type="text" readonly value="${newYear}" style="background: #111; padding: 8px; border-radius: 4px; border: 1px solid #333; width: 100%; color: var(--accent-color); font-weight: bold; text-align: center;">
        </div>
        <div style="flex: 1;">
            <label style="font-size: 0.8rem; color: #aaa;">Historia</label>
            <div class="visual-editor-container" data-target="team_history_${newYear}">
                <div class="textarea-toolbar" style="display: flex; gap: 5px; background: #222; padding: 5px; border: 1px solid #444; border-bottom: none; border-radius: 4px 4px 0 0; position: sticky; top: 0; z-index: 100;">
                    <button type="button" onmousedown="formatVisual(event, 'bold')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Negrita"><i class="fa-solid fa-bold"></i></button>
                    <div style="width: 1px; background: #444; margin: 0 5px;"></div>
                    <button type="button" onmousedown="formatVisual(event, 'foreColor', '#ffffff')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Texto Blanco"><i class="fa-solid fa-droplet"></i> Blanco</button>
                    <button type="button" onmousedown="formatVisual(event, 'foreColor', '#716d4a')" style="background: #333; color: var(--accent-color); border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Texto Dorado"><i class="fa-solid fa-droplet"></i> Dorado</button>
                    <div style="width: 1px; background: #444; margin: 0 5px;"></div>
                    <button type="button" onmousedown="formatVisual(event, 'justifyLeft')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Izquierda"><i class="fa-solid fa-align-left"></i></button>
                    <button type="button" onmousedown="formatVisual(event, 'justifyCenter')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Centro"><i class="fa-solid fa-align-center"></i></button>
                    <button type="button" onmousedown="formatVisual(event, 'justifyRight')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Derecha"><i class="fa-solid fa-align-right"></i></button>
                    <button type="button" onmousedown="formatVisual(event, 'justifyFull')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Justificar"><i class="fa-solid fa-align-justify"></i></button>
                </div>
                <div class="rich-editor" contenteditable="true" style="min-height: 100px; background: #111; color: #fff; border: 1px solid #333; border-radius: 0 0 4px 4px; padding: 10px; outline: none; overflow-y: auto; white-space: pre-wrap;" oninput="syncEditor(this)"></div>
                <textarea name="team_history_${newYear}" rows="3" style="display: none;"></textarea>
            </div>
        </div>
    </div>\`;
    
    container.insertAdjacentHTML('beforeend', html);
}

