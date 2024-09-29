async function downloadConvData(eventData) {
        try {
            const response = await fetch('/api/conversation_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(eventData)
            });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const disposition = response.headers.get('Content-Disposition');
        const filenameRegex = /filename="(.+)"/;
        const matches = filenameRegex.exec(disposition);
        const filename = matches && matches[1] ? matches[1] : 'conversation.zip';

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function downloadTextData(eventData) {
        try {
            const response = await fetch('/api/text_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(eventData)
            });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const disposition = response.headers.get('Content-Disposition');
        const filenameRegex = /filename="(.+)"/;
        const matches = filenameRegex.exec(disposition);
        const filename = matches && matches[1] ? matches[1] : 'conversation.zip';

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function checkSessionExp() {
    try {
        let response = await fetch('/api/session_exp');
        let resp_data = await response.json();
        if (!resp_data) {
            window.location.href = '/login'
        }
    } catch (err) {
        console.error(err)
    }
}

document.addEventListener('DOMContentLoaded', function () {
    setInterval(checkSessionExp, 10000);
})
