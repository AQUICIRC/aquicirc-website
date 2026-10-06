/* Locator map on site pages. Nothing third-party loads until "Show map" is
   pressed; then self-hosted Leaflet draws OpenStreetMap tiles and a circle
   marker per coordinate. Without this file the OpenStreetMap link remains. */
(function () {
    "use strict";
    var frame = document.querySelector(".map-frame[data-map]");
    if (!frame) return;
    var button = frame.querySelector("[data-map-load]");
    button.hidden = false;

    var load = function (tag, attrs) {
        return new Promise(function (resolve, reject) {
            var el = document.createElement(tag);
            Object.keys(attrs).forEach(function (k) { el.setAttribute(k, attrs[k]); });
            el.onload = resolve;
            el.onerror = reject;
            document.head.appendChild(el);
        });
    };

    button.addEventListener("click", function () {
        button.disabled = true;
        button.textContent = "Loading map…";
        Promise.all([
            load("link", { rel: "stylesheet", href: "/vendor/leaflet/leaflet.css" }),
            load("script", { src: "/vendor/leaflet/leaflet.js" })
        ]).then(function () {
            var points = JSON.parse(frame.getAttribute("data-points"));
            frame.textContent = "";
            frame.classList.add("loaded");
            frame.setAttribute("tabindex", "0");
            frame.setAttribute("aria-label", "Map of " + frame.getAttribute("data-label"));
            var map = window.L.map(frame, { scrollWheelZoom: false });
            window.L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 18,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            var flow = getComputedStyle(document.documentElement).getPropertyValue("--flow").trim() || "#2471A1";
            var markers = points.map(function (p) {
                return window.L.circleMarker(p, { radius: 8, color: "#fff", weight: 2, fillColor: flow, fillOpacity: 1 }).addTo(map);
            });
            map.fitBounds(window.L.featureGroup(markers).getBounds(), { maxZoom: 11, padding: [40, 40] });
            frame.focus();
        }).catch(function () {
            button.disabled = false;
            button.textContent = "Show map";
            var note = document.createElement("p");
            note.textContent = "The map could not be loaded. Use the OpenStreetMap link above instead.";
            frame.appendChild(note);
        });
    });
})();
