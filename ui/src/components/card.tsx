const cardStyles = {
  height: 250,
  width: 150,
  marginRight: 10,
  marginBottom: 15,
  display: 'inline-block',
  border: 'solid 2px',
  cursor: 'pointer',
} as const;

export const Card = ({ card }: { card: any }) => (
  <div style={{ ...cardStyles, background: card.defaultColor }}>
    <span style={{ marginLeft: 5 }}>{card.characterName ?? 'X'}</span>
  </div>
)