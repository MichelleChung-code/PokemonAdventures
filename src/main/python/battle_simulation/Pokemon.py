import battle_simulation.constants as const
import random
from battle_simulation.battle_common import battle_log_msg


class Pokemon:

    def __init__(self, name, pokemon_info_df, moveset, status_effect_df):
        """
        Args:
            name: <float> Pokemon name
            pokemon_info_df: <pd.DataFrame> containing the Pokemon base stat information
            moveset: <dict> of the moveset, can only contain damage causing moves currently.  4 moves max.

            Example of moveset dict:
                {1: {'Confusion': {const.POW: 50, const.ACC: 100}}, 2: {'Pound': {const.POW: 40, const.ACC: 100}},
                3: {'Mega Punch': {const.POW: 80, const.ACC: 85}}, 4: {'Psychic': {const.POW: 90, const.ACC: 100}}}
        """
        self.name = name
        self.hp = pokemon_info_df.loc[name, const.HP]
        self.max_hp = self.hp
        self.attack = pokemon_info_df.loc[name, const.ATTACK]
        self.defense = pokemon_info_df.loc[name, const.DEFENSE]
        self.speed = pokemon_info_df.loc[name, const.SPEED]
        self.moveset = moveset
        self.status_effect = None
        self.status_effect_turn = 0
        self.status_effect_info = status_effect_df

        # Check that moveset has exactly 4 moves
        if len(self.moveset.keys()) != 4:
            raise Exception('{name} moveset does not contain 4 moves.'.format(name=self.name))

    def apply_status_effect(self, other_pokemon):
        """
        Apply existing status effect on current pokemon.

        Args:
            other_pokemon: <Pokemon> that current is battling against.  Needed for the leech seed effect.
        """
        # Assume can only be inflicted by 1 effect at a time

        # todo add condition to not allow being affected with other condition, right now will just update to new condition
        # If effected with inf length status condition, cannot be affected with new condition

        min_turn = self.status_effect_info.loc[self.status_effect, const.MIN_TURN]
        max_turn = self.status_effect_info.loc[self.status_effect, const.MAX_TURN]

        if (min_turn == 'inf' and max_turn != 'inf') or (min_turn != 'inf' and max_turn == 'inf'):
            raise Exception("Max and min turn inputs either need to be both 'inf' or neither 'inf'")

        if self.status_effect_turn == max_turn:
            battle_log_msg('{name} recovered from {status_name}'.format(name=self.name, status_name=self.status_effect))
            self.status_effect = None
            self.status_effect_turn = 0
            return

        if self.status_effect not in [const.FROZEN, const.PARALYZED]:  # logging handled during move use for these ones
            battle_log_msg('{name} is {status_name}'.format(name=self.name, status_name=self.status_effect))

        effect_1 = self.status_effect_info.loc[self.status_effect, const.EFFECT_1]
        effect_2 = self.status_effect_info.loc[self.status_effect, const.EFFECT_2]

        effect_1 = effect_1.split('_') if isinstance(effect_1, str) else effect_1
        effect_2 = effect_2.split('_') if isinstance(effect_2, str) else effect_2

        damage_from_effect = 0

        # dictionary value False if the effect is handled elsewhere (not in this function)
        status_effect_dict = {const.ATTACK: self.base_attack_speed_stat_status_effect,
                              const.SPEED: self.base_attack_speed_stat_status_effect,
                              const.DAMAGE_PERC_MAX_HP: self.damage_max_hp_percent_status_effect,
                              const.DAMAGE_CHANCE: self.damage_chance_status_effect,
                              const.DAMAGE_PERC_MAX_HP_INC: self.damage_max_hp_percent_increasing_status_effect,
                              const.OPP_HP_GAIN: self.opponent_gains_hp_status_effect,
                              const.SKIP_TURN: False}

        for effect in [effect_1, effect_2]:
            if not isinstance(effect, list):  # np.NaN value
                continue
            else:
                effect[-1] = float(effect[-1])

            status_effect_call = status_effect_dict.get(effect[0])

            if status_effect_call is None:
                raise NotImplemented
            elif status_effect_call is False:
                pass  # handled separately outside of this function
            elif effect[0] == const.OPP_HP_GAIN:
                status_effect_call(other_pokemon, damage_from_effect)
            elif effect[0] in [const.ATTACK, const.SPEED]:  # affects base stats
                # only apply the first time that the status effect takes place
                if self.status_effect_turn == 1:
                    status_effect_call(effect)
            else:
                status_effect_call(effect)

        if damage_from_effect != 0:
            battle_log_msg('{name} is {status_name} and lost {damage} HP.'.format(name=self.name,
                                                                                  status_name=self.status_effect,
                                                                                  damage=damage_from_effect))

    def base_attack_speed_stat_status_effect(self, effect):
        """
        Applies the status decrease to either speed or attack base stats
        Args:
            effect: <list> [base stat to apply to, percentage decrease of base stat to apply]
            data types are [<str>, <float>]
        """
        self.attack *= (effect[-1] / 100) if effect[0] == const.ATTACK else self.attack
        self.speed *= (effect[-1] / 100) if effect[0] == const.SPEED else self.speed

    def damage_max_hp_percent_status_effect(self, effect):
        """
        Applies percentage of max hp decrease on current hp
        Args:
            effect: <list> [const.DAMAGE_PERC_MAX_HP <str>, percentage to decrease hp by <float>]
        """
        damage_from_effect = (self.max_hp * (effect[-1] / 100))
        self.hp -= damage_from_effect

    def damage_chance_status_effect(self, effect):
        """
        Applies 10% max hp decrease on current hp depending on the chance to apply damage given
        Args:
            effect: <list> [const.DAMAGE_CHANCE <str>, chance of self-inflicting damage <float>]
        """
        # assume self-inflicted damage is 10% of max HP
        if random.randrange(0, 100) < effect[-1]:
            damage_from_effect = self.max_hp * 0.1
            self.hp -= damage_from_effect

    def damage_max_hp_percent_increasing_status_effect(self, effect):
        """
        Applies percentage of max hp damage to current hp.  Each turn the applied damage increases by this amount too.
        Args:
            effect: <list> [const.DAMAGE_PERC_MAX_HP_INC <str>, percentage to decrease hp by <float>]
        """
        # amount increases per turn that it is in effect
        damage_from_effect = (self.max_hp * (effect[-1] / 100) * self.status_effect_turn)
        self.hp -= damage_from_effect

    def opponent_gains_hp_status_effect(self, other_pokemon, damage_from_effect):
        """
        Applies increase to opponent pokemon HP
        Args:
            other_pokemon: <Pokemon> Opponent pokemon to apply HP increase to
            damage_from_effect: <float> amount of HP to increase opponent HP by
        """
        other_pokemon.hp += damage_from_effect
        # also involves logging message
        battle_log_msg(
            '{name} is effected by {status_name}. {other_pokemon} gained {hp} HP'.format(name=self.name,
                                                                                         status_name=self.status_effect,
                                                                                         other_pokemon=other_pokemon.name,
                                                                                         hp=damage_from_effect))

    # todo add ability and effects to use status changing moves
    def take_damage(self, other_pokemon, move_damage):
        """
        Current Pokemon takes damage from an opposing one
        Assume damage initially set to 100 with contributions from current Pokemon's defense and opposing one's attack

        Args:
            other_pokemon: <Pokemon> Pokemon that is inflicting damage on current one
            move_damage: <int> Power factor of the move that the other Pokemon is using to inflict damage on current one
        """

        # assume equal contributions
        # from move power: 0.5 * (move_power/100) * 100
        damage = max((0.5 * move_damage) + (0.5 * (other_pokemon.attack - self.defense)),
                     0)  # Needs to be positive damage

        self.hp = max(self.hp - damage, 0)

        if self.hp == 0:
            battle_log_msg('{name} has fainted.'.format(name=self.name))
            battle_log_msg('{other_name} is the winner.'.format(other_name=other_pokemon.name))
        else:
            battle_log_msg('{name} HP is now {hp}.'.format(name=self.name, hp=self.hp))

    def use_move(self, other_pokemon, chosen_move=False):
        """
        Args:
            other_pokemon: <Pokemon> to use the move against
            chosen_move: <int> overwrites the move choice to use.  If False, randomly select a move in the moveset. 
        """
        # Apply status condition at the beginning of the current turn
        if self.status_effect is not None:
            self.status_effect_turn += 1
            self.apply_status_effect(other_pokemon)

        # Assume that move accuracy is capped at 100%
        # choose random move to use unless chosen_move specified

        if chosen_move:
            move_dict = self.moveset[str(chosen_move)]
        else:
            move_dict = self.moveset[str(random.randint(1, 4))]  # {'Confusion': {'power':50, 'accuracy':100}}

        move_name = list(move_dict.keys())[0]
        battle_log_msg('{name} used {move_name}!'.format(name=self.name, move_name=move_name))

        skip_chance_from_status = False
        if self.status_effect in [const.FROZEN, const.PARALYZED]:  # Skip turn effects
            battle_log_msg('{name} is {status_name}'.format(name=self.name, status_name=self.status_effect))
            skip_chance_from_status = int(
                self.status_effect_info.loc[self.status_effect, const.EFFECT_1].split('_')[-1])
            if skip_chance_from_status == 100:
                battle_log_msg('{name} could not move from being {status_name}!'.format(name=self.name,
                                                                                        status_name=self.status_effect))
                return

        if skip_chance_from_status:
            if random.randrange(0, 100) < skip_chance_from_status:
                battle_log_msg('{name} could not move from being {status_name}!'.format(name=self.name,
                                                                                        status_name=self.status_effect))
                return

        # Assume that move accuracy is capped at 100%
        if move_dict[move_name][const.ACC] == 100:
            if move_dict[move_name][const.STATUS_EFFECT]:  # apply status effect moves
                other_pokemon.status_effect = move_dict[move_name][const.STATUS_EFFECT]
            else:
                other_pokemon.take_damage(self, move_dict[move_name][const.POW])
        else:
            if random.randrange(0, 100) < move_dict[move_name][const.ACC]:
                if move_dict[move_name][const.STATUS_EFFECT]:
                    other_pokemon.status_effect = move_dict[move_name][const.STATUS_EFFECT]
                else:
                    other_pokemon.take_damage(self, move_dict[move_name][const.POW])
            else:
                battle_log_msg('{name} missed.'.format(name=self.name))
