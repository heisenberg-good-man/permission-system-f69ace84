# 招聘平台 (前后端分离骨架)

一个基于 Python Flask + Vue3 + Element Plus 的招聘平台前后端分离骨架，包含完整的主流程交互。

## 功能特性

### 主流程
- **发布招聘信息**：招聘方可以发布、编辑、关闭、删除职位
- **浏览职位**：应聘方可以浏览职位列表，支持搜索和筛选
- **投递简历**：应聘方可以查看职位详情并提交简历投递
- **候选人管理**：招聘方可以查看投递列表，标记状态（待处理/沟通中/不合适/已录用）
- **沟通面板**：双方可以实时沟通，消息联动状态

### 界面模块
- 顶部统计状态栏（职位数、投递数、各状态数量）
- 职位列表页（卡片式展示，支持搜索/城市/状态筛选）
- 职位详情/发布编辑区
- 候选人投递列表（支持状态标记）
- 沟通面板（左侧列表 + 右侧聊天）
- 角色切换（应聘方 / 招聘方，无需登录）

### 数据特点
- 所有数据来自同一批本地 mock 数据，完全联动
- 新增职位后立即在列表可见
- 投递后候选人列表和统计同步更新
- 状态变更即时生效
- 刷新页面或点击"重置数据"可恢复初始状态

## 项目结构

```
permission-system-f69ace84/
├── backend/                 # Python Flask 后端
│   ├── app.py              # 主入口，所有 REST API
│   ├── mock_data.py        # 本地 mock 数据与数据操作类
│   └── requirements.txt    # Python 依赖
├── frontend/                # Vue3 + Element Plus 前端
│   ├── src/
│   │   ├── api/            # API 接口封装
│   │   ├── router/         # 路由配置
│   │   ├── views/          # 页面组件
│   │   │   ├── Jobs.vue          # 职位列表（应聘方）
│   │   │   ├── JobDetail.vue     # 职位详情 + 投递表单
│   │   │   ├── JobManage.vue     # 职位管理（招聘方）
│   │   │   ├── Applications.vue  # 候选人管理（招聘方）
│   │   │   ├── MyApplications.vue# 我的投递（应聘方）
│   │   │   └── Communication.vue # 沟通面板
│   │   ├── App.vue         # 主布局（导航/统计/角色切换）
│   │   ├── main.js         # 入口文件
│   │   └── style.css       # 全局样式
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## 本地启动方式

### 1. 启动后端 (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端启动后监听 `http://localhost:5000`

### 2. 启动前端 (Vue3)

```bash
cd frontend
npm install
npm run dev
```

前端启动后访问 `http://localhost:3000`

## 使用说明

### 角色切换
页面右上角可以切换「应聘方」和「招聘方」视角：

- **应聘方**：
  - 职位浏览：查看所有招聘中的职位
  - 我的投递：查看已投递的职位和状态
  - 点击职位进入详情，可填写简历并投递

- **招聘方**：
  - 职位管理：发布、编辑、关闭、删除职位
  - 候选人：查看所有投递，标记状态，发起沟通

### 沟通面板
- 左侧：候选人/投递列表
- 右侧：聊天消息区，输入消息按 Enter 发送
- 招聘方首次发送消息时，候选人状态自动变为"沟通中"

### 数据重置
点击右上角「重置数据」按钮，所有数据恢复到初始 mock 状态。

## API 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/stats | 获取统计数据 |
| GET | /api/jobs | 职位列表 |
| GET | /api/jobs/:id | 职位详情 |
| POST | /api/jobs | 发布职位 |
| PUT | /api/jobs/:id | 更新职位 |
| DELETE | /api/jobs/:id | 删除职位 |
| GET | /api/applications | 投递列表 |
| POST | /api/jobs/:id/apply | 投递简历 |
| PUT | /api/applications/:id/status | 更新投递状态 |
| GET | /api/applications/:id/messages | 获取沟通记录 |
| POST | /api/applications/:id/messages | 发送消息 |
| POST | /api/reset | 重置所有数据 |
