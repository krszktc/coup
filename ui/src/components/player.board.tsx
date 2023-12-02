import { Card } from "./card";

const containerStyles = {
  marginRight: 20,
  display: 'inline-block',
  background: 'lightgrey',
  padding: '5px 20px 15px 25px',
} as const;


export const PlayerBoard = ({ player, isActive }: { player: any, isActive: boolean }) => (
  <div style={containerStyles}>
    <div>
      <p style={{fontWeight: isActive ? 600 : 200}}>
        {player.user.nick} {isActive ? '<---' : ''}
      </p>
      {
        player.cards.map((card: any) => <Card card={card} />)
      }
    </div>
    <div>
      {
        [...Array(player.coins)].map(_ => <span>🟡</span>)
      }
    </div>
    <div style={{ marginTop: 15, float: 'right' }}>
      <button style={{ marginRight: 5 }}>pass</button>
      <button style={{ marginRight: 10 }}>challenge</button>
    </div>
  </div>
)