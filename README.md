
# spotify playlist api

Nesta api é possível criar utilizadores, musicas e artistas como também criar playlists com avaliações.




## Autores

- Bernardo Rebelo, 55856.
- Felipe Habib, 57157.


## Como adicionar Spotify token

Fazer o login via,
```http
  GET /login
```
e conectar-se com a sua conta Spotify.
## Documentação da API

#### Perfil
```http
  GET /profile
```
Informação sobre o perfil spotify.

#### Criar utilizador


```http
  POST /utilizadores
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| nome | `string` | **Obrigatório**. nome de utilizador |
| senha | `string` | **Obrigatório**. senha de utilizador |


#### Criar artista

```http
  POST /artistas
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| id de artista | `string` | **Obrigatório**. id Spotify base-62 |


#### Cria música

```http
  POST /musicas
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| id de música | `string` | **Obrigatório**. id Spotify base-62 |



#### Criar na playlist uma avaliação de uma musica

```http
  POST /utilizadores/id/playlist
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do utilizador |
| id_musica      | `int` | **Obrigatório**. O ID da música |
| avaliacao      | `string` | **Obrigatório**. Avaliação da música |

#### Update de uma avaliação de uma música

```http
  PUT /utilizadores/id_1/playlist/id_2
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_1`      | `int` | **Obrigatório**. O ID do utilizador |
| `id_1`      | `int` | **Obrigatório**. O ID da Música |
| avaliacao      | `string` | **Obrigatório**. Avaliação da música |

#### Update de uma senha de um utilizador

```http
  PUT /utilizadores/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do utilizador |
| senha | `string` | **Obrigatório**. senha de utilizador |

#### Retorna todos os utilizadores

```http
  GET /utilizadores
```

#### Retorna todas as musicas avaliadas pelo utilizador

```http
  GET /utilizadores/id/playlist
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador do utilizador  |

#### Retorna um utilizador

```http
  GET /utilizadores/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador do utilizador  |


#### Deleta todas as musicas avaliadas pelo utilizador

```http
  DELETE /utilizadores/id/playlist
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador do utilizador  |

#### Retorna todos os artistas
```http
  GET /artistas
```

#### Retorna um artista
```http
  GET /artistas/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador do artista  |

#### Retorna todas as musicas avaliadas de um artista
```http
  GET /artistas/id/playlist
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador do artista  |

#### Deleta todas as musicas avaliadas de um artista
```http
  DELETE /artistas/id/playlist
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador do artista  |


#### Retorna todas as musicas
```http
  GET /musicas
```
#### Retorna uma musica 
```http
  GET /musicas/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. Identificador da musica  |

#### Retorna as musicas com uma dada avaliação 
```http
  GET /musicas/playlist/avl
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `avl`      | `string` | **Obrigatório**. Sigla da avaliação, deve ser um da lista de avaliações: M m MB B S  |

#### Deleta as musicas com uma dada avaliação 
```http
  DELETE /artista/playlist/avl
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `avl`      | `string` | **Obrigatório**. Sigla da avaliação, deve ser um da lista de avaliações: M m MB B S  |

#### Delete de um utilizador

```http
  DELETE /utilizadores/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do utilizador |

#### Delete de um artistas

```http
  DELETE /artistas/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do artista |


#### Delete de uma música

```http
  DELETE /musicas/id
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID da música |


#### Delete de todos os utilizadores

```http
  DELETE /utilizadores
```


#### Delete de todos os artistas

```http
  DELETE /artistas
```



#### Delete de todas as músicas

```http
  DELETE /musicas
```













## Client api

Ver imagem clientapi.png