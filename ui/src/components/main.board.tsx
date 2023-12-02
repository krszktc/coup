import { useState } from "react"
import { PlayerBoard } from "./player.board"
import { Card } from "./card"

const MOCK_BASIC_CARDS = [
  {
    code: 'e1',
    action: 'Income',
    effect: 'Take 1 coin',
  },
  {
    code: 'e2',
    action: 'Foreign Aid',
    effect: 'Take 2 coin',
  },
  {
    code: 'e3',
    action: 'Coup',
    effect: 'Pay 7 coin',
  }
]

const MOCK_POWER_CARDS = [
  {
    code: 'dk',
    characterName: 'Duke',
    defaultColor: 'red',
    action: 'Tax',
    effect: 'Take 3 coins',
    contraction: 'Foreign Aid',
  },
  {
    code: 'as',
    characterName: 'Assassin',
    defaultColor: 'grey',
    action: 'Assassinate',
    effect: 'Pay3 coins',
    contraction: '',
  },
  {
    code: 'am',
    characterName: 'Ambassador',
    defaultColor: 'yellow',
    action: 'Exchange',
    effect: 'Exchange cards',
    contraction: 'Stealing',
  },
  {
    code: 'cp',
    characterName: 'Captain',
    defaultColor: 'blue',
    action: 'Steal',
    effect: 'Steal 2 coins',
    contraction: 'Stealing',
  },
  {
    code: 'cn',
    characterName: 'Contessa',
    defaultColor: 'orange',
    contraction: 'Assassinate',
  },
]

const MOCK_PLAYERS = [
  {
    user: { id: '11', name: 'some name', nick: 'nick1' },
    coins: 2,
    cards: [{ ...MOCK_POWER_CARDS[1] }, { ...MOCK_POWER_CARDS[4] }],
    claim: undefined,
  },
  {
    user: { id: '22', name: 'other name', nick: 'nick2' },
    coins: 2,
    cards: [{ ...MOCK_POWER_CARDS[0] }, { ...MOCK_POWER_CARDS[1] }],
    claim: undefined,
  },
  {
    user: { id: '33', name: 'another name', nick: 'nick3' },
    coins: 2,
    cards: [{ ...MOCK_POWER_CARDS[2] }, { ...MOCK_POWER_CARDS[3] }],
    claim: undefined,
  },
  {
    user: { id: '44', name: 'next name', nick: 'nick4' },
    coins: 2,
    cards: [{ ...MOCK_POWER_CARDS[2] }, { ...MOCK_POWER_CARDS[4] }],
    claim: undefined,
  }
]

const MOCK_GAME = {
  id: '112233',
  cards: [...MOCK_POWER_CARDS],
  players: [MOCK_PLAYERS],
  action_player: MOCK_PLAYERS[1],
  state: 'INVITE'
}

export const MainBoard = () => (
  <div style={{ marginLeft: 15 }}>
    <p>game id: {MOCK_GAME.id}</p>
    <p>status: {MOCK_GAME.state}</p>
    {
      MOCK_PLAYERS.map(player =>
        <PlayerBoard
          player={player}
          isActive={player === MOCK_GAME.action_player} />
      )
    }
    <div style={{ marginTop: 50 }}>
      {
        [...MOCK_BASIC_CARDS, ...MOCK_POWER_CARDS].map(card => (
          <div style={{ display: 'inline-block' }}>
            <Card card={card} />
            <p>{card.effect ?? 'none'}</p>
          </div>
        ))
      }
    </div>
  </div>
)
