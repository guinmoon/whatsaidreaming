var i_was_here=false;
function update_spcae_height(){
    $("#stars").css('height', $("#galery").css('height')); 
    $("#twinkling").css('height', $("#galery").css('height'));
    $("#clouds").css('height', $("#galery").css('height'));
}
function reset_spcae_height(){
    $("#stars").css('height', '100vh'); 
    $("#twinkling").css('height', '100vh');
    $("#clouds").css('height', '100vh');
}

window.onpopstate = function(e){
    load_template(e.state.template_name)
};


function load_template(template_name){    
    clearInterval(flying_interval);
    clearInterval(galery_interval);     
    about_page = false;
    $.ajax({
        url: `/templates/${template_name}`,
        type: 'GET',        
        success: function(res) {
            is_i_was_her();
            $("#main_container").css('opacity',0);            
            var delayInMilliseconds = 800;
            setTimeout(function() {
                $("#main_container").empty();
                $("#main_container").append(res);
                $("#main_container").css('opacity',1);
            }, delayInMilliseconds);
            reset_spcae_height();
            // document.title = "What's AI dreaming?";
            window.history.pushState({"template_name":template_name},"", "");
        }
    });
    
}

function update_player_width(){
    $("#player").css('width', $("#galery").css('height')); 
}

$(document).ready(function(){    
    document.addEventListener("scroll", (event) => {
        update_spcae_height();
    });
    is_i_was_her();
    // alert(is_i_was_her());

});


function is_i_was_her(){
    i_was_here=getCookie('i_was_here');
    if (i_was_here==undefined||i_was_here==""){
        salt=Math.floor(Math.random() * 10)
        setCookie('i_was_here', (Date.now())+salt,365);
        return false;
    }else{
        return true;
    }
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  
 