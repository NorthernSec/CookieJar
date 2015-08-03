$(document).ready(function(){
  var allCookies;
  var selectedC=[];

  $.getJSON('/_query', {
    domain:"", name:"", id:"", value:"", browser:"", user:""
  }, function(data){
    allCookies=data['results'];
    fillTable(allCookies);
  })

  $('#actionfield').append('<button id="inject" class="btn btn-default">Inject!</button>');
  $('#inject').click(function(){
    var items=[];
    $('[id^="chk:"]:checked').each(function(){ items.push(this.id) });
    var toSend=items;
    for(x in items){
      toSend=$.grep(toSend, function (item){ return item.indexOf(items[x]+"|") !== 0; });
    }
    if(toSend.length == 0){alert("Please select where to inject the cookies to!");return;}
    if(selectedC.length == 0){alert("Please select cookies to inject!");return;}
    $.getJSON('/_inject', {inject: toSend.toString(), cookies:selectedC.toString()}, function(data){
      $("#status").empty();
      $("#status").removeClass();
      if(data['inject']=="success"){
        $("#status").addClass("alert alert-success");
        $("#status").append("<span class='glyphicon glyphicon-ok-sign'></span>");
        $("#status").append(" Cookies succesfully injected!");
      }else{
        $("#status").addClass("alert alert-danger");
        $("#status").append("<span class='glyphicon glyphicon-remove-sign'></span>");
        if(data['success'].length>0){
          $("#status").append(" Cookies succesfully injected into: <br /><ul>");
          for(x in data['success']){
            $("#status").append("<li>"+data['success'][x]+"</li>"); }
          $("#status").append("</ul><br />");
        }
        $("#status").append(" Failed to inject the cookies to: <br /> <ul>");
        for(x in data['failures']){
          $("#status").append("<li>"+data['failures'][x]+"</li>"); }
        $("#status").append("</ul>");
      }
    })
  });

  $("#search").on('input propertychange paste',function(){
    s="###"
    cookies=[]
    text = $("#search").val();
    if (text.length==0){cookies=allCookies}
    else{
      for(c in allCookies){
        d=allCookies[c];
        if((d['host']+s+d['name']+s+d['user']).indexOf(text)>-1){cookies.push(d);}
      }
    }
    fillTable(cookies);
  })
  function fillTable(data){
    $('#searchresult > tbody').empty();
    for(j=0;j<data.length;j++){
      i=data[j];
      if(selectedC.indexOf(i['id'].toString())>-1){chk='<input type="checkbox" id="chk:'+i['id']+'" checked>';
      }else{ chk='<input type="checkbox" id="cookie-'+i['id']+'">' }
      $('#searchresult > tbody').append('<tr><td>'+chk+'</td><td>'+i['host']+'</td><td>'+i['name']+'</td><td>'+i['user']+'</td></tr>');
    }
    $('[id^="cookie-"]').change(function(){
      var id = $(this).attr("id");
      var iid= id.replace("cookie-", "");
      if($('#'+id).is(":checked")){ if(selectedC.indexOf(iid)<0){selectedC.push(iid)};}else{ if(selectedC.indexOf(iid)>=0){selectedC.pop(iid)}; }
    });
  }
})


