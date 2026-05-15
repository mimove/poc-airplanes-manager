export default function AlertBadge({ active, label }) {
  return active ? <span>{label}</span> : null;
}
