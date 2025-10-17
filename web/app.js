// API 配置
const API_BASE_URL = 'http://127.0.0.1:8000';

// 全局状态
let isConnected = false;
let chatHistory = [];

// 智能体图标映射
const AGENT_ICONS = {
    'email': 'fa-envelope',
    'doc': 'fa-file-alt',
    'schedule': 'fa-calendar-alt',
    'data': 'fa-chart-bar',
    'knowledge': 'fa-brain',
    'file': 'fa-folder-open'
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('日常办公超级智能体 - 前端已加载');
    
    // 检查连接状态
    checkConnection();
    
    // 加载智能体列表
    loadAgents();
    
    // 加载系统状态
    loadSystemStats();
    
    // 自动调整文本框高度
    const textarea = document.getElementById('userInput');
    textarea.addEventListener('input', autoResizeTextarea);
    
    // 定期更新状态（每30秒）
    setInterval(() => {
        checkConnection();
        loadSystemStats();
    }, 30000);
});

// 检查连接状态
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateConnectionStatus(true);
        } else {
            updateConnectionStatus(false);
        }
    } catch (error) {
        console.error('连接检查失败:', error);
        updateConnectionStatus(false);
    }
}

// 更新连接状态显示
function updateConnectionStatus(connected) {
    isConnected = connected;
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    
    if (connected) {
        statusDot.classList.add('online');
        statusDot.classList.remove('offline');
        statusText.textContent = '已连接';
    } else {
        statusDot.classList.add('offline');
        statusDot.classList.remove('online');
        statusText.textContent = '未连接';
    }
}

// 加载智能体列表
async function loadAgents() {
    const agentsList = document.getElementById('agentsList');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/agents`);
        const data = await response.json();
        
        if (data.agents && data.agents.length > 0) {
            agentsList.innerHTML = data.agents.map(agent => {
                const icon = AGENT_ICONS[agent.toLowerCase()] || 'fa-robot';
                const agentName = getAgentDisplayName(agent);
                
                return `
                    <div class="agent-item">
                        <i class="fas ${icon}"></i>
                        <span class="agent-name">${agentName}</span>
                        <i class="fas fa-check-circle" style="color: var(--secondary-color);"></i>
                    </div>
                `;
            }).join('');
        } else {
            agentsList.innerHTML = '<div class="loading">暂无可用智能体</div>';
        }
    } catch (error) {
        console.error('加载智能体失败:', error);
        agentsList.innerHTML = '<div class="loading">加载失败</div>';
    }
}

// 获取智能体显示名称
function getAgentDisplayName(agent) {
    const names = {
        'email': '邮件智能体',
        'doc': '文档智能体',
        'schedule': '日程智能体',
        'data': '数据分析智能体',
        'knowledge': '知识问答智能体',
        'file': '文件管理智能体'
    };
    return names[agent.toLowerCase()] || agent;
}

// 加载系统状态
async function loadSystemStats() {
    try {
        // 加载记忆统计
        const memoryResponse = await fetch(`${API_BASE_URL}/api/memory/stats`);
        const memoryData = await memoryResponse.json();
        document.getElementById('memoryCount').textContent = memoryData.total_memories || 0;
        
        // 加载向量数据库统计
        const vectorResponse = await fetch(`${API_BASE_URL}/api/vector_db/stats`);
        const vectorData = await vectorResponse.json();
        document.getElementById('vectorCount').textContent = vectorData.total_documents || 0;
    } catch (error) {
        console.error('加载系统状态失败:', error);
    }
}

// 自动调整文本框高度
function autoResizeTextarea() {
    const textarea = document.getElementById('userInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// 处理键盘事件
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 发送消息
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    if (!isConnected) {
        alert('未连接到服务器，请检查后端服务是否启动');
        return;
    }
    
    // 清空输入框
    input.value = '';
    input.style.height = 'auto';
    
    // 添加用户消息到界面
    addMessage('user', message);
    
    // 显示加载状态
    const loadingId = addLoadingMessage();
    
    // 禁用发送按钮
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    
    try {
        // 发送请求到后端
        const response = await fetch(`${API_BASE_URL}/api/task`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_input: message,
                context: {}
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 移除加载消息
        removeLoadingMessage(loadingId);
        
        // 添加AI回复
        addMessage('assistant', data.result, data);
        
    } catch (error) {
        console.error('发送消息失败:', error);
        removeLoadingMessage(loadingId);
        addMessage('assistant', `抱歉，处理您的请求时出现错误：${error.message}`, null, true);
    } finally {
        // 重新启用发送按钮
        sendBtn.disabled = false;
        input.focus();
    }
}

// 添加消息到聊天窗口
function addMessage(role, content, taskData = null, isError = false) {
    const chatMessages = document.getElementById('chatMessages');
    
    // 移除欢迎消息
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = role === 'user' ? 
        '<i class="fas fa-user"></i>' : 
        '<i class="fas fa-robot"></i>';
    
    let taskDetailsHtml = '';
    if (taskData && taskData.task_understanding) {
        const understanding = taskData.task_understanding;
        taskDetailsHtml = `
            <div class="task-details">
                <h4><i class="fas fa-tasks"></i> 任务分析</h4>
                <div class="task-info">
                    ${understanding.task_type ? `
                        <span class="task-badge">
                            <i class="fas fa-tag"></i> ${understanding.task_type}
                        </span>
                    ` : ''}
                    ${understanding.selected_agent ? `
                        <span class="task-badge">
                            <i class="fas fa-robot"></i> ${getAgentDisplayName(understanding.selected_agent)}
                        </span>
                    ` : ''}
                    ${taskData.subtasks_count ? `
                        <span class="task-badge">
                            <i class="fas fa-list"></i> ${taskData.subtasks_count} 个子任务
                        </span>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    const bubbleClass = isError ? 'message-bubble error' : 'message-bubble';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="${bubbleClass}">${formatMessage(content)}</div>
            ${taskDetailsHtml}
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // 保存到历史记录
    chatHistory.push({
        role,
        content,
        taskData,
        timestamp: new Date().toISOString()
    });
}

// 添加加载消息
function addLoadingMessage() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingId = `loading-${Date.now()}`;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant loading';
    messageDiv.id = loadingId;
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="loading">AI 正在思考</div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return loadingId;
}

// 移除加载消息
function removeLoadingMessage(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

// 格式化消息内容
function formatMessage(content) {
    if (typeof content !== 'string') {
        content = JSON.stringify(content, null, 2);
    }
    
    // 转换换行符
    content = content.replace(/\n/g, '<br>');
    
    // 转换列表
    content = content.replace(/^- (.+)$/gm, '<li>$1</li>');
    if (content.includes('<li>')) {
        content = content.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return content;
}

// 获取当前时间
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// 快捷任务
function sendQuickTask(task) {
    const input = document.getElementById('userInput');
    input.value = task;
    sendMessage();
}

// 清空对话
function clearChat() {
    if (confirm('确定要清空所有对话记录吗？')) {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <i class="fas fa-robot robot-icon"></i>
                <h3>欢迎使用日常办公超级智能体！</h3>
                <p>我可以帮您处理以下任务：</p>
                <ul>
                    <li>📧 邮件管理 - 自动分类、回复、归档</li>
                    <li>📄 文档处理 - 格式转换、摘要提取、对比</li>
                    <li>📅 日程管理 - 会议安排、提醒、冲突检测</li>
                    <li>📊 数据分析 - 数据处理、可视化、报表生成</li>
                    <li>💡 知识问答 - 基于知识库的智能问答</li>
                    <li>📁 文件管理 - 智能整理、重复检测、空间优化</li>
                </ul>
                <p>请输入您的需求，我会帮您处理！</p>
            </div>
        `;
        chatHistory = [];
    }
}

// 导出聊天记录
function exportChat() {
    const dataStr = JSON.stringify(chatHistory, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chat-history-${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    URL.revokeObjectURL(url);
}
