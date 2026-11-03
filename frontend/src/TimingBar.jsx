function TimingBar({ timings, roundTrip }) {
  if (!timings) return null;

  const seconds = (ms) => (ms / 1000).toFixed(2) + " s";

  return (
    <div className="timing-bar">
      <span>
        Total: <strong>{seconds(roundTrip)}</strong>
      </span>
      {timings.ai_ms !== undefined && <span>AI: {seconds(timings.ai_ms)}</span>}
      {timings.db_ms !== undefined && <span>Database: {seconds(timings.db_ms)}</span>}
    </div>
  );
}

export default TimingBar;