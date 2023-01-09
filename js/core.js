function update_spcae_height(){
    $("#stars").css('height', $("#galery").css('height')); 
    $("#twinkling").css('height', $("#galery").css('height'));
    $("#clouds").css('height', $("#galery").css('height'));
}

function load_template(template_name){    
    clearInterval(flying_interval);
    clearInterval(galery_interval);    
    $.ajax({
        url: `/templates/${template_name}`,
        type: 'GET',        
        success: function(res) {
            $("#main_container").css('opacity',0);            
            var delayInMilliseconds = 800;
            setTimeout(function() {
                $("#main_container").empty();
                $("#main_container").append(res);
                $("#main_container").css('opacity',1);
            }, delayInMilliseconds);
        }
    });
    
}

function update_player_width(){
    $("#player").css('width', $("#galery").css('height')); 
}

