import unittest
from poker_simulations.engine import *

from poker_simulations.player import Player, EmptySeat, Slave, Players
from .io_tests import ExampleHands


class CardTests(unittest.TestCase):
    def test_card(self):
        C = Card(2, 'S')
        self.assertTrue(isinstance(C, Card))

    def test_card_errors(self):
        pass

    def test_card_equiv(self):
        c1 = Card(6, 'H')
        c2 = Card(6, 'H')
        self.assertTrue(c1 == c2)

    def test_card_not_equiv(self):
        c1 = Card(6, 'H')
        c2 = Card(6, 'D')
        self.assertTrue(c1 != c2)

    def test_card_greater_than_and_less_than(self):
        c1 = Card(2, 'S')
        c2 = Card(3, 'S')
        self.assertTrue(c2 > c1)
        self.assertTrue(c1 < c2)

    def test_card_greater_than_and_less_than2(self):
        c1 = Card('A', 'S')
        c2 = Card('K', 'S')
        self.assertTrue(c1 > c2)
        self.assertTrue(c2 < c1)


class DeckTests(unittest.TestCase):
    def setUp(self):
        self.D = Deck()
        self.D.shuffle()

    def test_number_of_cards(self):
        self.assertEqual(len(self.D.cards), 52)

    def test_shuffling(self):
        self.assertFalse(self.D == self.D.shuffle())

    def test_shuffling2(self):
        """
        make sure shuffling doesn't happen in
        predictable way
        :return:
        """
        D1 = Deck()
        D2 = Deck()
        self.assertFalse(D1 == D2)

    def test_get_card(self):
        self.assertEqual(Card(5, 'S'), self.D.get(5, 'S'))

    def test_get_card_removed_from_deck(self):
        card = self.D.get(5, 'D')
        self.assertEqual(len(self.D), 51)

    def test_pop(self):
        d = Deck()
        len_before = len(d)
        d.pop()
        len_after = len(d)
        self.assertNotEqual(len_before, len_after)

    def test_place(self):
        card = Card(5, 'D')
        d = Deck()
        d = d.place(0, card)
        self.assertEqual(d[0], card)


class PlayerTests(unittest.TestCase):
    def setUp(self):
        self.p = [Player(name='player{}'.format(i), stack=1.0,
                         position=POSITIONS[i]) for i in range(9)]

    def test_player(self):
        p = Player('Ciaran', 50, 1, 'BTN')
        self.assertIsInstance(p, Player)


class EmptySeatTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_name(self):
        e = EmptySeat('co')
        self.assertEqual('Empty', e.name)

    def test_status(self):
        e = EmptySeat('co')
        self.assertEqual('Empty', e.status)

    def test_stack(self):
        e = EmptySeat('co')
        self.assertEqual(0, e.stack)


class SlaveTests(unittest.TestCase):
    def setUp(self):
        self.line = {
            'Jamex19': [
                {'player': 'Jamex19',
                 'action': 'raises',
                 'amount': 0.5,
                 'pot': 0.75},
                {'player': 'Jamex19',
                 'action': 'bets',
                 'amount': '0.90',
                 'pot': None},
                {'player': 'Jamex19',
                 'action': 'calls',
                 'amount': '1.65',
                 'pot': None},
                {'player': 'Jamex19',
                 'action': 'checks',
                 'amount': None,
                 'pot': None},
                {'player': 'Jamex19',
                 'action': 'calls',
                 'amount': '3.25',
                 'pot': None}
            ]}

    def test_instantiation(self):
        s = Slave(position='co', stack=500, line=self.line,
                  name='slavador')
        self.assertIsInstance(s, Slave)

    def test_(self):
        s = Slave(position='co', stack=500, line=self.line,
                  name='Jamex19')
        p = Players.full_ring()
        p['btn'] = s
        t = Table(p)
        t.play_game()

        print(t.game)

        ##maybe i need to emulate all the players
        ##actions, not just the one i'm following.

    def test__(self):
        ##todo what about subclassing table and literally rigging the deck

        # todo extract lines must be changed so keys are position
        eh = ExampleHands().hand5_game_end_at_showdown()
        game = Game.from_parser(eh)

        t = Table(game=game, players=game.players)
        # for pos, pl in game.players.items():
        #     print(pos, pl)
        print(t.play_game())
        # todo change extract i
        # p = Players()
        # print(game.players)
        # for pos, line in game.extract_lines().items():
        #     print(pos, line)
        #     line = line[0]
        #     p[pos] = Slave(position=pos, name=line['name'],
        #                    )
        # # print(p)


class PlayersTest(unittest.TestCase):
    def setUp(self):
        import numpy
        seats = numpy.linspace(1, 9, num=9)
        shuffle(seats)
        # shuffle(positions)
        p = {}
        for i, pos in POSITIONS.items():
            p[pos] = Player(name='player' + str(i), position=pos, stack=1.0)
        self.p = p

        assert self.p['btn'] != self.p['co']

    def test_players_ordered(self):
        p = Players(self.p)
        self.assertGreater(p[7], p[6])

    def test_position1(self):
        p = Players(self.p)
        self.assertEqual(p[0].position, 'btn')

    def test_position4(self):
        p = Players(self.p)
        self.assertEqual(p[3].position, 'utg1')

    def test_position9(self):
        p = Players(self.p)
        self.assertEqual(p[8].position, 'co')

    def test_len(self):
        p = Players(self.p)
        self.assertEqual(len(p), 9)

    def test_iterable_is_dct(self):
        p = Players(self.p)
        self.assertEqual(p['btn'].name, 'player0')

    def test_iter(self):
        p = Players(self.p)

        l = []
        for i in p:
            l.append(i)
        self.assertListEqual(['btn', 'sb', 'bb', 'utg1', 'utg2', 'mp1', 'mp2', 'mp3', 'co'], l)


class GameTests(unittest.TestCase):

    def setUp(self):
        self.p1 = {'name': 'a', 'stack': 100, 'position': 'btn'}
        self.p2 = {'name': 'b', 'stack': 110, 'position': 'sb'}
        self.p3 = {'name': 'c', 'stack': 190, 'position': 'bb'}
        self.p4 = {'name': 'd', 'stack': 140, 'position': 'utg1'}
        self.p5 = {'name': 'e', 'stack': 160, 'position': 'utg2'}
        self.p6 = {'name': 'f', 'stack': 120, 'position': 'mp1'}
        self.p7 = {'name': 'g', 'stack': 110, 'position': 'mp2'}
        self.p8 = {'name': 'h', 'stack': 100, 'position': 'mp3'}
        self.p = [self.p1, self.p2, self.p3, self.p4,
                  self.p5, self.p5, self.p7, self.p8]
        self.p = Players([Player(**i) for i in self.p])

    def test_create_seats1(self):
        g = Game(self.p)
        expected = 140
        self.assertEqual(expected, g.seats[3].stack)

    def test_create_seats2(self):
        g = Game(self.p)
        expected = 'Empty'
        self.assertEqual(expected, g.seats[8].status)

    def test_to_yml(self):
        p = self.p
        t = Table(name='super_poker', players=p)
        game = t.play_game(to='river')
        self.assertTrue('players: !Players' in game.to_yaml())

    def test_yaml_load(self):
        string = """players: !Players
  num_players: 8
  iterable:
    btn: !Player
      name: a
      stack: !Stack
        amount: 100
        currency: $
      position: btn
      status: playing
      cards:
      - !Card
        rank: 9
        suit: H
      - !Card
        rank: 6
        suit: D
      hole_cards_hidden: true
    sb: !Player
      name: b
      stack: !Stack
        amount: 110
        currency: $
      position: sb
      status: playing
      cards:
      - !Card
        rank: 4
        suit: D
      - !Card
        rank: 7
        suit: C
      hole_cards_hidden: true
    bb: !Player
      name: c
      stack: !Stack
        amount: 190
        currency: $
      position: bb
      status: playing
      cards:
      - !Card
        rank: Q
        suit: H
      - !Card
        rank: A
        suit: D
      hole_cards_hidden: true
    utg1: !Player
      name: d
      stack: 90.0
      position: utg1
      status: playing
      cards:
      - !Card
        rank: 6
        suit: S
      - !Card
        rank: 6
        suit: C
      hole_cards_hidden: true
    utg2: !Player
      name: e
      stack: !Stack
        amount: 160
        currency: $
      position: utg2
      status: playing
      cards:
      - !Card
        rank: 9
        suit: C
      - !Card
        rank: 8
        suit: D
      hole_cards_hidden: true
    mp1: !Player
      name: e
      stack: !Stack
        amount: 160
        currency: $
      position: utg2
      status: playing
      cards:
      - !Card
        rank: 10
        suit: H
      - !Card
        rank: 5
        suit: C
      hole_cards_hidden: true
    mp2: !Player
      name: g
      stack: !Stack
        amount: 110
        currency: $
      position: mp2
      status: playing
      cards:
      - !Card
        rank: Q
        suit: C
      - !Card
        rank: 2
        suit: S
      hole_cards_hidden: true
    mp3: !Player
      name: h
      stack: !Stack
        amount: 100
        currency: $
      position: mp3
      status: playing
      cards:
      - !Card
        rank: 10
        suit: D
      - !Card
        rank: 7
        suit: H
      hole_cards_hidden: true
pot: 0"""
        y = Yaml()

    def test_summary(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='river')

    def test_extract_line(self):
        eh = ExampleHands()
        g = Game.from_parser(eh.hand5_game_end_at_showdown())
        # print(g.action_history)
        lines = g.extract_lines()
        print(lines)
        self.assertEqual(lines['Jamex19'][0]['action'], 'raises')

    def test_positions(self):
        eh = ExampleHands()
        g = Game.from_parser(eh.hand5_game_end_at_showdown())
        self.assertEqual(g.positions()['shelepova'], 'btn')

    def test_setattr(self):
        p = self.p
        t = Table(name='super_poker', players=p)
        game = t.play_game(to='river')
        self.assertNotEqual(game.action_history['preflop'], [])

    # def test_mind_control(self):
    #     # make sure that test mind control works.
    #     # Then modify the player class action method such that
    #     # when mind control is not empty, they player is forced to
    #     # act in a predefined way
    #     eh = ExampleHands()
    #     g = Game.from_parser(eh.hand5_game_end_at_showdown())
    #     self.assertEqual('calls', g.players['utg1'].mind_control[2]['action'])


class ParsePokerstarsTests(unittest.TestCase):

    def setUp(self):
        self.eh = ExampleHands()

    def test(self):
        '''

        can I somehow use the game class to put actions in the plsyers mouth?


        Returns:

        '''
        g = Game.from_parser2(self.eh.hand5_game_end_at_showdown())
        # t = Table(game=g, players=g.players)
        # print(t.replay_game())


class TableTests(unittest.TestCase):
    positions = {
        1: 'btn',
        2: 'sb',
        3: 'bb',
        4: 'utg1',
        5: 'utg2',
        6: 'mp1',
        7: 'mp2',
        8: 'mp3',
        9: 'co',
    }

    def setUp(self):
        self.p = [Player(name='player{}'.format(i), stack=1.0,
                         position=self.positions[i]) for i in range(1, 9)]
        self.p = Players(self.p)

    def test_instantiation(self):
        t = Table(name='super_poker', players=self.p)
        self.assertIsInstance(t, Table)

    def test_play_to_flop(self):
        p = self.p
        t = Table(name='super_poker', players=p)
        game = t.play_game(to='flop')
        self.assertNotEqual([], game.game_info.action_history['preflop'])

    def test_play_to_turn(self):
        p = self.p
        t = Table(name='super_poker', players=p)
        game = t.play_game(to='turn')
        h = game.game_info.action_history
        self.assertNotEqual([], game.game_info.action_history['flop'])

    def test_play_to_river(self):
        p = self.p
        t = Table(name='super_poker', players=p)
        game = t.play_game(to='river')
        self.assertNotEqual([], game.game_info.action_history['river'])

    def test_we_have_intended_number_of_empty_seats(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='preflop')
        expected = 1
        l = []
        for pos, player in game.players.items():
            if player.name == 'Empty':
                l.append(player)
        self.assertEqual(expected, len(l))

    def test_deal_holecards(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='preflop')
        for i in game.players:
            if game.players[i].name != 'Empty':
                self.assertEqual(2, len(game.players[i].cards))

    def test_deal_flop(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='flop')
        self.assertEqual(3, len(game.game_info.community_cards))

    def test_deal_flop(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='flop')
        self.assertEqual(3, len(game.game_info.community_cards))

    def test_deal_turn(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='turn')
        self.assertEqual(4, len(game.game_info.community_cards))

    def test_deal_river(self):
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='river')
        self.assertEqual(5, len(game.game_info.community_cards))

    def test_pot_during_play(self):
        p = self.p
        t = Table(name='super_poker', players=p)
        game = t.play_game(to='river')
        h = game.game_info.action_history
        self.assertNotEqual([], game.game_info.action_history['river'])

    def test_Winner(self):
        ## the way Im updating the history needs to change
        ## currently I append each action to the list for a steet
        ## but this
        ##todo implement another set of options for the bb as they can only checka dn raise

        ## when calling a raise, we need to modify the existing money

        ## get players that are still in the game and test to see whether the amount hte
        ## have put into the pot is the same. If not we continue
        t = Table(name='super_poker', players=self.p)
        game = t.play_game(to='river')
        winner = t.get_winner(t.game)
        self.assertTrue(winner['winner'])

    def test_play_batch_games(self):
        p = [Player(name='player{}'.format(i), stack=500,
                    position=self.positions[i]) for i in range(1, 9)]
        p = Players(p)
        t = Table(name='super_poker', players=p)
        winners = t.play_batch(2)
        # for i in winners:
        #     print(i)
        # h = game.game_info.action_history
        # for i in h:
        #     print(i, h[i])
        # self.assertNotEqual([], game.game_info.action_history['river'])

        ## at the start of every street, has_checked needs to be turned to False

class RiggedTableTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_correct_cards(self):
        eh = ExampleHands().hand5_game_end_at_showdown()
        game = Game.from_parser(eh)
        rt = RiggedTable(game)
        ex = ['5S', '4D', '2H', '4S']
        self.assertListEqual(ex, rt.deck[:4])

    def test_deck_is_right_len(self):
        eh = ExampleHands().hand5_game_end_at_showdown()
        game = Game.from_parser(eh)
        rt = RiggedTable(game)
        ex = ['5S', '4D', '2H', '4S']
        self.assertEqual(52, len(rt.deck))


class RotatePositionTests(unittest.TestCase):

    def test_full_ring(self):
        p = [Player(name='player{}'.format(i), stack=1.0,
                    position=POSITIONS[i]) for i in range(9)]
        p = Players(p)
        t = Table(name='super_poker', players=p)
        t.play_game(to='river')
        t._rotate_players()
        expected = 'player0'
        self.assertEqual(expected, t.players['sb'].name)

    def test_8_players_btn_not_empty(self):
        p = [Player(name='player{}'.format(i), stack=1.0,
                    position=POSITIONS[i]) for i in range(8)]
        p = Players(p)
        t = Table(name='super_poker', players=p)
        t.play_game(to='river')
        t._rotate_players()
        expected = 'Empty'
        self.assertNotEqual(expected, t.players['btn'].status)

    def test_8_players_sb_not_empt(self):
        p = [Player(name='player{}'.format(i), stack=1.0,
                    position=POSITIONS[i]) for i in range(8)]
        p = Players(p)
        t = Table(name='super_poker', players=p)
        t.play_game(to='river')
        t._rotate_players()
        expected = 'Empty'
        self.assertNotEqual(expected, t.players['sb'].status)

    def test_8_players_bb_not_empty(self):
        p = [Player(name='player{}'.format(i), stack=1.0,
                    position=POSITIONS[i]) for i in range(8)]
        p = Players(p)
        t = Table(name='super_poker', players=p)
        t.play_game(to='river')
        t._rotate_players()
        for pos, pl in t.players.items():
            print(pos, pl)
        expected = 'Empty'
        self.assertNotEqual(expected, t.players['bb'].status)

    def test_6_players_bb_not_empty(self):
        p = [Player(name='player{}'.format(i), stack=1.0,
                    position=POSITIONS[i]) for i in range(6)]
        p = Players(p)
        t = Table(name='super_poker', players=p)
        t.play_game(to='river')
        t._rotate_players()
        for pos, pl in t.players.items():
            print(pos, pl)
        expected = 'Empty'
        self.assertNotEqual(expected, t.players['bb'].status)


# todo enable controlling the game play via a script in order to test all potential situations.

if __name__ == '__main__':
    unittest.main()
