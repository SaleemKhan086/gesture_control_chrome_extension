window.onload = function() {
    var btnStart = document.getElementById("start");
    var btnStop = document.getElementById("stop");

    btnStart.addEventListener('click',startExtension);
    btnStop.addEventListener('click',stopExtension);
};

function startExtension(){
 if($("#start").hasClass('disabled'))
 {
   $("#alert").fadeIn();
   $("#alert").fadeOut(3000);
   return ;
 }
 chrome.extension.sendMessage({
        txt: "start",
        previous_tab:document.getElementById("previous_tab").value,
        next_tab:document.getElementById("next_tab").value,
        scroll_up:document.getElementById("scroll_up").value,
        scroll_down:document.getElementById("scroll_down").value,
        zoom_out:document.getElementById("zoom_out").value,
        zoom_in:document.getElementById("zoom_in").value,
        perform:3
    });
}
function stopExtension(){
  chrome.extension.sendMessage({
        txt: "stop"
    });
}

var switchStatus = false;

$(document).ready(function() {
  $("select").on("change", function() {
    var count=0;
    $("select").not(this).children("option:contains(" + $(this).children("option:selected").text() + ")").hide();
    $("select").each(function (){
      if($(this).val()== "none")
        count++;
    });
    if(count>0)
    {
      $("#start").addClass('disabled');
    }
    else {
        $("#start").removeClass('disabled');
    }
  });
 //  $("#reset").click( function() {
   //   $("select option").show();
    //});
});





