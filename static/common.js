function setCookie(key, value, iDay) {
    var oDate = new Date();
    oDate.setDate(oDate.getDate() + iDay);
    document.cookie = key + '=' + value + ';expires=' + oDate;
}
function removeCookie(key) {
    setCookie(key, '', -1)
}
function getCookie(key) {
    var cookieArr = document.cookie.split('; ');
    for (var i = 0; i < cookieArr.length; i++) {
        var arr = cookieArr[i].split('=');
        if (arr[0] === key) {
            return arr[1];
        }
    }
    return false;
}
var prompt = function (message, style, time){
    style = (style === undefined) ? 'alert-success' : style;
    time = (time === undefined) ? 1200 : time;
    $('<div>')
        .appendTo('body')
        .addClass('alert-prompt ' + style)
        .html(message)
        .show()
        .delay(time)
        .fadeOut();
};

var prompt_success = function(message, time)
{
    prompt(message, 'alert-success-prompt', time);
};
var prompt_fail = function(message, time){
    prompt(message, 'alert-danger-prompt', time);
};
var prompt_warning = function(message, time){
    prompt(message, 'alert-warning-prompt', time);
};

var prompt_info = function(message, time){
    prompt(message, 'alert-info-prompt', time);
};