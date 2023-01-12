var global_galery={};
var current_image={};
flying_opacity=1;

function update_galery(){
    $.ajax({
        url: `${glaery_dir_name}/today.json`,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            global_galery= res;   
            console.log(global_galery);         
        }
    }); 
}


function change_flying_img(){
    gallery_len=global_galery.images.length;
    image=global_galery.images[Math.floor(Math.random() * gallery_len-1)];
    current_image = image;
    flying_image_div=$("#flying_image");
    if(about_page){
        update_about();
    }else{
        update_chat();
    }
    var new_src = `${glaery_dir_name}/${encodeURI(image.f_name)}`;
    flying_1_div=$("#flying_1")  
    flying_0_div=$("#flying_0")            
    var values =  $("#flying_1").css('transform').split('(')[1].split(')')[0].split(',');
    var angle = Math.round(Math.atan2(values[1], values[0]) * (180/Math.PI));       
    var degr =0;
    if (Math.floor(Math.random() * 2)>0)
        degr=angle+Math.floor(Math.random() * 30);
    else
        degr=angle-Math.floor(Math.random() * 30);
    flying_1_div.css('transform', 'rotate('+degr+'deg)'); 
    flying_0_div.css('transform', 'rotate('+degr+'deg)');
    flying_1_div.css('opacity', 0);        
    flying_0_div.css('opacity', flying_opacity);
    flying_0_div.attr("src",new_src)
    flying_0_div.attr("alt",`${image.prompt}`)
    var delayInMilliseconds = 1500;
    setTimeout(function() {
        flying_1_div.attr("src",new_src)
        flying_1_div.css('opacity', flying_opacity);
    }, delayInMilliseconds);
}

function init_flying_images(){    
    $.ajax({
        url: `${glaery_dir_name}/today.json`,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            global_galery= res;
            // console.log(res);            
            var img_num=0;
            gallery_len=res.images.length;
            image=res.images[Math.floor(Math.random() * gallery_len-1)];
            current_image = image;
            flying_image_div=$("#flying_image");
            flying_image_div.append(`
                <a href="${glaery_dir_name}/${encodeURI(image.f_name)}">
                <img id="flying_0" class="flying_img" src="${glaery_dir_name}/${encodeURI(image.f_name)}" alt="${image.prompt}">
                <img id="flying_1" class="flying_img" src="${glaery_dir_name}/${encodeURI(image.f_name)}" alt="${image.prompt}">
                </a>`);
            var gegr=0;
            if (Math.floor(Math.random() * 2)>0)
                degr=Math.floor(Math.random() * 30);
            else
                degr=-Math.floor(Math.random() * 30);
            $("#flying_1").css('transform', 'rotate('+degr+'deg)'); 
            $("#flying_0").css('transform', 'rotate('+degr+'deg)');
            $("#flying_1").css('opacity', flying_opacity);
            $("#flying_0").css('opacity', 0);
            update_chat();
            update_spcae_height();
        }
    });
    galery_interval = window.setInterval(function(){ update_galery();},60000);
    flying_interval = window.setInterval(function(){ change_flying_img();}, image_change_delay);
}





