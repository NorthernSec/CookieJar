$(document).ready(function(){
  $("#search").click(function(){
    $.getJSON('/_query', {
      domain: $('#domain').val().trim(),
      name:   $('#name').val().trim(),
      id:     $('#id').val().trim(),
      value:  $('#value').val().trim(),
      browser:$('#browser').val().trim(),
      user:   $('#user').val().trim()
    }, function(data){
      fillTable(data);
    })
  })
})

function fillTable(data){
  $('#data > tbody > tr').remove();
  for(i=0;i<data.length;i++){
    $('#data > tbody').append('<tr><td>'+i['domain']+'</td><td>'+i['host']+'</td><td>'+i['name']+'</td><td>'+i['browser']+'</td><td>'+i['user']+'</td><td>'+i[timejarred]+'</td></tr>');
  }
}
