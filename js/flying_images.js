$(document).ready(function(){
    global_galery={};
    $.ajax({
        url: "https://aliceghome.online/dream/galery/galery.json",
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            global_galery= res;
            // console.log(res);            
            var img_num=0;
            gallery_len=res.images.length;
            image=res.images[Math.floor(Math.random() * gallery_len-1)];
            flying_image_div=$("#flying_image");
            flying_image_div.append(`<a href="https://aliceghome.online/dream/galery/${encodeURI(image.f_name)}">
                <img id="flying_1" src="https://aliceghome.online/dream/galery/${encodeURI(image.f_name)}" alt="${image.prompt}">
                </a>`);
            degr=Math.floor(Math.random() * 180)
            $("#flying_1").css('transform', 'rotate('+degr+'deg)'); 
        }
    });
    var intervalId = window.setInterval(function(){      
      gallery_len=global_galery.images.length;
      image=global_galery.images[Math.floor(Math.random() * gallery_len-1)];
      flying_image_div=$("#flying_image");
      flying_image_div.empty();
      flying_image_div.append(`<a href="https://aliceghome.online/dream/galery/${encodeURI(image.f_name)}">
          <img id="flying_1" src="https://aliceghome.online/dream/galery/${encodeURI(image.f_name)}" alt="${image.prompt}">
          </a>`);
      degr=Math.floor(Math.random() * 180)
      $("#flying_1").css('transform', 'rotate('+degr+'deg)'); 
    }, 5000);

    // clearInterval(intervalId) 
});

