$(document).ready(function(){
    $("#header0").load("./reuse/header.htm");   
    $("#header1").load("./reuse/header_en.htm");   
    $("#myindicators").load("./reuse/slide_indicators.htm");
    $("#myinner").load("./reuse/slide_inner.htm");
    $("#publist").load("./reuse/publist.htm");
    $("#footer0").load("./reuse/footer.htm");  
    $("#footer1").load("./reuse/footer_en.htm");  
    $.get("./reuse/gotop.htm",function(data){$("body").append(data);});   
 });