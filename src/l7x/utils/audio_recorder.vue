<template>
</template>

<script>
export default {
    data() {
        return {
            isRecording: false,
            audioChunks: [],
            mediaRecorder: null,
            stream: null,
            audioURL: null,
            audioBlob: null,
        };
    },
    mounted() {
        this.requestMicrophonePermission();
    },
    watch: {
        audioBlob(newBlob, oldBlob) {
            if (newBlob && newBlob !== oldBlob) {
                this.emitBlob();
            }
        },
    },
    methods: {
        async requestMicrophonePermission() {
            try {
                this.stream = await navigator.mediaDevices.getUserMedia({audio: true});
            } catch (error) {
                console.error('Error accessing microphone:', error);
            }
        },
        async startRecording() {
            try {
                if (!this.stream) {
                    await this.requestMicrophonePermission();
                }
                this.audioChunks = [];
                this.mediaRecorder = new MediaRecorder(this.stream);
                this.mediaRecorder.addEventListener('dataavailable', (event) => {
                    if (event.data.size > 0) {
                        this.audioChunks.push(event.data);
                    }
                });
                this.mediaRecorder.start();
                this.isRecording = true;
            } catch (error) {
                console.error('Error accessing microphone:', error);
            }
        },
        stopRecording() {
            if (this.isRecording) {
                this.mediaRecorder.addEventListener('stop', () => {
                    this.isRecording = false;
                    this.saveBlob();
                });
                this.mediaRecorder.stop();
            }
        },
        async saveBlob() {
            this.audioBlob = await new Blob(this.audioChunks, {type: 'audio/wav'});
        },
        async emitBlob() {
            try {
                const formData = new FormData()
                formData.append('file', this.audioBlob)
                let save_audio_response = await fetch('/api/save_audio', {
                    method: 'POST',
                    body: formData,
                    signal: AbortSignal.timeout(20000) ,
                });
                if (save_audio_response.ok) {
                    let response_json = await save_audio_response.json()
                    if (response_json.status === 'ok') {
                        await this.$emit('audio_ready', {
                            status: 'ok',
                            audio_uuid: response_json.audio_uuid,
                        });
                        return
                    }
                }
                await this.$emit('audio_ready', {status: 'response_error'});
            } catch (error) {
                if (error.name === 'TimeoutError') {
                    console.error('Timeout: It took more than 20 seconds to get the result!');
                    await this.$emit('audio_ready', {status: 'timeout_error'});
                } else if (error.name === 'AbortError') {
                    console.error('Fetch aborted by user action (browser stop button, closing tab, etc.');
                    await this.$emit('audio_ready', {status: 'abort_error'});
                } else {
                    console.error('Fetch Audio Error', error);
                    await this.$emit('audio_ready', {status: 'error'});
                }
            }
        },
    },
};
</script>
