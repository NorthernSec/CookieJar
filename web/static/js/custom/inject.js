$(document).ready(function(){
  var allCookies;
  $.getJSON('/_query', {
    domain:"", name:"", id:"", value:"", browser:"", user:""
  }, function(data){
    allCookies=data['results'];
    alert(allCookies)
    fillTable(allCookies);
  })

  $("#search").change(function(){
    var cookies=[]
    var text = $("#search").val();
    for(c in allCookies){
      if($.inArray(text, [c["host"], c["name"], c["user"]])){
        cookies.push(c);
      }
    }
    fillTable(cookies);
  })
})

function fillTable(data){
  $('#searchresult > tbody').empty();
  for(j=0;j<data.length;j++){
    i=data[j];
    $('#searchresult > tbody').append('<tr><td>'+i['host']+'</td><td>'+i['name']+'</td><td>'+i['user']+'</td></tr>');
  }
}

