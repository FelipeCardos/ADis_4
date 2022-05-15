from database import Database
db = Database("spotify.db")
db.set_foreign_keys()
id = 1
db.query("DELETE FROM musicas WHERE id IN (SELECT DISTINCT ID FROM musicas, playlists WHERE id = playlists.id_musica and playlists.id_user = ?)", (id,))
