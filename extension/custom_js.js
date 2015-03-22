function get_more_info()
{
    $.getJSON('http://127.0.0.1:5000/image?url=http://www.replacebase.co.uk/ekmps/shops/replacebase/resources/Design/macbook-pro.jpg', function(data){
        console.log(data);
        
    });
    
}

(function(history){
    var pushState = history.pushState;
    history.pushState = function(state) {
        if (typeof history.onpushstate == "function") {
            history.onpushstate({state: state});
        }
        $('#info-data').remove();
        $('button.fbhack-button').remove();
        // maybe call onhashchange e.handler
        return pushState.apply(history, arguments);
    }
})(window.history);