$(document).ready(function(){

    $('#idcs-show-list').datagrid({
        url:'/resource/list-idcs/',
        title:'机房信息',
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
//            {field:'idc-id':title:'ID',with 5},
            {field:'idc-name', title:'名称', width:40},
            {field:'end-date', title:'到期日期', width:40},
            {field:'idc-contacts', title:'联系人', width:40},
            {field:'cellphone-num', title:'手机号码', width:40},
            {field:'phone-num', title:'联系电话', width:40},
            {field:'email-addr', title:'联系邮箱', width:40},
            {field:'idc-post', title:'邮编', width:20},
            {
                field:'idc-address',
                title:'地址',
                width:80,
                formatter:function(value, row, index) {
                    return value + "<span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<a href='javascript:void(0)' onclick='modify_addr(" + index + ")'>修改</a></span>"
                }
            },
            {
                field:'idc-summary',
                title:'操作',
                align:'center',
                formatter:function(value, row, index) {
                    return "<a href='javascript:void(0)' onclick='open_summary(" + index + ")'>资源概况</a>"
                }
            }
        ]],
        onSelect:function(rowIndex, rowData) {
            $('#btn-update').linkbutton('enable')
            $('#btn-del').linkbutton('enable')
        },
        onDblClickRow:function () {
            update_idc_detail()
        },
        toolbar:[{
            id:'btn-add',
            text:'添加',
            iconCls:'icon-add',
            handler:function(){
                $('#add-idc-div').dialog('open')
            }
        },{
            id:'btn-update',
            text:"更新",
            iconCls:'icon-edit',
            disabled:true,
            handler:function() {
                update_idc_detail()
            }
        },'-',{
            id:'btn-del',
            text:'删除',
            iconCls:'icon-clear',
            disabled:true,
            handler:function(){
                $.messager.confirm('删除确认', '请确认需要删除该任务信息!<br><br>该操作将不可撤销!', function(r){
                    if (r){
                        var val = $('#idcs-show-list').datagrid('getSelected')
                        if (val) {
                            var sid=val['idc-id']
                            $.post('/resource/del-idc/',
                                {'idc-id':sid},
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
    var p = $('#idcs-show-list').datagrid('getPager');
    $(p).pagination({
        pageSize:10,
        pageList:[10,30,50,100],
        beforePageText:'第',
        afterPageText:'页 共 {pages} 页',
        displayMsg:'当前显示 {from} - {to} 条记录   共 {total} 条记录'
    })
})

function commit_add_idc() {
    if ($('#add-form-id').form('validate')) {
        $.post('/resource/add-idc/',
            $('#add-form-id').serialize(),
            function(data, status) {
                if (status == 'success') {
                    alert('添加成功')
                    $('#add-idc-div').dialog('close')
                    $('#idcs-show-list').datagrid('reload')
                }
            })
    } else { return false }
}

function do_cancel(bid) {
    $(bid).dialog('close')
}

function modify_addr(index) {
    $('#modify-addr').dialog('open')
    var idc_id = $('#idcs-show-list').datagrid('getRows')[index]['idc-id']
    $('#modify-addr-idc-id').attr('value', idc_id)
}

function commit_modify_addr() {
    if ($('#modify-addr-form').form('validate')) {
        $.post('/resource/modify-addr/',
            $('#modify-addr-form').serialize(),
            function(data, status) {
                if (status == 'success') {
                    alert('修改成功')
                    $('#idcs-show-list').datagrid('reload')
                    do_cancel('#modify-addr');
                }
            })
    } else { return false }
}

function update_idc_detail() {
    var row = $('#idcs-show-list').datagrid('getSelected')
    $('#idc-up-idc-id').attr('value', row['idc-id'])
    $('#idc-up-name').val(row['idc-name'])
    $('#idc-up-contact').val(row['idc-contacts'])
    $('#idc-up-cellphone').numberbox('setValue', row['cellphone-num'])
    $('#idc-up-phone').numberbox('setValue', row['phone-num'])
    $('#idc-up-email').val(row['email-addr'])
    $('#idc-up-end-date').datebox('setValue',row['end-date'])
    $('#idc-update').dialog('open')
}

function commit_update_idc() {
    if ($('#idc-up-form').form('validate')) {
        $.post('/resource/update-idc/',
            $('#idc-up-form').serialize(),
            function(data, status) {
                if (status == 'success') {
                    alert('修改成功')
                    $('#idcs-show-list').datagrid('reload')
                    do_cancel('#idc-update');
                }
            })
    } else { return false }
}

function open_summary(index) {
    $('#resource-summary').dialog('open')
    $('#resource-summary-detail').datagrid({
        queryParams:{
            'idc-id' : $('#idcs-show-list').datagrid('getRows')[index]['idc-id']
        },
        url:'/resource/idc-summary/',
        fit:true,
        iconCls:'icon-filter',
        fitColumns:true,
        collapsible:true,
        loadMsg:"加载中,请稍候...",
        singleSelect:true,
        striped:true,
        columns:[[
            {field:'resource-name', title:'名称', width:40},
            {
                field:'total-num',
                title:'总数',
                width:40,
                align:'center',
                formatter:function(value, row, index) {
                    if (value == -1) {
                        return '-'
                    } else {return value}
                }
            },
            {
                field:'be-used',
                title:'已使用',
                width:40,
                align:'center',
                formatter:function(value, row, index) {
                    if (value == -1) {
                        return '--'
                    } else {return value}
                }
            },
            {
                field:'available-num',
                title:'可使用',
                width:40,
                align:'center',
                formatter:function(value, row, index) {
                    if (value == -1) {
                        return '--'
                    } else {return value}
                }
            },
            {
                field:'other-num',
                title:'其它状态',
                width:40,
                align:'center',
                formatter:function(value, row, index) {
                    if (value == -1) {
                        return '--'
                    } else {return value}
                }
            }
        ]]
    })
}















