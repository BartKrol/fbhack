(function () {

    var script = document.createElement('script');
    script.src = chrome.extension.getURL('/custom_js.js');
    document.getElementsByTagName('head')[0].appendChild(script);
    
    setInterval(function () {
        try {

            if (document.getElementById('info-data') == null) {
                var box = document.getElementById('fbPhotoSnowliftViews');
                box.innerHTML += '<div id="info-data" style="background: rgb(228, 229,233); padding: 3px"><div><b>Info</b></div><div><button onclick="get_more_info()">Show Info</button></div></div>';
            }
        }
        catch (e) {
            //console.log(e);

        }
    }, 1000);
})();