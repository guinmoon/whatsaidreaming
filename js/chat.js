function update_chat(){
    let chat_msg = $(`<a class="a_chat_message" href="${glaery_dir_name}/${encodeURI(image.f_name)}">
    <p class="chat_message">${current_image.prompt}</p>
    </a>`);
    chat_msg.css('opacity',0);
    var hello_chat=$("#hello_chat")
    if (hello_chat[0].childNodes!=undefined && hello_chat[0].childNodes.length>=chat_max_msg_count){
        hello_chat[0].removeChild(hello_chat[0].childNodes[0]);
        // hello_chat[0].childNodes[0].css('height',0);
    }
    hello_chat.append(chat_msg);            
    setTimeout(function() {
        chat_msg.css('opacity',0.9);
    }, 500);

}