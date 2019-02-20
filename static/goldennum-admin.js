$('#startRoom').click(
    function tryStartRoom() {
        var secret = $('input[name="secret"]').val();
        var roomid = $('input[name="roomid"]').val();
        var roomtime = $('input[name="roomtime"]').val();
        var json = {
            "key"   : secret,
            "roomid": roomid,
            "time"  : roomtime
        };
        $.get('startRoom/', json, function(data, status){
            if (data == "Invalid request"){
                prompt_warning("参数错误", 2000);
            }else if (data == "Certification failed"){
                prompt_fail("管理密码错误", 2000);
            }else{
                prompt_success(data, 2000);
            }
        })
    }
)

$('#stopRoom').click(
    function tryStopRoom() {
        var secret = $('input[name="secret"]').val();
        var roomid = $('input[name="roomid"]').val();
        var json = {
            "key"   : secret,
            "roomid": roomid,
        };
        $.get('stopRoom/', json, function(data, status){
            if (data == "Invalid request"){
                prompt_warning("参数错误", 2000);
            }else if (data == "Certification failed"){
                prompt_fail("管理密码错误", 2000);
            }else{
                prompt_success(data, 2000);
            }
        })
    }
)