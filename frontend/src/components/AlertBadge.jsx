export default function AlertBadge({ active, label }) {
  if (!active) return null;
  return (
    <span
      style={{
        display: "inline-block",
        background: "#f59e0b",
        color: "#fff",
        padding: "2px 8px",
        borderRadius: "4px",
        fontSize: "0.75rem",
        fontWeight: 600,
        marginRight: "4px",
      }}
    >
      ⚠ {label}
    </span>
  );
}
