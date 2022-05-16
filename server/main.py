from database import Database
from flask import Flask, request
from spotify import Spotify

app = Flask(__name__)

db = Database("spotify.db")
db.set_foreign_keys()
spotify = Spotify("BQC6h7H4SANzoFOx3wAjkfSY5KOq34ai_yATnucgIv9oEZSay1aX5urb_XHWeTIRJk4ufx6ZzmoPSiJ4GkDDMXHGZcWTsDzUh5roY6A57AprIfvCG_8lWhK3gvPpQAlIYS6dT_hmMkEdeA")

print("----------------------------------------------------")

@app.route("/utilizadores", methods=["GET", "DELETE", "POST"])
@app.route("/utilizadores/<int:id>/playlist", methods=["POST","GET","DELETE"])
@app.route("/utilizadores/<int:id>", methods=["GET","PUT","DELETE"])
@app.route("/utilizadores/<int:id>/playlist/<int:playlist_id>", methods=["PUT"])
def utilizadores(id = None, playlist_id = None):
    
    if request.method == "POST":
        if request.path == "/utilizadores":
            try:
                nome = request.form["nome"]
                senha = request.form["senha"]
            except:
                return "Erro: nome e senha são obrigatórios", 400
            db.query("INSERT INTO utilizadores (nome, senha) VALUES (?, ?)", (nome, senha))
            return "Utilizador inserido com sucesso", 201
        elif "/playlist" in request.path:
            try:
                avaliacao = request.form["avaliacao"]
                id_musica = request.form["id_musica"]
            except:
                return "Avaliacao e id da musica sao obrigatorios", 400
            query =  db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if not query:
                return "Utilizador não existe", 404
            else:
                query = db.query("SELECT id FROM avaliacoes WHERE sigla = ?", (avaliacao))
                if query:
                    query = db.query("SELECT * FROM musicas WHERE id = ?", (id_musica))
                    if query:
                        if db.query("SELECT * FROM playlists WHERE id_user = ? AND id_musica = ?", (id, id_musica)):
                            return "Avaliação ja existe na playlist", 400
                        else:
                            db.query("INSERT OR IGNORE INTO playlists (id_user, id_musica, id_avaliacao) VALUES (?, ?, ?)",(id, id_musica, query[0][0]))
                            return "Avaliação inserida com sucesso", 201
                    else:
                        return "Musica nao existe", 400
                else:
                    return "Avaliação invalida", 400
                
    if request.method == "PUT":
        if "/playlist" in request.path:
            try:
                avaliacao = request.form["avaliacao"]
            except:
                return "Avaliação é obrigatório", 400
            query = db.query("SELECT * FROM playlists WHERE id_user = ? AND id_musica = ?",(id, playlist_id))
            if query:
                query = db.query("SELECT id FROM avaliacoes WHERE sigla = ?", (avaliacao,))
                if query:
                    idNovaAvaliacao = query[0][0]
                    db.query("UPDATE playlists SET id_avaliacao = ? WHERE id_musica = ? AND id_user = ?", (idNovaAvaliacao, playlist_id, id))
                    return "Avaliacao alterada com sucesso", 200
                else:
                    return "Avaliacao não pertence a lista M m S B MB", 404
            else:
                return "Musica/Utilizador não encontrado", 404
        if "/utilizadores" in request.path:
            try:
                senha = request.form["senha"]
            except:
                return "senha é obrigatório", 400
            query =  db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if not query:
                return "Utilizador não existe", 404
            else:
                db.query("UPDATE utilizadores SET senha = ? WHERE id = ?", (senha, id,))
                return "Utilizador atualizado com sucesso", 200

            
    if request.method == "DELETE":
        if request.path == "/utilizadores":
            query = db.query("SELECT * FROM utilizadores")
            if query:
                db.query("DELETE FROM utilizadores")
                return "Todos os utilizadores foram apagados", 200
            else:
                return "Não existem utilizadores", 404
        if "/playlist" in request.path:
            query = db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if query:
                query = db.query("SELECT * FROM playlists WHERE id_user = ? AND id_musica = ?", (id, playlist_id))
                if query:
                    db.query("DELETE FROM musicas WHERE id IN (SELECT DISTINCT ID FROM musicas, playlists WHERE id = playlists.id_musica and playlists.id_user = ?)", (id,))
                    return "Avaliação apagada com sucesso", 200
                else:
                    return "Não existem avaliações", 404
            else:
                return "Utilizador não encontrado", 404
        else:
            query = db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if query:
                db.query("DELETE FROM utilizadores WHERE id = ?", (id,))
                return "Utilizador removido com sucesso", 200
            else:
                return "Utilizador não encontrado", 404
    
    if request.method == "GET":
        if request.path == "/utilizadores":
            query = db.query("SELECT * FROM utilizadores")
            result = {"utilizadores": []}
            for x in query:
                result["utilizadores"].append({"id": x[0], "nome": x[1]})
            return str(result), 200
        if "/playlist" in request.path:
            query = db.query("SELECT id from utilizadores WHERE id = ?", (id,))
            if query:        
                query = db.query("SELECT DISTINCT musicas.nome FROM playlists,musicas,avaliacoes,utilizadores WHERE id_musica = musicas.id AND id_user = utilizadores.id AND id_avaliacao = avaliacoes.id AND utilizadores.id = ?",(id,))
                response = {"musicas avaliadas do utilizador":[]}
                for musica in query:
                    response["musicas avaliadas do utilizador"].append(musica[0])
                return str(response), 200 
        else:
            result = db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if result:
                return {"utilizador":{"id": result[0][0], "nome": result[0][1]}}, 200
            else:
                return "Utilizador não encontrado", 404







@app.route("/artistas", methods=["GET","DELETE", "POST"])
@app.route("/artistas/<int:id>", methods=["GET","DELETE"])
@app.route("/artistas/<int:id>/playlist", methods=["GET","DELETE"])
def artistas(id = None):
    
    if request.method == "POST":
        try:
            artist_id = request.form["id_spotify"]
        except:
            return "Erro: artist_id é obrigatório", 400
        query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (artist_id,))
        if query:
            return "Artista já existe", 409
        else:
            try:
                result = spotify.get_artist(artist_id)
            except:
                return "Erro: Artista não encontrado", 404
            if result:
                db.query("INSERT INTO artistas (id_spotify, nome) VALUES (?, ?)", (artist_id, result))
                return result, 201
            else:
                return "Artista não encontrado", 404
            
    if request.method == "DELETE":
        if request.path == "/artistas":
            query = db.query("SELECT * FROM artistas")
            if query:
                db.query("DELETE FROM artistas")
                return "Todos os artistas foram apagados", 200
            else:
                return "Não existem artistas", 404
        if "/playlist" in request.path:
            query = db.query("SELECT * FROM artistas WHERE id = ?", (id,))
            if query:
                query = db.query("SELECT * FROM playlists, musicas WHERE id_musica = musicas.id AND id_artista = ?", (id,))
                if query:
                    query = db.query("DELETE FROM musicas WHERE id IN (SELECT DISTINCT ID FROM musicas, playlists WHERE id = playlists.id_musica and musicas.id_artista = ?)", (id,))
                    return "Todas as músicas avaliadas do artista foram apagadas com sucesso",200
                else:
                    return "Não existem músicas avaliadas do artista", 404
            else:
                return "Artista não encontrado", 404
        else:
            query = db.query("SELECT * FROM artistas WHERE id = ?", (id,))
            if query:
                result = db.query("DELETE FROM artistas WHERE id = ?", (id,))
                return "Artista removido com sucesso", 200
            else:
                return "Artista não encontrado", 404
            
    if request.method == "GET":
        if request.path == "/artistas":
            query = db.query("SELECT * FROM artistas")
            result = {"artistas": []}
            for x in query:
                result["artistas"].append({"id": x[0], "id_spotify": x[1], "nome": x[2]})
            return str(result), 200
        if "/playlist" in request.path:
            query = db.query("SELECT id from artistas WHERE id = ?", (id,))
            if query:        
                query = db.query("SELECT DISTINCT musicas.nome FROM playlists,musicas,avaliacoes,artistas WHERE id_musica = musicas.id AND id_artista = artistas.id AND id_avaliacao = avaliacoes.id AND artistas.id = ?",(id,))
                response = {"musicas avaliadas do artista":[]}
                for musica in query:
                    response["musicas avaliadas do artista"].append(musica[0])
                return str(response), 200    
        else:
            result = db.query("SELECT * FROM artistas WHERE id = ?", (id,))
            if result:
                return {"artista":{"id": result[0][0], "id_spotify": result[0][1], "nome": result[0][2]}}, 200
            else:
                return "Artista não encontrado", 404









@app.route("/musicas", methods=["GET","DELETE","POST"])
@app.route("/musicas/<int:id>", methods=["GET","DELETE"])
@app.route("/musicas/playlist/<string:avl>", methods=["GET","DELETE"])
def musicas(id = None, avl= None):
    
    if request.method == "POST":
        try:
            track_id = request.form["id_spotify"]
        except:
            return "Erro: track_id é obrigatório", 400
        query = db.query("SELECT * FROM musicas WHERE id_spotify = ?", (track_id,))
        if query:
            return "Música já existe", 409
        else:
            try:
                result_track = spotify.get_track(track_id)
            except:
                return "Erro: Música não encontrada", 404
            if result_track:
                query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (result_track['artist_id'],))
                if query:
                    db.query("INSERT INTO musicas (id_spotify, nome, id_artista) VALUES (?, ?, ?)", (track_id, result_track['name'], query[0][0]))
                    return result_track['name'], 201
                else:
                    db.query("INSERT INTO artistas (id_spotify, nome) VALUES (?, ?)", (result_track['artist_id'], result_track['artist_name']))
                    query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (result_track['artist_id'],))
                    db.query("INSERT INTO musicas (id_spotify, nome, id_artista) VALUES (?, ?, ?)", (track_id, result_track['name'], query[0][0]))
                    return result_track['name'], 201
            else:
                return "Música não encontrada", 404
    
    if request.method == "DELETE":
        if request.path == "/musicas":
            query = db.query("SELECT * FROM musicas")
            if query:
                db.query("DELETE FROM musicas")
                return "Todas as músicas foram apagadas", 200
            else:
                return "Não existem músicas", 404
        if "/playlist" in request.path:
            query = db.query("SELECT id FROM avaliacoes WHERE sigla = ?", (avl,))
            if query:
                db.query("DELETE FROM musicas WHERE id IN (SELECT id_musica FROM playlists, avaliacoes WHERE avaliacoes.id = playlists.id_avaliacao AND  avaliacoes.sigla = ?)",(avl))
                return "Todas as musicas avaliadas com a avaliação foram apagadas com sucesso",200
            else:
                return "A avaliacao digitada não pertence a lista M m S B MB"
        else:
            query = db.query("SELECT * FROM musicas WHERE id = ?", (id,))
            if query:
                db.query("DELETE FROM musicas WHERE id = ?", (id,))
                return "Música removida com sucesso", 200
            else:
                return "Música não encontrada", 404
            
            
    if request.method == "GET":
        if request.path == "/musicas":
            query = db.query("SELECT * FROM musicas")
            result = {"musicas": []}
            for x in query:
                result["musicas"].append({"id": x[0], "id_spotify": x[1], "nome": x[2], "id_artista": x[3]})
            return str(result), 200

#------------------------- ALL MUSICAS -------------------------------------
        if "/playlist" in request.path:
            response = {"musicas avaliadas com uma dada avaliação":[]}
            query = db.query("SELECT DISTINCT nome FROM musicas,playlists WHERE id_musica = id AND id_avaliacao IN (SELECT id FROM avaliacoes WHERE sigla = ?)",(avl,))
            for musicas in query:
                response["musicas avaliadas com uma dada avaliação"].append(musicas[0])
            return str(response), 200
        else:
            result = db.query("SELECT * FROM musicas WHERE id = ?", (id,))
            if result:
                return {"musica":{"id": result[0][0], "id_spotify": result[0][1], "nome": result[0][2], "id_artista": result[0][3]}}, 200
            else:
                return "Música não encontrada", 404

if __name__ == "__main__":
    app.run(debug=True)