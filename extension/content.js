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


(function () {

    var scriptJ = document.createElement('script');
    scriptJ.src = chrome.extension.getURL('/bower_components/jquery/dist/jquery.min.js');
    document.getElementsByTagName('head')[0].appendChild(scriptJ);

    var script = document.createElement('script');
    script.src = chrome.extension.getURL('/custom_js.js');
    document.getElementsByTagName('head')[0].appendChild(script);

    setInterval(function () {
        try {

            if (document.getElementById('info-data') == null) {
                var box = document.getElementById('fbPhotoSnowliftViews');
                box.innerHTML += '<div id="info-data" style="background: rgb(228, 229,233); padding: 3px"><div><b>Info</b></div><div id="info-results"></div></div>';

                var link = document.createElement('button');
                link.innerText = 'Get Info';
                link.onclick = function () {

                    var img = $('img.spotlight').attr('src');

                    convertImgToBase64(img, function (imgData) {
                        console.log(imgData);


                        $.post('https://127.0.0.1:5000/image',{'url': imgData.split(',')[1]}, function (data) {
                            var json = JSON.parse(data);
                            var results = document.getElementById('info-results');
                            results.innerHTML = json['html'];

                        });
                    });

                }

                box.appendChild(link);

            }
        }
        catch (e) {
            //console.log(e);

        }
    }, 1000);
})();

