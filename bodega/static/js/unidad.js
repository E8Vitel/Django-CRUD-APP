$(document).ready(function () {
    $("#formularioCrearUnidad").hide();

    $("#mostrarFormulario").click(function () {
        $("#formularioCrearUnidad").fadeIn();
    });

    $(document).mouseup(function (e) {
        var formulario = $("#formularioCrearUnidad");
        if (!formulario.is(e.target) && formulario.has(e.target).length === 0) {
            formulario.hide();
        }
    });
});