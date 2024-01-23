$(document).ready(function () {
    var contadorProductos = 1;

    $("#agregarOtroProducto").click(function () {
        contadorProductos++;
        var nuevoProducto = $(".producto:first").clone();
        nuevoProducto.find("input, select").val("");
        nuevoProducto.find(".productos").attr("name", "productos_" + contadorProductos);
        nuevoProducto.find(".cantidades").attr("name", "cantidades_" + contadorProductos);

        nuevoProducto.append('<span class="eliminarProducto" onclick="eliminarProducto(this)">-</span>');

        nuevoProducto.find(".eliminarProducto").css({
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "cursor": "pointer",
            "font-size": "18px",
            "color": "#fff",
            "background": "#e74c3c",
            "border-radius": "20%",
            "width": "30px",
            "height": "30px",
            "margin-left": "10px",
        });

        nuevoProducto.appendTo(".productos-container");
    });

    eliminarProducto = function (elemento) {
        $(elemento).closest('.producto').remove();
    };
});