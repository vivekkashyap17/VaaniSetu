const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_KEY = import.meta.env.VITE_API_KEY || "";

export async function translateText(text, targetLanguage, sourceLanguage = "auto") {
  let response;

  try {
    response = await fetch(`${API_BASE}/api/v1/translate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
      },
      body: JSON.stringify({
        text,
        source_language: sourceLanguage,
        target_language: targetLanguage,
      }),
    });
  } catch (err) {
    throw new Error(
      "Could not reach the translation server. Is the backend running?"
    );
  }

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;

    try {
      const data = await response.json();
      if (data.detail) detail = data.detail;
    } catch (_) {
      // non-JSON error body — keep the generic message
    }

    if (response.status === 401) detail = "Invalid or missing API key.";
    if (response.status === 429)
      detail = "Rate limit reached — wait a minute and try again.";

    throw new Error(detail);
  }

  return response.json();
}
