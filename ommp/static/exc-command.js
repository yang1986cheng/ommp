$(document).ready(function(){
    $('#exc-type').combo({
        required:true,
        multiple:false,
        editable:false,
        width:120
    })
    $('#sp').appendTo($('#exc-type').combo('panel'));
    $('#sp input').click(function(){
        var v = $(this).val();
        var s = $(this).next('span').text();
        var exec_type = $("input[name='exc-type']:checked").val();
        $('#exc-type').combo('setValue', v).combo('setText', s).combo('hidePanel');
        if (exec_type == 1) {
            $('#exec-as-project').show();
            $('#exec-as-hosts').hide();
            $('#exec-idcs-list').combobox('setValue', '-1')
            $('#exec-hosts-list').combobox('setValue', '-1')
            $('#exec-project-list').combobox({
                onBeforeLoad:function(param){
                    param.list_type = 0;
                },
                url:'/project/list-projects/'
//                onSelect:function() {
//                    alert($('#exec-project-list').combobox('getValue'))
//                }
            })
        }
        if (exec_type == 2) {
            $('#exec-as-project').hide();
            $('#exec-as-hosts').show();
            $('#exec-project-list').combobox('setValue', '-1');
            $('#exec-hosts-list').combobox('clear')
            $('#exec-idcs-list').combobox({
                url:'/resource/get-idcs/',
                onSelect:function(rec) {
                    $('#exec-hosts-list').combobox({
                        onBeforeLoad:function(param) {
                            param.idc = rec.id
                        },
                        url:'/resource/get-ips/'
                    })
                }
            })
        }
    });
    $('#display-result').datagrid({
        fitColumns:true,
        rownumbers:true,
        collapsible:true,
        loadMsg:"加载中,请稍候...",
        singleSelect:true,
        columns:[[
//          {field:'exec-host-name', title:'计算机名', width:20},
            {field:'exec-ip', title:'IP', width:20},
            {field:'exec-idc', title:'所在机房', width:20},
            {field:'exec-result', title:'结果', width:140}
        ]]
    })
})

function do_exec_command() {
    if ($('#exec-command-form').form('validate')) {
        $('#display-result').datagrid({
            data:[]
        })
        $.post('/functions/exc-command-handler/',
        $('#exec-command-form').serialize(),
        function(data, status) {
            if (status == 'success') {
                $('#display-result').datagrid({
                    data:data
                })
            }
        })
    } else {return false}
}