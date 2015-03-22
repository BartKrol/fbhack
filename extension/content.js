function convertImgToBase64(url, callback, outputFormat) {
    var canvas = document.createElement('CANVAS');
    var ctx = canvas.getContext('2d');
    var img = new Image;
    img.crossOrigin = 'Anonymous';
    img.onload = function () {
        canvas.height = img.height;
        canvas.width = img.width;
        ctx.drawImage(img, 0, 0);
        var dataURL = canvas.toDataURL(outputFormat || 'image/png');
        callback.call(this, dataURL);
        // Clean up
        canvas = null;
    };
    img.src = url;
}


function getLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(callback);
    } else {
        callback(null);
    }
}

(function () {

    getLocation(function (d) {
        console.log(d)

    });

    var scriptJ = document.createElement('script');
    scriptJ.src = chrome.extension.getURL('/bower_components/jquery/dist/jquery.min.js');
    scriptJ.onload = function () {
        var tabsJS = document.createElement('script');
        tabsJS.src = chrome.extension.getURL('/tabs.js');
        document.getElementsByTagName('head')[0].appendChild(tabsJS);
        var script = document.createElement('script');
        script.src = chrome.extension.getURL('/custom_js.js');
        document.getElementsByTagName('head')[0].appendChild(script);
    };

    document.getElementsByTagName('head')[0].appendChild(scriptJ);


    if (window.location.href.toString().indexOf('facebook') == -1) {

        //HOVER
        $('img').hover(function(){
           

            
            $(this).wrap('<div id="active-info-image"></div>');
            
            $('#active-info-image').append('<div class="info-image-overlay"><div><h1>Click for info!</h1></div></div>');
            
            $('div.info-image-overlay').click(function(event){
                event.preventDefault();
                $('div.info-image-overlay').append('<img src="' + chrome.extension.getURL("/loader2.gif") + '" id="hack-loader2" style="padding-left: 220px; padding-top: 130px;"></img>');
                convertImgToBase64($('#active-info-image img').attr('src'), function (imgData) {
                    console.log(imgData);

                    $.post('https://127.0.0.1:5000/image', {'url': imgData.split(',')[1]}, function (data) {

                        // $('div._10').remove();
                        var json = JSON.parse(data);
                        console.log(json);
                        $('body').parent().append('<div id="info-modal">'+json['html']+'</div>');

                        $('ul.tabs li').click(function () {
                            var tab_id = $(this).attr('data-tab');

                            $('ul.tabs li').removeClass('current');
                            $('.tab-content').removeClass('current');

                            $(this).addClass('current');
                            $("#" + tab_id).addClass('current');
                        });

                        $("#hack-loader2").remove();


                    });
                    
                    
                    
                });

               // console.log($('#active-info-image img'));
            });
            

            
           // $(this).parent().append('<div id="info-modal">HELLO</div>');
            
        });

    }
    else {
        //FACEBOOK SPECIFIC

        var posts = document.getElementsByClassName('_5vsi');


        for (var i = 0; i < posts.length; i++) {


            var entityButton = document.createElement('button');

            entityButton.innerText = 'Get Info';
            entityButton.className = 'fbhack-button get-info-button';
            entityButton.id = "g" + i.toString();
            entityButton.onclick = function (event) {

                var j = parseInt(event.target.id.substring(1));
                console.log(event.target.id);
                var text = $('div.userContent')[j].innerText;

                $.getJSON('https://127.0.0.1:5000/entity?text=' + encodeURI(text), function (data) {
                    console.log(data);
                    if (data['status'] !== 'error')
                        document.getElementsByClassName('_5vsi')[j].innerHTML += data['html'];
                });

            };

            posts[i].appendChild(entityButton);
        }


        setInterval(function () {

            try {

                if (document.getElementById('info-data') == null) {


                    var box = document.getElementById('fbPhotoSnowliftViews');
                    box.innerHTML += '<div id="info-data"><div id="info-results"></div></div>';

                    var link = document.createElement('button');
                    link.innerText = 'Get Info';
                    link.className = 'fbhack-button get-info-button';
                    link.onclick = function () {

                        var img = $('img.spotlight').attr('src');
                        box.innerHTML += '<img src="' + chrome.extension.getURL("/loader.gif") + '" id="hack-loader" style="padding-left: 110px"/>';
                        $("button.get-info-button").fadeOut('slow');
                        convertImgToBase64(img, function (imgData) {
                            console.log(imgData);

                            $.post('https://127.0.0.1:5000/image', {'url': imgData.split(',')[1]}, function (data) {

                                // $('div._10').remove();
                                var json = JSON.parse(data);
                                console.log(json);
                                var results = document.getElementById('info-results');
                                results.innerHTML = json['html'];

                                $('ul.tabs li').click(function () {
                                    var tab_id = $(this).attr('data-tab');

                                    $('ul.tabs li').removeClass('current');
                                    $('.tab-content').removeClass('current');

                                    $(this).addClass('current');
                                    $("#" + tab_id).addClass('current');
                                });

                                $("#hack-loader").remove();


                            });
                        });

                    };

                    box.appendChild(link);

                }
            }
            catch (e) {
                //console.log(e);

            }
        }, 1000);


    }


})();

