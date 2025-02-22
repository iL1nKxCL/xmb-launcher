const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let win;

function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // Asegúrate de que esto esté configurado correctamente
            enableRemoteModule: true,
        }
    });

    win.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Manejar eventos de configuración
ipcMain.on('toggle-fullscreen', () => {
    if (!win.isFullScreen()) {
        win.setFullScreen(true);
    } else {
        win.setFullScreen(false);
    }
});

ipcMain.on('toggle-windowed', () => {
    if (win.isFullScreen()) {
        win.setFullScreen(false);
        win.setSize(800, 600); // Tamaño de ventana en modo ventana
    } else {
        win.center();
        alert('Modo ventana ya activado');
    }
});
