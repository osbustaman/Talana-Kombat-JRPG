from app.api.kombat import Kombat
from flask import Flask, jsonify, request, render_template, send_from_directory


app = Flask(__name__)

def create_app():

    @app.route("/")
    @app.route("/talana-kombat")
    def kombat():
        return render_template('kombat.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)


    @app.route("/create-combat", methods=['GET', 'POST'])
    def createCombat():
        try:
            # Obtener los datos enviados en el cuerpo de la solicitud
            data = request.get_json()

            # Obtener los movimientos y golpes de cada jugador
            player1_moves = data['player1']['movimientos']
            player1_hits = data['player1']['golpes']
            player2_moves = data['player2']['movimientos']
            player2_hits = data['player2']['golpes']

            # Validar los movimientos
            Kombat.validate_movements(data)

            # Validar los hits
            Kombat.validate_hits(data)

            # Validar y convertir los movimientos y golpes
            player1_moves, player1_hits = Kombat.validate_characters(
                player1_moves, player1_hits)
            
            player2_moves, player2_hits = Kombat.validate_characters(
                player2_moves, player2_hits)
            
            # Resolver el combate
            first_player_attack, second_player_attack = Kombat.init_kombat(
                player1_moves, player1_hits, player2_moves, player2_hits)

            # Obtener movimientos y golpes de los jugadores
            first_player_move = data[first_player_attack]["movimientos"]
            first_player_hits = data[first_player_attack]["golpes"]
            second_player_move = data[second_player_attack]["movimientos"]
            second_player_hits = data[second_player_attack]["golpes"]

            name_first_player = list(
                Kombat.SPECIAL_HITS[first_player_attack].keys())[0]
            name_second_player = list(
                Kombat.SPECIAL_HITS[second_player_attack].keys())[0]

            energy_player1 = Kombat.SPECIAL_HITS[first_player_attack]['energy']
            energy_player2 = Kombat.SPECIAL_HITS[second_player_attack]['energy']

            list_combat = []

            while energy_player1 > 0 and energy_player2 > 0:

                if energy_player1 > 0:
                    if first_player_move and first_player_hits:
                        player1_move = first_player_move.pop(0)
                        player1_hit = first_player_hits.pop(0)
                    else:
                        player1_move = ""
                        player1_hit = ""

                    name_attack_player1, energy_attack_player1, other_move_player1 = Kombat.resolve_combat(
                        [first_player_attack, name_first_player], player1_move, player1_hit)
                    
                    list_combat.append(f"{name_first_player} {other_move_player1} {name_attack_player1}")
                    energy_player2 -= energy_attack_player1

                if energy_player2 > 0:
                    if second_player_move and second_player_hits:
                        player2_move = second_player_move.pop(0)
                        player2_hit = second_player_hits.pop(0)
                    else:
                        player2_move = ""
                        player2_hit = ""

                    name_attack_player2, energy_attack_player2, other_move_player2 = Kombat.resolve_combat(
                        [second_player_attack, name_second_player], player2_move, player2_hit)
                    
                    list_combat.append(f"{name_second_player} {other_move_player2} {name_attack_player2}")
                    energy_player1 -= energy_attack_player2
                    
                # Determinar al ganador
                if energy_player1 <= 0 and energy_player2 <= 0:
                    list_combat.append("¡Es un empate!")
                elif energy_player1 <= 0:
                    list_combat.append(
                        f"{name_second_player} gana la pelea y aun le queda {energy_player2} de energía")
                elif energy_player2 <= 0:
                    list_combat.append(
                        f"{name_first_player} gana la pelea y aun le queda {energy_player1} de energía")

            response = {
                'accion': 'success',
                'fight': list_combat
            }
            return jsonify(response), 200

        except ValueError as e:
            response = {
                'accion': 'error',
                'mensaje': str(e)
            }
            return jsonify(response), 400

    return app
