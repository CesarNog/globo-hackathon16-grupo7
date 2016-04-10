## Seja bem vindo ao Camera Track - Globo Esporte

Ocular é um sistema embarcado conectado a uma câmera e um aplicativo. 

Ocular proporciona uma experiência única para torcedores de times de futebol com base na visualização de dois jogadores escolhidos por eles, antes da partida, em um aplicativo que além de transmitir o jogo, transmite ao vivo o vídeo dos jogadores escolhidos a partir de câmeras especificas. E mais, é possível ver o seu jogador preferido através de uma câmera que o segue a todo o momento durante a partida. O aplicativo ainda traz vários indicadores do jogador, como: número de cartões amarelos e vermelhos, número de faltas recebidas e cometidas, número de gols, chutes a gol e bolas interceptadas, velocidade média do jogador, distância percorrida, gráfico de pontos percorridos no campo, entre outros.

<hr>

Estrutura do Projeto
--------

  ```sh
  ├── Procfile
  ├── Procfile.dev
  ├── README.md
  ├── app.py
  ├── config.py
  ├── error.log
  ├── forms.py
  ├── models.py
  ├── requirements.txt
  ├── static
  │   ├── css
  │   │   ├── bootstrap-3.0.0.min.css
  │   │   ├── bootstrap-theme-3.0.0.css
  │   │   ├── bootstrap-theme-3.0.0.min.css
  │   │   ├── font-awesome-3.2.1.min.css
  │   │   ├── layout.forms.css
  │   │   ├── layout.main.css
  │   │   ├── main.css
  │   │   ├── main.quickfix.css
  │   │   └── main.responsive.css
  │   ├── font
  │   │   ├── FontAwesome.otf
  │   │   ├── fontawesome-webfont.eot
  │   │   ├── fontawesome-webfont.svg
  │   │   ├── fontawesome-webfont.ttf
  │   │   └── fontawesome-webfont.woff
  │   ├── ico
  │   │   ├── apple-touch-icon-114-precomposed.png
  │   │   ├── apple-touch-icon-144-precomposed.png
  │   │   ├── apple-touch-icon-57-precomposed.png
  │   │   ├── apple-touch-icon-72-precomposed.png
  │   │   └── favicon.png
  │   ├── img
  │   └── js
  │       ├── libs
  │       │   ├── bootstrap-3.0.0.min.js
  │       │   ├── jquery-1.10.2.min.js
  │       │   ├── modernizr-2.6.2.min.js
  │       │   └── respond-1.3.0.min.js
  │       ├── plugins.js
  │       └── script.js
  └── templates
      ├── errors
      │   ├── 404.html
      │   └── 500.html
      ├── forms
      │   ├── forgot.html
      │   ├── login.html
      │   └── register.html
      ├── layouts
      │   ├── form.html
      │   └── main.html
      └── pages
          ├── placeholder.about.html
          └── placeholder.home.html
  ```

### Inicio Rápido (Localhost)

1. Clone nosso repositório
  ```
  $ git clone https://github.com/cesarnog/globo-hackathon16-grupo7.git
  $ cd globo-hackathon16-grupo7
  ```

2. Inicialize e ative a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Instale as dependencias:
  ```
  $ pip install -r requirements.txt
  ```

5. Rode o servidor de desenvolvimentor:
  ```
  $ python app.py
  ```

6. Navigue até [http://localhost:5000](http://localhost:5000)

# globo-hackaton16-grupo7
