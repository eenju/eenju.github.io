        $(document).ready(function(){
            $("#header0").load("../reuse/header.htm");   
            $("#myindicators").load("./reuse/slide_indicators.htm");
            $("#myinner").load("./reuse/slide_inner.htm");
           $("#publist").load("./reuse/publist.htm");
            $("#footer0").load("./reuse/footer.htm");  
            $.get("./reuse/gotop.htm",function(data){$("body").append(data);});   
        });