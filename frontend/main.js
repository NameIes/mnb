const {app, BrowserWindow} = require('electron');

const url = require('url');
const path = require('path');

let mainWindow;

function createWindow() {
    let subpy = require('child_process').spawn('./app');

    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    mainWindow.setMenu(null);

    mainWindow.loadURL(
        url.format({
            pathname: path.join(__dirname, './dist/index.html'),
            protocol: 'file:',
            slashes: true
        })
    );

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
    app.quit();
});

app.on('activate', function () {
    if (mainWindow === null) createWindow();
});
