

$(document).ready( function () {
    $('#dados').DataTable();
} );

$(document).ready(function(){
    $("#pesquisa").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#res .entrada").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });



  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  })


  $(document).getElementById('langButton').addEventListener('click', function() {
    const selectElement = document.getElementById('languageSelect');
    const selectedLanguage = selectElement.options[selectElement.selectedIndex].value;
    console.log('Selected language:', selectedLanguage);
  });