document.addEventListener('DOMContentLoaded', function() {
    // 初始化
    loadErrorList();
    
    // 设置当前日期
    document.getElementById('errorDate').valueAsDate = new Date();
    
    // 添加事件监听器
    document.getElementById('saveErrorButton').addEventListener('click', saveError);
    document.getElementById('searchButton').addEventListener('click', searchErrors);
    document.getElementById('searchInput').addEventListener('keyup', function(e) {
        if(e.key === 'Enter') {
            searchErrors();
        }
    });
});

// 保存错误记录
function saveError() {
    const errorTitle = document.getElementById('errorTitle').value;
    const errorDate = document.getElementById('errorDate').value;
    const errorContext = document.getElementById('errorContext').value;
    const errorDescription = document.getElementById('errorDescription').value;
    const errorSolution = document.getElementById('errorSolution').value;
    const errorReferences = document.getElementById('errorReferences').value;
    const errorTags = document.getElementById('errorTags').value.split(',').map(tag => tag.trim()).filter(tag => tag);
    
    if (!errorTitle) {
        alert('请输入错误标题');
        return;
    }
    
    const errorId = 'error_' + Date.now();
    const errorRecord = {
        id: errorId,
        title: errorTitle,
        date: errorDate,
        context: errorContext,
        description: errorDescription,
        solution: errorSolution,
        references: errorReferences,
        tags: errorTags
    };
    
    // 获取现有的错误记录
    let errorRecords = JSON.parse(localStorage.getItem('errorRecords')) || [];
    
    // 添加新记录
    errorRecords.push(errorRecord);
    
    // 保存到本地存储
    localStorage.setItem('errorRecords', JSON.stringify(errorRecords));
    
    // 清空表单
    clearForm();
    
    // 刷新错误列表
    loadErrorList();
}

// 清空表单
function clearForm() {
    document.getElementById('errorTitle').value = '';
    document.getElementById('errorDate').valueAsDate = new Date();
    document.getElementById('errorContext').value = '';
    document.getElementById('errorDescription').value = '';
    document.getElementById('errorSolution').value = '';
    document.getElementById('errorReferences').value = '';
    document.getElementById('errorTags').value = '';
}

// 加载错误列表
function loadErrorList(records) {
    const errorListContainer = document.getElementById('errorListContainer');
    errorListContainer.innerHTML = '';
    
    // 如果没有传入记录，则从本地存储获取
    const errorRecords = records || JSON.parse(localStorage.getItem('errorRecords')) || [];
    
    if (errorRecords.length === 0) {
        errorListContainer.innerHTML = '<p>暂无错误记录</p>';
        return;
    }
    
    // 按日期降序排序（最新的在前面）
    errorRecords.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // 渲染每个错误记录
    errorRecords.forEach(error => {
        const errorCard = document.createElement('div');
        errorCard.className = 'error-card';
        errorCard.dataset.id = error.id;
        
        const formattedDate = new Date(error.date).toLocaleDateString('zh-CN');
        
        let tagsHTML = '';
        if (error.tags && error.tags.length > 0) {
            tagsHTML = `
                <div class="tags">
                    ${error.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            `;
        }
        
        errorCard.innerHTML = `
            <h3>${error.title}</h3>
            <div class="date">记录日期: ${formattedDate}</div>
            ${tagsHTML}
            
            <div class="section">
                <div class="section-title">环境/上下文</div>
                <div>${error.context.replace(/\n/g, '<br>')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">错误详情</div>
                <div>${error.description.replace(/\n/g, '<br>')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">解决方案</div>
                <div>${error.solution.replace(/\n/g, '<br>')}</div>
            </div>
            
            ${error.references ? `
            <div class="section">
                <div class="section-title">参考资料</div>
                <div>${error.references.replace(/\n/g, '<br>')}</div>
            </div>
            ` : ''}
            
            <div class="actions">
                <button class="action-button edit-button" onclick="editError('${error.id}')">编辑</button>
                <button class="action-button delete-button" onclick="deleteError('${error.id}')">删除</button>
            </div>
        `;
        
        errorListContainer.appendChild(errorCard);
    });
}

// 搜索错误记录
function searchErrors() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    
    // 如果搜索词为空，显示所有记录
    if (!searchTerm) {
        loadErrorList();
        return;
    }
    
    // 获取所有错误记录
    const errorRecords = JSON.parse(localStorage.getItem('errorRecords')) || [];
    
    // 过滤符合搜索条件的记录
    const filteredRecords = errorRecords.filter(error => {
        return (
            error.title.toLowerCase().includes(searchTerm) ||
            error.context.toLowerCase().includes(searchTerm) ||
            error.description.toLowerCase().includes(searchTerm) ||
            error.solution.toLowerCase().includes(searchTerm) ||
            error.references.toLowerCase().includes(searchTerm) ||
            error.tags.some(tag => tag.toLowerCase().includes(searchTerm))
        );
    });
    
    // 加载过滤后的记录
    loadErrorList(filteredRecords);
}

// 编辑错误记录
function editError(errorId) {
    const errorRecords = JSON.parse(localStorage.getItem('errorRecords')) || [];
    const errorToEdit = errorRecords.find(error => error.id === errorId);
    
    if (!errorToEdit) {
        alert('找不到该记录');
        return;
    }
    
    // 填充表单
    document.getElementById('errorTitle').value = errorToEdit.title;
    document.getElementById('errorDate').value = errorToEdit.date;
    document.getElementById('errorContext').value = errorToEdit.context;
    document.getElementById('errorDescription').value = errorToEdit.description;
    document.getElementById('errorSolution').value = errorToEdit.solution;
    document.getElementById('errorReferences').value = errorToEdit.references;
    document.getElementById('errorTags').value = errorToEdit.tags.join(', ');
    
    // 删除旧记录
    deleteError(errorId, true);
    
    // 滚动到表单位置
    document.querySelector('.add-error-form').scrollIntoView({ behavior: 'smooth' });
}

// 删除错误记录
function deleteError(errorId, skipConfirm = false) {
    if (!skipConfirm && !confirm('确定要删除这条记录吗？')) {
        return;
    }
    
    // 获取所有错误记录
    let errorRecords = JSON.parse(localStorage.getItem('errorRecords')) || [];
    
    // 过滤掉要删除的记录
    errorRecords = errorRecords.filter(error => error.id !== errorId);
    
    // 保存到本地存储
    localStorage.setItem('errorRecords', JSON.stringify(errorRecords));
    
    // 刷新错误列表
    loadErrorList();
} 