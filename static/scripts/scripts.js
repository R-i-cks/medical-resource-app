function delete_conceito(designacao){ 
    $.ajax({
        url: '/conceitos/' + designacao,
        type: 'DELETE',
        success: function(result){
            // Algo c o result
            alert('Deleted!')
            window.location.href = '/conceitos';
        }
    });
    
}

$(document).ready( function () {
    $('#table_id').DataTable();
} );