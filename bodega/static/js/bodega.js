$(document).ready(function () {
    $('#productoModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var productoNombre = button.data('producto');
        var proveedorNombre = button.data('proveedor');
        
        $('#productoNombre').text(productoNombre);
        $('#proveedorNombre').text(proveedorNombre);
    });
    
    $("#mostrarBotones").click(function () {
        $(".opciones-adicionales").slideToggle();
    });

});