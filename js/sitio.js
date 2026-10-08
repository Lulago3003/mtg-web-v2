// Catálogo de relojes: filtro por categoría y cambio de color.
// Sin JavaScript la página muestra todos los modelos en su primer color.
(function () {
  var catalogo = document.querySelector("[data-catalogo]");
  if (!catalogo) return;

  var numero = catalogo.getAttribute("data-whatsapp");
  var filtros = document.querySelectorAll("[data-filtro]");
  var relojes = catalogo.querySelectorAll(".reloj");
  var conteo = document.querySelector("[data-conteo]");

  function enlaceWhatsApp(modelo, color, precio, variosColores) {
    var texto = "Hola, me interesa el reloj " + modelo +
      (variosColores ? " en color " + color.toLowerCase() : "") +
      " de USD " + precio + ". ¿Está disponible?";
    return "https://wa.me/" + numero + "?text=" + encodeURIComponent(texto);
  }

  function filtrar(id, actualizarDireccion) {
    var visibles = 0;
    filtros.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-filtro") === id ? "true" : "false");
    });
    relojes.forEach(function (r) {
      var mostrar = id === "todos" || r.getAttribute("data-categoria") === id;
      r.hidden = !mostrar;
      if (mostrar) visibles++;
    });
    if (conteo) conteo.textContent = visibles === 1 ? "1 modelo" : visibles + " modelos";
    if (actualizarDireccion && history.replaceState) {
      history.replaceState(null, "", id === "todos" ? location.pathname : "#" + id);
    }
  }

  filtros.forEach(function (b) {
    b.addEventListener("click", function () { filtrar(b.getAttribute("data-filtro"), true); });
  });

  function desdeDireccion() {
    var id = location.hash.replace("#", "");
    var valido = Array.prototype.some.call(filtros, function (b) { return b.getAttribute("data-filtro") === id; });
    filtrar(valido ? id : "todos", false);
  }
  desdeDireccion();
  window.addEventListener("hashchange", desdeDireccion);

  relojes.forEach(function (r) {
    var muestras = r.querySelectorAll(".muestra");
    var foto = r.querySelector(".reloj-foto img");
    var existencias = r.querySelector(".existencias");
    var nombreColor = r.querySelector(".colores-nombre");
    var boton = r.querySelector(".boton-wa");
    var modelo = r.getAttribute("data-modelo");
    var precio = r.getAttribute("data-precio");

    muestras.forEach(function (m) {
      m.addEventListener("click", function () {
        muestras.forEach(function (o) { o.setAttribute("aria-pressed", o === m ? "true" : "false"); });
        var color = m.getAttribute("data-m");
        var n = m.getAttribute("data-existencias");
        foto.src = m.getAttribute("data-foto");
        foto.alt = modelo + " en color " + color.toLowerCase();
        existencias.textContent = n + " en existencia";
        if (nombreColor) nombreColor.textContent = color;
        boton.href = enlaceWhatsApp(modelo, color, precio, muestras.length > 1);
      });
    });
  });
})();
