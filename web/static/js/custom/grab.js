$(document).ready(function(){
  $('#actionfield').append('<button id="grab" class="btn btn-default">Grab!</button>');
  $('#grab').click(function(){
    var items=[];
    $('[id^="chk:"]:checked').each(function(){ items.push(this.id) });
    var toSend=items;
    for(x in items){
      toSend=$.grep(toSend, function (item){ return item.indexOf(items[x]+"|") !== 0; });
    }
    $.getJSON('/_grab', {grab: toSend.toString()}, function(data){
      $("#status").empty();
      $("#status").removeClass();
      if(data['store']=="success"){
        $("#status").addClass("alert alert-success");
        $("#status").append("<span class='glyphicon glyphicon-ok-sign'></span>");
        $("#status").append(" Found "+data['all']+" cookies, of which "+data['new']+" are new.");
      }else{
        $("#status").addClass("alert alert-danger");
        $("#status").append("<span class='glyphicon glyphicon-remove-sign'></span>");
        $("#status").append(" Found "+data['all']+" cookies, but we could not save them to the database.");
      }
      if(data['failures'].length > 0){
        $("#status").append("<br /><b>Failed to grab the following cookies:</b><br /><ul>");
        for(x in data['failures']){
          $("#status").append("<li>"+data['failures'][x]+"</li>"); }
        $("#status").append("</ul>");
      }
    })
  });
})

