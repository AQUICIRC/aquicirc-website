/* Maps. Leaflet is self-hosted and loaded once, only when a map is needed:
   - the sites map (`.sitesmap-frame[data-sites]`) loads as it nears the viewport;
   - the site-page locator (`.map-frame[data-map]`) loads when "Show map" is pressed.
   Tiles come from OpenStreetMap. Without this file the site list and the
   OpenStreetMap link remain. */
(function () {
    "use strict";

    var loading = null;
    var loadLeaflet = function () {
        if (loading) return loading;
        var add = function (tag, attrs) {
            return new Promise(function (resolve, reject) {
                var el = document.createElement(tag);
                Object.keys(attrs).forEach(function (k) { el.setAttribute(k, attrs[k]); });
                el.onload = resolve;
                el.onerror = reject;
                document.head.appendChild(el);
            });
        };
        loading = Promise.all([
            add("link", { rel: "stylesheet", href: "/vendor/leaflet/leaflet.css" }),
            add("script", { src: "/vendor/leaflet/leaflet.js" })
        ]);
        return loading;
    };

    var newMap = function (el) {
        /* Fractional zoom so the Netherlands-to-Cape span fills the frame. */
        var map = window.L.map(el, { scrollWheelZoom: false, zoomSnap: 0.25 });
        window.L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            detectRetina: true,   /* sharp tiles on high-density screens */
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        return map;
    };
    var marker = function (point, title, count) {
        var group = count > 1;
        return window.L.marker(point, {
            icon: window.L.divIcon({
                className: "site-marker" + (group ? " site-marker-group" : ""),
                iconSize: group ? [26, 26] : [16, 16],
                html: group ? String(count) : ""
            }),
            title: title, alt: title, keyboard: true
        });
    };
    var siteBlock = function (site) {
        var box = document.createElement("div");
        box.className = "site-popup";
        var name = document.createElement("strong");
        name.textContent = site.name;
        var teaser = document.createElement("p");
        teaser.textContent = site.teaser;
        var link = document.createElement("a");
        link.href = site.url;
        link.textContent = "Go to the site page";
        var hidden = document.createElement("span");
        hidden.className = "sr-only";
        hidden.textContent = ": " + site.name;
        link.appendChild(hidden);
        box.append(name, teaser, link);
        return box;
    };
    var failed = function (el, text) {
        var note = document.createElement("p");
        note.className = "map-error";
        note.textContent = text;
        el.appendChild(note);
    };

    /* -- the sites map --------------------------------------------------- */
    Array.prototype.forEach.call(document.querySelectorAll(".sitesmap-frame[data-sites]"), function (frame) {
        var sites = JSON.parse(frame.getAttribute("data-sites"));
        var build = function () {
            loadLeaflet().then(function () {
                var map = newMap(frame);
                var points = [];
                sites.forEach(function (site) {
                    site.points.forEach(function (p) { points.push({ at: window.L.latLng(p), site: site }); });
                });
                /* Markers closer than 22px on screen merge into one numbered
                   marker whose popup lists each site; zooming in separates them.
                   Recomputed on every zoom. */
                var layer = window.L.layerGroup().addTo(map);
                var render = function () {
                    layer.clearLayers();
                    var groups = [];
                    points.forEach(function (pt) {
                        var px = map.latLngToLayerPoint(pt.at);
                        var near = groups.filter(function (g) { return g.px.distanceTo(px) < 22; })[0];
                        if (near) near.items.push(pt); else groups.push({ px: px, items: [pt] });
                    });
                    groups.forEach(function (g) {
                        var unique = [];
                        g.items.forEach(function (pt) { if (unique.indexOf(pt.site) === -1) unique.push(pt.site); });
                        var lat = 0, lng = 0;
                        g.items.forEach(function (pt) { lat += pt.at.lat; lng += pt.at.lng; });
                        var centre = [lat / g.items.length, lng / g.items.length];
                        var popup = document.createElement("div");
                        unique.forEach(function (site) { popup.appendChild(siteBlock(site)); });
                        var title = unique.map(function (s) { return s.name; }).join(" and ");
                        layer.addLayer(marker(centre, title, unique.length).bindPopup(popup));
                    });
                };
                map.fitBounds(points.map(function (pt) { return pt.at; }), { padding: [24, 24] });
                render();
                map.on("zoomend", render);
            }).catch(function () {
                failed(frame, "The map could not be loaded. The list of sites beside it links to every site.");
            });
        };
        /* Never compete with the page's own load: wait for `load`, then build
           once the map is near the viewport. */
        var watch = function () {
            if (!("IntersectionObserver" in window)) { build(); return; }
            var seen = new IntersectionObserver(function (entries) {
                if (entries.some(function (e) { return e.isIntersecting; })) {
                    seen.disconnect();
                    build();
                }
            }, { rootMargin: "200px 0px" });
            seen.observe(frame);
        };
        if (document.readyState === "complete") watch();
        else window.addEventListener("load", watch, { once: true });
    });

    /* -- the site-page locator -------------------------------------------- */
    var frame = document.querySelector(".map-frame[data-map]");
    if (!frame) return;
    var button = frame.querySelector("[data-map-load]");
    button.hidden = false;
    button.addEventListener("click", function () {
        button.disabled = true;
        button.textContent = "Loading map…";
        loadLeaflet().then(function () {
            var points = JSON.parse(frame.getAttribute("data-points"));
            var label = frame.getAttribute("data-label");
            frame.textContent = "";
            frame.classList.add("loaded");
            frame.setAttribute("tabindex", "0");
            frame.setAttribute("aria-label", "Map of " + label);
            var map = newMap(frame);
            points.forEach(function (p) { marker(p, label).addTo(map); });
            map.fitBounds(points, { maxZoom: 11, padding: [40, 40] });
            frame.focus();
        }).catch(function () {
            button.disabled = false;
            button.textContent = "Show map";
            failed(frame, "The map could not be loaded. Use the OpenStreetMap link above instead.");
        });
    });
})();
