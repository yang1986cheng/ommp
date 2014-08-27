$(document).ready(function() {
    $('.idc-detail-list input').each(function() {$(this).attr('disabled', 'true')})
    $("div.idc-noitem").click(function(){
        $("div.mask").show();
        $("div.add-idc").show();
    });

    $("input.add-cancel").click(function() {
        $("div.mask").hide();
        $("div.add-idc").hide();
    });

    $('div.idc-item').click(function() {
        var vv = $(this).children(".idc-item-hidden").val();
        $.post("/resource/idc-detail/",
            {"idc-id" : vv},
            function(data, status) {
                if (status == "success") {
                    $('#idc-detail-name').attr('value',data['idc_name']);
                    $('#idc-detail-zipcode').numberbox('setValue',data['zipcode']);
                    $('#idc-detail-contact').attr('value',data['contact']);
                    $('#idc-detail-phone').numberbox('setValue',data['phone']);
                    $('#idc-detail-email').attr('value',data['email']);
                    $('#idc-detail-date').datebox('setValue',data['end_date']);
                    $('#idc-detail-address').attr('value',data['address']);
                    $('.idc-detail-list input').each(function() {$(this).attr('disabled', 'true')})

                    idc_name = "机房详情-" + data['idc_name']
                    $('#idc-detail').dialog({title:idc_name})
                    $("#idc-detail").window("open");
                    $("#idc-detail").window("center");
                } else {alert("获取资料失败，请重试!")}
            })
    })

    $('#add-idc-div').dialog({
        width:200,
        height:540,
        title:'添加机房信息',
        closed : true,
        minimizable:false,
        maximizable:false,
        closable:true,
        modal:true,
        iconCls:'icon-add',
        buttons:[{
            text:'Add',
            iconCls:'icon-add',
            handler:function() {
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
            }
        },{
            text:'Cancel',
            iconCls:'icon-cancel',
            handler:function(){$('#add-idc-div').window('close')}
        }]
    })



    $('#idc-detail').dialog({
        width:800,
        height:450,
        title:'机房详细信息',
        closed : true,
        minimizable:false,
        maximizable:false,
        closable:true,
        modal:true,
        iconCls:'icon-add',
        toolbar:[{
            text:'修改',
            iconCls:'icon-edit',
            handler:function() {
                $('.idc-detail-list input').each(function() {$(this).removeAttr('disabled')}),
                $()
            }
        },'-',{
            text:'保存',
            iconCls:'icon-save',
            handler:function(){
                $('.idc-detail-list input').each(function() {$(this).attr('disabled', 'true')}),
                    $.post("/resource/add-idc/",
                    $("form.add-form").serialize(),
                    $("form.add-form").serialize(),
                    function(data, status) {
                        if (status == "success") {
                            alert("修改成功!")
                            parent.location.reload();
                        } else {
                            alert("添加失败!")
                        }
                    })
            }
        },'-',{
           text:'删除',
            iconCls:'icon-no',
            handler:function() {check_confirm('删除确认', '确定要删除该机房？<br><br>该操作不可撤销')}
        }],
        buttons:[{
            text:'OK',
            iconCls:'icon-ok',
            handler:function() {$('#idc-detail').window('close')}
        }]
    })
});



function open_add_idc_div() {
    $('#add-idc-div').window("open");
    $('#add-idc-div').window('center')
}

function close_add_idc_div() {
    $('#add-idc-div').window('close');
}

function check_confirm(title, message){
    $.messager.confirm(title, message + '！', function(r){
        if (r){
            alert('confirmed:'+r);
        }
    });
}