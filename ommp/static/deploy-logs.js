$(document).ready(function(){

    $('#template-main').datagrid({
        queryParams:{ 'list-type':'1'},
        url:'/tasks/list-task-log/',
        title:'任务执行列表',
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
//            {field:'task-id':title:'ID',with 5},
//            {field:'status-code':title:'status-id',with 5},
//            {field:'config':title:'config',with 5},
            {field:'task-log-id', title:'任务ID', width:40},
            {field:'task-target', title:'任务名称', width:40},
            {field:'operate-user', title:'操作人', width:40},
            {field:'add-time', title:'创建时间', width:40},
            {field:'start-time', title:'启动时间', width:40},
            {field:'end-time', title:'完成时间', width:40},
            {
                field:'status-name',
                title:'任务状态',
                width:40,
                align:'center',
                formatter:function(value, row, index) {
                    if (row['status-code'] == 0) {
                        return '初始化成功...'
                    }
                    if (row['status-code'] == 1) {
                        return '执行中...'
                    }
                    if (row['status-code'] == 2) {
                        return '暂停...'
                    }
                    if (row['status-code'] == 3) {
                        return '停止...'
                    }
                    if (row['status-code'] == 4) {
                        return '完成'
                    }
                    if (row['status-code'] == 5) {
                        return '被取消'
                    }
                }
            },
            {
                field:'task-detail',
                title:'任务详情',
                width:20,
                align:'center',
                formatter:function(value, row, index) {
                    return "<a href='javascript:void(0)' onclick='check_detail(" + index + ", \"no\")'>点击查看</a>"
                }
            },
            {
                field:'operation',
                title:'操作', width:20,
                align:'center',
                formatter:function(value, row, index){
                    if (row['status-code'] == 0)
                        return "<a href='javascript:void(0)' onclick='start_task(" + index + ")'>启动</a>&nbsp&nbsp<a href='javascript:void(0)' onclick='end_task(" + index + ")'>结束任务</a>"
                    if (row['status-code'] == 1)
                        return "<a href='javascript:void(0)' onclick='start_task(" + index + ")'>暂停</a>&nbsp&nbsp<a href='javascript:void(0)' onclick='stop_task(" + index + ")'>停止</a>"
                    if (row['status-code'] == 2)
                        return "<a href='javascript:void(0)' onclick='restart_task(" + index + ")'>重新执行</a>"
                    if (row['status-code'] == 3)
                        return "<a href='javascript:void(0)' onclick='continue_task(" + index + ")'>继续执行</a>"
                    if (row['status-code'] == 4)
                        return "<a href='javascript:void(0)' onclick='redo_task(" + index + ")'>恢复此次发布</a>"
                    if (row['status-code'] == 5)
                        return "不可操作"
                }
            }
        ]]
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

function get_task_log_id(index) {
    var task_id = $('#template-main').datagrid('getRows')[index]['task-id']
    return task_id
}

function start_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/start-process/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('启动成功')
            } else {
                alert('启动失败，请重试')
            }
        })
}

function pause_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/pause-process/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('暂停成功')
            } else {
                alert('暂停失败，请重试')
            }
        })
}

function restart_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/restart-process/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('重新执行成功')
            } else {
                alert('重新执行失败，请重试')
            }
        })
}

function continue_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/continue-process/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('任务成功执行')
            } else {
                alert('继续执行失败，请重试')
            }
        })
}

function end_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/end-process/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('结束任务成功')
            } else {
                alert('结束失败，请重试')
            }
        })
}

function stop_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/stop-process/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('停止任务成功')
            } else {
                alert('停止失败，请重试')
            }
        })
}

function redo_task(index) {
    var task_log_id = get_task_log_id(index)
    $.post('/tasks/redo-task/',
        {'task-log-id' : task_log_id},
        function(data, status) {
            if (status == 'success' && data['status'] == 'success') {
                alert('恢复任务启动成功')
            } else {
                alert('停止失败，请重试')
            }
        })
}

function check_detail(index, loop) {
    var timer = 5000
    var task_log_id = get_task_log_id(index)
    var title = $('#template-main').datagrid('getRows')[index]['task-target']
    $('#detail_show_view').dialog({onBeforeClose:function() {
        window.clearInterval(interval)
    }})
    $('#detail_show_view').dialog('setTitle', '任务 —— ' + title)
    $('#detail_show_view').dialog('open')
    $('#show_main').val('')
    if (loop == 'yes') {
        var interval = setInterval(function(){
            get_detail_msg(task_log_id)
        },timer)
    } else {
        get_detail_msg(task_log_id)
    }
}

function get_detail_msg(task_id) {
    $.post('/tasks/detail-msg/',
        {'task-log-id' : task_id},
        function(data, status) {
            if (status == 'success') {
                $('#show_main').val(data['data'])
            }
        })
}













































