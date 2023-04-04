
var about_messages=["Hi. The content on this site was generated using text2text, text2img and text2music neural networks.",
"Content is automatically added every 20 minutes and is fully updated every day.",
"<a href='https://habr.com/ru/users/guinmoon/posts/'>Here you can look at the leather one that created me.</a>",
"<a href='https://github.com/guinmoon'>And here.</a>"]
function update_chat(){
    
    var hello_chat=$("#hello_chat")
    if (hello_chat[0].childNodes!=undefined && hello_chat[0].childNodes.length>=chat_max_msg_count){
        return;
        // hello_chat[0].removeChild(hello_chat[0].childNodes[0]);
        // hello_chat[0].childNodes[0].css('height',0);
    }
    let chat_msg = $(`<p class="a_chat_message" >
    <p class="chat_message">${about_messages[hello_chat[0].childNodes.length-1]}</p>
    </p>`);
    chat_msg.css('opacity',0);
    hello_chat.append(chat_msg);            
    setTimeout(function() {
        chat_msg.css('opacity',0.9);
    }, 500);
}