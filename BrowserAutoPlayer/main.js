
let runningIntervals = {};

tabsEnum = Object.freeze({
    HOME: "home",
    LAB: "lab",
    STATS: "stats",
    RECYCLER: "recycler",
    GATE: "gate",
    REFLECTION: "reflection"
})

function changeTab(tabEnum) {
    SharkGame.TabHandler.keybindSwitchTab(tabEnum);
}

function saveGame(timeout) {
    runningIntervals["SaveInterval"] = setInterval(() => {
        SharkGame.Save.saveGame();
        SharkGame.Log.addMessage(`Saved game.`);
    }, timeout);
}

eventKeyS = new KeyboardEvent('keydown', {code: 'KeyS'});
function pressKey(keyEvent, timeout) {
    runningIntervals[`${keyEvent.code}-KeyInterval`] = setInterval(() => {
        document.dispatchEvent(keyEvent);
    }, timeout);
}

function print_running_intervals(timout) {
    runningIntervals["PrintInterval"] = setInterval(() => {
        let keys = Object.keys(runningIntervals);
        console.log("Running intervals: ", keys);
    }, timout);
}

function click_all_buttons_in_page(timeout) {
    runningIntervals["ClickAllButtonsInterval"] = setInterval(() => {
        changeTab(tabsEnum.HOME);
        let buttons = document.getElementById("buttonList").children;
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].click();
        }
    }, timeout);
}

function start_intervals() {
    print_running_intervals(10000);
    pressKey(eventKeyS, 1000);
    click_all_buttons_in_page(5000);
    saveGame(5000);
}

function stop_intervals() {
    for (const [key, value] of Object.entries(runningIntervals)) {
        console.log(`Clearing interval: ${key}`);
        clearInterval(value);
    }
}

start_intervals();
