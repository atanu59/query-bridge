import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000/api/query";

function App() {
  const [question, setQuestion] = useState("");
  const [lastQuestion, setLastQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function runQuery(q) {
    if (!q.trim()) {
      setError("Please enter a question.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    setLastQuestion(q);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await response.json();
      if (data.ok) {
        setResult(data);
      } else {
        setError(data.error);
        if (data.sql) setResult({ sql: data.sql });
      }
    } catch {
      setError("Could not reach the server. Is Flask running?");
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setQuestion("");
    setLastQuestion("");
    setResult(null);
    setError("");
  }

  return (
    <div className="container">
      <h1>Query Bridge</h1>
      <p className="subtitle">Ask your database a question in plain English.</p>

      <div className="input-row">
        <input
          type="text"
          value={question}
          placeholder="e.g. Which customers placed orders over 500?"
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runQuery(question)}
        />
        <button onClick={() => runQuery(question)} disabled={loading}>
          {loading ? "Running..." : "Run"}
        </button>
        <button onClick={() => runQuery(lastQuestion)} disabled={loading || !lastQuestion}>
          Refresh
        </button>
        <button onClick={handleClear} disabled={loading}>
          Clear
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {result?.sql && (
        <div className="sql-box">
          <strong>Generated SQL</strong>
          <pre>{result.sql}</pre>
        </div>
      )}

      {result?.ok && (
        <div className="table-wrap">
          <p>{result.row_count} row(s)</p>
          <table>
            <thead>
              <tr>
                {result.columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.rows.map((row, i) => (
                <tr key={i}>
                  {row.map((cell, j) => (
                    <td key={j}>{cell === null ? "NULL" : String(cell)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;