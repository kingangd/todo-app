// 后端接口地址，部署到 Render/其他服务器后使用相对路径
const BASE_URL = '/api/todos';
// 当前筛选状态：all=全部，0=未完成，1=已完成
let currentFilter = 'all';

// 页面加载完成后执行
window.onload = function() {
    // 获取所有任务
    fetchTodos();
    // 绑定添加按钮事件
    document.getElementById('addBtn').addEventListener('click', addTodo);
    // 绑定筛选按钮事件
    bindFilterEvents();
};

// 1. 从后端获取任务列表
function fetchTodos() {
    fetch(BASE_URL)
        .then(res => res.json())
        .then(data => {
            renderTodoList(data);
        })
        .catch(err => {
            console.error('获取任务失败：', err);
            alert('获取任务失败，请检查后端是否启动');
        });
}

// 2. 渲染任务列表到页面
function renderTodoList(todoList) {
    const listEl = document.getElementById('todoList');
    listEl.innerHTML = '';

    // 根据筛选条件过滤
    const filteredList = todoList.filter(item => {
        if (currentFilter === 'all') return true;
        return String(item.status) === currentFilter;
    });

    // 空状态
    if (filteredList.length === 0) {
        listEl.innerHTML = '<li style="text-align:center;color:#999;padding:30px;">暂无任务</li>';
        return;
    }

    // 循环生成列表项
    filteredList.forEach(item => {
        const li = document.createElement('li');
        li.className = `todo-item ${item.status === 1 ? 'completed' : ''}`;
        li.innerHTML = `
            <input type="checkbox" class="todo-checkbox" 
                   ${item.status === 1 ? 'checked' : ''} 
                   data-id="${item.id}" data-status="${item.status}">
            <div class="todo-content">
                <div class="todo-title">${item.title}</div>
                <div class="todo-desc">${item.content || '无详情'} · 截止：${item.deadline || '无'}</div>
            </div>
            <button class="delete-btn" data-id="${item.id}">删除</button>
        `;
        listEl.appendChild(li);
    });

    // 绑定复选框切换事件
    bindCheckboxEvents();
    // 绑定删除按钮事件
    bindDeleteEvents();
}

// 3. 新增任务
function addTodo() {
    const titleInput = document.getElementById('titleInput');
    const contentInput = document.getElementById('contentInput');
    const deadlineInput = document.getElementById('deadlineInput');

    const title = titleInput.value.trim();
    if (!title) {
        alert('任务标题不能为空');
        return;
    }

    const data = {
        title: title,
        content: contentInput.value.trim(),
        deadline: deadlineInput.value
    };

    fetch(BASE_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(() => {
        // 添加成功后清空输入框，刷新列表
        titleInput.value = '';
        contentInput.value = '';
        deadlineInput.value = '';
        fetchTodos();
    })
    .catch(err => {
        console.error('添加失败：', err);
        alert('添加任务失败');
    });
}

// 4. 切换任务完成状态
function bindCheckboxEvents() {
    const checkboxes = document.querySelectorAll('.todo-checkbox');
    checkboxes.forEach(box => {
        box.addEventListener('change', function() {
            const id = this.dataset.id;
            // 切换状态：0变1，1变0
            const newStatus = this.checked ? 1 : 0;

            fetch(`${BASE_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: newStatus })
            })
            .then(res => res.json())
            .then(() => {
                fetchTodos();
            })
            .catch(err => {
                console.error('更新状态失败：', err);
                alert('更新失败');
            });
        });
    });
}

// 5. 删除任务
function bindDeleteEvents() {
    const deleteBtns = document.querySelectorAll('.delete-btn');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            if (!confirm('确定要删除这个任务吗？')) return;

            fetch(`${BASE_URL}/${id}`, {
                method: 'DELETE'
            })
            .then(res => res.json())
            .then(() => {
                fetchTodos();
            })
            .catch(err => {
                console.error('删除失败：', err);
                alert('删除失败');
            });
        });
    });
}

// 6. 筛选功能
function bindFilterEvents() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 切换选中样式
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // 更新筛选条件并刷新
            currentFilter = this.dataset.status;
            fetchTodos();
        });
    });
}
