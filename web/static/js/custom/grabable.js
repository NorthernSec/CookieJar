$(document).ready(function(){
  $('[id^="chk:"]').change(function(){
    id=$(this).attr("id");
    if($(this).is(":checked")){
      $('[id^="'+id+'"]').prop("checked", true);
    }else{
      split=id.split("|")
      if(split.length>1){$('[id="'+split[0]+'"]').prop("checked",false);}
      if(split.length>2){$('[id="'+split[0]+"|"+split[1]+'"]').prop("checked",false);}
    }
  });
  $('#all').click(function(){$('[id^="chk:"]').prop("checked", true);});
  $('#none').click(function(){$('[id^="chk:"]').prop("checked", false);});
})
