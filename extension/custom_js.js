function get_more_info()
{
    $.getJSON('http://127.0.0.1:5000/image?url=http://www.replacebase.co.uk/ekmps/shops/replacebase/resources/Design/macbook-pro.jpg', function(data){
        console.log(data);
        
    });
    
}