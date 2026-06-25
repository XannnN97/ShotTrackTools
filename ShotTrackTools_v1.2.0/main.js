const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    useContentSize: true,
    minWidth: 700,
    minHeight: 500,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => { app.quit(); });

function getPythonEnv() {
  const env = Object.assign({}, process.env);
  const resolveModules = path.join(
    process.env.PROGRAMDATA || 'C:\ProgramData',
    'Blackmagic Design', 'DaVinci Resolve', 'Support', 'Developer', 'Scripting', 'Modules'
  );
  env.PYTHONPATH = env.PYTHONPATH ? resolveModules + ';' + env.PYTHONPATH : resolveModules;

  if (!env.RESOLVE_SCRIPT_LIB) {
    const candidates = [
      'C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll',
      'C:\Program Files (x86)\Blackmagic Design\DaVinci Resolve\fusionscript.dll',
      'D:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll',
      'E:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll'
    ];
    for (const candidate of candidates) {
      if (fs.existsSync(candidate)) {
        env.RESOLVE_SCRIPT_LIB = candidate;
        break;
      }
    }
    if (!env.RESOLVE_SCRIPT_LIB) {
      env.RESOLVE_SCRIPT_LIB = 'C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll';
    }
  }
  return env;
}

async function callPython(action, data) {
  return new Promise((resolve, reject) => {
    const pluginDir = __dirname;
    const pythonCmd = process.platform === 'win32' ? 'py' : 'python3';
    const scriptPath = path.join(pluginDir, 'backend.py');

    const proc = spawn(pythonCmd, ['-3', scriptPath], {
      cwd: pluginDir,
      env: getPythonEnv(),
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';
    let timeout = setTimeout(() => {
      proc.kill();
      reject(new Error('Operation timed out (60s)'));
    }, 60000);

    proc.stdout.on('data', (d) => { stdout += d.toString(); });
    proc.stderr.on('data', (d) => { stderr += d.toString(); });

    proc.on('close', (code) => {
      clearTimeout(timeout);
      if (stderr) console.error('[Python stderr]', stderr);
      try {
        const lines = stdout.trim().split('\n').filter(l => l);
        const result = JSON.parse(lines[lines.length - 1]);
        resolve(result);
      } catch (e) {
        reject(new Error('Parse error. stdout: ' + stdout + ' | stderr: ' + stderr));
      }
    });

    proc.on('error', (err) => {
      clearTimeout(timeout);
      reject(err);
    });
    proc.stdin.write(JSON.stringify({ action, ...data }) + '\n');
    proc.stdin.end();
  });
}

ipcMain.handle('execute', async (e, data) => callPython('execute', data));
ipcMain.handle('undo', async (e, data) => callPython('undo', data));
ipcMain.handle('getTracks', async () => callPython('get_tracks', {}));
ipcMain.handle('getConfig', async () => callPython('get_config', {}));
ipcMain.handle('setConfig', async (e, data) => callPython('set_config', { params: data }));
ipcMain.handle('browse-output', async () => {
  const r = await dialog.showOpenDialog(mainWindow, { properties: ['openDirectory'] });
  return r.filePaths[0] || null;
});
