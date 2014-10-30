$(document).ready(function(){

    $('#template-main').datagrid({
        queryParams:{ 'list-type':'1'},
        url:'/tasks/list-tasks/',

        title:'项目发布任务列表',
        fit:true,
        iconCls:'icon-filter',
        fitColumns:true,
        rownumbers:true,
        collapsible:true,
        pagination:true,
        loadMsg:"加载中,请稍候...",
        singleSelect:true,
        striped:true,
        columns:[[
//            {field:'temp-id':title:'ID',with 5},
//            {field:'pro-id', title:'pro_id'},
//            {field:'backup-dir', title:'backup'},
            {field:'temp-name', title:'模板名称', width:40},
            {field:'task-target', title:'目标项目', width:40},
            {
                field:'target-type',
                title:'发布类型',
                width:40,
                formatter:function(value, row, index){
                    if (value == '1') {
                        return '按项目发布'
                    }
                    if (value == '2') {
                        return '指定服务器发布'
                    }
                }
            },
            {
                field:'is-backup',
                title:'保留备份',
                width:40,
                formatter:function(value, row, index){
                    if (value == '0') {
                        return "无备份"
                    } else {
                        return "有备份"
                    }
                }
            },
            {
                field:'login-user',
                title:'登录用户',
                width:40,
                formatter:function(value, row, index) {
                    if (value == '') {
                        return '未指定'
                    } else {
                        return value
                    }
                }
            },
            {field:'add-args', title:'额外参数', width:40},
            {field:'source-dir', title:'源目录', width:40},
            {field:'temporary-dir', title:'临时目录', width:40},
            {field:'target-dir', title:'目标目录', width:40},
            {field:'exclude-files', title:'忽略文件', width:80},
            {field:'after-task', title:'发布后操作', width:40},
            {field:'thread-count', title:'线程', width:15},
            {
                field:'operation',
                title:'操作', width:20,
                align:'center',
                formatter:function(value, row, index){
//                    return "<a href='javascript:void(0)' onclick='open_task(" + index + ",create)'>生成任务</a>"
                    return "<a href='javascript:void(0)' onclick='open_task(" + index + ",\"create\")'>生成任务</a>"
                }
            }
        ]],
        onSelect:function(rowIndex, rowData) {
            $('#btn-update').linkbutton('enable')
            $('#btn-del').linkbutton('enable')
        },
        onDblClickRow:function () {
            var row = $('#template-main').datagrid('getSelected')
            var index = $('#template-main').datagrid('getRowIndex', row)
            open_task(index, 'update')
        },
        toolbar:[{
            id:'btn-add',
            text:'添加',
            iconCls:'icon-add',
            handler:function(){
                open_deploy_add()
            }
        },{
            id:'btn-update',
            text:"更新",
            iconCls:'icon-edit',
            disabled:true,
            handler:function() {
                var row = $('#template-main').datagrid('getSelected')
                var index = $('#template-main').datagrid('getRowIndex', row)
                open_task(index, 'update')
            }
        },'-',{
            id:'btn-del',
            text:'删除',
            iconCls:'icon-clear',
            disabled:true,
            handler:function(){
                $.messager.confirm('删除确认', '请确认需要删除该任务信息!<br><br>该操作将不可撤销!', function(r){
                    if (r){
                        var val = $('#template-main').datagrid('getSelected')
                        if (val) {
                            var sid=val['temp-id']
                            $.post('/tasks/delete-task/',
                                {'task-id':sid},
                                function(data, status) {
                                    if(status == 'success' && data['status'] == 'success') {
                                        alert("删除成功!")
                                        $('#template-main').datagrid('reload')
                                    } else {alert(data['data'])}
                                })
                        }
                    }
                });
            }
        }]
    })
    var p = $('#template-main').datagrid('getPager');
    $(p).pagination({
        pageSize:10,
        pageList:[10,30,50,100],
        beforePageText:'第',
        afterPageText:'页 共 {pages} 页',
        displayMsg:'当前显示 {from} - {to} 条记录   共 {total} 条记录'
    })
})

function open_task(index, type) {
    show_tips()
    $('#btn-1').hide()
    $('#btn-2').hide()
    $('#btn-3').hide()
    $('#template-edit').dialog('open')
    var val = $('#template-main').datagrid('getRows')[index]
    $('#task-id').val(val['temp-id'])
    $('#template-name-edit').val(val['temp-name'])
    $('#target-project-id').val(val['pro-id'])
    $('#target-project-edit').val(val['task-target'])
    $('#thread-count-edit').numberbox('setValue',val['thread-count'])
    $('#backup-dir-edit').val(val['backup-dir'])
    if (val['is-backup'] == 1) {
        $('#is-save-backup').attr('checked','true')
    } else {
        $('#backup-dir-edit').attr('disabled', 'disabled')
    }
    $('#login_name').val(val['login-user'])
    $('#add-args').val(val['add-args'])
    $('#source-dir').val(val['source-dir'])
    $('#temporary-dir').val(val['temporary-dir'])
    $('#target-dir').val(val['target-dir'])
    $('#exclude-files-edit').val(val['exclude-files'])
    $('#after-operation-edit').val(val['after-task'])
    if (type == 'create') {
        $('#template-edit').dialog('setTitle','任务确认')
        $('#btn-1').show()
        $('#btn-2').show()
        $('#div1').hide()
        $('#div2').hide()

        $('#thread-count-edit').numberbox('disable')
        $('#exclude-files-edit').attr('disabled','disabled')
        $('#target-dir').attr('disabled','disabled')
        $('#source-dir').attr('disabled','disabled')
        $('#temporary-dir').attr('disabled','disabled')
        $('#add-args').attr('disabled','disabled')
        $('#login_name').attr('disabled','disabled')
        $('#is-save-backup').attr('disabled', 'disabled')
        $('#after-operation-edit').attr('disabled','disabled')
    }
    if (type == 'update') {
        $('#btn-3').show()
        $('#div1').show()
        $('#div2').show()
        $('#deploy-type').val(val['target-type'])
        $('#after-operation-edit').removeAttr('disabled')
        $('#thread-count-edit').numberbox({disabled:false})
    }
}

function open_deploy_add() {
    show_tips()
    $('#template-add').dialog('open')
    $('#target-project').combobox({
        onBeforeLoad:function(param) {
            param.list_type = 1
        },
        url:'/project/list-projects/'
    })
}

function commit_deploy_item() {
    if ($('#template-add-form').form('validate')){
        $.post('/tasks/add-task/',
            $('#template-add-form').serialize(),
            function(data, status) {
                if (status == 'success') {
                    alert('添加成功')
                    $('#template-add').dialog('close')
                    $('#template-main').datagrid('reload')
                }
            })
    } else {return false}
}

function do_cancel(bid) {
    $(bid).dialog('close')
}

function add_task_to_list() {
    var task_id = $('#task-id').val()
    $.post('/tasks/add-tasks-to-list/',
        {'task-id' : task_id},
    function(data, status) {
        if (status == 'success' && data['status'] == 'success') {
            alert('任务生成成功')
            $('#template-edit').dialog('close')
        } else {
            alert('生成失败，请稍后再试')
        }
    })
}

function update_commit(do_alert) {
    if ($('#template-edit-form').form('validate')) {
        $.post('/tasks/update-task/',
        $('#template-edit-form').serialize(),
        function(data, status) {
            if (status == 'success') {
                if (do_alert == 0) {
                    alert('修改成功')
                    $('#template-edit').dialog('close')
                    $('#template-main').datagrid('reload')
                } else {
                    $('#template-main').datagrid('reload')
                }
            }
        })
        return true
    } else {return false}
}

function change_deploy_type(type, idc, host) {
    if ($(type).val() == '1') {
        $(idc).combobox('disable')
        $(host).combobox('disable')
    } else {
        $(idc).combobox({
            url:'/resource/get-idcs/',
            disabled:false,
            onSelect:function(record) {
                $(host).combobox('clear')
                $(host).combobox({
                    onBeforeLoad:function(param) {
                        param.idc = record.id
                    },
                    url:'/resource/get-ips/',
                    disabled:false
                })
            }
        })
    }
}

function show_tips() {
    $('.login-user-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">指定登录用户<br><br>如不指定，以服务器配置用户登录</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })

    $('.source-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">指定代码源目录</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })

    $('.temporary-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">如登录用户不能直接操作目标目录<br><br>指定该目录作为在服务器上的临时中转目录</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })

    $('.target-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">代码将发布到服务器上的目录信息</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })

    $('.exclude-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">不发布的目录和文件：<br><br>每行一个，相对于源目录的路径</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })

    $('.after-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">shell指令：<br><br>将在对每台服务器代码发布完成后执行。</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })

    $('.add-args-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">该发布底层调用系统 rsync指令：<br><br>默认参数 -azx</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })
    
    $('.backup-dir-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">指定备份存储位置(绝对路径)</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })
}

function is_deploy_as_hosts(type, idc, host) {
    if (!$(type).is(":checked")) {
        $(idc).combobox('disable')
        $(host).combobox('disable')
    } else {
        $(idc).combobox({
            url:'/resource/get-idcs/',
            disabled:false,
            onSelect:function(record) {
                $(host).combobox('clear')
                $(host).combobox({
                    onBeforeLoad:function(param) {
                        param.idc = record.id
                    },
                    url:'/resource/get-ips/',
                    disabled:false
                })
            }
        })
    }
}

function is_backup(is_checked, backup_dir) {
    if (!$(is_checked).is(":checked")) {
        $(backup_dir).attr('disabled', 'disabled')
    } else {
        $(backup_dir).removeAttr('disabled')
    }
}












































