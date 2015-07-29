$(document).ready(function(){
  var allCookies;
  $.getJSON('/_query', {
    domain:"", name:"", id:"", value:"", browser:"", user:""
  }, function(data){
    allCookies=data['results'];
    fillTable(allCookies);
  })

  $("#search").on('input propertychange paste',function(){
    var s="###"
    var cookies=[]
    var text = $("#search").val();
    if (text.length==0){cookies=allCookies}
    for(c in allCookies){
      d=allCookies[c];
      if((d['host']+s+d['name']+s+d['user']).indexOf(text)>-1){
        cookies.push(d);
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

