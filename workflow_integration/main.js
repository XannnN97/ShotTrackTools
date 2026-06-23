// ShotTrackTools Workflow Integration - Electron Main Process
// Compatible with DaVinci Resolve v19.0.2+ (contextIsolation + sandboxing)

const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let pythonProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 500,
        height: 350,
        useContentSize: true,
        resizable: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    mainWindow.loadFile('index.html');

    // 窗口关闭时清理 Python 子进程
    mainWindow.on('close', () => {
        if (pythonProcess) {
            pythonProcess.kill();
            pythonProcess = null;
        }
    });
}

app.whenReady().then(() => {
    console.log('ShotTrackTools Workflow Integration initialized');
    createWindow();
});

app.on('window-all-closed', () => {
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// 处理启动 Python 脚本的请求
ipcMain.on('launch-python', () => {
    if (pythonProcess) {
        console.log('Python script already running');
        return;
    }

    const pluginDir = __dirname;
    const pythonCmd = process.platform === 'win32' ? 'py' : 'python3';
    const scriptPath = path.join(pluginDir, 'ShotTrackTools_Workflow.py');

    // 设置 PYTHONPATH 帮助 Python 找到 Resolve Scripting 模块
    const env = Object.assign({}, process.env);
    const resolveModules = path.join(
        process.env.PROGRAMDATA || 'C:\\ProgramData',
        'Blackmagic Design', 'DaVinci Resolve', 'Support', 'Developer', 'Scripting', 'Modules'
    );
    env.PYTHONPATH = env.PYTHONPATH ? resolveModules + ';' + env.PYTHONPATH : resolveModules;
    // 同时设置 RESOLVE_SCRIPT_LIB 环境变量（帮助 DaVinciResolveScript 找到 DLL）
    if (!env.RESOLVE_SCRIPT_LIB) {
        env.RESOLVE_SCRIPT_LIB = 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll';
    }

    console.log('Launching Python script:', scriptPath);
    console.log('PYTHONPATH:', env.PYTHONPATH);

    pythonProcess = spawn(pythonCmd, ['-3', scriptPath], {
        cwd: pluginDir,
        env: env,
        detached: false
    });

    pythonProcess.stdout.on('data', (data) => {
        console.log('[Python stdout]', data.toString().trim());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error('[Python stderr]', data.toString().trim());
    });

    pythonProcess.on('close', (code) => {
        console.log('Python process exited with code', code);
        pythonProcess = null;
    });

    pythonProcess.on('error', (err) => {
        console.error('Failed to start Python process:', err.message);
        pythonProcess = null;
    });
});
