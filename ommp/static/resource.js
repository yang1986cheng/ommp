$(document).ready(function() {
    $("div.idc-noitem").click(function(){
        $("div.mask").show();
        $("div.add-idc").show();
    });

    $("input.add-cancel").click(function() {
        $("div.mask").hide();
        $("div.add-idc").hide();
    });

    $("input.add-submit").click(function() {
        $.post("/resource/add-idc/",
            $("form.add-form").serialize(),
            function(data, status) {
                if (status == "success") {
                    alert("添加成功!")
                    parent.location.reload();
                } else {
                    alert("添加失败!")
                }
            })
    });
});
