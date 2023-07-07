// Mapa para PROBOSQUE Cambio Cobertura Arbórea 2015-2022
// Autor: urielm

// Cargar mapa en el Estado de México con un zoom de 8
var map = L.map('map').setView([19.3672, -99.7233], 8); // Estado de México

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

