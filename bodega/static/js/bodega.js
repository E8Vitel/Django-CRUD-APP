$(document).ready(function () {
    $("#mostrarBotones").click(function () {
        $(".opciones-adicionales").slideToggle();
    });

    $(".btn-editar").click(function () {
        var filaId = $(this).data('fila');

        // Obtén los detalles del producto correspondiente
        var nombre = $("#nombre_producto_" + filaId).text();
        var descripcion = $("#descripcion_" + filaId).text();
        var stock = $("#stock_" + filaId).text();
        var precio = $("#precio_" + filaId).text();
        var categoria = $("#categoria_" + filaId).text();

        // Muestra el formulario con los detalles
        $("#formularioEditar").show();
        $("#nombre_producto_editar").val(nombre);
        $("#descripcion_editar").val(descripcion);
        $("#stock_editar").val(stock);
        $("#precio_editar").val(precio);
        $("#categoria_editar").val(categoria);
    });

    // Se oculta el formulario al hacer clic fuera de él
    $(document).mouseup(function (e) {
        var formulario = $("#formularioAgregar");
        if (!formulario.is(e.target) && formulario.has(e.target).length === 0) {
            formulario.hide();
        }
    });

});