import { useState } from "react";
import "./App.css";
import { translateText } from "./api";

const TARGET_LANGUAGES = [
  "english",
  "hindi",
  "bengali",
  "tamil",
  "telugu",
  "marathi",
  "gujarati",
  "punjabi",
  "kannada",
  "malayalam",
  "urdu",
  "french",
  "spanish",
  "german",
];

function titleCase(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function App() {
  const [text, setText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("english");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleTranslate(event) {
    event.preventDefault();

    if (!text.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await translateText(text, targetLanguage);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const showRefined =
    result &&
    result.refined_translation &&
    result.refined_translation.trim() !== result.translated_text.trim();

  return (
    <div className="app">
      <header className="header">
        <h1>
          Bhasha<span>Bridge</span>
        </h1>
        <p>Multilingual translation for Indian languages &amp; beyond</p>
      </header>

      <form className="card" onSubmit={handleTranslate}>
        <label className="label" htmlFor="text">
          Text to translate
        </label>
        <textarea
          id="text"
          className="textarea"
          placeholder="Type or paste text in any language…"
          value={text}
          onChange={(event) => setText(event.target.value)}
          rows={4}
        />

        <div className="controls">
          <div className="field">
            <label className="label" htmlFor="target">
              Translate to
            </label>
            <select
              id="target"
              className="select"
              value={targetLanguage}
              onChange={(event) => setTargetLanguage(event.target.value)}
            >
              {TARGET_LANGUAGES.map((lang) => (
                <option key={lang} value={lang}>
                  {titleCase(lang)}
                </option>
              ))}
            </select>
          </div>

          <button
            className="button"
            type="submit"
            disabled={loading || !text.trim()}
          >
            {loading ? "Translating…" : "Translate"}
          </button>
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="card result">
          <div className="result-main">
            <span className="result-label">Translation</span>
            <p className="translation">{result.translated_text}</p>
          </div>

          {showRefined && (
            <div className="result-block">
              <span className="result-label">Refined</span>
              <p>{result.refined_translation}</p>
            </div>
          )}

          <div className="meta">
            <span className="chip">Detected: {result.detected_language}</span>
            <span className="chip">
              Confidence: {Math.round(result.confidence_score * 100)}%
            </span>
            <span className="chip">Time: {result.processing_time}s</span>
          </div>
        </div>
      )}

      <footer className="footer">Powered by NLLB + IndicTrans2</footer>
    </div>
  );
}

export default App;
