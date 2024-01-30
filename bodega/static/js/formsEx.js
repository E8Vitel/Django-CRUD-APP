$(document).ready(function () {
    var contadorProductos = 1;

    $("#agregarOtroProducto").click(function () {
        contadorProductos++;
        var nuevoProducto = $(".producto:first").clone();
        nuevoProducto.find("input, select").val("");
        nuevoProducto.find(".productos").attr("name", "productos[]");
        nuevoProducto.find(".precios").attr("name", "precios[]");
        nuevoProducto.find(".cantidades").attr("name", "cantidades[]");

        nuevoProducto.append('<button type="button" class="eliminarProducto btn btn-danger" onclick="eliminarProducto(this)"><i class="material-icons">remove</i></button>');
        nuevoProducto.after('<hr class="separador">');

        nuevoProducto.appendTo(".productos-container");
    });

    eliminarProducto = function (elemento) {
        $(elemento).closest('.producto').remove();
    };
});