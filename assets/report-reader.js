(() => {
  "use strict";

  const API_KEY_STORAGE_KEY = "newsReportReader.googleTtsApiKey";
  const VOICE_STORAGE_KEY = "newsReportReader.googleTtsVoice";
  const DEFAULT_GOOGLE_VOICE = "cmn-CN-Wavenet-A";
  const GOOGLE_LANGUAGE_CODE = "cmn-CN";
  const WEB_SPEECH_LANG = "zh-CN";
  const GOOGLE_TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize?key=";
  const MAX_GOOGLE_TEXT_BYTES = 4500;

  const encoder = new TextEncoder();

  function getStorageValue(key) {
    try {
      return window.localStorage.getItem(key) || "";
    } catch (_error) {
      return "";
    }
  }

  function setStorageValue(key, value) {
    try {
      if (value) {
        window.localStorage.setItem(key, value);
      } else {
        window.localStorage.removeItem(key);
      }
      return true;
    } catch (_error) {
      return false;
    }
  }

  function getReportText() {
    return Array.from(document.body.querySelectorAll("section"))
      .map((node) => node.innerText.trim())
      .filter(Boolean)
      .join("\n\n");
  }

  function pushByteLimitedText(text, chunks) {
    let current = "";
    for (const character of text) {
      const candidate = `${current}${character}`;
      if (current && encoder.encode(candidate).length > MAX_GOOGLE_TEXT_BYTES) {
        chunks.push(current);
        current = character;
        continue;
      }
      current = candidate;
    }
    if (current) chunks.push(current);
  }

  function splitTextForGoogle(text) {
    const chunks = [];
    let current = "";
    for (const paragraph of text.split(/\n{2,}/)) {
      const candidate = current ? `${current}\n\n${paragraph}` : paragraph;
      if (encoder.encode(candidate).length <= MAX_GOOGLE_TEXT_BYTES) {
        current = candidate;
        continue;
      }
      if (current) chunks.push(current);
      current = "";

      let sentenceChunk = "";
      for (const sentence of paragraph.split(/(?<=[。！？!?；;])\s*/u)) {
        const sentenceCandidate = sentenceChunk ? `${sentenceChunk}${sentence}` : sentence;
        if (encoder.encode(sentenceCandidate).length <= MAX_GOOGLE_TEXT_BYTES) {
          sentenceChunk = sentenceCandidate;
          continue;
        }
        if (sentenceChunk) chunks.push(sentenceChunk);
        sentenceChunk = "";
        if (encoder.encode(sentence).length <= MAX_GOOGLE_TEXT_BYTES) {
          sentenceChunk = sentence;
        } else {
          pushByteLimitedText(sentence, chunks);
        }
      }
      if (sentenceChunk) current = sentenceChunk;
    }
    if (current) chunks.push(current);
    return chunks.filter(Boolean);
  }

  function base64ToBlobUrl(base64Audio) {
    const raw = window.atob(base64Audio);
    const bytes = new Uint8Array(raw.length);
    for (let index = 0; index < raw.length; index += 1) {
      bytes[index] = raw.charCodeAt(index);
    }
    const blob = new Blob([bytes], { type: "audio/mpeg" });
    return URL.createObjectURL(blob);
  }

  function openSettingsDialog(settingsDialog) {
    if (!settingsDialog) return;
    if (typeof settingsDialog.showModal === "function") {
      if (!settingsDialog.open) settingsDialog.showModal();
      return;
    }
    settingsDialog.setAttribute("open", "");
  }

  function closeSettingsDialog(settingsDialog) {
    if (!settingsDialog) return;
    if (typeof settingsDialog.close === "function" && settingsDialog.open) {
      settingsDialog.close();
      return;
    }
    settingsDialog.removeAttribute("open");
  }

  async function synthesizeGoogleAudio(text, apiKey, voiceName) {
    const response = await fetch(`${GOOGLE_TTS_ENDPOINT}${encodeURIComponent(apiKey)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        input: { text },
        voice: {
          languageCode: GOOGLE_LANGUAGE_CODE,
          name: voiceName || DEFAULT_GOOGLE_VOICE,
        },
        audioConfig: {
          audioEncoding: "MP3",
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Google TTS request failed: ${response.status}`);
    }

    const data = await response.json();
    if (!data.audioContent) {
      throw new Error("Google TTS response did not include audioContent");
    }
    return base64ToBlobUrl(data.audioContent);
  }

  function createGooglePlayer(status) {
    const audio = new Audio();
    let urls = [];
    let index = 0;

    function revokeUrls() {
      urls.forEach((url) => URL.revokeObjectURL(url));
      urls = [];
    }

    audio.addEventListener("ended", () => {
      index += 1;
      if (index >= urls.length) {
        status.textContent = "朗读完成。";
        revokeUrls();
        return;
      }
      audio.src = urls[index];
      audio.play();
    });

    return {
      async play(newUrls) {
        audio.pause();
        revokeUrls();
        urls = newUrls;
        index = 0;
        audio.src = urls[index];
        status.textContent = "正在使用 Google TTS 朗读。";
        await audio.play();
      },
      pause() {
        audio.pause();
      },
      resume() {
        if (audio.src) audio.play();
      },
      stop() {
        audio.pause();
        audio.removeAttribute("src");
        revokeUrls();
      },
    };
  }

  function speakWithWebSpeech(text, rate, status) {
    if (!("speechSynthesis" in window) || typeof SpeechSynthesisUtterance === "undefined") {
      status.textContent = "此浏览器不支持浏览器朗读。";
      return false;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = WEB_SPEECH_LANG;
    utterance.rate = Number(rate || 1);
    utterance.onend = () => {
      status.textContent = "朗读完成。";
    };
    status.textContent = "正在使用浏览器语音朗读。";
    window.speechSynthesis.speak(utterance);
    return true;
  }

  function initReader(controls) {
    const status = controls.querySelector("[data-reader-status]");
    const rate = controls.querySelector("[data-reader-rate]");
    const settingsDialog = controls.querySelector("[data-reader-settings]");
    const settingsOpenButton = controls.querySelector("[data-reader-settings-open]");
    const settingsCloseButton = controls.querySelector("[data-reader-settings-close]");
    const settingsScope = settingsDialog || controls;
    const apiKeyInput = settingsScope.querySelector("[data-google-tts-key]") || controls.querySelector("[data-google-tts-key]");
    const voiceSelect = settingsScope.querySelector("[data-google-tts-voice]") || controls.querySelector("[data-google-tts-voice]");
    const googlePlayer = createGooglePlayer(status);

    if (apiKeyInput) apiKeyInput.value = getStorageValue(API_KEY_STORAGE_KEY);
    if (voiceSelect) voiceSelect.value = getStorageValue(VOICE_STORAGE_KEY) || DEFAULT_GOOGLE_VOICE;

    settingsOpenButton?.addEventListener("click", () => {
      if (!settingsDialog) return;
      if (settingsDialog.open) {
        closeSettingsDialog(settingsDialog);
      } else {
        openSettingsDialog(settingsDialog);
      }
    });

    settingsCloseButton?.addEventListener("click", () => {
      closeSettingsDialog(settingsDialog);
    });

    settingsDialog?.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeSettingsDialog(settingsDialog);
    });

    settingsDialog?.addEventListener("click", (event) => {
      if (event.target === settingsDialog) {
        closeSettingsDialog(settingsDialog);
      }
    });

    settingsDialog?.addEventListener("close", () => {
      settingsOpenButton?.focus();
    });

    controls.querySelector("[data-google-tts-save]")?.addEventListener("click", () => {
      const keySaved = setStorageValue(API_KEY_STORAGE_KEY, apiKeyInput?.value.trim() || "");
      const voiceSaved = setStorageValue(VOICE_STORAGE_KEY, voiceSelect?.value || DEFAULT_GOOGLE_VOICE);
      status.textContent = keySaved && voiceSaved ? "Google TTS 设置已保存在本机浏览器。" : "无法写入浏览器本机存储。";
    });

    controls.querySelector("[data-google-tts-clear]")?.addEventListener("click", () => {
      setStorageValue(API_KEY_STORAGE_KEY, "");
      setStorageValue(VOICE_STORAGE_KEY, "");
      if (apiKeyInput) apiKeyInput.value = "";
      if (voiceSelect) voiceSelect.value = DEFAULT_GOOGLE_VOICE;
      status.textContent = "已清除本机 Google TTS 设置。";
    });

    controls.querySelector("[data-reader-start]")?.addEventListener("click", async () => {
      const text = getReportText();
      if (!text) {
        status.textContent = "没有可朗读的正文。";
        return;
      }

      googlePlayer.stop();
      if ("speechSynthesis" in window) window.speechSynthesis.cancel();

      const apiKey = getStorageValue(API_KEY_STORAGE_KEY);
      const voiceName = getStorageValue(VOICE_STORAGE_KEY) || DEFAULT_GOOGLE_VOICE;
      if (apiKey) {
        try {
          status.textContent = "正在请求 Google TTS。";
          const urls = [];
          for (const chunk of splitTextForGoogle(text)) {
            urls.push(await synthesizeGoogleAudio(chunk, apiKey, voiceName));
          }
          await googlePlayer.play(urls);
          return;
        } catch (error) {
          status.textContent = `Google TTS 不可用，改用浏览器朗读。${error.message}`;
        }
      }

      speakWithWebSpeech(text, rate?.value || 1, status);
    });

    controls.querySelector("[data-reader-pause]")?.addEventListener("click", () => {
      googlePlayer.pause();
      if ("speechSynthesis" in window) window.speechSynthesis.pause();
      status.textContent = "已暂停。";
    });

    controls.querySelector("[data-reader-resume]")?.addEventListener("click", () => {
      googlePlayer.resume();
      if ("speechSynthesis" in window) window.speechSynthesis.resume();
      status.textContent = "继续朗读。";
    });

    controls.querySelector("[data-reader-stop]")?.addEventListener("click", () => {
      googlePlayer.stop();
      if ("speechSynthesis" in window) window.speechSynthesis.cancel();
      status.textContent = "已停止。";
    });

    window.addEventListener("beforeunload", () => {
      googlePlayer.stop();
      if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-reader-controls]").forEach(initReader);
  });
})();
