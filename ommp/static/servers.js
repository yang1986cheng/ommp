$(document).ready(function(){

    $('#svr-add-idc').combobox({
        onChange:function(newValue, oldValue) {
            $('#svr-add-cab').combobox({
                onBeforeLoad:function(param) {
                param.idcid=newValue
            },
            'url' : '/resource/get-cabs/'}
            )}
    })

    $('#svr-display-table').datagrid({
        title:'服务器列表',
        url:'/resource/get-servers/',
        fit:true,
        iconCls:'icon-filter',
        fitColumns:true,
//        nowrap:true,
//        sortName:"sum-servers",
//        sortOrder:"desc",
        rownumbers:true,
        collapsible:true,
        pagination:true,
        pageSize:30,
        loadMsg:"加载中,请稍候...",
        singleSelect:true,
        striped:true,
        columns:[[
//            {field:'svr-id':title:'ID',with 5},
//            {field:'cab-id', title:'CAB-ID'},
//            {field:'admin-id', title:'User-ID'},
//            {field:'svr-used-type', title:'usable'},
//            {field:'idc-id', title:'iid'},
//            {field:'father-id', title:'fid'},
            {field:'svr-name', title:'编号', width:40},
            {field:'idc-name', title:'所在机房', width:40},
//            {
//                field:'cab-name',
//                title:'所属机柜',
//                width:40,
//                formatter:function(value, row, index) {
//                    if (value == 0) {
//                        return '未指派'
//                    } else {
//                        return value
//                    }
//                }
//            },
            {field:'svr-size', title:'类型', width:20},
            {field:'svr-parts', title:'配置', width:60},
            {field:'svr-os', title:'操作系统', width:40},
            {field:'svr-hostname', title:'计算机名', width:40},
            {field:'svr-username', title:'登录用户', width:40},
            {field:'storage-date', title:'入库日期', width:40},
            {field:'end-date', title:'到期日期', width:40},
            {
                field:'svr-father',
                title:'父级',
                width:40,
                formatter:function(value, row, index) {
                    if (value == '无') {
                        return value + "&nbsp&nbsp&nbsp&nbsp&nbsp<span><a href='javascript:void(0)' onclick='update_father_server(" + index + ")'>指定</a></span>"
                    } else {
                        return value + "&nbsp&nbsp&nbsp&nbsp&nbsp<span><a href='javascript:void(0)' onclick='update_father_server(" + index + ")'>修改</a></span>"
                    }
                }
            },
            {
                field:'svr-usable',
                title:'状态',
                width:20,
                formatter:function(value, row, index) {
                    if (value == 0) {
                        return '测试'
                    }
                    if (value == 1) {
                        return '生产'
                    }
                    if (value == 2) {
                        return '禁用'
                    }
                    if (value == 3) {
                        return '空闲'
                    }
                }
            },
            {field:'admin-name', title:'负责人', width:20}
        ]],
        onSelect:function(rowIndex, rowData) {
            $('#btn-update').linkbutton('enable')
            $('#btn-del').linkbutton('enable')
        },
        onDblClickRow:function () {
            parts_tip()
            size_tip()
            father_tip()
            open_update_window()
        },
        toolbar:[{
            id:'btn-add',
            text:'添加',
            iconCls:'icon-add',
            handler:function(){
                parts_tip()
                size_tip()
                father_tip()
                $('#svr-add-new').dialog('open'),
                    $('#svr-admin').combobox({'url':'/resource/get-users/'}),
                    $('#svr-add-idc').combobox({'url':'/resource/get-idcs/'})
            }
        },{
            id:'btn-update',
            text:"更新",
            iconCls:'icon-edit',
            disabled:true,
            handler:function() {
                parts_tip()
                size_tip()
                father_tip()
                open_update_window()
            }
        },'-',{
            id:'btn-del',
            text:'删除',
            iconCls:'icon-clear',
            disabled:true,
            handler:function(){
                $.messager.confirm('删除确认', '请确认需要删除该机房信息!<br><br>该操作将不可撤销!', function(r){
                    if (r){
                        var val = $('#svr-display-table').datagrid('getSelected')
                        if (val) {
                            var sid=val['svr-id']
                            $.post('/resource/del-server/',
                                {'sid':sid},
                                function(data, status) {
                                    if(status == 'success' && data['status'] == 'success') {
                                        alert("删除成功!")
                                        $('#svr-display-table').datagrid('reload')
                                    } else {alert(data['data'])}
                                })
                        }
                    }
                });
            }
        }, '-', {
            id:'btn-import',
            text:'批量导入',
            iconCls:'icon-reload',
            handler:function(){
                $.messager.defaults={ok:'知道了', cancel:'太难、弃疗'}
                $.messager.alert('导入使用提示','1、支持03、07格式的Excel文件<br>' +
                    '2、每行一条服务器记录<br>' +
                    '3、每行12条信息，和列表信息一一对应<br>' +
                    '4、其中机房、状态、负责人填入对应ID<br>' +
                    '5、类型合法值包括xU、塔式、刀柜、刀片、虚拟机<br>' +
                    '6、ID可在导航栏查询<br>' +
                    '7、父级默认为无，随意填写','', function(){
                    $('#btn-import-1').window('open')
                })

            }
        }, '-', {
            id:'btn-idc-id',
            text:'机房ID',
            iconCls:'icon-help',
            handler:function(){
                $('#btn-idc-id-combobox').combobox({
                    url:'/resource/get-idcs/',
                    onSelect:function(rec){
                        alert('机房：' + rec.name + '\nID：' + rec.id)
                    }
                })
                $('#btn-idc-id-1').window('open')
            }
        }, '-', {
            id:'btn-status-id',
            text:'状态ID',
            iconCls:'icon-help',
            handler:function(){
                alert('测试：0\n生产：1\n禁用：2\n空闲：3\n')
            }
        }, '-', {
            id:'btn-admin-id',
            text:'负责人ID',
            iconCls:'icon-help',
            handler:function(){
                $('#btn-admin-id-combobox').combobox({
                    url:'/resource/get-users/',
                    onSelect:function(rec){
                        alert('机房：' + rec.username + '\nID：' + rec.id)
                    }
                })
                $('#btn-admin-id-1').window('open')
            }
        }]
    })
    var p = $('#svr-display-table').datagrid('getPager');
    $(p).pagination({
        pageSize:30,
        pageList:[10,30,50,100],
        beforePageText:'第',
        afterPageText:'页 共 {pages} 页',
        displayMsg:'当前显示 {from} - {to} 条记录   共 {total} 条记录'
    })

})

function add_server_commit() {
    $.post('/resource/add-server/',
        $('#svr-add-form').serialize(),
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert("添加成功!")
                $('#svr-add-new').dialog('close')
                $('#svr-display-table').datagrid('reload')
            } else {alert("添加失败，请重试!")}
        })
}

function add_server_cancel() {
    $('#svr-add-new').dialog('close')
}

function open_update_window() {
    var val = $('#svr-display-table').datagrid('getSelected')
    if (val) {
        var usable = val['svr-used-type']
        var x =[]
        var key = ['测试','生产','禁用', '空闲']
        var s
        for (i = 0; i < 4; i++) {
            if (usable == i) {
                s = {id:i,name:key[i],selected:true}
            } else {
                s = {id:i,name:key[i]}
            }
            x[i] = s
        }

        $('#svr-id').attr('value', val['svr-id'])
        $('#svr-name').attr('value',val['svr-name'])
        $('#svr-size').attr('value',val['svr-size'])
        $('#svr-update-os').attr('value',val['svr-os'])
        $('#svr-update-hostname').attr('value', val['svr-hostname'])
        $('#svr-end-date').datebox('setValue',val['end-date'])
        $('#svr-update-parts').attr('value', val['svr-parts'])
        $('#svr-update-username').attr('value', val['svr-username'])
        $('#svr-update-idc').combobox({
            onBeforeLoad:function(param) {
                param.idcid = val['idc-id']
            },
            'url' : '/resource/get-idcs/',
            onChange:function(newValue, oldValue) {
                $('#svr-update-cab').combobox({
                    onBeforeLoad:function(param) {
                        param.idcid = $('#svr-update-idc').combobox('getValue')
                        param.cabid = val['cab-id']
                    },
                    url:'/resource/get-cabs/',
                    onChange:function(newValue, oldValue) {
                        $('#svr-update-father').combobox({
                            onBeforeLoad:function(param) {
                                param.fid = val['father-id']
                                param.cab = $('#svr-update-cab').combobox('getValue')
                            },
                            url:'/resource/get-servers/'
                        })
                    }
                })
            }
        })
        $('#svr-update-admin').combobox({
            onBeforeLoad:function(param) {
                param.uid = val['admin-id']
            },
            url:'/resource/get-users/'
        })

        $('#svr-update-usable').combobox({
            valueField:'id',
            textField:'name',
            data:x
        })
    }
    $('#svr-update-div').dialog('open')
}

function svr_update_commit() {
    $.post('/resource/update-server/',
        $('#svr-update-form').serialize(),
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {alert('修改成功')}
            $('#svr-update-div').dialog('close')
            $('#svr-display-table').datagrid('reload')
        })
}

function svr_update_cancel(sid) {
    $(sid).dialog('close')
}

function check_none_cab_selected() {
    if ($('#svr-none-cab').is(":checked")) {
        $('#svr-add-cab').combobox('disable')
        $('#svr-add-cab').combobox('setValue','0')
    } else {
        var idc = $('#svr-add-idc').combobox('getValue')
        $('#svr-add-cab').combobox({
            url:'/resource/get-cabs/',
            onBeforeLoad:function(param) {
                param.idcid = idc;
            },
            disabled:false
        })
    }
}

function check_father_selected() {
    if (!$('#svr-none-father').is(":checked")) {
        $('#svr-add-father').combobox('disable')
    } else {
        var idc = $('#svr-add-idc').combobox('getValue')
        $('#svr-add-father').combobox({
            url:'/resource/get-father-servers/',
            onBeforeLoad:function(param) {
                param.idc = idc;
            },
            disabled:false
        })
    }
}

function check_project_selected() {
    if (!$('#svr-none-project').is(":checked")) {
        $('#svr-add-project').combobox('disable')
    } else {$('#svr-add-project').combobox('enable')}
}

function check_update_father_selected() {
    if (!$('#svr-update-none-father').is(":checked")) {
    	$('#svr-update-father').combobox('clear')
        $('#svr-update-father').combobox('disable')
    } else {
        $('#svr-update-father').combobox('enable')
    }
}

function check_update_project_selected() {
    if (!$('#svr-update-none-project').is(":checked")) {
        $('#svr-update-project').combobox('disable')
    } else {$('#svr-update-project').combobox('enable')}
}

function parts_tip() {
    $('.parts-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">格式如下：<br><br>8核|8G-DDR3|160G-SSD</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })
}

function size_tip() {
    $('.size-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">合法内容包括：<br><br>xU<br>塔式<br>刀柜<br>刀片<br>虚拟机</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })
}

function father_tip() {
    $('.father-tip').tooltip({
        position:'right',
        content:'<span style="color: #000000">该服务器是否构建在其它服务器下，<br><br>如刀片机的父服务器为某个刀柜，<br>虚拟机的父服务器为某个物理机。<br>有则选选择有</span> ',
        onShow:function() {
            $(this).tooltip('tip').css({
                backgroundColor:'#ffe48d',
                borderColor:'#666'
            })
        }
    })
}

function get_cab_base_on_idc() {
    var iid = $('#svr-add-idc').combobox().getValue()
    alert(iid)
}

function update_father_server(index) {
    var val = $('#svr-display-table').datagrid('getRows')[index]
    var idc_id = val['idc-id']
    var svr_id = val['svr-id']
    $('#up-father-svr').dialog('open')
    $('#up-father-idc-id').attr('value', idc_id)
    $('#up-father-svr-id').attr('value', svr_id)
    $('#up-father-father-id').combobox({
        onBeforeLoad:function(param) {
            param.idc = idc_id
        },
        url:'/resource/get-father-servers/'
    })
}

function commit_up_father_svr() {
    if ($('#up-father-svr-form').form('validate')) {
        $.post('/resource/update-father-servers/',
            $('#up-father-svr-form').serialize(),
            function(data, status) {
                if (status == 'success' && data['status'] == 'success') {
                    alert('修改成功')
                    svr_update_cancel('#up-father-svr')
                    $('#svr-display-table').datagrid('reload')
                } else {
                    alert('修改失败')
                }
            })
    } else { return false }
}





















