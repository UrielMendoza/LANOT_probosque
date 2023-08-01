// Mapa para PROBOSQUE Cambio Cobertura Arbórea 2015-2022
// Autor: urielm

// Inicio
window.addEventListener('DOMContentLoaded', function() {
    var inicio = document.getElementById('inicio');
    var btnInicio = document.getElementById('btn-inicio-container');
    var inicioTitulo = document.getElementById('inicio-titulo');
    var inicioLogos = document.getElementById('inicio-logos');
    var mapaContainer = document.getElementsByClassName('mapa-container')[0];
    var menu = document.getElementById('menu');
    var mapaTitulo = document.getElementById('mapa-titulo');
    var mapaSimbologia = document.getElementById('mapa-simbologia');
    //var mapaSimbologiaImg_1 = document.getElementById('mapa-simbologia-img_1');
    //var mapaSimbologiaImg_2 = document.getElementById('mapa-simbologia-img_2');
    var mapaSimbologiaImg = document.getElementById('mapa-simbologia-img');

    // Mostrar el título y los logos después de 1 segundo
    setTimeout(function() {
        //inicioTitulo.style.opacity = '1';
        //inicioLogos.style.opacity = '1';
    }, 2000);
    // Mostrar el botón de inicio después de 3 segundos
    setTimeout(function() {
        btnInicio.style.opacity = '1';
    }, 1000);
    

    // Manejar el evento clic en el botón de inicio
    document.getElementById('btn-inicio').addEventListener('click', function() {
        inicio.style.display = 'none';
        mapaContainer.style.opacity = '1';
        mapaTitulo.style.opacity = '0.75';
        mapaSimbologia.style.background = 'var(--white)';
        mapaSimbologiaImg.style.opacity = '1';
        //mapaSimbologiaImg_1.style.opacity = '1';
        //mapaSimbologiaImg_2.style.opacity = '0.85';

        // Activa la simbologia de la capa 1
        mapaSimbologiaImg.src = './assets/icons/simbologia.png';

        var mapContainer = document.getElementById('map');
        mapContainer.style.height = (window.innerHeight - 20) + 'px'; // Ajusta el tamaño del mapa

        // Ajusta el tamaño del mapa al cambiar el tamaño de la ventana
        window.addEventListener('resize', function() {
            var mapContainer = document.getElementById('map');
            mapContainer.style.height = (window.innerHeight - 20) + 'px'; // Ajusta el tamaño del mapa
        });

        // Inicializar el mapa
        // Mapa
        const map = L.map('map', {
        }).setView([19.3, -99.5], 9);
        
        // Tiles hasta detras de las capas
        const cartodb = L.tileLayer('https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://cartodb-basemaps-a.global.ssl.fastly.net">cartoDB</a>',
            zindex: 0
        }).addTo(map);
        const cartodb_dark = L.tileLayer('http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://a.basemaps.cartocdn.com/">cartoDB</a>',
            zindex: 0
        });
        const osm = L.tileLayer('http://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://a.tile.openstreetmap.org">OSM</a>',
            zindex: 0
        });
        const ESRI_satelital = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://server.arcgisonline.com">ESRI</a>',
            zindex: 0
        });
        const ESRI_topo = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://server.arcgisonline.com">ESRI</a>',
            zindex: 0
        });
        const googlemaps = L.tileLayer('https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://mt1.google.com">GoogleMaps</a>',
            zindex: 0
        });
        const googlemaps_satelital = L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://mt1.google.com">GoogleMaps</a>',
            zindex: 0
        });
        
        // Controlador de eventos para el checkbox
        function toggleLayer(checkboxId, wmsLayer) {
            const checkbox = document.getElementById(checkboxId);
        
            checkbox.addEventListener('change', function () {
                if (this.checked) {
                    wmsLayer.addTo(map);
                    /* Pone la capa al frente de las demas */
                    wmsLayer.bringToFront();
                    mapaSimbologiaImg.style.opacity = '1';

                    // Pone la capa de sombras al frente de las demas
                    sombra_igecem2.bringToFront();
                    entidades.bringToFront();

                    // Controlador de simbologia al activar la capa
                    if (checkboxId == 'capa1') {
                        mapaSimbologiaImg.src = './assets/icons/simbologia.png';
                    } else if (checkboxId == 'capa2') {
                        mapaSimbologiaImg.src = './assets/icons/simbologia.png';
                    } else if (checkboxId == 'capa3') {
                        mapaSimbologiaImg.src = './assets/icons/simbologia_cambio.png';
                    } else if (checkboxId == 'capa4') {
                        mapaSimbologiaImg.src = './assets/icons/simbologia_vegdominante.png';
                    } else {
                        mapaSimbologiaImg.src = '';
                    }
                } else {
                    map.removeLayer(wmsLayer);
                    mapaSimbologiaImg.style.opacity = '0';
                }
            });
        }
              

        // Capas WMS
        const wms = 'http://132.247.103.145:8080/geoserver/probosque/wms'

        var edomex_2022 = L.tileLayer.wms(wms, {
            layers: 'probosque:edomex_2022',
            transparent: true,
            format: 'image/png',
            zindex: 5
        }).addTo(map);

        const select = document.getElementById('cobertura');

        select.addEventListener('change', function () {
            const selectedValue = this.value;
            const cqlFilter = "clase_2022 = " + selectedValue; // Reemplaza "atributo_de_la_capa" con el nombre del atributo en tu capa WMS
            
            // Si el valor es "todos", pone todas las categorías
            if (selectedValue == 'todos') {
            // Actualizar el parámetro CQL_FILTER de la capa WMS
            edomex_2022.setParams({ CQL_FILTER: null });
            }
            else {
            // Actualizar el parámetro CQL_FILTER de la capa WMS
            edomex_2022.setParams({ CQL_FILTER: cqlFilter });
            }
        });

        var edomex_2015 = L.tileLayer.wms(wms, {
            layers: 'probosque:edomex_2015',
            transparent: true,
            format: 'image/png',
            zindex: 5
        });

        var edomex_2015_2022 = L.tileLayer.wms(wms, {
            layers: 'probosque:edomex_2015_2022',
            transparent: true,
            format: 'image/png',
            zindex: 5,
            opacity: 0.75
        });

        var edomex_veg_dominante = L.tileLayer.wms(wms, {
            layers: 'probosque:edomex_veg_dominante',
            transparent: true,
            format: 'image/png',
            zindex: 5,
            opacity: 0.5
        });

        //const select_2015 = document.getElementById('cobertura_2015');

        //select_2015.addEventListener('change', function () {
        //    const selectedValue = this.value;
        //    const cqlFilter = "clase_2015 = " + selectedValue; // Reemplaza "atributo_de_la_capa" con el nombre del atributo en tu capa WMS
        
            // Actualizar el parámetro CQL_FILTER de la capa WMS
        //    edomex_2015.setParams({ CQL_FILTER: cqlFilter });
        //});

        var sombra_igecem2 = L.tileLayer.wms(wms, {
            layers: 'probosque:sombra_igecem2',
            transparent: true,
            format: 'image/png',
            opacity: 0.25,
            // Siempre esta por encima de las demas
            zindex: 10
        }).addTo(map);

        var planet_true_color = L.tileLayer.wms(wms, {
            layers: 'probosque:planet_true_color',
            transparent: true,
            format: 'image/png',
            zindex: 0.5
        });

        var planet_false_color = L.tileLayer.wms(wms, {
            layers: 'probosque:planet_false_color',
            transparent: true,
            format: 'image/png',
            zindex: 1
        });

        var planet_nir_color = L.tileLayer.wms(wms, {
            layers: 'probosque:planet_nir_color',
            transparent: true,
            format: 'image/png',
            zindex: 1
        });

        var spot_ndvi_2015 = L.tileLayer.wms(wms, {
            layers: 'probosque:spot_ndvi_2015',
            transparent: true,
            format: 'image/png'
        });

        var planet_ndvi_2022 = L.tileLayer.wms(wms, {
            layers: 'probosque:planet_ndvi_2022',
            transparent: true,
            format: 'image/png'
        });

        var spot_planet_dndvi = L.tileLayer.wms(wms, {
            layers: 'probosque:spot_planet_dndvi',
            transparent: true,
            format: 'image/png'
        });

        var spot_planet_dndvi_1sd = L.tileLayer.wms(wms, {
            layers: 'probosque:spot_planet_dndvi_1sd',
            transparent: true,
            format: 'image/png'
        });

        var spot_planet_dndvi_2sd = L.tileLayer.wms(wms, {
            layers: 'probosque:spot_planet_dndvi_2sd',
            transparent: true,
            format: 'image/png'
        });

        var spot_planet_dndvi_3sd = L.tileLayer.wms(wms, {
            layers: 'probosque:spot_planet_dndvi_3sd',
            transparent: true,
            format: 'image/png'
        });

        var entidades = L.tileLayer.wms(wms, {
            layers: 'probosque:entidades_probosque',
            transparent: true,
            format: 'image/png',
            // Siempre esta por encima de las demas
            zindex: 10
        }).addTo(map);

        // Pone al frente la capa de entidades y la sombra
        entidades.bringToFront();
        sombra_igecem2.bringToFront();

        // Activacion y desactivacion de capas
        toggleLayer('capa1', edomex_2022);
        toggleLayer('capa2', edomex_2015);
        toggleLayer('capa3', edomex_2015_2022);
        toggleLayer('capa4', edomex_veg_dominante);
        toggleLayer('capa5', sombra_igecem2);
        toggleLayer('capa6', entidades);
        toggleLayer('capa7', planet_true_color);
        toggleLayer('capa8', planet_false_color);
        toggleLayer('capa9', planet_nir_color);
/*         toggleLayer('capa7', spot_ndvi_2015); 
        toggleLayer('capa8', planet_ndvi_2022);
        toggleLayer('capa9', spot_planet_dndvi);
        toggleLayer('capa10', spot_planet_dndvi_1sd);
        toggleLayer('capa11', spot_planet_dndvi_2sd);
        toggleLayer('capa12', spot_planet_dndvi_3sd); */


        // Control de capas
        var baseMaps = {
            "CartoDB Light": cartodb,
            "CartoDB Dark": cartodb_dark,
            "OSM": osm,
            "ESRI Satelital": ESRI_satelital,
            "ESRI Topo": ESRI_topo,
            "Google Maps": googlemaps,
            "Google Maps Satelital": googlemaps_satelital
        };

/*         var overlays = {
        "Edomex_2022":edomex_2022,
        "Planet True Color": planet_true_color,
        "Planet False Color": planet_false_color,
        "Planet NIR Color": planet_nir_color,
        "Spot NDVI 2015": spot_ndvi_2015,
        "Planet NDVI 2022": planet_ndvi_2022,
        "Spot-Planet DNDVI": spot_planet_dndvi,
        "Spot-Planet DNDVI 1 SD": spot_planet_dndvi_1sd,
        "Spot-Planet DNDVI 2 SD": spot_planet_dndvi_2sd,
        "Spot-Planet DNDVI 3 SD": spot_planet_dndvi_3sd,
        "Sombra IGECEM2": sombra_igecem2,
        "Entidades": entidades
        }; */


        var overlays = {
        };
        
        // Crear el controlador de capas y agregarlo al mapa
        L.control.layers(baseMaps, overlays).addTo(map);

        // Función para obtener información de la capa
        function getFeatureInfo(evt) {
            var url = wms + '?service=WMS&version=1.1.1&request=GetFeatureInfo&' +
                'layers=' + edomex_2022.options.layers + '&' +
                'query_layers=' + edomex_2022.options.layers + '&' +
                'info_format=text/html&' +
                'feature_count=50&' +
                'format=image/png&' +
                'transparent=true&' +
                'width=' + map.getSize().x + '&' +
                'height=' + map.getSize().y + '&' +
                'srs=' + map.options.crs.code + '&' +
                'bbox=' + map.getBounds().toBBoxString() + '&' +
                'x=' + evt.layerPoint.x + '&' +
                'y=' + evt.layerPoint.y;

            // Realizar una solicitud AJAX para obtener la información de la capa
            $.ajax({
                url: url,
                dataType: 'html',
                success: function(data) {
                    // Mostrar el contenido en un pop-up
                    L.popup()
                        .setLatLng(evt.latlng)
                        .setContent(data)
                        .openOn(map);
                }
            });
        }

        // Evento click en la capa para obtener información
        edomex_2022.on('click', getFeatureInfo);

        // Añadir un control de escala
        L.control.scale().addTo(map);

        
    });
});


