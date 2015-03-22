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

    getLocation(function(d){
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




    setInterval(function () {
        
        try {

            if (document.getElementById('info-data') == null) {
                
               
                
                var box = document.getElementById('fbPhotoSnowliftViews');
                box.innerHTML += '<div id="info-data" style="background: rgb(228, 229,233); padding: 3px"><div><b>Info</b></div><div id="info-results"></div></div>';

                var link = document.createElement('button');
                link.innerText = 'Get Info';
                link.className = 'fbhack-button';
                link.onclick = function () {

                    var img = $('img.spotlight').attr('src');
                    box.innerHTML += '<img src="' + chrome.extension.getURL("/loader.gif")+ '" id="hack-loader"/>';

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
})();

