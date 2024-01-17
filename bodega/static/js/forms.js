$(document).ready(function () {
    var contadorProductos = 1;

    $("#agregarOtroProducto").click(function () {
        contadorProductos++;
        var nuevoProducto = $(".producto:first").clone();
        nuevoProducto.find("input, select").val("");
        nuevoProducto.find("label[for^='nombreProducto']").attr("for", "nombreProducto" + contadorProductos);
        nuevoProducto.find("input[id^='nombreProducto']").attr("id", "nombreProducto" + contadorProductos);
        nuevoProducto.find("label[for^='precio']").attr("for", "precio" + contadorProductos);
        nuevoProducto.find("input[id^='precio']").attr("id", "precio" + contadorProductos);
        nuevoProducto.find("label[for^='cantidad']").attr("for", "cantidad" + contadorProductos);
        nuevoProducto.find("input[id^='cantidad']").attr("id", "cantidad" + contadorProductos);
        nuevoProducto.find("label[for^='categoria']").attr("for", "categoria" + contadorProductos);
        nuevoProducto.find("select[id^='categoria']").attr("id", "categoria" + contadorProductos);
        nuevoProducto.find("label[for^='proveedor']").attr("for", "proveedor" + contadorProductos);
        nuevoProducto.find("select[id^='proveedor']").attr("id", "proveedor" + contadorProductos);

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