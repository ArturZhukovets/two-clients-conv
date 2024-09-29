let fullScreen = false;
const elem = document.documentElement;

async function openFullscreen() {
    if (elem.requestFullscreen) {
        await elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        await elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        await elem.msRequestFullscreen();
    }
}

async function closeFullscreen() {
    if (document.exitFullscreen) {
        await document.exitFullscreen();
    } else if (document.webkitExitFullscreen) { /* Safari */
        await document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE11 */
        await document.msExitFullscreen();
    }
}

function setAutoDirection() {
    let langSelector = document.querySelector('.q-menu');
    if (langSelector){
        let divElements = langSelector.querySelectorAll('div');
        if (divElements.length > 0 && divElements[0].getAttribute('dir') === 'auto') {
            return;
        }
        divElements.forEach(function(div) {
            div.setAttribute('dir', 'auto');
        });
    }
}

async function checkSessionExp() {
    try {
        let response = await fetch('/api/session_exp');
        let resp_data =await response.json();
        if (!resp_data) {
            window.location.href = '/login'
        }
    } catch (err) {
        console.error(err)
    }
}

function initScrollObserver() {
    const chat_container = document.querySelector('.chat-container');
    const chat_window = document.querySelector('.chat-window');

    if (chat_container && chat_window) {
        chat_window.scrollTop = chat_window.scrollHeight;
        let observer = new MutationObserver((mutationsList) => {
            for (const mutation of mutationsList) {
                chat_window.scrollTop = chat_window.scrollHeight;
            }
        });
        const config = {childList: true};
        observer.observe(chat_container, config);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const companyLogo = document.querySelector('.company-logo')

    companyLogo.addEventListener('contextmenu', async (e) => {
        e.preventDefault();
        if (fullScreen) {
            await closeFullscreen()
            fullScreen = false
        } else {
            await openFullscreen()
            fullScreen = true
        }
    })

    setInterval(checkSessionExp, 10000);
    let bodyObserver = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                initScrollObserver();
                setAutoDirection();
            }
        }
    });

    const bodyConfig = { childList: true, subtree: true };
    bodyObserver.observe(document.querySelector('.my-page-container'), bodyConfig);
    initScrollObserver()
})
