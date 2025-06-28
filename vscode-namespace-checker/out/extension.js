"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const https = require("https");
// 存储所有找到的命名空间
let foundNamespaces = [];
// 诊断集合，全局使用一个实例以避免重复
const diagnosticCollection = vscode.languages.createDiagnosticCollection('namespaceChecker');
// 上次更新时间戳，用于节流
let lastUpdateTimestamp = 0;
let UPDATE_THROTTLE_MS = 500; // 更新间隔（毫秒）
// 激活扩展
function activate(context) {
    console.log('命名空间查重器已激活');
    // 加载配置
    loadConfiguration();
    // 监听配置变更
    const configChangeDisposable = vscode.workspace.onDidChangeConfiguration(event => {
        if (event.affectsConfiguration('namespaceChecker')) {
            loadConfiguration();
        }
    });
    // 注册命令
    const disposable = vscode.commands.registerCommand('namespace-checker.checkNamespace', () => {
        checkNamespaces();
    });
    // 注册远程仓库查重命令
    const remoteCheckDisposable = vscode.commands.registerCommand('namespace-checker.checkRemoteNamespace', async () => {
        // 弹出输入框让用户输入远程仓库URL
        const repoUrl = await vscode.window.showInputBox({
            prompt: '请输入要查重的远程仓库URL (GitHub/GitLab)',
            placeHolder: 'https://github.com/username/repo',
            validateInput: (text) => {
                return text && (text.startsWith('https://github.com/') || text.startsWith('https://gitlab.com/'))
                    ? null
                    : '请输入有效的GitHub或GitLab仓库URL';
            }
        });
        if (repoUrl) {
            await checkWithRemoteRepository(repoUrl);
        }
    });
    // 注册内容查重命令
    const contentCheckDisposable = vscode.commands.registerCommand('namespace-checker.checkContent', () => {
        checkCodeContent();
    });
    // 注册文档更改事件（使用节流来提高性能）
    const documentChangeDisposable = vscode.workspace.onDidChangeTextDocument((event) => {
        const document = event.document;
        // 只处理C/C++文件
        if (document.languageId === 'cpp' || document.languageId === 'c') {
            const currentTime = Date.now();
            if (currentTime - lastUpdateTimestamp > UPDATE_THROTTLE_MS) {
                lastUpdateTimestamp = currentTime;
                checkDocumentNamespacesAndContent(document);
            }
        }
    });
    // 注册文档打开事件
    const documentOpenDisposable = vscode.workspace.onDidOpenTextDocument((document) => {
        // 只处理C/C++文件
        if (document.languageId === 'cpp' || document.languageId === 'c') {
            checkDocumentNamespacesAndContent(document);
        }
    });
    // 注册文档保存事件
    const documentSaveDisposable = vscode.workspace.onDidSaveTextDocument((document) => {
        // 只处理C/C++文件
        if (document.languageId === 'cpp' || document.languageId === 'c') {
            checkDocumentNamespacesAndContent(document);
        }
    });
    // 将所有事件注册到上下文中
    context.subscriptions.push(disposable, remoteCheckDisposable, contentCheckDisposable, documentChangeDisposable, documentOpenDisposable, documentSaveDisposable, configChangeDisposable, diagnosticCollection);
    // 初始化时扫描工作区中的所有命名空间和代码内容
    scanWorkspaceNamespacesAndContent();
    // 初始化时加载配置的远程仓库
    loadRemoteRepositories();
}
exports.activate = activate;
// 加载配置
function loadConfiguration() {
    const config = vscode.workspace.getConfiguration('namespaceChecker');
    UPDATE_THROTTLE_MS = config.get('updateInterval', 500);
}
// 加载配置的远程仓库
async function loadRemoteRepositories() {
    // 获取远程仓库配置
    const config = vscode.workspace.getConfiguration('namespaceChecker');
    const remoteRepos = config.get('remoteRepos', []);
    if (remoteRepos.length > 0) {
        vscode.window.showInformationMessage(`开始从 ${remoteRepos.length} 个远程仓库获取代码...`);
        // 逐个加载远程仓库代码
        for (const repoUrl of remoteRepos) {
            try {
                await checkWithRemoteRepository(repoUrl);
            }
            catch (error) {
                vscode.window.showErrorMessage(`加载远程仓库 ${repoUrl} 失败: ${error.message}`);
            }
        }
    }
}
// 扫描工作区中的所有命名空间和代码内容
async function scanWorkspaceNamespacesAndContent() {
    // 清空之前的结果
    foundNamespaces = [];
    diagnosticCollection.clear();
    // 获取配置的搜索路径
    const config = vscode.workspace.getConfiguration('namespaceChecker');
    const searchPaths = config.get('searchPaths', ['src', 'include']);
    // 获取工作区目录
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
        vscode.window.showInformationMessage('没有打开的工作区');
        return;
    }
    // 显示进度提示
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "正在扫描代码...",
        cancellable: false
    }, async (progress) => {
        let processedFiles = 0;
        let totalFiles = 0;
        // 首先计算总文件数
        for (const folder of workspaceFolders) {
            for (const searchPath of searchPaths) {
                const fullPath = path.join(folder.uri.fsPath, searchPath);
                if (fs.existsSync(fullPath)) {
                    const cppFiles = await findCppFiles(fullPath);
                    totalFiles += cppFiles.length;
                }
            }
        }
        // 对每个工作区目录进行处理
        for (const folder of workspaceFolders) {
            // 对每个搜索路径进行处理
            for (const searchPath of searchPaths) {
                const fullPath = path.join(folder.uri.fsPath, searchPath);
                // 检查路径是否存在
                if (fs.existsSync(fullPath)) {
                    // 查找所有C/C++文件
                    const cppFiles = await findCppFiles(fullPath);
                    // 处理每个文件
                    for (const file of cppFiles) {
                        const document = await vscode.workspace.openTextDocument(file);
                        extractNamespacesAndContent(document);
                        // 更新进度
                        processedFiles++;
                        progress.report({
                            message: `处理文件 ${processedFiles}/${totalFiles}`,
                            increment: (1 / totalFiles) * 100
                        });
                    }
                }
            }
        }
    });
    // 检查所有命名空间和内容是否有重复
    checkAllNamespacesAndContent();
    vscode.window.showInformationMessage(`已扫描命名空间: ${foundNamespaces.length}个`);
}
// 查找指定目录下的所有C/C++文件
async function findCppFiles(directory) {
    const result = [];
    // 递归扫描目录
    async function scanDirectory(dir) {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.isDirectory()) {
                await scanDirectory(fullPath);
            }
            else if (entry.isFile()) {
                // 检查是否是C/C++文件
                if (/\.(cpp|cc|cxx|c|hpp|h|hxx)$/i.test(entry.name)) {
                    result.push(fullPath);
                }
            }
        }
    }
    await scanDirectory(directory);
    return result;
}
// 检查当前文档中的命名空间和内容
function checkDocumentNamespacesAndContent(document) {
    // 清除当前文档的诊断信息
    diagnosticCollection.delete(document.uri);
    // 从全局命名空间列表中移除当前文档中的命名空间
    foundNamespaces = foundNamespaces.filter(ns => ns.file !== document.fileName);
    // 提取当前文档中的命名空间和内容
    const currentNamespaces = extractNamespacesAndContent(document);
    // 检查是否有重复的命名空间
    checkNamespaceDuplicates(document, currentNamespaces);
    // 检查是否有重复的代码内容
    const config = vscode.workspace.getConfiguration('namespaceChecker');
    const enableContentCheck = config.get('enableContentCheck', true);
    if (enableContentCheck) {
        checkContentDuplicates(document, currentNamespaces);
    }
}
// 检查所有命名空间和内容是否有重复
function checkAllNamespacesAndContent() {
    // 获取所有打开的文本编辑器
    const editors = vscode.window.visibleTextEditors;
    // 处理每个打开的编辑器
    for (const editor of editors) {
        const document = editor.document;
        // 只处理C/C++文件
        if (document.languageId === 'cpp' || document.languageId === 'c') {
            // 获取当前文档中的命名空间
            const documentNamespaces = foundNamespaces.filter(ns => ns.file === document.fileName);
            // 检查命名空间是否有重复
            checkNamespaceDuplicates(document, documentNamespaces);
            // 检查代码内容是否有重复
            checkContentDuplicates(document, documentNamespaces);
        }
    }
}
// 检查命名空间是否有重复
function checkNamespaceDuplicates(document, namespaces) {
    // 创建诊断信息数组
    const diagnostics = [];
    // 检查每个命名空间是否有重复
    for (const ns of namespaces) {
        const duplicates = foundNamespaces.filter(item => item.name === ns.name && (item.file !== ns.file || item.line !== ns.line));
        // 如果有重复，创建诊断信息
        if (duplicates.length > 0) {
            // 获取命名空间在文档中的位置
            const position = new vscode.Position(ns.line, ns.column);
            const range = getNamespaceRange(document, position);
            if (range) {
                // 创建诊断消息
                let message = `命名空间 "${ns.name}" 与以下位置重复:\n`;
                for (const dup of duplicates) {
                    if (dup.isRemote) {
                        message += `- [远程] ${dup.repository}: ${dup.file}:${dup.line + 1}:${dup.column + 1}\n`;
                    }
                    else {
                        const relativePath = vscode.workspace.asRelativePath(dup.file);
                        message += `- ${relativePath}:${dup.line + 1}:${dup.column + 1}\n`;
                    }
                }
                // 创建诊断
                const diagnostic = new vscode.Diagnostic(range, message, vscode.DiagnosticSeverity.Warning);
                // 设置诊断代码
                diagnostic.code = 'duplicate-namespace';
                // 添加到诊断数组
                diagnostics.push(diagnostic);
            }
        }
    }
    // 将诊断信息设置到诊断集合中
    if (diagnostics.length > 0) {
        diagnosticCollection.set(document.uri, diagnostics);
    }
}
// 检查代码内容是否有重复
function checkContentDuplicates(document, namespaces) {
    // 已有的诊断信息
    let diagnostics = [...(diagnosticCollection.get(document.uri) || [])];
    // 检查每个命名空间的内容是否有重复
    for (const ns of namespaces) {
        // 跳过没有内容的命名空间
        if (!ns.content) {
            continue;
        }
        // 查找内容相似但命名空间名称不同的命名空间
        const contentDuplicates = foundNamespaces.filter(item => item.content &&
            item.content === ns.content &&
            item.name !== ns.name);
        // 如果有重复，创建诊断信息
        if (contentDuplicates.length > 0) {
            // 获取命名空间在文档中的位置
            const position = new vscode.Position(ns.line, ns.column);
            const range = getNamespaceRange(document, position);
            if (range) {
                // 创建诊断消息
                let message = `命名空间 "${ns.name}" 的内容与以下命名空间相同或高度相似:\n`;
                for (const dup of contentDuplicates) {
                    if (dup.isRemote) {
                        message += `- [远程] ${dup.repository}: 命名空间 "${dup.name}" (${dup.file}:${dup.line + 1}:${dup.column + 1})\n`;
                    }
                    else {
                        const relativePath = vscode.workspace.asRelativePath(dup.file);
                        message += `- 命名空间 "${dup.name}" (${relativePath}:${dup.line + 1}:${dup.column + 1})\n`;
                    }
                }
                // 创建诊断
                const diagnostic = new vscode.Diagnostic(range, message, vscode.DiagnosticSeverity.Information);
                // 设置诊断代码
                diagnostic.code = 'similar-content';
                // 添加到诊断数组
                diagnostics.push(diagnostic);
            }
        }
    }
    // 将诊断信息设置到诊断集合中
    if (diagnostics.length > 0) {
        diagnosticCollection.set(document.uri, diagnostics);
    }
}
// 获取命名空间范围
function getNamespaceRange(document, position) {
    // 查找命名空间声明的范围
    const range = document.getWordRangeAtPosition(position, /namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)/);
    if (range) {
        return range;
    }
    // 如果找不到命名空间声明的范围，则使用整行作为范围
    return new vscode.Range(new vscode.Position(position.line, 0), new vscode.Position(position.line, document.lineAt(position.line).text.length));
}
// 提取文档中的命名空间和内容
function extractNamespacesAndContent(document) {
    const foundInDocument = [];
    const text = document.getText();
    // 正则表达式匹配命名空间声明
    const namespaceRegex = /namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*{/g;
    let match;
    while ((match = namespaceRegex.exec(text)) !== null) {
        const namespaceName = match[1];
        const position = document.positionAt(match.index);
        // 提取命名空间内容
        const content = extractNamespaceContent(text, match.index + match[0].length);
        const namespaceInfo = {
            name: namespaceName,
            file: document.fileName,
            line: position.line,
            column: position.character,
            content: content
        };
        // 添加到当前文档命名空间列表
        foundInDocument.push(namespaceInfo);
        // 添加到全局命名空间列表（如果不存在）
        if (!foundNamespaces.some(ns => ns.name === namespaceInfo.name &&
            ns.file === namespaceInfo.file &&
            ns.line === namespaceInfo.line)) {
            foundNamespaces.push(namespaceInfo);
        }
    }
    return foundInDocument;
}
// 提取命名空间内容
function extractNamespaceContent(text, startIndex) {
    let braceCount = 1; // 已经找到了开始的 '{'
    let endIndex = startIndex;
    while (braceCount > 0 && endIndex < text.length) {
        const char = text[endIndex];
        if (char === '{') {
            braceCount++;
        }
        else if (char === '}') {
            braceCount--;
        }
        endIndex++;
    }
    // 如果找到了匹配的结束括号，返回内容
    if (braceCount === 0) {
        return text.substring(startIndex, endIndex - 1).trim();
    }
    // 如果没有找到匹配的结束括号，返回空字符串
    return '';
}
// 检查代码内容
function checkCodeContent() {
    // 获取当前活动的编辑器
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showInformationMessage('没有打开的编辑器');
        return;
    }
    const document = editor.document;
    // 只处理C/C++文件
    if (document.languageId !== 'cpp' && document.languageId !== 'c') {
        vscode.window.showInformationMessage('当前文件不是C/C++文件');
        return;
    }
    // 检查当前文档中的命名空间和内容
    checkDocumentNamespacesAndContent(document);
    vscode.window.showInformationMessage('代码内容查重完成');
}
// 手动检查命名空间
function checkNamespaces() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showInformationMessage('没有打开的编辑器');
        return;
    }
    // 更新工作区命名空间
    scanWorkspaceNamespacesAndContent().then(() => {
        // 检查当前文档
        checkDocumentNamespacesAndContent(editor.document);
        vscode.window.showInformationMessage('命名空间检查完成');
    });
}
// 从远程仓库获取代码并检查命名空间
async function checkWithRemoteRepository(repoUrl) {
    try {
        vscode.window.showInformationMessage(`开始从 ${repoUrl} 获取代码...`);
        // 解析仓库URL
        const repoInfo = parseRepositoryUrl(repoUrl);
        if (!repoInfo) {
            vscode.window.showErrorMessage('无法解析仓库URL');
            return;
        }
        // 显示进度条
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `正在从 ${repoUrl} 获取代码...`,
            cancellable: true
        }, async (progress, token) => {
            try {
                // 获取仓库文件列表
                const files = await getRepositoryFiles(repoInfo);
                // 过滤出C/C++文件
                const cppFiles = files.filter(file => /\.(cpp|cc|cxx|c|hpp|h|hxx)$/i.test(file.path));
                progress.report({ message: `找到 ${cppFiles.length} 个C/C++文件，正在分析...` });
                // 记录远程命名空间
                const remoteNamespaces = [];
                // 逐个分析文件
                for (let i = 0; i < cppFiles.length; i++) {
                    if (token.isCancellationRequested) {
                        break;
                    }
                    const file = cppFiles[i];
                    progress.report({
                        message: `分析文件 (${i + 1}/${cppFiles.length}): ${file.path}`,
                        increment: 100 / cppFiles.length
                    });
                    try {
                        // 获取文件内容
                        const content = await getFileContent(repoInfo, file.path);
                        // 提取命名空间
                        const namespaces = extractNamespacesFromText(content);
                        // 添加到远程命名空间列表
                        for (const ns of namespaces) {
                            remoteNamespaces.push({
                                name: ns.name,
                                file: file.path,
                                line: ns.line,
                                column: ns.column,
                                isRemote: true,
                                repository: repoUrl
                            });
                        }
                    }
                    catch (e) {
                        console.error(`Error processing file ${file.path}:`, e);
                    }
                }
                // 将远程命名空间添加到全局列表
                foundNamespaces = [...foundNamespaces, ...remoteNamespaces];
                // 检查当前编辑器中的文件
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    checkDocumentNamespacesAndContent(editor.document);
                }
                vscode.window.showInformationMessage(`从 ${repoUrl} 找到 ${remoteNamespaces.length} 个命名空间`);
            }
            catch (e) {
                vscode.window.showErrorMessage(`获取仓库代码失败: ${e.message}`);
            }
        });
    }
    catch (error) {
        vscode.window.showErrorMessage(`检查远程仓库失败: ${error.message}`);
    }
}
// 从文本内容中提取命名空间
function extractNamespacesFromText(text) {
    const result = [];
    const lines = text.split('\n');
    // 对每一行分析
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const namespaceMatch = line.match(/namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*{/);
        if (namespaceMatch) {
            const name = namespaceMatch[1];
            const column = namespaceMatch.index || 0;
            result.push({
                name,
                line: i,
                column
            });
        }
    }
    return result;
}
// 解析仓库URL
function parseRepositoryUrl(url) {
    try {
        if (url.startsWith('https://github.com/')) {
            const parts = url.replace('https://github.com/', '').split('/');
            if (parts.length >= 2) {
                return { type: 'github', owner: parts[0], repo: parts[1] };
            }
        }
        else if (url.startsWith('https://gitlab.com/')) {
            const parts = url.replace('https://gitlab.com/', '').split('/');
            if (parts.length >= 2) {
                return { type: 'gitlab', owner: parts[0], repo: parts[1] };
            }
        }
        return null;
    }
    catch (e) {
        return null;
    }
}
// 获取仓库文件列表
async function getRepositoryFiles(repoInfo) {
    if (repoInfo.type === 'github') {
        const apiUrl = `https://api.github.com/repos/${repoInfo.owner}/${repoInfo.repo}/git/trees/master?recursive=1`;
        const response = await httpRequest(apiUrl, {
            headers: {
                'User-Agent': 'VS Code Namespace Checker'
            }
        });
        const data = JSON.parse(response);
        return data.tree.filter((item) => item.type === 'blob');
    }
    else if (repoInfo.type === 'gitlab') {
        const apiUrl = `https://gitlab.com/api/v4/projects/${encodeURIComponent(`${repoInfo.owner}/${repoInfo.repo}`)}/repository/tree?recursive=true`;
        const response = await httpRequest(apiUrl);
        const data = JSON.parse(response);
        return data
            .filter((item) => item.type === 'blob')
            .map((item) => ({ path: item.path, type: 'blob' }));
    }
    return [];
}
// 获取文件内容
async function getFileContent(repoInfo, filePath) {
    if (repoInfo.type === 'github') {
        const apiUrl = `https://api.github.com/repos/${repoInfo.owner}/${repoInfo.repo}/contents/${filePath}`;
        const response = await httpRequest(apiUrl, {
            headers: {
                'User-Agent': 'VS Code Namespace Checker',
                'Accept': 'application/vnd.github.v3.raw'
            }
        });
        return response;
    }
    else if (repoInfo.type === 'gitlab') {
        const apiUrl = `https://gitlab.com/api/v4/projects/${encodeURIComponent(`${repoInfo.owner}/${repoInfo.repo}`)}/repository/files/${encodeURIComponent(filePath)}/raw?ref=master`;
        const response = await httpRequest(apiUrl);
        return response;
    }
    return '';
}
// HTTP请求辅助函数
async function httpRequest(url, options = {}) {
    return new Promise((resolve, reject) => {
        const req = https.get(url, options, (res) => {
            if (res.statusCode === 301 || res.statusCode === 302) {
                // 处理重定向
                if (res.headers.location) {
                    httpRequest(res.headers.location, options)
                        .then(resolve)
                        .catch(reject);
                    return;
                }
            }
            if (res.statusCode !== 200) {
                reject(new Error(`HTTP请求失败: ${res.statusCode}`));
                return;
            }
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve(data));
        });
        req.on('error', reject);
        req.end();
    });
}
// 扩展被停用时
function deactivate() {
    // 清除诊断信息
    diagnosticCollection.clear();
    diagnosticCollection.dispose();
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map