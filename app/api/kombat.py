class Kombat:

    SPECIAL_HITS = {
        'player1': {
            'Tonyn Stallone': [
                {'name': 'usa un Taladoken', 'combination': 'DSD+P', 'energy': 3},
                {'name': 'conecta un Remuyuken', 'combination': 'SD+K', 'energy': 2},
                {'name': 'le da un puñetazo al pobre ',
                    'combination': 'P', 'energy': 1},
                {'name': 'le da una Patada al pobre',
                    'combination': 'K', 'energy': 1},
            ],
            'energy': 6
        },
        'player2': {
            'Arnaldor Shuatseneguer': [
                {'name': 'conecta un Remuyuken', 'combination': 'SA+K', 'energy': 3},
                {'name': 'usa un Taladoken', 'combination': 'ASA+P', 'energy': 2},
                {'name': 'da un puñetazo', 'combination': 'P', 'energy': 1},
                {'name': 'le da una patada', 'combination': 'K', 'energy': 1},
            ],
            'energy': 6
        }
    }

    MOVEMENT = {
        "W": "salta y",
        "S": "se agacha y",
        "A": "retrocede y",
        "D": "avanza y"
    }

    @classmethod
    def validate_characters(self, movements, hits):
        allowed_chars = ['w', 's', 'a', 'd', 'p',
                         'k', '', 'W', 'S', 'A', 'D', 'P', 'K',
                         'DSD', 'dsd', 'SD', 'sd', 'SA', 'sa', 'ASA', 'asa']
        valid_movements = []
        valid_hits = []
        error = False

        for movement in movements:
            movement = movement.upper()
            if len(movement) <= 5 and set(movement).issubset(allowed_chars):
                valid_movements.append(movement)
            else:
                raise ValueError(
                    f"{movement} no corresponde a los movimientos permitidos")

        for hit in hits:
            hit = hit.upper()
            if hit in "PK":
                if len(hit) <= 1 and set(hit).issubset(allowed_chars):
                    valid_hits.append(hit)
                else:
                    raise ValueError(
                        f"{hit} no corresponde a los golpes permitidos")
            else:
                raise ValueError(
                    f"La tecla {hit} no corresponde a un golpe, los golpes son (P) puño o (K) patada")

        return valid_movements, valid_hits

    @classmethod
    def init_kombat(self, player1_moves, player1_hits, player2_moves, player2_hits):
        # Validar y convertir los movimientos y golpes
        player1_moves, player1_hits = self.count_characters(
            player1_moves, player1_hits)
        player2_moves, player2_hits = self.count_characters(
            player2_moves, player2_hits)

        points_player1 = player1_moves + player1_hits
        points_player2 = player2_moves + player2_hits

        if points_player1 < points_player2:
            first_attack = "player1"
            second_attack = "player2"
        elif points_player2 < points_player1:
            first_attack = "player2"
            second_attack = "player1"
        else:
            # caso de empate
            if player1_moves < player2_moves:
                first_attack = "player1"
                second_attack = "player2"
            elif player2_moves < player1_moves:
                first_attack = "player2"
                second_attack = "player1"
            else:
                # caso de empate
                if player1_hits < player2_hits:
                    first_attack = "player1"
                    second_attack = "player2"
                elif player2_hits < player1_hits:
                    first_attack = "player2"
                    second_attack = "player1"
                else:
                    # caso de empate
                    first_attack = "player1"
                    second_attack = "player2"

        return first_attack, second_attack

    @classmethod
    def count_characters(self, moves, hits):
        total_moves = 0
        total_hits = 0

        for m in moves:
            total_moves += len(m)

        for h in hits:
            total_hits += len(h)

        return total_moves, total_hits

    @classmethod
    def comment_motion(self, string_motion):
        strint_motion_attack = ""
        for character in string_motion:
            strint_motion_attack += self.MOVEMENT[character]
        return strint_motion_attack

    @classmethod
    def validate_movements(self, json_data):
        try:
            player1_movements = json_data['player1']['movimientos']
            player2_movements = json_data['player2']['movimientos']

            for movements in player1_movements + player2_movements:
                if not isinstance(movements, str) or len(movements) > 5:
                    raise ValueError(
                        "Los movimientos deben ser de un largo de 5 caracteres máximo")
            return True

        except KeyError:
            return False

    @classmethod
    def validate_hits(self, json_data):
        try:
            player1_hits = json_data['player1']['golpes']
            player2_hits = json_data['player2']['golpes']

            for hits in player1_hits + player2_hits:
                if not isinstance(hits, str) or len(hits) > 1:
                    raise ValueError(
                        "Los movimientos deben ser de un largo de 1 caracteres máximo")
            return True

        except KeyError:
            return False

    @classmethod
    def resolve_combat(self, player, movement, hit):
        # Lógica para procesar el turno actual
        # Aquí puedes implementar la funcionalidad deseada

        combination_string = f"{movement}+{hit}"
        list_combinations_hits = self.SPECIAL_HITS[player[0]][player[1]]
        other_move = ""

        if len(movement) > 0 and len(hit) > 0:
            for lch in list_combinations_hits:
                if combination_string[-1*(len(lch['combination'])):] == lch['combination'] and len(lch['combination']) > 1:
                    other_move = combination_string[:len(
                        combination_string) - len(lch['combination'])]
                    return lch['name'], lch['energy'], self.comment_motion(other_move)

        if len(hit) > 0:
            combination_to_find = hit
            for hit in list_combinations_hits:
                if hit['combination'] == combination_to_find:
                    other_move = movement
                    return hit['name'], hit['energy'], self.comment_motion(other_move)

        else:
            return "se mueve" if len(movement) == 0 else "", 0, "se mueve" if len(other_move) == 0 else ""
