$(document).ready(function(){
    
    $.ajax({
        url: `https://aliceghome.online/dream/${glaery_dir_name}/${glaery_json_name}`,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log(res);
            galery_div=$("#galery") ;
            var img_num=0;
            var lazy_src="src";
            res.images.forEach((image) => {
                if (img_num>2){
                  lazy_src="data-src";
                }
                galery_div.append(`<a href="https://aliceghome.online/dream/${glaery_dir_name}/${encodeURI(image.f_name)}">
                <img class="img_main lazy" ${lazy_src}="https://aliceghome.online/dream/${glaery_dir_name}/${encodeURI(image.f_name)}" alt="${image.prompt}">
                </a>`);   
                img_num++;             
              });
              (function () {
                function logElementEvent(eventName, element) {
                  console.log(Date.now(), eventName, element.getAttribute("data-src"));
                }
        
                var callback_enter = function (element) {
                  logElementEvent("🔑 ENTERED", element);
                };
                var callback_exit = function (element) {
                  logElementEvent("🚪 EXITED", element);
                };
                var callback_loading = function (element) {
                  logElementEvent("⌚ LOADING", element);
                };
                var callback_loaded = function (element) {
                  logElementEvent("👍 LOADED", element);
                };
                var callback_error = function (element) {
                  logElementEvent("💀 ERROR", element);
                  element.src = "https://via.placeholder.com/440x560/?text=Error+Placeholder";
                };
                var callback_finish = function () {
                  logElementEvent("✔️ FINISHED", document.documentElement);
                };
                var callback_cancel = function (element) {
                  logElementEvent("🔥 CANCEL", element);
                };
        
                var ll = new LazyLoad({
                  class_applied: "lz-applied",
                  class_loading: "lz-loading",
                  class_loaded: "lz-loaded",
                  class_error: "lz-error",
                  class_entered: "lz-entered",
                  class_exited: "lz-exited",
                  // Assign the callbacks defined above
                  callback_enter: callback_enter,
                  callback_exit: callback_exit,
                  callback_cancel: callback_cancel,
                  callback_loading: callback_loading,
                  callback_loaded: callback_loaded,
                  callback_error: callback_error,
                  callback_finish: callback_finish
                });
              })();
        }
    });
    document.addEventListener("scroll", (event) => {
      update_spcae_height();
  });
});

